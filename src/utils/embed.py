# src/utils/embed.py

import numpy as np
import torch
import torch.nn.functional as F
from torch import Tensor
from tqdm import tqdm
from typing import List, Tuple

def cls_pool(hidden_states: Tensor, mask: Tensor) -> Tensor:
    return hidden_states[:, 0]

def last_token_pool(hidden_states: Tensor, mask: Tensor) -> Tensor:
    left_padded = (mask[:, -1].sum() == mask.size(0))
    if left_padded:
        return hidden_states[:, -1]
    seq_lens = mask.sum(dim=1) - 1
    batch_size = hidden_states.size(0)
    return hidden_states[torch.arange(batch_size, device=hidden_states.device), seq_lens]

def mean_pool(hidden_states: Tensor, mask: Tensor) -> Tensor:
    mask = mask.unsqueeze(-1).to(hidden_states.dtype)
    summed = (hidden_states * mask).sum(dim=1)
    counts = mask.sum(dim=1)
    return summed / counts

POOL_FN = {
    "cls":  cls_pool,
    "last": last_token_pool,
    "mean": mean_pool,
}

def embed_texts(
    model,
    tokenizer,
    texts: List[str],
    max_len: int,
    batch_size: int,
    pool_tag: str,
    device: str,
    dtype: torch.dtype,
    use_encode: bool = False,
    desc: str = "embed"
) -> Tuple[np.ndarray, List[int]]:
    """
    Batch-encode a list of texts into L2-normalized embeddings.

    Args:
      model:      a HuggingFace model or any object with encode()
      tokenizer:  corresponding tokenizer
      texts:      list of input strings
      max_len:    maximum token length per text
      batch_size: number of texts per batch
      pool_tag:   one of "cls", "last", or "mean" for pooling
      device:     torch device string ("cpu" or "cuda")
      dtype:      torch dtype for the output embeddings
      use_encode: if True, call model.encode() directly
      desc:       tqdm progress bar description

    Returns:
      embs:       numpy array of shape (num_valid, hidden_dim)
      valid_idxs: list of indices for texts successfully embedded
    """
    pool_fn = POOL_FN[pool_tag]
    total = len(texts)
    all_embs: List[np.ndarray] = []
    valid_idxs: List[int] = []

    for start in tqdm(range(0, total, batch_size), desc=desc, unit="batch"):
        end = min(start + batch_size, total)
        batch_texts = texts[start:end]
        try:
            if use_encode and hasattr(model, "encode"):
                arr = model.encode(batch_texts, max_length=max_len)
                t = arr if isinstance(arr, torch.Tensor) else torch.from_numpy(arr)
                emb = t.to(device).to(dtype)
                emb = F.normalize(emb, p=2, dim=1)
            else:
                tok = tokenizer(
                    batch_texts,
                    max_length=max_len,
                    truncation=True,
                    padding=True,
                    return_tensors="pt"
                ).to(device)
                with torch.no_grad():
                    out = model(**tok)
                hidden = out.last_hidden_state if hasattr(out, "last_hidden_state") else out[0]
                emb = pool_fn(hidden, tok["attention_mask"])
                emb = F.normalize(emb, p=2, dim=1).to(dtype)

            emb_np = emb.cpu().numpy()
            all_embs.append(emb_np)
            valid_idxs.extend(range(start, end))

        except Exception as e:
            print(f"skip batch {start}-{end}: {e}")
            continue

    if all_embs:
        embs = np.concatenate(all_embs, axis=0)
    else:
        hidden_size = model.config.hidden_size if hasattr(model, "config") and hasattr(model.config, "hidden_size") else 0
        embs = np.empty((0, hidden_size), dtype=np.float32)

    return embs, valid_idxs

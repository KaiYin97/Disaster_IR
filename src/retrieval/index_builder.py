# src/retrieval/index_builder.py

import gc
from pathlib import Path
from typing import Dict

import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from usearch.index import Index

from utils.embed         import embed_texts
from configs.path_config import BASELINE_INDEX_DIR
from configs.model_config import (
    MODEL_CONFIGS,
    MODEL_CACHE_DIR,
    DEFAULT_BATCH,
    DEFAULT_MAXLEN,
    DEVICE,
    DTYPE,
)


class IndexBuilder:
    def __init__(
        self,
        cache_dir: str = BASELINE_INDEX_DIR,
        device: str = DEVICE,
        dtype: torch.dtype = DTYPE
    ):
        """
        Prepare index cache directory and set device/dtype for embeddings.
        """
        self.cache = Path(cache_dir)
        self.cache.mkdir(parents=True, exist_ok=True)
        self.device = device
        self.dtype = dtype

    def _emb_path(self, model_name: str) -> Path:
        """
        Return path for storing/loading numpy embeddings.
        """
        fn = model_name.replace("/", "_") + ".fp32.npy"
        return self.cache / fn

    def _idx_path(self, model_name: str) -> Path:
        """
        Return path for saving/restoring Usearch index.
        """
        fn = model_name.replace("/", "_") + ".usearch"
        return self.cache / fn

    def corpus_embedding(
        self,
        model_name: str,
        cfg: Dict,
        corpus: list[str],
        rebuild: bool = False,
    ) -> np.ndarray:
        """
        Compute (or load) and cache dense embeddings for the corpus.
        """
        emb_fp = self._emb_path(model_name)
        if emb_fp.exists() and not rebuild:
            return np.load(emb_fp, mmap_mode="r")

        print(f"→ encoding corpus with {model_name}")
        # load tokenizer and model
        tok = AutoTokenizer.from_pretrained(
            model_name, trust_remote_code=True, cache_dir=MODEL_CACHE_DIR
        )
        mdl = AutoModel.from_pretrained(
            model_name, trust_remote_code=True, cache_dir=MODEL_CACHE_DIR
        ).to(self.device).eval()

        # embed in batches and normalize
        embs, _ = embed_texts(
            mdl,
            tok,
            corpus,
            max_len=DEFAULT_MAXLEN,
            batch_size=DEFAULT_BATCH,
            pool_tag=cfg.get("pool", "cls"),
            device=self.device,
            dtype=self.dtype,
            use_encode=cfg.get("use_encode", False),
            desc=f"{model_name}-corpus"
        )
        embs = embs.astype(np.float32)
        np.save(emb_fp, embs)

        # free GPU memory
        del mdl, tok
        torch.cuda.empty_cache()
        gc.collect()

        return embs

    def ann_index(
        self,
        model_name: str,
        embs: np.ndarray,
        rebuild: bool = False
    ) -> Index:
        """
        Build (or load) an ANN index for the given embeddings.
        """
        idx_fp = self._idx_path(model_name)
        if idx_fp.exists() and not rebuild:
            return Index.restore(str(idx_fp))

        # create a new Usearch index (inner-product metric)
        idx = Index(
            ndim=embs.shape[1],
            metric="ip",
            dtype="f32",
            connectivity=16,
            expansion_add=128,
            expansion_search=64
        )
        # add all vector IDs and vectors
        idx.add(np.arange(len(embs), dtype=np.int64), embs, copy=True, threads=1)
        idx.save(str(idx_fp))
        return idx

    def build_all(self, corpus: list[str]) -> tuple[np.ndarray, Dict[str, Index]]:
        """
        For all models in MODEL_CONFIGS, compute corpus embeddings once
        and build ANN indices reusing the same embeddings.
        Returns (embeddings, {model_name: Index}).
        """
        ann_idxs: Dict[str, Index] = {}
        base_embs = None

        for name, cfg in MODEL_CONFIGS.items():
            # only embed once with the first dense model
            if base_embs is None:
                base_embs = self.corpus_embedding(name, cfg, corpus)
            # build or load ANN index
            ann_idxs[name] = self.ann_index(name, base_embs)

        return base_embs, ann_idxs

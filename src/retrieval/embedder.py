# src/retrieval/embedder.py

import json
import glob
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import torch
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModel

from src.utils.embed         import embed_texts
from configs.path_config import TEST_QUERY_DIR, QUERY_EMB_DIR
from configs.model_config import (
    MODEL_CONFIGS,
    MODEL_CACHE_DIR,
    DEFAULT_BATCH,
    DEFAULT_MAXLEN,
    DEVICE,
    DTYPE,
)
from configs.gen_config import TASK2PREFIX


class QueryEmbedder:
    def __init__(
        self,
        test_query_dir: str = TEST_QUERY_DIR,
        out_dir: str        = QUERY_EMB_DIR,
        batch: int          = DEFAULT_BATCH,
        max_len: int        = DEFAULT_MAXLEN,
        device: str         = DEVICE,
        dtype: torch.dtype  = DTYPE,
    ):
        """
        Prepare directories and embedding parameters.
        """
        self.test_query_dir = Path(test_query_dir)
        self.out_dir        = Path(out_dir)
        self.batch          = batch
        self.max_len        = max_len
        self.device         = device
        self.dtype          = dtype

        self.out_dir.mkdir(parents=True, exist_ok=True)

    def _embed_model(self, name: str, cfg: Dict):
        """
        Embed all JSON query files for a single model.
        """
        slug = name.replace("/", "_")
        model_dir = self.out_dir / slug
        model_dir.mkdir(exist_ok=True)

        tokenizer = AutoTokenizer.from_pretrained(
            name, trust_remote_code=True, cache_dir=MODEL_CACHE_DIR
        )
        model = AutoModel.from_pretrained(
            name, trust_remote_code=True, cache_dir=MODEL_CACHE_DIR
        ).to(self.device).eval()

        for fp in glob.glob(str(self.test_query_dir / "*.json")):
            stem = Path(fp).stem
            np_out = model_dir / f"{stem}.npy"
            if np_out.exists():
                continue  # skip if already embedded

            data = json.load(open(fp, encoding="utf-8"))
            task = stem.split("_")[0]
            prefix = TASK2PREFIX.get(task, "")
            queries = [
                f"Instruct: {prefix}\nQuery: {item['user_query'].strip()}"
                for item in data
            ]

            embs, valid = embed_texts(
                model,
                tokenizer,
                queries,
                max_len=self.max_len,
                batch_size=self.batch,
                pool_tag=cfg.get("pool", "cls"),
                device=self.device,
                dtype=self.dtype,
                use_encode=cfg.get("use_encode", False),
                desc=f"{slug}-{stem}"
            )

            if len(valid) != len(queries):
                print(f"[WARN] {name} ({stem}): embedded {len(valid)}/{len(queries)} queries")

            np.save(np_out, embs.astype(np.float32))

        del model, tokenizer
        torch.cuda.empty_cache()

    def run(self, only: Optional[List[str]] = None):
        """
        Loop over all dense models and embed queries.
        Skip BM25 models and respect optional inclusion filter.
        """
        for name, cfg in MODEL_CONFIGS.items():
            if only and name not in only:
                continue

            print(f"\nEncoding queries with {name}")
            self._embed_model(name, cfg)

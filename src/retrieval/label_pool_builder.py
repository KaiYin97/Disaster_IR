# src/retrieval/label_pool_builder.py

import json
from pathlib import Path
import numpy as np
from filelock import FileLock

from src.utils.io import load_test_file

class LabelPoolBuilder:
    """
    Merge exact+ANN retrieval results into a single label_pool JSON per query file.
    """

    def __init__(self, out_dir: str, query_emb_dir: str):
        self.out_dir       = Path(out_dir)
        self.query_emb_dir = Path(query_emb_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def _dedup(self, lst):
        seen, uniq = set(), []
        for x in lst:
            if x not in seen:
                uniq.append(x)
                seen.add(x)
        return uniq

    def build_for_file(self, query_json: str, model: str, retriever):
        stem = Path(query_json).stem
        slug = model.replace("/", "_")
        q_emb_fp = self.query_emb_dir / slug / f"{stem}.npy"
        if not q_emb_fp.exists():
            print(f"[WARN] missing q_emb for {model} → {stem}")
            return

        q_emb = np.load(str(q_emb_fp))
        results = retriever.retrieve(model, q_emb)

        data, _ = load_test_file(query_json)
        for i, d in enumerate(data):
            d.setdefault("baseline_results", {})
            d["baseline_results"].setdefault(f"{model}_exact", results["exact"][i])
            d["baseline_results"].setdefault(f"{model}_ann",   results["ann"][i])
            d.setdefault("label_pool", [])
            d["label_pool"].extend(results["exact"][i])
            d["label_pool"].extend(results["ann"][i])
            d["label_pool"] = self._dedup(d["label_pool"])

        out_fp = self.out_dir / f"{stem}_label_pool.json"
        lock_fp = Path(str(out_fp) + ".lock")
        with FileLock(str(lock_fp)):
            with open(out_fp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"wrote {out_fp.name}")

#!/usr/bin/env python3
# scripts/build_label_pool.py

import sys
import glob
from pathlib import Path

import torch

# add project root so that `src` and `configs` are on PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))


from configs.path_config import (
    CORPUS_DIR,
    TEST_QUERY_DIR,
    QUERY_EMB_DIR,
    BASELINE_INDEX_DIR,
    LABEL_POOL_DIR,
)
from configs.model_config import MODEL_CONFIGS, DEFAULT_TOPK
from src.corpus.manager             import CorpusManager
from src.retrieval.embedder         import QueryEmbedder
from src.retrieval.index_builder    import IndexBuilder
from src.retrieval.retriever        import Retriever
from src.retrieval.label_pool_builder import LabelPoolBuilder


def main():
    # 1. choose device
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # 2. load or build ordered corpus
    oc_json = Path(CORPUS_DIR) / "ordered_corpus.json"
    cm = CorpusManager(CORPUS_DIR, str(oc_json))
    corpus = cm.load() if oc_json.exists() else cm.build()

    # 3. generate or load query embeddings
    qe = QueryEmbedder(
        test_query_dir=TEST_QUERY_DIR,
        out_dir=QUERY_EMB_DIR,
        batch=DEFAULT_TOPK,        
        max_len=512,               
        device=device,
        dtype=torch.float32,
    )
    qe.run()

    # 4. build corpus embeddings + ANN indexes
    ib = IndexBuilder(
        cache_dir=BASELINE_INDEX_DIR,
        device=device,
        dtype=torch.float32,
    )
    corpus_emb, ann_idxs = ib.build_all(corpus)

    # 5. instantiate retriever
    retriever = Retriever(
        corpus=corpus,
        corpus_emb=corpus_emb,
        ann_idxs=ann_idxs,
        top_k=DEFAULT_TOPK,
        device=device,
    )

    # 6. build label pools
    lpb = LabelPoolBuilder(
        out_dir=LABEL_POOL_DIR,
        query_emb_dir=QUERY_EMB_DIR,
    )

    for q_json in glob.glob(str(Path(TEST_QUERY_DIR) / "*.json")):
        for model_name, cfg in MODEL_CONFIGS.items():
            
            print(f"Building label pool for {Path(q_json).stem} with {model_name}")
            lpb.build_for_file(q_json, model_name, retriever)

    print("Label pool construction completed!")


if __name__ == "__main__":
    main()

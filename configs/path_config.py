from pathlib import Path

# ─── Data directories 
BASE_DIR            = Path("path_to_your_base_dir").expanduser().resolve()
CORPUS_DIR          = BASE_DIR / "corpus"
TEST_QUERY_DIR      = BASE_DIR / "test_queries"
QUERY_EMB_DIR       = BASE_DIR / "query_embeddings"
BASELINE_INDEX_DIR  = BASE_DIR / "baseline_indexes"
LABEL_POOL_DIR      = BASE_DIR / "label_pools"

# ─── Downloader / Processor 
RAW_PDF_ROOT        = BASE_DIR / "raw_pdfs"
TXT_ROOT            = BASE_DIR / "extracted_txt"
DEDUP_TXT_ROOT      = BASE_DIR / "dedup_txt"
CHUNK_JSON_ROOT     = BASE_DIR / "chunks_json"

# ─── Intermediate / Output 
EMBED_DEDUP_ROOT    = BASE_DIR / "chunks_deduped"
SEARCH_CACHE_DIR    = BASE_DIR / "search_cache"
OUTPUT_QRELS_DIR    = BASE_DIR / "qrels"
OUTPUT_SCORES_DIR   = BASE_DIR / "scores"

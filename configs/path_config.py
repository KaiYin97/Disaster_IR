from pathlib import Path

# ─── Base Directory 
BASE_DIR = Path("path_to_your_base_dir").expanduser().resolve()

# ─── Corpus & Embedding Directories  
CORPUS_DIR          = BASE_DIR / "corpus"
TEST_QUERY_DIR      = BASE_DIR / "test_queries"
QUERY_EMB_DIR       = BASE_DIR / "query_embeddings"
BASELINE_INDEX_DIR  = BASE_DIR / "baseline_indexes"
LABEL_POOL_DIR      = BASE_DIR / "label_pools"

# ─── Download & Processing Roots 
RAW_PDF_ROOT        = BASE_DIR / "raw_pdfs"
TXT_ROOT            = BASE_DIR / "extracted_txt"
DEDUP_TXT_ROOT      = BASE_DIR / "dedup_txt"    
DUP_TXT_ROOT        = BASE_DIR / "dup_txt"     
CHUNK_JSON_ROOT     = BASE_DIR / "chunks_json"  

# ─── Intermediate & Cache 
EMBED_DEDUP_ROOT    = BASE_DIR / "chunks_deduped"
SEARCH_CACHE_DIR    = BASE_DIR / "search_cache"

# ─── Final Outputs
OUTPUT_QRELS_DIR    = BASE_DIR / "qrels"
OUTPUT_SCORES_DIR   = BASE_DIR / "scores"

# ─── Query Generation Pipeline
INPUT_DIR       = BASE_DIR / "chunks_json"         
OUTPUT_DIR      = BASE_DIR / "generated_queries"   
DOC_INPUT_DIR   = BASE_DIR / "doc_chunks"          
DOC_OUTPUT_DIR  = BASE_DIR / "doc_generated"       

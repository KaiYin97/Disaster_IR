from pathlib import Path

# —— GPT & Generation Settings ——
OPENAI_API_KEY         = "your_openai_key_here"
MODEL_NAME             = "gpt-4o-mini"
MAX_RETRIES            = 3
RETRY_DELAY            = 5
DEFAULT_TEMPERATURE    = 0.0  

# —— Tokenizer / Generation Limits ——
DEFAULT_MAX_TOKENS_SCORE   = 10   
DEFAULT_MAX_TOKENS_WILLIAM = 25  
ITEMS_PER_PART             = 50   
SAVE_INTERVAL              = 10  

# —— Query Prefix Mapping ——
TASK2PREFIX = {
    "FactCheck": "Given the claim, retrieve the most relevant document that supports or refutes it",
    "NLI":       "Given the premise, retrieve the most relevant entailed hypothesis",
    "QA":        "Given the question, retrieve the most relevant passage answering it",
    "QAdoc":     "Given the question, retrieve the most relevant document answering it",
    "STS":       "Given the sentence, retrieve a semantically equivalent sentence",
    "Twitter":   "Given the user query, retrieve the most relevant Twitter text"
}

# —— Prompt Template Path ——
PROMPTS_FILE = Path(__file__).parent / "query_gen_prompts.json" 



# ── Semantic Chunking
PDF_MAX_CHUNK_TOKENS = 512
FIRST_CHUNK_ID       = 0
MAX_ITEMS_PER_JSON   = 1000

# ── MinHash Deduper 
MINHASH_THRESHOLD = 0.8
MINHASH_PERM      = 128

# ── PDF Downloader 
MAX_PDFS_PER_KEYWORD = 20
GOOGLE_PAUSE_SEC     = 5
HTTP_429_SLEEP_MIN   = 60

# ── PDF Processor
TABLES_EXTRACT = False

# ── Query Generators 
# Adjust these lists to control sampling behavior
QA_QUERY_LENGTHS  = [
    "less than 10 words", "5 to 20 words",
    "at least 150 words", "less than 20 words",
    "at least 50 words"
] 
QA_DIFFICULTIES   = ["elementary school", "high school", "college", "PhD"]
QA_CLARITIES      = ["clear", "understandable with some effort", "ambiguous"]
QA_NUM_WORDS      = ["at least 100 words", "at least 200 words", "at most 50 words", "50 to 150 words"]

STS_QUERY_LENGTHS = ["less than 10 words", "5 to 20 words", "at least 50 words", "at most 50 words"]
STS_DIFFICULTIES  = ["elementary school", "high school", "college", "PhD"]
STS_CLARITIES     = ["clear", "understandable with some effort", "ambiguous"]
STS_NUM_WORDS     = ["less than 10 words", "5 to 20 words", "at least 50 words", "at most 50 words"]

FC_QUERY_LENGTHS  = [
    "less than 10 words", "5 to 20 words",
    "at least 10 words", "at least 20 words",
    "at least 50 words"
]
FC_DIFFICULTIES   = ["elementary school", "high school", "college", "PhD"]
FC_CLARITIES      = ["clear", "understandable with some effort", "ambiguous"]
FC_NUM_WORDS      = ["at most 15 words", "at most 50 words", "50 to 150 words", "at most 100 words", "at least 100 words"]

NLI_QUERY_LENGTHS = [
    "less than 10 words", "5 to 20 words",
    "at least 20 words", "at least 50 words",
    "at least 150 words"
]
NLI_DIFFICULTIES  = ["elementary school", "high school", "college", "PhD"]
NLI_CLARITIES     = ["clear", "understandable with some effort", "ambiguous"]
NLI_NUM_WORDS     = ["less than 10 words", "5 to 20 words", "at least 50 words", "at least 20 words", "at most 50 words"]

# ── Pipeline Slicing 
MIN_TOKENS         = 10     
CHECKPOINT_SIZE    = 1000   
DOC_ITEMS_PER_FILE = 100    

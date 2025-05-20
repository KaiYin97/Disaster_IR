from pathlib import Path

# —— GPT & Generation Settings ——
OPENAI_API_KEY         = "your_openai_api_key_here"
MODEL_NAME             = "gpt-4o-mini"
MAX_RETRIES            = 3
RETRY_DELAY            = 5
DEFAULT_TEMPERATURE    = 0.0  # Deterministic output

# —— Tokenizer / Generation Limits ——
DEFAULT_MAX_TOKENS_SCORE   = 10   # For scoring outputs
DEFAULT_MAX_TOKENS_WILLIAM = 25   # For short text generations
ITEMS_PER_PART             = 50   # Batch size when splitting work
SAVE_INTERVAL              = 10   # Save progress every N items

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

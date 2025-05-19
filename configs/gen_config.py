from pathlib import Path
# —— GPT & 生成相关 —— 
OPENAI_API_KEY         = "your_openai_api_key_here"
MODEL_NAME             = "gpt-4o-mini"
MAX_RETRIES            = 3
RETRY_DELAY            = 5
DEFAULT_TEMPERATURE    = 0.0

# —— Tokenizer / 生成参数 —— 
DEFAULT_MAX_TOKENS_SCORE   = 10
DEFAULT_MAX_TOKENS_WILLIAM = 25
ITEMS_PER_PART             = 50
SAVE_INTERVAL              = 10

# —— Query 前缀 —— 
TASK2PREFIX = {
    "FactCheck": "Given the claim, retrieve the most relevant document that supports or refutes it",
    "NLI":       "Given the premise, retrieve the most relevant entailed hypothesis",
    "QA":        "Given the question, retrieve the most relevant passage answering it",
    "QAdoc":     "Given the question, retrieve the most relevant document answering it",
    "STS":       "Given the sentence, retrieve a semantically equivalent sentence",
    "Twitter":   "Given the user query, retrieve the most relevant Twitter text"
}

# —— Prompt 模板文件 —— 
# 如果你想把 prompts.json 拆出来，这里只保留文件路径
PROMPTS_FILE = Path(__file__).parent / "query_gen_prompts.json" 

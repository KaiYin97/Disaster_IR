import os
import torch
from pathlib import Path

MODEL_CACHE_DIR = os.getenv("DISASTIR_MODEL_CACHE", str(Path.home() / ".cache" / "models"))


DEFAULT_BATCH   = 32
DEFAULT_MAXLEN  = 256
DEFAULT_TOPK    = 10  

# Pooling strategy or encoding flag for each model
MODEL_CONFIGS = {
    "infly/inf-retriever-v1":                   {"pool": "last"},
    "nvidia/NV-Embed-v2":                       {"use_encode": True},
    "infly/inf-retriever-v1-1.5b":              {"pool": "last"},
    "Linq-AI-Research/Linq-Embed-Mistral":      {"pool": "last"},
    "nvidia/NV-Embed-v1":                       {"use_encode": True},
    "Salesforce/SFR-Embedding-Mistral":         {"pool": "last"},
    "Snowflake/snowflake-arctic-embed-l":       {"pool": "cls"},
    "Snowflake/snowflake-arctic-embed-l-v2.0":  {"pool": "cls"},
    "Snowflake/snowflake-arctic-embed-m-v2.0":  {"pool": "cls"},
    "Alibaba-NLP/gte-Qwen2-7B-instruct":        {"pool": "last"},
    "Snowflake/snowflake-arctic-embed-m-v1.5":  {"pool": "cls"},
    "intfloat/e5-mistral-7b-instruct":          {"pool": "last"},
    "Snowflake/snowflake-arctic-embed-m":       {"pool": "cls"},
    "ibm-granite/granite-embedding-125m-english": {"pool": "cls"},
    "BAAI/bge-large-en-v1.5":                   {"pool": "cls"},
    "mixedbread-ai/mxbai-embed-large-v1":       {"pool": "cls"},
    "Snowflake/snowflake-arctic-embed-s":       {"pool": "cls"},
    "BAAI/bge-base-en-v1.5":                    {"pool": "cls"},
    "BAAI/bge-small-en-v1.5":                   {"pool": "cls"},
    "intfloat/multilingual-e5-large-instruct":  {"pool": "mean"},
    "thenlper/gte-base":                        {"pool": "mean"},
    "intfloat/multilingual-e5-large":           {"pool": "mean"},
    "Alibaba-NLP/gte-Qwen2-1.5B-instruct":      {"pool": "last"},
    "intfloat/e5-base-v2":                      {"pool": "mean"},
    "intfloat/e5-large-v2":                     {"pool": "mean"},
    "intfloat/e5-small-v2":                     {"pool": "mean"},
    "sentence-transformers/all-mpnet-base-v2":  {"add_pooling_layer": True}, 
    "Alibaba-NLP/gte-base-en-v1.5":             {"pool": "cls"},
    "Alibaba-NLP/gte-large-en-v1.5":            {"pool": "cls"},
    "llmrails/ember-v1":                        {"pool": "mean"}
}

# Device setup
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE  = torch.float32

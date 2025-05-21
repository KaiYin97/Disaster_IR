# src/query/client.py

import os
import time
import re
import json

from openai import OpenAI, OpenAIError
import tiktoken

from configs.gen_config import OPENAI_API_KEY, MODEL_NAME, MAX_RETRIES, RETRY_DELAY

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
client = OpenAI()

tokenizer = tiktoken.encoding_for_model(MODEL_NAME)


def _extract_json(content: str) -> any:
    """
    Try to pull out a JSON object from the model's response.
    """
    m = re.search(r'```json\s*([\s\S]*?)```', content)
    if m:
        blob = m.group(1)
    else:
        m2 = re.search(r'(\{[\s\S]*\})', content)
        blob = m2.group(1) if m2 else content
    try:
        return json.loads(blob)
    except json.JSONDecodeError:
        return None


def safe_generate(
    prompt: str,
    user_content: str,
    retries: int = MAX_RETRIES,
    backoff: int = RETRY_DELAY
) -> any:
    """
    Send a chat completion request with simple retry/backoff.
    Returns parsed JSON if possible, else raw string.
    """
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user",   "content": user_content},
    ]
    for attempt in range(retries):
        try:
            resp = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=0.0,
            )
            text = resp.choices[0].message.content
            parsed = _extract_json(text)
            return parsed if parsed is not None else text.strip()
        except OpenAIError as e:
            # backoff on errors
            time.sleep(backoff * (attempt + 1))
    return None

# src/utils/llm.py

import os
import time
import re
import json

from openai import OpenAI, OpenAIError
import tiktoken

from configs.gen_config import OPENAI_API_KEY, MODEL_NAME, MAX_RETRIES, RETRY_DELAY, DEFAULT_TEMPERATURE

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
client = OpenAI()

tokenizer = tiktoken.encoding_for_model(MODEL_NAME)


def call_gpt(
    system_message: str | None,
    user_prompt: str,
    model: str = MODEL_NAME,
    max_retries: int = MAX_RETRIES,
    delay: int = RETRY_DELAY,
    temperature: float = DEFAULT_TEMPERATURE,
    max_tokens: int = 50,
    response_format: dict | None = None
) -> str:
    """
    Send a chat completion request with optional system message,
    retrying on transient errors with exponential backoff.
    Returns the raw response content.
    """
    messages = []
    if system_message is not None:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": user_prompt})

    for attempt in range(max_retries):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **({"response_format": response_format} if response_format else {})
            )
            return resp.choices[0].message.content
        except OpenAIError:
            time.sleep(delay * (attempt + 1))
    # if retries exhausted, raise error
    raise RuntimeError(f"GPT call failed after {max_retries} attempts")


def parse_llm_json_response(
    response: str,
    key: str,
    expected_type: type,
    valid_values: list | None = None,
    method_name: str = "parse_llm_json_response"
) -> any:
    """
    Extract JSON object from LLM response, then return response[key].
    Raises if JSON parse fails, key is missing, wrong type, or invalid value.
    """
    m = re.search(r'```json\s*([\s\S]*?)```', response)
    blob = m.group(1) if m else response
    try:
        data = json.loads(blob)
    except json.JSONDecodeError:
        raise ValueError(f"{method_name}: invalid JSON:\n{response}")

    if key not in data:
        raise KeyError(f"{method_name}: key '{key}' not found in JSON")
    value = data[key]
    if expected_type is float and isinstance(value, int):
        value = float(value)
    if not isinstance(value, expected_type):
        raise TypeError(f"{method_name}: {key} is {type(value)}, expected {expected_type}")
    if valid_values is not None and value not in valid_values:
        raise ValueError(f"{method_name}: {key}={value} not in valid values {valid_values}")
    return value

# src/scoring/raters/zeroshot_rater.py

from typing import Optional
from openai import OpenAI
from configs.gen_config import MODEL_NAME, MAX_RETRIES, RETRY_DELAY, DEFAULT_TEMPERATURE, PROMPTS_FILE
from .base import BaseRater, get_task_prompts
from utils.llm import call_gpt, parse_llm_json_response

import json

# load prompt templates once
METHOD_PROMPTS = json.load(open(PROMPTS_FILE, "r", encoding="utf-8"))


class ZeroShotRater(BaseRater):
    """
    Zero-shot relevance/similarity rater using direct prompt-response.
    """

    def __init__(self):
        self.method = "zero_shot"

    def rate(
        self,
        client: OpenAI,
        task: str,
        input1: str,
        input2: str,
        force_default_prompts: bool = False
    ) -> Optional[int]:
        """
        Send a single prompt to the model and parse the final score.
        """
        prompts = get_task_prompts(self.method, task, force_default_prompts)
        prompt = prompts["prompt_template"].format(input1=input1, input2=input2)
        resp = call_gpt(
            client=client,
            system_message=prompts.get("system"),
            user_prompt=prompt,
            model=MODEL_NAME,
            max_retries=MAX_RETRIES,
            delay=RETRY_DELAY,
            temperature=DEFAULT_TEMPERATURE,
            max_tokens=25,
            response_format={"type": "json_object"},
        )
        key = "final_similarity_score" if task == "STS" else "final_score"
        valid = list(range(6)) if task == "STS" else [0, 1, 2, 3]
        return parse_llm_json_response(
            response=resp,
            key=key,
            expected_type=int,
            valid_values=valid,
            method_name=f"ZeroShot-{task}"
        )

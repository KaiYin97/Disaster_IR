# RAG/code/Disaster_IR/src/scoring/raters/zeroshot_rater.py

from typing import Optional
from openai import OpenAI

from configs.gen_config import MODEL_NAME, MAX_RETRIES, RETRY_DELAY, DEFAULT_TEMPERATURE
from .base import BaseRater, get_task_prompts
from src.utils.llm import call_gpt, parse_llm_json_response


class ZeroShotRater(BaseRater):
    """
    Zero-shot relevance/similarity rater using a single prompting step.
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
        prompts = get_task_prompts(self.method, task, force_default_prompts)

        user_prompt = prompts["prompt_template"].format(
            input1=input1,
            input2=input2
        )

        resp = call_gpt(
            system_message=prompts.get("system"),
            user_prompt=user_prompt,
            model=MODEL_NAME,
            max_retries=MAX_RETRIES,
            delay=RETRY_DELAY,
            temperature=DEFAULT_TEMPERATURE,
            max_tokens=25,
            response_format={"type": "json_object"},
        )

        key = "final_similarity_score" if task == "STS" else "final_score"
        valid_values = list(range(6)) if task == "STS" else [0, 1, 2, 3]

        return parse_llm_json_response(
            response=resp,
            key=key,
            expected_type=int,
            valid_values=valid_values,
            method_name=f"ZeroShot-{task}"
        )

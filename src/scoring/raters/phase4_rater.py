# src/scoring/raters/phase4_rater.py

import json
from typing import Dict, Optional, Tuple

from openai import OpenAI
from configs.gen_config import MODEL_NAME, MAX_RETRIES, RETRY_DELAY, DEFAULT_TEMPERATURE
from utils.llm import call_gpt, parse_llm_json_response

from .base import BaseRater, get_task_prompts

class Phase4Rater(BaseRater):
    """
    Four-phase decomposed relevance/similarity rater.
    """

    def __init__(self):
        self.method = "rate4"

    def rate(
        self,
        client: OpenAI,
        task: str,
        input1: str,
        input2: str,
        force_default_prompts: bool = False
    ) -> Tuple[Optional[int], Dict[str, Optional[int]]]:
        # Phase 1: score each criterion separately
        prompts = get_task_prompts(self.method, task, force_default_prompts)
        sub_scores: Dict[str, Optional[int]] = {}

        for name, definition in prompts["criteria"].items():
            # format decomposition prompt for this criterion
            prompt = prompts["decomp_prompt_template"].format(
                criterion_name=name.replace("_", " "),
                criterion_definition=definition,
                input1=input1,
                input2=input2,
            )
            resp = call_gpt(
                client=client,
                system_message=prompts["decomp_system"],
                user_prompt=prompt,
                model=MODEL_NAME,
                max_retries=MAX_RETRIES,
                delay=RETRY_DELAY,
                temperature=DEFAULT_TEMPERATURE,
                max_tokens=30,
                response_format={"type": "json_object"},
            )
            sub_scores[name] = parse_llm_json_response(
                response=resp,
                key="criterion_score",
                expected_type=int,
                valid_values=[0, 1, 2, 3],
                method_name=f"Phase4-{task}-{name}"
            )

        # Phase 2: combine sub-scores into final prompt
        fmt = {
            f"{k.replace(' ', '_')}_score": str(v) if isinstance(v, int) else "N/A"
            for k, v in sub_scores.items()
        }
        final_prompt = prompts["final_prompt_template"].format(
            input1=input1,
            input2=input2,
            **fmt
        )
        resp_final = call_gpt(
            client=client,
            system_message=prompts["final_system"],
            user_prompt=final_prompt,
            model=MODEL_NAME,
            max_retries=MAX_RETRIES,
            delay=RETRY_DELAY,
            temperature=DEFAULT_TEMPERATURE,
            max_tokens=30,
            response_format={"type": "json_object"},
        )
        key_name = "final_similarity_score" if task == "STS" else "final_relevance_score"
        valid_vals = list(range(6)) if task == "STS" else [0, 1, 2, 3]
        final_score = parse_llm_json_response(
            response=resp_final,
            key=key_name,
            expected_type=int,
            valid_values=valid_vals,
            method_name=f"Phase4-{task}-Final"
        )

        # normalize missing sub-scores to None
        clean_sub = {k: (v if isinstance(v, int) else None) for k, v in sub_scores.items()}
        return final_score, clean_sub

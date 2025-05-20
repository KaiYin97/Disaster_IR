# RAG/code/Disaster_IR/src/scoring/raters/cot_rater.py

from typing import Any, Dict, Optional, Tuple

from openai import OpenAI
from configs.gen_config import MODEL_NAME, MAX_RETRIES, RETRY_DELAY, DEFAULT_TEMPERATURE

from .base import BaseRater, get_task_prompts
from src.utils.llm import call_gpt, parse_llm_json_response


class ChainOfThoughtRater(BaseRater):
    """
    Chain-of-Thought style rater: multi-phase reasoning before scoring.
    """

    def __init__(self):
        self.method = "rate_cot"

    def rate(
        self,
        client: OpenAI,
        task: str,
        input1: str,
        input2: str,
        force_default_prompts: bool = False
    ) -> Any:
        # Phase 1: detect if input2 answers/relates to input1
        prompts = get_task_prompts(self.method, task, force_default_prompts)
        p1 = prompts["phase1_prompt_template"].format(input1=input1, input2=input2)
        r1 = call_gpt(
           
            system_message=None,
            user_prompt=p1,
            model=MODEL_NAME,
            max_retries=MAX_RETRIES,
            delay=RETRY_DELAY,
            temperature=DEFAULT_TEMPERATURE,
            max_tokens=30,
            response_format={"type": "json_object"},
        )
        flag_key = "has_relation" if task == "STS" else "has_answer"
        flag = parse_llm_json_response(
            response=r1,
            key=flag_key,
            expected_type=str,
            valid_values=["Yes", "No"],
            method_name=f"COT-P1-{task}"
        )
        if flag is None:
            return None

        # If STS and no relation, early exit with zero score
        if task == "STS" and flag == "No":
            return 0

        # Determine which criteria to score
        if task != "STS" and flag == "No":
            criteria = prompts.get("phase2_criteria_alt", [])
        else:
            criteria = prompts.get("phase2_criteria", [])

        # Phase 2: score each criterion
        sub_scores: Dict[str, Optional[int]] = {}
        for name in criteria:
            definition = prompts["criteria"][name]
            p2 = prompts["phase2_prompt_template"].format(
                criterion_name=name,
                criterion_definition=definition,
                input1=input1,
                input2=input2
            )
            r2 = call_gpt(
                
                system_message=prompts.get("phase2_system"),
                user_prompt=p2,
                model=MODEL_NAME,
                max_retries=MAX_RETRIES,
                delay=RETRY_DELAY,
                temperature=DEFAULT_TEMPERATURE,
                max_tokens=30,
                response_format={"type": "json_object"},
            )
            sub_scores[name] = parse_llm_json_response(
                response=r2,
                key="criterion_score",
                expected_type=int,
                valid_values=[0, 1, 2, 3],
                method_name=f"COT-P2-{task}-{name}"
            )

        # Phase 3: final relevance/similarity scoring
        if task == "STS":
            final_template = prompts["phase3_relevant_prompt_template"]
            sys_msg = prompts["phase3_relevant_system"]
            out_key = "final_similarity_score"
            valid_vals = list(range(6))
        else:
            if flag == "Yes":
                final_template = prompts["phase3_relevant_prompt_template"]
                sys_msg = prompts["phase3_relevant_system"]
                out_key = "relevance_score"
                valid_vals = [2, 3]
            else:
                final_template = prompts["phase3_irrelevant_prompt_template"]
                sys_msg = prompts["phase3_irrelevant_system"]
                out_key = "relevance_score"
                valid_vals = [0, 1]

        p3 = final_template.format(
            input1=input1,
            input2=input2,
            **{f"{k}_score": sub_scores[k] for k in sub_scores}
        )
        r3 = call_gpt(
            
            system_message=sys_msg,
            user_prompt=p3,
            model=MODEL_NAME,
            max_retries=MAX_RETRIES,
            delay=RETRY_DELAY,
            temperature=DEFAULT_TEMPERATURE,
            max_tokens=30,
            response_format={"type": "json_object"},
        )
        final_score = parse_llm_json_response(
            response=r3,
            key=out_key,
            expected_type=int,
            valid_values=valid_vals,
            method_name=f"COT-P3-{task}"
        )

        if task == "STS":
            return final_score
        return final_score, flag, sub_scores

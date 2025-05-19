# src/scoring/raters/base.py

import json
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple, Type

from openai import OpenAI
from configs.gen_config import PROMPTS_FILE, MODEL_NAME, MAX_RETRIES, RETRY_DELAY, DEFAULT_TEMPERATURE

# load all prompt templates from external JSON
METHOD_PROMPTS = json.load(open(PROMPTS_FILE, "r", encoding="utf-8"))


def get_task_prompts(method_group: str, task: str, force_default: bool = False) -> Dict[str, Any]:
    """
    Retrieve the prompt definitions for the given method group and task.
    If force_default is True and task is in ('FactCheck','NLI'), return the 'default' prompts.
    """
    key = "default" if (force_default and task in {"FactCheck", "NLI"}) else task
    return METHOD_PROMPTS.get(method_group, {}).get(key, METHOD_PROMPTS.get(method_group, {}).get("default", {}))


class BaseRater(ABC):
    """
    Abstract base class for all relevance/similarity raters.
    Subclasses must implement rate().
    """

    @abstractmethod
    def rate(
        self,
        client: OpenAI,
        task: str,
        input1: str,
        input2: str,
        force_default_prompts: bool = False
    ) -> Any:
        """
        Rate the pair (input1, input2) under the given task.
        Returns a score or tuple of scores, depending on subclass.
        """
        pass

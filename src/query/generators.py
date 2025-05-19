# src/query/generators.py

import json
import random
from pathlib import Path
from typing import Dict, List

from client import safe_generate
from configs.gen_config import (
    PROMPTS_FILE,
    QA_QUERY_LENGTHS, QA_DIFFICULTIES, QA_CLARITIES, QA_NUM_WORDS,
    STS_QUERY_LENGTHS, STS_DIFFICULTIES, STS_CLARITIES, STS_NUM_WORDS,
    FC_QUERY_LENGTHS, FC_DIFFICULTIES, FC_CLARITIES, FC_NUM_WORDS,
    NLI_QUERY_LENGTHS, NLI_DIFFICULTIES, NLI_CLARITIES, NLI_NUM_WORDS,
)

# load all prompt templates from external JSON
PROMPTS = json.load(open(PROMPTS_FILE, "r", encoding="utf-8"))


class BaseGenerator:
    def __init__(self, name: str):
        self.name = name
        self.err_key = name

    def _append_err(self, errors: Dict[str, List[str]], key: str):
        errors[self.err_key].append(key)

    def apply(self, content: str, record: Dict, idx: str, errors: Dict[str, List[str]]):
        """
        Must be implemented by subclasses:
        apply the generator to `content`, update `record`, log errors in `errors`.
        """
        raise NotImplementedError


class TwitterGenerator(BaseGenerator):
    def __init__(self):
        super().__init__("tw")

    def apply(self, content, record, idx, errors):
        # Phase 1: choose twitter task
        tasks = safe_generate(PROMPTS["tw_task"], "Paragraph: " + content)
        if not isinstance(tasks, list) or not tasks:
            return self._append_err(errors, f"{idx}_tasks_fail")

        cfg = {"task": tasks[0]}
        record.setdefault("Twitter_config", {})[f"headline_{idx}"] = cfg

        # Phase 2: generate query and hard negatives
        res = safe_generate(
            PROMPTS["tw_query"].format(**cfg),
            "Paragraph: " + content
        )
        if res and all(k in res for k in ("query", "positive_tweet", "hard_negative_tweet")):
            tw = record.setdefault("Twitter", {})
            tw[f"query_{idx}"]               = res["query"]
            tw[f"positive_tweet_{idx}"]      = res["positive_tweet"]
            tw[f"hard_negative_tweet_{idx}"] = res["hard_negative_tweet"]
        else:
            self._append_err(errors, idx)


class QAGenerator(BaseGenerator):
    def __init__(self):
        super().__init__("qa")

    def apply(self, content, record, idx, errors):
        # Phase 1: choose QA task and sampling config
        tasks = safe_generate(PROMPTS["qa_task"], "Paragraph: " + content)
        if not isinstance(tasks, list) or not tasks:
            return self._append_err(errors, f"{idx}_tasks_fail")

        cfg = {
            "task":         tasks[0],
            "query_length": random.choice(QA_QUERY_LENGTHS),
            "clarity":      random.choice(QA_CLARITIES),
            "difficulty":   random.choice(QA_DIFFICULTIES),
            "num_words":    random.choice(QA_NUM_WORDS),
        }
        record.setdefault("QA_config", {})[f"user_query_{idx}"] = cfg

        # Phase 2: generate positive & hard-negative document queries
        res = safe_generate(
            PROMPTS["qa_query"].format(**cfg),
            "Paragraph: " + content
        )
        if res and all(k in res for k in ("user_query", "positive_document", "hard_negative_document")):
            qa = record.setdefault("QA", {})
            qa[f"user_query_{idx}"]             = res["user_query"]
            qa[f"positive_document_{idx}"]      = res["positive_document"]
            qa[f"hard_negative_document_{idx}"] = res["hard_negative_document"]
        else:
            self._append_err(errors, idx)


class STSGenerator(BaseGenerator):
    def __init__(self):
        super().__init__("sts")

    def apply(self, content, record, idx, errors):
        # Phase 1: choose STS task
        tasks = safe_generate(PROMPTS["sts_task"], "Paragraph: " + content)
        if not isinstance(tasks, list) or not tasks:
            return self._append_err(errors, f"{idx}_tasks_fail")

        cfg = {
            "task":         tasks[0],
            "query_length": random.choice(STS_QUERY_LENGTHS),
            "clarity":      random.choice(STS_CLARITIES),
            "difficulty":   random.choice(STS_DIFFICULTIES),
            "num_words":    random.choice(STS_NUM_WORDS),
        }
        record.setdefault("STS_config", {})[f"query_{idx}"] = cfg

        # Phase 2: generate semantically equivalent and negative examples
        res = safe_generate(
            PROMPTS["sts_query"].format(**cfg),
            "Paragraph: " + content
        )
        if res and all(k in res for k in ("query", "positive", "hard_negative")):
            sts = record.setdefault("STS", {})
            sts[f"query_{idx}"]         = res["query"]
            sts[f"positive_{idx}"]      = res["positive"]
            sts[f"hard_negative_{idx}"] = res["hard_negative"]
        else:
            self._append_err(errors, idx)


class FactCheckGenerator(BaseGenerator):
    def __init__(self):
        super().__init__("fc")

    def apply(self, content, record, idx, errors):
        # Phase 1: choose FactCheck task
        tasks = safe_generate(PROMPTS["fc_task"], "Paragraph: " + content)
        if not isinstance(tasks, list) or not tasks:
            return self._append_err(errors, f"{idx}_tasks_fail")

        cfg = {
            "task":         tasks[0],
            "query_length": random.choice(FC_QUERY_LENGTHS),
            "clarity":      random.choice(FC_CLARITIES),
            "difficulty":   random.choice(FC_DIFFICULTIES),
            "num_words":    random.choice(FC_NUM_WORDS),
        }
        record.setdefault("FactCheck_config", {})[f"claim_{idx}"] = cfg

        # Phase 2: generate claim and document negatives
        res = safe_generate(
            PROMPTS["fc_query"].format(**cfg),
            "Paragraph: " + content
        )
        if res and all(k in res for k in ("claim", "positive_document", "hard_negative_document")):
            fc = record.setdefault("FactCheck", {})
            fc[f"claim_{idx}"]                  = res["claim"]
            fc[f"positive_document_{idx}"]      = res["positive_document"]
            fc[f"hard_negative_document_{idx}"] = res["hard_negative_document"]
        else:
            self._append_err(errors, idx)


class NLIGenerator(BaseGenerator):
    def __init__(self):
        super().__init__("nli")

    def apply(self, content, record, idx, errors):
        # Phase 1: choose NLI task
        tasks = safe_generate(PROMPTS["nli_task"], "Paragraph: " + content)
        if not isinstance(tasks, list) or not tasks:
            return self._append_err(errors, f"{idx}_tasks_fail")

        cfg = {
            "task":         tasks[0],
            "query_length": random.choice(NLI_QUERY_LENGTHS),
            "clarity":      random.choice(NLI_CLARITIES),
            "difficulty":   random.choice(NLI_DIFFICULTIES),
            "num_words":    random.choice(NLI_NUM_WORDS),
        }
        record.setdefault("NLI_config", {})[f"premise_{idx}"] = cfg

        # Phase 2: generate premise & hypothesis pairs
        res = safe_generate(
            PROMPTS["nli_query"].format(**cfg),
            "Paragraph: " + content
        )
        if res and all(k in res for k in ("premise", "entailed_hypothesis", "contradiction", "neutral")):
            nli = record.setdefault("NLI", {})
            nli[f"premise_{idx}"]             = res["premise"]
            nli[f"entailed_hypothesis_{idx}"] = res["entailed_hypothesis"]
            nli[f"contradiction_{idx}"]       = res["contradiction"]
            nli[f"neutral_{idx}"]             = res["neutral"]
        else:
            self._append_err(errors, idx)

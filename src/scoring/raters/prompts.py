# --- Criteria Definitions---
CRITERIA_DEFAULT = {
    "Exactness": "how precisely the passage answers the query",
    "Coverage": "proportion of content discussing the query",
    "Topicality": "subject alignment between passage and query",
    "Contextual Fit": "presence of relevant background information"
}
CRITERIA_FACTCHECK = {
    "Exactness": "how precisely the passage supports or refutes the claim",
    "Coverage": "the extent to which the passage discusses content directly relevant to the claim",
    "Topicality": "how closely the subject matter of the passage aligns with the topic of the claim",
    "Contextual Fit": "how much relevant background or contextual information is provided to help verify the claim"
}
CRITERIA_NLI = {
    "Exactness": "how precisely the hypothesis is entailed by the premise",
    "Coverage": "the extent to which the hypothesis reflects core information from the premise",
    "Topicality": "how closely the subject matter of the hypothesis aligns with that of the premise",
    "Contextual Fit": "how well the hypothesis fits within the context or background established by the premise"
}

# --- rate4 Decomposition System Message---
rate4_DECOMP_SYSTEM_DEFAULT = (
    "Please assess how well the provided passage meets specific criteria in relation to the query. Use the "
    "following scoring scale (0-3) for evaluation:\n"
    "0: Not relevant at all / No information provided.\n"
    "1: Marginally relevant / Partially addresses the criterion.\n"
    "2: Fairly relevant / Adequately addresses the criterion.\n"
    "3: Highly relevant / Fully satisfies the criterion.\n"
    "Your output MUST be a valid JSON object containing a single key 'criterion_score' with the integer score."
)
rate4_DECOMP_SYSTEM_FACTCHECK = (
    "Please assess how well the provided passage serves as evidence for evaluating the claim. Use the following scoring scale (0–3) for evaluation:\n"
    "0: Not relevant at all / No information provided.\n"
    "1: Marginally relevant / Partially addresses the criterion.\n"
    "2: Fairly relevant / Adequately addresses the criterion.\n"
    "3: Highly relevant / Fully satisfies the criterion.\n"
    "Your output MUST be a valid JSON object containing a single key 'criterion_score' with the integer score."
)
rate4_DECOMP_SYSTEM_NLI = (
    "Please assess how well the provided hypothesis is entailed by the premise according to the following criteria. "
    "Use the following scoring scale (0–3) for evaluation:\n"
    "0: Not relevant at all / No information provided.\n"
    "1: Marginally relevant / Partially addresses the criterion.\n"
    "2: Fairly relevant / Adequately addresses the criterion.\n"
    "3: Highly relevant / Fully satisfies the criterion.\n"
    "Your output MUST be a valid JSON object containing a single key 'criterion_score' with the integer score."
)

# --- rate4 Decomposition Prompt Template---
rate4_DECOMP_PROMPT_TEMPLATE_DEFAULT = (
    "Please rate how well the given passage meets the {criterion_name} criterion in relation to the query. "
    "The output should be a single score (0-3) indicating {criterion_definition}.\n\n"
    "Query: {input1}\n"
    "Passage: {input2}\n"
    "{criterion_name}:\n\n"
    'Output your rating as a valid JSON object containing a single key "criterion_score", like this: {{"criterion_score": <integer_score_0_to_3>}}'
)
rate4_DECOMP_PROMPT_TEMPLATE_FACTCHECK = (
    "Please rate how well the given passage meets the {criterion_name} criterion in relation to the claim. "
    "The output should be a single score (0-3) indicating {criterion_definition}.\n\n"
    "Claim: {input1}\n"
    "Passage: {input2}\n"
    "{criterion_name}:\n\n"
    'Output your rating as a valid JSON object containing a single key "criterion_score", like this: {{"criterion_score": <integer_score_0_to_3>}}'
)
rate4_DECOMP_PROMPT_TEMPLATE_NLI = (
    "Please rate how well the given hypothesis meets the {criterion_name} criterion in relation to the premise. "
    "The output should be a single score (0–3) indicating {criterion_definition}.\n\n"
    "Premise: {input1}\n"
    "Hypothesis: {input2}\n"
    "{criterion_name}:\n\n"
    'Output your rating as a valid JSON object containing a single key "criterion_score", like this: {{"criterion_score": <integer_score_0_to_3>}}'
)

# --- rate4 Final Grading System Message---
rate4_FINAL_SYSTEM_DEFAULT = (
    "You are a search quality rater evaluating the relevance of passages. Given a query and passage, you "
    "must provide a score on an integer scale of 0 to 3 with the following meanings:\n"
    "3 = Perfectly relevant\n2 = Highly relevant\n1 = Related\n0 = Irrelevant\n" 
    "Base your decision on the provided sub-scores.\n"
    "Your output MUST be a valid JSON object containing a single key 'final_relevance_score' with the integer score."
)
rate4_FINAL_SYSTEM_FACTCHECK = (
    "You are a search quality rater evaluating evidence relevance for fact-checking. Given a claim, passage and sub-scores, provide a final score (0-3):\n"
    "3 = Perfectly relevant (direct support/refutation)\n2 = Highly relevant (helps verification)\n1 = Related (topic match, no verification aid)\n0 = Irrelevant\n"
    "Base your decision on the provided sub-scores.\n"
    "Your output MUST be a valid JSON object containing a single key 'final_relevance_score' with the integer score."
)
rate4_FINAL_SYSTEM_NLI = (
    "You are a search quality rater evaluating entailment. Given a premise, hypothesis and sub-scores, provide a final score (0-3):\n"
    "3 = Perfectly entailed\n2 = Mostly entailed\n1 = Related but not entailed\n0 = Not entailed/Contradicted\n"
    "Base your decision on the provided sub-scores.\n"
    "Your output MUST be a valid JSON object containing a single key 'final_relevance_score' with the integer score."
)

# --- rate4 Final Grading Prompt Template---
rate4_FINAL_PROMPT_TEMPLATE_DEFAULT = (
    "Please rate how the given passage is relevant to the query based on the given scores. "
    "The output must be only a score that indicates how relevant they are.\n\n"
    "Query: {input1}\n"
    "Passage: {input2}\n"
    "Exactness: {Exactness_score}\nTopicality: {Topicality_score}\nCoverage: {Coverage_score}\nContextual Fit: {Contextual_Fit_score}\n"
    "Score:\n\n"
    'Output your final rating as a valid JSON object containing a single key "final_relevance_score", like this: {{"final_relevance_score": <integer_score_0_to_3>}}'
)
rate4_FINAL_PROMPT_TEMPLATE_FACTCHECK = (
    "Please rate how relevant the given passage is to the claim based on the given scores.\n\n"
    "Claim: {input1}\n"
    "Passage: {input2}\n"
    "Exactness: {Exactness_score}\nTopicality: {Topicality_score}\nCoverage: {Coverage_score}\nContextual Fit: {Contextual_Fit_score}\n"
    "Score:\n\n"
    'Output your final rating as a valid JSON object containing a single key "final_relevance_score", like this: {{"final_relevance_score": <integer_score_0_to_3>}}'
)
rate4_FINAL_PROMPT_TEMPLATE_NLI = (
    "Please rate how well the given hypothesis is entailed by the premise based on the given scores. "
    "The output must be only a score that indicates the degree of entailment.\n\n"
    "Premise: {input1}\n"
    "Hypothesis: {input2}\n"
    "Exactness: {Exactness_score}\nTopicality: {Topicality_score}\nCoverage: {Coverage_score}\nContextual Fit: {Contextual_Fit_score}\n"
    "Score:\n\n"
    'Output your final rating as a valid JSON object containing a single key "final_relevance_score", like this: {{"final_relevance_score": <integer_score_0_to_3>}}'
)

# --- rate-CoT Prompts ---
COT_PHASE1_PROMPT_TEMPLATE_DEFAULT = (
    "Instruction: Given a passage and a query, predict whether the passage includes an answer to the query by producing either \"Yes\" or \"No\".\n"
    "Question: {input1}\nPassage: {input2}\nAnswer:\n\n"
    'Output your prediction as a valid JSON object containing a single key "has_answer", like this: {{"has_answer": "Yes"}} or {{"has_answer": "No"}}'
)
COT_PHASE1_PROMPT_TEMPLATE_FACTCHECK = (
    "Instruction: Given a passage and a claim, predict whether the passage includes information that supports or refutes the claim by producing either \"Yes\" or \"No\".\n"
    "Claim: {input1}\nPassage: {input2}\nAnswer:\n\n"
    'Output your prediction as a valid JSON object containing a single key "has_answer", like this: {{"has_answer": "Yes"}} or {{"has_answer": "No"}}'
)
COT_PHASE1_PROMPT_TEMPLATE_NLI = (
    "Instruction: Given a hypothesis and a premise, predict whether the hypothesis is entailed by the premise by producing either \"Yes\" or \"No\".\n"
    "Premise: {input1}\nHypothesis: {input2}\nAnswer:\n\n"
    'Output your prediction as a valid JSON object containing a single key "has_answer", like this: {{"has_answer": "Yes"}} or {{"has_answer": "No"}}'
)
# Phase 2 reuses rate4 Decomp System & Prompt Templates

COT_PHASE3_RELEVANT_SYSTEM_DEFAULT = (
    "You are a search quality rater. Provide a final relevance score (2 or 3).\n"
    "2 = Highly relevant\n3 = Perfectly relevant\n"
    "Your output MUST be a valid JSON object containing a single key 'relevance_score'."
)
COT_PHASE3_RELEVANT_PROMPT_TEMPLATE_DEFAULT = (
    "The passage is relevant. Rate how relevant (2 or 3).\n\nQuery: {input1}\nPassage: {input2}\nScore:\n\n"
    'Output JSON: {{"relevance_score": <2_or_3>}}'
)
COT_PHASE3_IRRELEVANT_SYSTEM_DEFAULT = (
    "You are a search quality rater. Provide a final relevance score (0 or 1).\n"
    "0 = Irrelevant\n1 = Related\n"
    "Your output MUST be a valid JSON object containing a single key 'relevance_score'."
)
COT_PHASE3_IRRELEVANT_PROMPT_TEMPLATE_DEFAULT = (
    "The passage is irrelevant. Rate how irrelevant (0 or 1).\n\nQuery: {input1}\nPassage: {input2}\nScore:\n\n"
    'Output JSON: {{"relevance_score": <0_or_1>}}'
)
# FactCheck Phase 3
COT_PHASE3_RELEVANT_SYSTEM_FACTCHECK = (
    "You are a rater evaluating evidence for fact-checking. Score 2 or 3:\n"
    "2 = Highly relevant (some support/refutation)\n3 = Perfectly relevant (direct support/refutation)\n"
    "Your output MUST be a valid JSON object with key 'relevance_score'."
)
COT_PHASE3_RELEVANT_PROMPT_TEMPLATE_FACTCHECK = (
    "Passage is relevant. Rate its relevance (2 or 3).\n\nClaim: {input1}\nPassage: {input2}\nScore:\n\n"
    'Output JSON: {{"relevance_score": <2_or_3>}}'
)
COT_PHASE3_IRRELEVANT_SYSTEM_FACTCHECK = (
    "You are a rater evaluating evidence for fact-checking. Score 0 or 1:\n"
    "0 = Irrelevant\n1 = Related (no support/refutation)\n"
    "Your output MUST be a valid JSON object with key 'relevance_score'."
)
COT_PHASE3_IRRELEVANT_PROMPT_TEMPLATE_FACTCHECK = (
    "Passage irrelevant for evidence. Rate its relevance (0 or 1).\n\nClaim: {input1}\nPassage: {input2}\nScore:\n\n"
    'Output JSON: {{"relevance_score": <0_or_1>}}'
)
# NLI Phase 3
COT_PHASE3_RELEVANT_SYSTEM_NLI = (
    "You are a rater evaluating entailment. Score 2 or 3:\n"
    "2 = Mostly entailed\n3 = Perfectly entailed\n"
    "Your output MUST be a valid JSON object with key 'relevance_score'."
)
COT_PHASE3_RELEVANT_PROMPT_TEMPLATE_NLI = (
    "Hypothesis is entailed. Rate how well (2 or 3).\n\nPremise: {input1}\nHypothesis: {input2}\nScore:\n\n"
    'Output JSON: {{"relevance_score": <2_or_3>}}'
)
COT_PHASE3_IRRELEVANT_SYSTEM_NLI = (
    "You are a rater evaluating entailment. Score 0 or 1:\n"
    "0 = Not entailed/Contradicted\n1 = Related but not entailed\n"
    "Your output MUST be a valid JSON object with key 'relevance_score'."
)
COT_PHASE3_IRRELEVANT_PROMPT_TEMPLATE_NLI = (
    "Hypothesis not entailed. Rate its relevance (0 or 1).\n\nPremise: {input1}\nHypothesis: {input2}\nScore:\n\n"
    'Output JSON: {{"relevance_score": <0_or_1>}}'
)

# --- Zero-Shot Prompts ---
ZERO_SHOT_SYSTEM_DEFAULT = "You are a search quality rater evaluating passage relevance based on detailed instructions and outputting JSON."
ZERO_SHOT_PROMPT_TEMPLATE_DEFAULT = (
    "Given a query and a passage, provide a score (0-3):\n0=Irrelevant, 1=Related, 2=Highly relevant, 3=Perfectly relevant.\n\n"
    "Important: 1 if somewhat related but not completely, 2 if important info + extra, 3 if only refers to topic.\n\n"
    "Query: {input1}\nPassage: {input2}\n\n"
    "Consider intent, content match (M), trustworthiness (T), then decide final score (O).\n\n"
    'Output MUST be JSON: {{"final_score": <0-3>}}' # Simplified JSON instruction
)
ZERO_SHOT_SYSTEM_FACTCHECK = "You are a search quality rater evaluating evidence for fact-checking and outputting JSON."
ZERO_SHOT_PROMPT_TEMPLATE_FACTCHECK = (
    "Given a claim and passage, score relevance (0-3):\n0=Irrelevant, 1=Related (no help), 2=Relevant (unclear/mixed), 3=Direct Support/Refutation.\n\n"
    "Important: 1 if related but no help, 2 if important info + noise, 3 if clearly supports/refutes.\n\n"
    "Claim: {input1}\nPassage: {input2}\n\n"
    "Consider intent, support/refutation (M), trustworthiness (T), then decide final score (O).\n\n" 
    'Output MUST be JSON: {{"final_score": <0-3>}}'
)
ZERO_SHOT_SYSTEM_NLI = "You are a rater evaluating entailment. Output only the final score in JSON."
ZERO_SHOT_PROMPT_TEMPLATE_NLI = (
    "Given a premise and hypothesis, score entailment (0-3):\n0=Not entailed/Contradicted, 1=Related not entailed, 2=Mostly entailed, 3=Perfectly entailed.\n\n"
    "Important: 1 if related but not inferable, 2 if captures important implied content but not fully, 3 if clearly/fully supported.\n\n"
    "Premise: {input1}\nHypothesis: {input2}\n\n"
    "Consider premise implications, logical following (E), info gaps, then decide final score (O).\n\n"
    'Output MUST be JSON: {{"final_score": <0-3>}}'
)

# ---------- STS ----------
CRITERIA_STS = {
    "Lexical_Overlap":        "how much the two sentences share similar words or expressions",
    "Semantic_Equivalence":   "how closely the two sentences express the same meaning using different words",
    "Information_Alignment":  "whether both sentences convey the same core pieces of information",
    "Pragmatic_Consistency":  "whether the two sentences make sense in the same context or intent",
}

STS_DECOMP_PROMPT_TEMPLATE = (
    "Please rate alignment on the dimension: {criterion_name} (def: {criterion_definition}). "
    "Use a 0–3 scale:\n0 = None | 1 = Slight | 2 = Moderate | 3 = Strong\n\n"
    "Sentence A: {input1}\nSentence B: {input2}\n\n"
    'Output JSON: {{"criterion_score": <0_to_3>}}'
)

STS_FINAL_PROMPT_TEMPLATE = (
    "Using the four dimension scores below, give an overall semantic-similarity score 0-5:\n"
    "0 unrelated | 1 slight | 2 partial | 3 moderate | 4 high | 5 equivalent\n\n"
    "Sentence A: {input1}\nSentence B: {input2}\n\n"
    "Lexical_Overlap: {Lexical_Overlap_score}\n"
    "Semantic_Equivalence: {Semantic_Equivalence_score}\n"
    "Information_Alignment: {Information_Alignment_score}\n"
    "Pragmatic_Consistency: {Pragmatic_Consistency_score}\n\n"
    'Output JSON: {{"final_similarity_score": <0_to_5>}}'
)

STS_PHASE1_PROMPT_TEMPLATE = (
    "Instruction: Are the two sentences semantically related at all? "
    "Return JSON 'Yes' or 'No'.\n\nSentence A: {input1}\nSentence B: {input2}\n"
    'Output: {{"has_relation":"Yes"}} or {{"has_relation":"No"}}'
)

STS_PHASE2_PROMPT_TEMPLATE = STS_DECOMP_PROMPT_TEMPLATE  
STS_PHASE3_PROMPT_TEMPLATE = STS_FINAL_PROMPT_TEMPLATE   

STS_ZERO_SHOT_SYSTEM = (
    "You are a semantic-similarity rater. Output JSON with a score 0-5 "
    "where 0 = unrelated, 5 = semantically equivalent."
)
STS_ZERO_SHOT_PROMPT_TEMPLATE = (
    "Rate the semantic similarity 0-5:\n0 unrelated | 1 slight | 2 partial | 3 moderate | 4 high | 5 equivalent\n\n"
    "Sentence A: {input1}\nSentence B: {input2}\n\n"
    'Output JSON: {{"final_similarity_score": <0_to_5>}}'
)


METHOD_PROMPTS = {
    "rate4": {
        "default": {
            "decomp_system": rate4_DECOMP_SYSTEM_DEFAULT,
            "decomp_prompt_template": rate4_DECOMP_PROMPT_TEMPLATE_DEFAULT,
            "final_system": rate4_FINAL_SYSTEM_DEFAULT,
            "final_prompt_template": rate4_FINAL_PROMPT_TEMPLATE_DEFAULT,
            "criteria": CRITERIA_DEFAULT
        },
        "FactCheck": {
            "decomp_system": rate4_DECOMP_SYSTEM_FACTCHECK,
            "decomp_prompt_template": rate4_DECOMP_PROMPT_TEMPLATE_FACTCHECK,
            "final_system": rate4_FINAL_SYSTEM_FACTCHECK,
            "final_prompt_template": rate4_FINAL_PROMPT_TEMPLATE_FACTCHECK,
            "criteria": CRITERIA_FACTCHECK
        },
        "NLI": {
            "decomp_system": rate4_DECOMP_SYSTEM_NLI,
            "decomp_prompt_template": rate4_DECOMP_PROMPT_TEMPLATE_NLI,
            "final_system": rate4_FINAL_SYSTEM_NLI,
            "final_prompt_template": rate4_FINAL_PROMPT_TEMPLATE_NLI,
            "criteria": CRITERIA_NLI
        },
        "STS": {
            "decomp_system": None,
            "decomp_prompt_template": STS_DECOMP_PROMPT_TEMPLATE,
            "final_system": None,
            "final_prompt_template": STS_FINAL_PROMPT_TEMPLATE,
            "criteria": CRITERIA_STS,
        }
    },
    "rate_cot": {
         "default": {
             "phase1_prompt_template": COT_PHASE1_PROMPT_TEMPLATE_DEFAULT,
             "phase2_criteria": ["Exactness", "Coverage"],
             "phase2_criteria_alt": ["Contextual Fit", "Topicality"],
             "phase2_system": rate4_DECOMP_SYSTEM_DEFAULT, 
             "phase2_prompt_template": rate4_DECOMP_PROMPT_TEMPLATE_DEFAULT, 
             "phase3_relevant_system": COT_PHASE3_RELEVANT_SYSTEM_DEFAULT,
             "phase3_relevant_prompt_template": COT_PHASE3_RELEVANT_PROMPT_TEMPLATE_DEFAULT,
             "phase3_irrelevant_system": COT_PHASE3_IRRELEVANT_SYSTEM_DEFAULT,
             "phase3_irrelevant_prompt_template": COT_PHASE3_IRRELEVANT_PROMPT_TEMPLATE_DEFAULT,
             "criteria": CRITERIA_DEFAULT 
         },
         "FactCheck": {
             "phase1_prompt_template": COT_PHASE1_PROMPT_TEMPLATE_FACTCHECK,
             "phase2_criteria": ["Exactness", "Coverage"],
             "phase2_criteria_alt": ["Contextual Fit", "Topicality"],
             "phase2_system": rate4_DECOMP_SYSTEM_FACTCHECK, 
             "phase2_prompt_template": rate4_DECOMP_PROMPT_TEMPLATE_FACTCHECK, 
             "phase3_relevant_system": COT_PHASE3_RELEVANT_SYSTEM_FACTCHECK,
             "phase3_relevant_prompt_template": COT_PHASE3_RELEVANT_PROMPT_TEMPLATE_FACTCHECK,
             "phase3_irrelevant_system": COT_PHASE3_IRRELEVANT_SYSTEM_FACTCHECK,
             "phase3_irrelevant_prompt_template": COT_PHASE3_IRRELEVANT_PROMPT_TEMPLATE_FACTCHECK,
             "criteria": CRITERIA_FACTCHECK 
         },
         "NLI": {
             "phase1_prompt_template": COT_PHASE1_PROMPT_TEMPLATE_NLI,
             "phase2_criteria": ["Exactness", "Coverage"],
             "phase2_criteria_alt": ["Contextual Fit", "Topicality"],
             "phase2_system": rate4_DECOMP_SYSTEM_NLI, 
             "phase2_prompt_template": rate4_DECOMP_PROMPT_TEMPLATE_NLI, 
             "phase3_relevant_system": COT_PHASE3_RELEVANT_SYSTEM_NLI,
             "phase3_relevant_prompt_template": COT_PHASE3_RELEVANT_PROMPT_TEMPLATE_NLI,
             "phase3_irrelevant_system": COT_PHASE3_IRRELEVANT_SYSTEM_NLI,
             "phase3_irrelevant_prompt_template": COT_PHASE3_IRRELEVANT_PROMPT_TEMPLATE_NLI,
             "criteria": CRITERIA_NLI 
         },
         "STS": {
            "phase1_prompt_template": STS_PHASE1_PROMPT_TEMPLATE,
            "phase2_criteria": list(CRITERIA_STS.keys()),
            "phase2_criteria_alt": [],  
            "phase2_system": None,
            "phase2_prompt_template": STS_PHASE2_PROMPT_TEMPLATE,
            "phase3_relevant_system": None,
            "phase3_relevant_prompt_template": STS_PHASE3_PROMPT_TEMPLATE,
            "phase3_irrelevant_system": None,
            "phase3_irrelevant_prompt_template": "",
            "criteria": CRITERIA_STS,
        }
    },
    "zero_shot": {
         "default": {
             "system": ZERO_SHOT_SYSTEM_DEFAULT,
             "prompt_template": ZERO_SHOT_PROMPT_TEMPLATE_DEFAULT
         },
         "FactCheck": {
             "system": ZERO_SHOT_SYSTEM_FACTCHECK,
             "prompt_template": ZERO_SHOT_PROMPT_TEMPLATE_FACTCHECK
         },
         "NLI": {
             "system": ZERO_SHOT_SYSTEM_NLI,
             "prompt_template": ZERO_SHOT_PROMPT_TEMPLATE_NLI
         },
         "STS": {
            "system": STS_ZERO_SHOT_SYSTEM,
            "prompt_template": STS_ZERO_SHOT_PROMPT_TEMPLATE,
        }
    }
}


for task in ["QA", "QAdoc", "Twitter", "FactCheck"]:
    if task not in METHOD_PROMPTS["rate4"]:
        METHOD_PROMPTS["rate4"][task] = METHOD_PROMPTS["rate4"]["default"]
    if task not in METHOD_PROMPTS["rate_cot"]:
        METHOD_PROMPTS["rate_cot"][task] = METHOD_PROMPTS["rate_cot"]["default"]
    if task not in METHOD_PROMPTS["zero_shot"]:
        METHOD_PROMPTS["zero_shot"][task] = METHOD_PROMPTS["zero_shot"]["default"]


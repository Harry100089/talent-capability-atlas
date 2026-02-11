import json
from llm.client import call_llm
from llm.prompts import normalization_prompt


CANONICAL_TAXONOMY = [
    "Machine Learning",
    "Ranking",
    "Evaluation",
    "Infrastructure",
    "Data Pipelines",
]


def normalize_skills(raw_skills):
    prompt = normalization_prompt(raw_skills, CANONICAL_TAXONOMY)
    output = call_llm(prompt)
    return json.loads(output)

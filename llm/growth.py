import json
from llm.client import call_llm
from llm.prompts import growth_prompt


def generate_growth_plan(person_name, skills, role_target, critical_skills):
    prompt = growth_prompt(person_name, skills, role_target, critical_skills)
    output = call_llm(prompt)
    return json.loads(output).get("growth_recommendations", [])

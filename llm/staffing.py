import json
from llm.client import call_llm
from llm.prompts import staffing_prompt

def build_staffing_summary(atlas):
    summary = []

    for profile in atlas.profiles:
        skills = [
            {
                "skill": s.skill,
                "confidence": s.confidence,
                "relevance": s.relevance_to_role
            }
            for s in profile.skills
        ]

        summary.append({
            "name": profile.name,
            "skills": skills
        })

    return summary

def generate_staffing_recommendation(atlas):
    profiles_summary = build_staffing_summary(atlas)

    prompt = staffing_prompt(
        atlas.org_hint,
        atlas.role_target,
        profiles_summary
    )

    output = call_llm(prompt)

    return json.loads(output)


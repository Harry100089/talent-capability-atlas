def role_requirement_prompt(role_target, org_hint):
    return f"""
You are defining critical skills for a role.

Role: {role_target}
Org context: {org_hint}

Return STRICT JSON:

{{
  "critical_skills": ["skill1", "skill2"]
}}
"""


def skill_extraction_prompt(artifact_text):
    return f"""
Extract technical skills from artifacts.

Return STRICT JSON:
[
  {{
    "skill": "string",
    "confidence": 0-1,
    "supporting_text": "quote"
  }}
]

Artifacts:
{artifact_text}
"""


def normalization_prompt(skills, taxonomy):
    return f"""
Map raw skills to canonical taxonomy.

Raw skills:
{skills}

Taxonomy:
{taxonomy}

Return STRICT JSON list of canonical skill names.
"""


def growth_prompt(person_name, skills, role_target, critical_skills):
    return f"""
Generate a personalized growth plan.

Person: {person_name}
Current skills: {skills}
Target role: {role_target}
Critical skills: {critical_skills}

Return STRICT JSON list of 3 specific growth recommendations.
"""

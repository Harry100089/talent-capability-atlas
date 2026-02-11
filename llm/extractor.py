import json
from models.schemas import SkillSignal, Evidence
from llm.client import call_llm
from llm.prompts import skill_extraction_prompt


def build_artifact_text(artifacts):
    texts = []
    for a in artifacts:
        texts.append(
            f"artifact_id: {a.get('id', '')}, {a.get('title', '')} {a.get('repo', '')} {a.get('message', '')} {a.get('summary', '')}"
        )
    return "\n".join(texts)


def extract_skills(artifacts, critical_skills):
    text = build_artifact_text(artifacts)
    prompt = skill_extraction_prompt(text, critical_skills)
    output = call_llm(prompt)

    data = json.loads(output)

    artifact_map = {a["id"]: a for a in artifacts}

    results = []
    for item in data:
        a = artifact_map[item["artifact_id"]]

        evidence = [
            Evidence(
                source=a["type"],
                id=a["id"],
                snippet=item["supporting_text"],
                timestamp=a.get("timestamp"),
            )
        ]

        results.append(
            SkillSignal(
                skill=item["skill"],
                confidence=float(item["confidence"]),
                relevance_to_role=float(item["relevance_to_role"]),
                evidence=evidence,
            )
        )

    return results

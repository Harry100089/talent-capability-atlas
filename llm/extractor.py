import json
from models.schemas import SkillSignal, Evidence
from llm.client import call_llm
from llm.prompts import skill_extraction_prompt


def build_artifact_text(artifacts):
    texts = []
    for a in artifacts:
        texts.append(
            f"{a.get('title', '')} {a.get('message', '')} {a.get('summary', '')}"
        )
    return "\n".join(texts)


def extract_skills(artifacts):
    text = build_artifact_text(artifacts)
    prompt = skill_extraction_prompt(text)
    output = call_llm(prompt)

    data = json.loads(output)

    results = []
    for item in data:
        evidence = [
            Evidence(
                source=a["type"],
                id=a["id"],
                snippet=item["supporting_text"],
                timestamp=a.get("timestamp"),
            )
            for a in artifacts
        ]

        results.append(
            SkillSignal(
                skill=item["skill"],
                confidence=float(item["confidence"]),
                evidence=evidence,
            )
        )

    return results

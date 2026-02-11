# extractor.py
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from models.schemas import SkillSignal, Evidence

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
MODEL = "moonshotai/Kimi-K2-Instruct-0905"


def call_llm(prompt: str):
    client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_API_KEY,
    )

    print(prompt)

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": f"{prompt}"
            }
        ],
    )

    print(completion)

    return completion.choices[0].message.content


def build_artifact_text(artifacts):
    texts = []
    for a in artifacts:
        if a["type"] == "github_commit":
            texts.append(a["message"])
        elif a["type"] == "rfc":
            texts.append(f"{a['title']}: {a['summary']}")
        elif a["type"] == "jira_ticket":
            texts.append(f"{a['title']}: {a['summary']}")
    return "\n".join(texts)


def extract_skills(person: str, artifacts: list):
    artifact_text = build_artifact_text(artifacts)

    prompt = f"""
You are extracting technical skills from engineering artifacts.

Return STRICT JSON only (no commentary):

[
  {{
    "skill": "string",
    "confidence": 0.0-1.0,
    "supporting_text": "short quote"
  }}
]

Artifacts:
{artifact_text}
"""

    output = call_llm(prompt)

    # attempt to isolate JSON
    start = output.find("[")
    end = output.rfind("]") + 1
    clean = output[start:end]

    parsed = json.loads(clean)

    skills = []

    for item in parsed:
        evidence_list = [
            Evidence(
                source=a["type"],
                id=a["id"],
                snippet=a["supporting_text"],
                timestamp=a.get("timestamp"),
            )
            for a in artifacts
        ]

        skills.append(
            SkillSignal(
                skill=item["skill"],
                confidence=float(item["confidence"]),
                evidence=evidence_list,
            )
        )

    return skills

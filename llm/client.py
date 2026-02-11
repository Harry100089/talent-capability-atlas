import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import re

load_dotenv()

MODEL = "moonshotai/Kimi-K2-Instruct-0905"
HF_API_KEY = os.getenv("HF_API_KEY")

def extract_json(text: str) -> str:
    # Remove markdown code fences if present
    text = text.strip()

    # If wrapped in ```json ... ```
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text)

    return text.strip()

def call_llm(prompt: str):
    print(f"Prompt sent to LLM:\n{prompt}\n")

    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=HF_API_KEY,
    )

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )

    print(f"Output received from LLM:\n{completion}\n")

    return extract_json(completion.choices[0].message.content)

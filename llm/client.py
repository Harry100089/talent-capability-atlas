import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = "moonshotai/Kimi-K2-Instruct-0905"
HF_API_KEY = os.getenv("HF_API_KEY")


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

    return completion.choices[0].message.content

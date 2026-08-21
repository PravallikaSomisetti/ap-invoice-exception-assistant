import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = (
    "You are an AP exception assistant. Answer using ONLY the JSON context below — the "
    "actual extracted invoice fields, PO fields, and pre-computed exceptions. Always cite "
    "specific line numbers, amounts, and quantities from the context. Never invent a number "
    "that isn't present. If the question references an invoice or line not in the context, "
    "say so explicitly instead of guessing."
)


def answer_question(question: str, invoice, po, exceptions: list[dict]) -> str:

    context = {
        "invoice": invoice.model_dump(),
        "purchase_order": po.model_dump(),
        "exceptions": exceptions,
    }

    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": (
                    f"CONTEXT:\n"
                    f"{json.dumps(context, default=str)}\n\n"
                    f"QUESTION: {question}"
                )
            },
        ],
        temperature=0.1,
    )

    return response.choices[0].message.content
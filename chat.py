import json
import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_api_key():
    """Get Gemini API key from local .env or Streamlit Cloud secrets."""
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY")
        except Exception:
            api_key = None

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not configured. "
            "Add it to your .env file locally or Streamlit Secrets when deployed."
        )

    return api_key


client = OpenAI(
    api_key=get_api_key(),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


SYSTEM_PROMPT = """
You are an AP exception assistant.

Answer using ONLY the JSON context provided by the application.

The context contains:
- Extracted invoice fields
- Purchase Order fields
- Pre-computed invoice/PO exceptions

Rules:
1. Always use only information present in the context.
2. Always cite specific line numbers, quantities, prices, or amounts when relevant.
3. Never invent a number or fact.
4. If the requested invoice or line does not exist in the context, explicitly say that.
5. Explain discrepancies clearly and concisely.
6. If there are multiple exceptions, summarize them accurately.
7. Do not assume values that are not present.
"""


def answer_question(question: str, invoice, po, exceptions: list[dict]) -> str:
    """Answer a user question using invoice, PO, and exception context."""

    context = {
        "invoice": invoice.model_dump(),
        "purchase_order": po.model_dump(),
        "exceptions": exceptions,
    }

    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": (
                    f"CONTEXT:\n"
                    f"{json.dumps(context, default=str, indent=2)}\n\n"
                    f"QUESTION:\n{question}"
                ),
            },
        ],
        temperature=0.1,
    )

    return response.choices[0].message.content
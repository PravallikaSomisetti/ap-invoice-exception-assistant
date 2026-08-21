import base64
import json
import os

import pymupdf
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from models import InvoiceData


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


EXTRACTION_PROMPT = """
You are an accounts-payable document extraction engine.

Extract these fields from the invoice image(s) exactly as printed:

- invoice_number
- vendor_name
- po_reference
- invoice_date
- line_items:
  - line_no
  - description
  - quantity
  - unit_price
  - tax_amount
  - line_total
- subtotal
- tax_total
- grand_total

Rules:

1. Use numeric values exactly as printed.
2. Do not round values.
3. Do not recompute values.
4. If a field is not present, use null.
5. Number line items in the order they appear, starting at 1.
6. Do not invent information.
7. Return ONLY one valid JSON object.
8. Do not include markdown.
9. Do not include explanations.

Return JSON matching this schema:

{schema}
"""


def pdf_to_images(file_bytes: bytes) -> list[bytes]:
    """Convert PDF pages into PNG images."""

    images = []

    doc = pymupdf.open(
        stream=file_bytes,
        filetype="pdf"
    )

    for page in doc:
        pix = page.get_pixmap(dpi=200)
        images.append(pix.tobytes("png"))

    doc.close()

    return images


def extract_invoice_data(
    file_bytes: bytes,
    filename: str
) -> InvoiceData:

    # Convert PDF pages to images.
    # For PNG/JPG/JPEG, use the uploaded image directly.
    if filename.lower().endswith(".pdf"):
        images = pdf_to_images(file_bytes)
    else:
        images = [file_bytes]

    schema_str = json.dumps(
        InvoiceData.model_json_schema()
    )

    content = [
        {
            "type": "text",
            "text": EXTRACTION_PROMPT.format(
                schema=schema_str
            ),
        }
    ]

    for img in images:

        b64 = base64.b64encode(img).decode("utf-8")

        content.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{b64}"
                },
            }
        )

    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        temperature=0,
    )

    raw = response.choices[0].message.content

    if not raw:
        raise ValueError(
            "Gemini returned an empty response."
        )

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Gemini returned invalid JSON: {raw}"
        ) from e

    return InvoiceData.model_validate(data)
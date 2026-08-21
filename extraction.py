import base64
import json
import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
from openai import OpenAI
from models import InvoiceData

load_dotenv()
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
EXTRACTION_PROMPT = """You are an accounts-payable document extraction engine.
Extract these fields from the invoice image(s) exactly as printed:
- invoice_number
- vendor_name
- po_reference (the PO number this invoice references, if present)
- invoice_date
- line_items: for each line -> line_no, description, quantity, unit_price, tax_amount, line_total
- subtotal, tax_total, grand_total

Rules:
- Use numeric values exactly as printed. Do not round or recompute anything.
- If a field is not present, use null.
- Number line items in the order they appear, starting at 1.
Return ONLY a single JSON object matching this schema (no markdown, no commentary):
{schema}
"""
def pdf_to_images(file_bytes: bytes) -> list[bytes]:
    images = []
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    for page in doc:
        pix = page.get_pixmap(dpi=200)
        images.append(pix.tobytes("png"))
    return images
def extract_invoice_data(file_bytes: bytes, filename: str) -> InvoiceData:
    images = (
        pdf_to_images(file_bytes)
        if filename.lower().endswith(".pdf")
        else [file_bytes]
    )
    schema_str = json.dumps(InvoiceData.model_json_schema())
    content = [
        {
            "type": "text",
            "text": EXTRACTION_PROMPT.format(schema=schema_str)
        }
    ]
    for img in images:
        b64 = base64.b64encode(img).decode()
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{b64}"
            }
        })
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {
                "role": "user",
                "content": content
            }
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    raw = response.choices[0].message.content
    return InvoiceData.model_validate(json.loads(raw))
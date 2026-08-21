# AP Invoice Exception Assistant

An AI-powered accounts payable assistant that extracts invoice data,
compares it against purchase orders, identifies exceptions, and
answers questions about invoice discrepancies.

## Features

- Vendor invoice upload
- PDF and image invoice processing
- AI-powered invoice data extraction
- Purchase Order JSON validation
- Invoice vs PO reconciliation
- Exception detection
- Severity classification
- AI-powered exception assistant
- Structured invoice data using Pydantic
- Streamlit web interface

## Tech Stack

- Python
- Streamlit
- Gemini API
- OpenAI-compatible Gemini API
- Pydantic
- PyMuPDF
- Pandas

## Project Structure

```text
ap-invoice-exception-assistant/
├── app.py
├── extraction.py
├── matching.py
├── chat.py
├── models.py
├── requirements.txt
├── .gitignore
└── README.md
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

4. Invoice vs PO Reconciliation

The extracted invoice is compared against the uploaded Purchase Order.

The reconciliation process checks for potential discrepancies such as:

Quantity mismatches
Unit price mismatches
Missing PO lines
Unbilled PO lines
Other configured invoice/PO exceptions
5. Exception Classification

Detected exceptions are classified by severity:

Severity	Meaning
High	Critical discrepancy requiring immediate review
Medium	Significant discrepancy requiring investigation
Low	Minor discrepancy or informational exception
6. AI Exception Assistant

Users can ask natural-language questions about processed invoices.

Examples:

Why was line 1 flagged?


Which invoice lines have mismatches?


What is the difference between the invoice and PO quantity?


Why was this invoice rejected?


Which exceptions require immediate attention?

The assistant answers using only the processed invoice, PO, and exception context.

System Workflow
                ┌─────────────────────┐
                │   Vendor Invoice    │
                │    PDF / Image      │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  Document Processing │
                │      PyMuPDF         │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │    Gemini AI        │
                │ Invoice Extraction  │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  Structured Invoice │
                │   Pydantic Model    │
                └──────────┬──────────┘
                           │
                           │
                           ▼
                ┌─────────────────────┐
                │ Purchase Order JSON │
                │      Validation     │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Invoice / PO        │
                │ Reconciliation      │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Exception Detection │
                │ & Severity Analysis │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   Exception Review  │
                │     Dashboard       │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   AI AP Assistant   │
                │ Natural Language Q&A│
                └─────────────────────┘
Architecture

The project follows a modular architecture:

ap-invoice-exception-assistant/
│
├── app.py
│   └── Streamlit application and UI
│
├── extraction.py
│   └── Invoice document processing and AI extraction
│
├── matching.py
│   └── Invoice vs PO reconciliation and exception detection
│
├── chat.py
│   └── AI-powered exception assistant
│
├── models.py
│   └── Pydantic data models
│
├── sample_po.json
│   └── Sample Purchase Order
│
├── requirements.txt
│   └── Python dependencies
│
├── .gitignore
│   └── Git ignored files and secrets
│
└── README.md
    └── Project documentation
Technology Stack
Technology	Purpose
Python	Core application development
Streamlit	Web application and UI
Gemini API	AI-powered invoice extraction and assistant
OpenAI Python SDK	Gemini OpenAI-compatible API client
Pydantic	Structured data validation
PyMuPDF	PDF-to-image conversion
Pandas	Data processing and tabular visualization
python-dotenv	Environment variable management
Project Structure
app.py

Main Streamlit application.

Responsible for:

File uploads
Application state
Document processing
Exception review
Assistant interface
extraction.py

Handles invoice document processing and AI-based extraction.

Responsibilities:

PDF page rendering
Image encoding
Gemini API interaction
Structured JSON extraction
Pydantic validation
models.py

Defines the application's structured data models.

Examples:

InvoiceData
InvoiceLineItem
PurchaseOrder
PurchaseOrderLineItem
matching.py

Contains the invoice-to-PO reconciliation logic.

Responsible for detecting:

Quantity mismatches
Price mismatches
Unmatched lines
Unbilled PO lines
Other configured exceptions
chat.py

Provides the natural-language AP assistant.

The assistant receives:

Invoice Data
+
Purchase Order Data
+
Detected Exceptions

and uses that context to answer user questions.

Installation
1. Clone the repository
git clone https://github.com/PravallikaSomisetti/ap-invoice-exception-assistant.git


cd ap-invoice-exception-assistant
2. Create a virtual environment

Windows:

python -m venv venv

Activate it:

venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
Environment Configuration

The application requires a Gemini API key.

Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_api_key_here

The .env file is intentionally excluded from version control.

Never commit or expose your API key.

Running the Application

Start the Streamlit application:

streamlit run app.py

The application will open in your browser.

Usage
Step 1 — Upload Invoice

Upload a vendor invoice in PDF or image format.

Step 2 — Upload Purchase Order

Upload a JSON Purchase Order following the expected schema.

Step 3 — Process Documents

Click:

Extract & Compare

The application will:

Process the invoice
Extract invoice fields using Gemini
Validate the extracted data
Validate the Purchase Order
Compare invoice and PO line items
Detect exceptions
Display the results
Step 4 — Review Exceptions

The Exception Review section displays:

Invoice line items
PO line items
Detected exceptions
Exception severity
Invoice values
PO values
Explanation of each discrepancy
Step 5 — Ask the Assistant

Use the AI assistant to investigate the processed invoice using natural-language questions.

Example Questions
Why was line 1 flagged?


Which invoice lines have exceptions?


What quantity was expected according to the PO?


What quantity was actually invoiced?


Which lines have a price mismatch?


Are there any unbilled PO lines?


Summarize the exceptions for this invoice.
Data Validation

Pydantic is used to ensure that extracted invoice data and uploaded Purchase Order data follow the expected structure.

This helps prevent malformed data from entering the reconciliation pipeline.

The system follows the principle:

Unstructured Document
        ↓
AI Extraction
        ↓
Structured JSON
        ↓
Schema Validation
        ↓
Business Rule Validation
        ↓
Exception Detection
Security

API credentials are managed using environment variables.

The project uses:

.env

for local secrets, while .gitignore prevents the file from being committed to the repository.

No API credentials should be stored directly in Python source code.

Future Improvements

Potential extensions include:

Multi-invoice batch processing
OCR fallback for low-quality scans
Advanced fuzzy matching for invoice/PO descriptions
Vendor-level analytics
Approval workflow integration
Exportable exception reports
Database-backed invoice history
Authentication and role-based access
Email notification for high-severity exceptions
ERP integration
Audit trail for invoice decisions
Confidence scores for extracted fields
Use Case

This project demonstrates how AI can be applied to automate repetitive Accounts Payable workflows.

Instead of manually reviewing every invoice:

Manual AP Review
      ↓
Invoice Reading
      ↓
PO Lookup
      ↓
Line-by-Line Comparison
      ↓
Exception Identification
      ↓
Investigation

the application automates the workflow:

Upload
   ↓
AI Extraction
   ↓
Validation
   ↓
Reconciliation
   ↓
Exception Detection
   ↓
AI Investigation

This reduces manual effort and provides a structured approach to invoice exception handling.

Author

Pravallika Somisetti

B.Tech — Artificial Intelligence & Data Science

GitHub:
https://github.com/PravallikaSomisetti

License

This project was developed as a technical assessment project and is intended for demonstration and educational purposes.



## After replacing the README


Since you've already initialized Git, do:


```cmd
git add README.md

Then:

git commit -m "Improve project documentation"

Then:

git push

# AP Invoice Exception Assistant

> AI-powered invoice extraction, purchase-order reconciliation, exception detection, and intelligent AP document analysis.

The **AP Invoice Exception Assistant** is an AI-powered application designed to automate the manual process of reviewing vendor invoices against Purchase Orders (POs).

The application accepts a vendor invoice in PDF or image format and a structured Purchase Order in JSON format. It extracts invoice information using AI, validates the extracted data, compares invoice line items against the Purchase Order, identifies discrepancies, and provides an AI assistant for investigating detected exceptions.

---

## Features

- Vendor invoice upload
- PDF and image invoice processing
- AI-powered invoice data extraction
- Purchase Order JSON validation
- Invoice-to-PO reconciliation
- Line-level exception detection
- Exception severity classification
- AI-powered exception assistant
- Structured data validation using Pydantic
- Streamlit-based web interface
- Secure API key management using environment variables

---

## Application Workflow

```text
Vendor Invoice + Purchase Order
              |
              v
      AI Invoice Extraction
              |
              v
       Structured Validation
              |
              v
      Invoice / PO Matching
              |
              v
       Exception Detection
              |
              v
       Exception Review
```
### System Architecture

```text
                         +----------------------+
                         |    Streamlit UI      |
                         |       app.py         |
                         +----------+-----------+
                                    |
                +-------------------+-------------------+
                |                   |                   |
                v                   v                   v
       +----------------+  +----------------+  +----------------+
       |   Extraction   |  |    Matching    |  | AI Assistant   |
       | extraction.py  |  |  matching.py   |  |    chat.py     |
       +-------+--------+  +-------+--------+  +-------+--------+
               |                   |                   |
               v                   v                   v
       +----------------+  +----------------+  +----------------+
       |   Gemini API   |  | Pydantic/Data  |  |   Gemini API   |
       |                |  |   Validation   |  |                |
       +----------------+  +----------------+  +----------------+
              |
              v
        AI AP Assistant
```

### Key Components
# Invoice Extraction

The application processes vendor invoices and extracts structured information using the Gemini API.

# Extracted fields include:

Invoice number
Vendor name
PO reference
Invoice date
Line number
Description
Quantity
Unit price
Tax amount
Line total
Subtotal
Tax total
Grand total

For PDF invoices, PyMuPDF is used to render document pages into images before AI processing.

### Purchase Order Validation

Purchase Orders are uploaded as JSON files and validated using Pydantic models.

This ensures that the uploaded PO follows the expected structure before reconciliation begins.

### Invoice-to-PO Reconciliation

The extracted invoice is compared against the uploaded Purchase Order at the line-item level.

The reconciliation logic checks for discrepancies such as:

Quantity mismatches
Unit price mismatches
Unmatched invoice lines
Unbilled PO lines
Other configured invoice/PO exceptions

### Exception Classification

Detected exceptions are classified according to their severity.

Severity	Description
High	Critical discrepancy requiring immediate review
Medium	Significant discrepancy requiring investigation
Low	Minor discrepancy or informational exception

Each exception can include:

Invoice line number
Exception type
Invoice value
PO value
Explanation
Severity

### AI Exception Assistant

# The application provides an AI-powered assistant for investigating processed invoices.

The assistant receives:
```text

Extracted Invoice Data
        +
Purchase Order Data
        +
Detected Exceptions
```

It is instructed to answer questions using only the supplied context and avoid inventing values that are not present in the processed invoice or Purchase Order.

# Example Questions
```text
Why was line 1 flagged?
Which invoice lines have mismatches?
What quantity was expected according to the PO?
What quantity was actually invoiced?
Which lines have a price mismatch?
Are there any unbilled PO lines?
Summarize the exceptions for this invoice.
```

### Technology Stack
```text
Technology	Purpose
Python	Core application development
Streamlit	Web application and user interface
Gemini API	AI-powered invoice extraction and assistant
OpenAI Python SDK	OpenAI-compatible client used to access the Gemini API
Pydantic	Structured data modeling and validation
PyMuPDF	PDF processing and page rendering
Pandas	Data processing and tabular visualization
python-dotenv	Environment variable management
```
### Project Structure
```text

ap-invoice-exception-assistant/
│
├── app.py
│   └── Main Streamlit application and user interface
│
├── extraction.py
│   └── Invoice document processing and AI extraction
│
├── matching.py
│   └── Invoice-to-PO reconciliation and exception detection
│
├── chat.py
│   └── AI-powered AP exception assistant
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
│   └── Ignored files and environment secrets
│
└── README.md
    └── Project documentation
```
### File Responsibilities

## app.py

Main Streamlit application.

Responsible for:

File uploads
Application state
Invoice processing
Purchase Order validation
Exception review
AI assistant interface

## extraction.py

Handles invoice document processing and AI-based extraction.

Responsibilities include:

PDF page rendering
Image processing
Base64 encoding
Gemini API interaction
Structured JSON extraction
Pydantic validation

## models.py

Defines the application's structured data models.

Examples include:
```text
InvoiceData
InvoiceLineItem
PurchaseOrder
PurchaseOrderLineItem
```
These models ensure that invoice and PO data follow a consistent schema.

## matching.py

Contains the invoice-to-PO reconciliation logic.

Responsible for detecting:

Quantity mismatches
Unit price mismatches
Unmatched invoice lines
Unbilled PO lines
Other configured exceptions

## chat.py

Provides the natural-language AP assistant.

The assistant receives:
```text

Invoice Data
      +
Purchase Order Data
      +
Detected Exceptions
```

and uses this context to answer questions about invoice discrepancies.

### Expected Purchase Order Format

The application expects the uploaded Purchase Order to follow this JSON structure:
```text

{
  "po_number": "PO-4521",
  "vendor_name": "Acme Supplies Inc.",
  "line_items": [
    {
      "line_no": 1,
      "description": "Widget A",
      "quantity": 10,
      "unit_price": 12.0,
      "tax_rate": 0.08
    },
    {
      "line_no": 2,
      "description": "Widget B",
      "quantity": 5,
      "unit_price": 25.0,
      "tax_rate": 0.08
    }
  ]
}
```
### Data Validation

Pydantic is used to validate both extracted invoice data and uploaded Purchase Order data.

The validation pipeline is:
```text
Unstructured Invoice
        |
        v
   AI Extraction
        |
        v
    JSON Data
        |
        v
 Schema Validation
        |
        v
Structured Data Models
        |
        v
Business Rule Validation
        |
        v
Exception Detection
```
This prevents malformed or unexpected data from directly entering the reconciliation logic.

### Installation
# Prerequisites

Make sure the following are installed:

Python 3.10 or later
pip
Git
Gemini API key

### 1. Clone the Repository
```text
git clone https://github.com/PravallikaSomisetti/ap-invoice-exception-assistant.git
```
Navigate into the project directory:

cd ap-invoice-exception-assistant

### 2. Create a Virtual Environment
Windows
```text
python -m venv venv
```
Activate the environment:
```text
venv\Scripts\activate
```
macOS / Linux
```text
python3 -m venv venv
```
Activate:
```text
source venv/bin/activate
```

### 3. Install Dependencies
```text
pip install -r requirements.txt
```
# Environment Configuration

The application requires a Gemini API key.

Create a file named:
```text
.env
```
in the root directory of the project.

Add:
```text
GEMINI_API_KEY=your_gemini_api_key_here
```
Replace your_gemini_api_key_here with your actual API key.

### Security Note

The .env file is intentionally excluded from Git using .gitignore.

Never commit or expose your actual API key.

The application reads the key through an environment variable rather than storing credentials directly in the source code.

# Running the Application

Start the Streamlit application with:

streamlit run app.py

The application will open in your browser.

The default local address is:

http://localhost:8501

# How to Use
### Step 1 — Upload Vendor Invoice

Upload a vendor invoice using the invoice uploader.

Supported formats:
```text
PDF
PNG
JPG
JPEG
```
### Step 2 — Upload Purchase Order

Upload the corresponding Purchase Order as a JSON file.

The JSON must follow the expected Purchase Order structure described above.

### Step 3 — Process Documents

Click:
```text
Extract & Compare
```
The application will:

Read the uploaded invoice
Convert PDF pages into images when required
Send the invoice content to the Gemini API
Extract structured invoice information
Validate the extracted invoice data
Validate the Purchase Order
Compare invoice and PO line items
Detect exceptions
Display the reconciliation results

# Step 4 — Review Exceptions

The Exception Review section displays:

Extracted invoice line items
Purchase Order line items
Detected exceptions
Exception severity
Invoice values
PO values
Explanation of discrepancies

If no exceptions are detected, the application reports that the invoice matches the Purchase Order within the configured reconciliation rules.

# Step 5 — Ask the Assistant

Use the AI assistant to investigate the processed invoice using natural-language questions.

For example:
```text
Why was invoice INV-2024-001 flagged?
Which invoice line has a quantity mismatch?
What was the PO quantity for line 2?
What quantity was invoiced?
Which lines have price mismatches?
Are there any unbilled PO lines?
```
### Security

API credentials are managed using environment variables.

The application uses:
```text
os.getenv("GEMINI_API_KEY")
```
The actual API key is stored locally in:
```text
.env
```
The .env file is excluded from version control through .gitignore.

### Security Practices
API keys are not hard-coded
.env is excluded from Git
Sensitive credentials are not stored in source files
API keys should never be committed to public repositories
Exposed API keys should be revoked and replaced immediately

# Error Handling

The application is designed to handle common processing and validation issues, including:

Invalid Purchase Order JSON
Missing required PO fields
Unsupported invoice file types
Invalid extracted invoice data
Invoice/PO mismatches
Missing PO references
API authentication errors
API quota or rate-limit errors

# Future Improvements

The project can be extended with:

Multi-invoice batch processing
OCR fallback for low-quality scans
Advanced fuzzy matching for invoice descriptions
Vendor master integration
Database-backed invoice history
Exportable exception reports
Invoice approval workflows
Role-based authentication
Audit trails
Email notifications for high-severity exceptions
ERP integration
Vendor analytics
Confidence scores for extracted fields
Automated approval recommendations

# Use Case

The project demonstrates how AI can automate repetitive Accounts Payable workflows.

### Traditional AP Workflow
```text
Manual Invoice Review
        |
        v
Invoice Reading
        |
        v
PO Lookup
        |
        v
Line-by-Line Comparison
        |
        v
Exception Identification
        |
        v
Manual Investigation
```
### AI-Assisted Workflow
```text
Invoice Upload
      |
      v
AI Extraction
      |
      v
Data Validation
      |
      v
PO Reconciliation
      |
      v
Exception Detection
      |
      v
Exception Review
      |
      v
AI Investigation
```
The goal is to reduce manual effort while providing a structured and explainable approach to invoice exception handling.

### Project Highlights
AI-powered document understanding
Automated invoice data extraction
Structured Pydantic data models
Purchase Order JSON validation
Invoice-to-PO reconciliation
Line-level exception detection
Exception severity classification
Natural-language invoice investigation
Modular Python architecture
Streamlit-based user interface
Environment-based API key management

### Author

# Pravallika Somisetti

B.Tech — Artificial Intelligence & Data Science

GitHub:
https://github.com/PravallikaSomisetti

### License

This project was developed as a technical assessment project and is intended for demonstration and educational purposes.



### After replacing the file


Save `README.md`, then run **only these commands**:


```cmd
git add README.md
git commit -m "Add professional project documentation"
git push

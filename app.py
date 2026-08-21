import json
import pandas as pd
import streamlit as st

from models import PurchaseOrder
from extraction import extract_invoice_data
from matching import evaluate_exceptions
from chat import answer_question

st.set_page_config(page_title="AP Invoice Exception Assistant", layout="wide")
st.title("AP Invoice Exception Assistant")

if "invoices" not in st.session_state:
    st.session_state.invoices = {}

with st.sidebar:
    st.header("1. Upload documents")
    invoice_file = st.file_uploader("Vendor invoice (PDF or image)", type=["pdf", "png", "jpg", "jpeg"])
    po_file = st.file_uploader("Mock Purchase Order (JSON)", type=["json"])
    process = st.button("Extract & Compare", type="primary")

    st.divider()
    st.caption("Expected PO JSON shape")
    st.code(json.dumps({
        "po_number": "PO-4521",
        "vendor_name": "Acme Supplies Inc.",
        "line_items": [
            {"line_no": 1, "description": "Widget A", "quantity": 10, "unit_price": 12.00, "tax_rate": 0.08},
            {"line_no": 2, "description": "Widget B", "quantity": 5, "unit_price": 25.00, "tax_rate": 0.08},
        ],
    }, indent=2), language="json")

if process and invoice_file and po_file:
    with st.spinner("Extracting invoice data and comparing against PO..."):
        po = PurchaseOrder.model_validate(json.load(po_file))
        invoice = extract_invoice_data(invoice_file.read(), invoice_file.name)
        exceptions = evaluate_exceptions(invoice, po)
        st.session_state.invoices[invoice.invoice_number] = {
            "invoice": invoice, "po": po, "exceptions": exceptions
        }
    st.success(f"Processed invoice {invoice.invoice_number}")

tab1, tab2 = st.tabs(["Exception Review", "Ask the Assistant"])

with tab1:
    if not st.session_state.invoices:
        st.info("Upload an invoice and PO to get started.")
    for inv_num, data in st.session_state.invoices.items():
        st.subheader(f"Invoice {inv_num} — {data['invoice'].vendor_name}")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Extracted invoice line items**")
            st.dataframe(pd.DataFrame([li.model_dump() for li in data["invoice"].line_items]))
        with col2:
            st.markdown("**PO line items**")
            st.dataframe(pd.DataFrame([li.model_dump() for li in data["po"].line_items]))

        st.markdown("**Exceptions flagged**")
        if not data["exceptions"]:
            st.success("No exceptions — invoice matches PO within tolerance.")
        else:
            for exc in data["exceptions"]:
                icon = {"high": "🔴", "medium": "🟠", "low": "🟡"}.get(exc["severity"], "⚪")
                with st.expander(f"{icon} Line {exc['line_no']} — {exc['field']} mismatch"):
                    st.write(exc["explanation"])
                    st.caption(f"Invoice value: {exc['invoice_value']} | PO value: {exc['po_value']}")

with tab2:
    st.markdown("Ask about a processed invoice, e.g. _\"why was invoice INV-2024-001 flagged?\"_")
    question = st.text_input("Your question")
    if st.button("Ask") and question:
        target = next((n for n in st.session_state.invoices if n.lower() in question.lower()), None)
        if not target and len(st.session_state.invoices) == 1:
            target = list(st.session_state.invoices.keys())[0]

        if not target:
            st.warning(
                "Couldn't match that to a processed invoice. Available: "
                + ", ".join(st.session_state.invoices.keys())
            )
        else:
            data = st.session_state.invoices[target]
            with st.spinner("Thinking..."):
                answer = answer_question(question, data["invoice"], data["po"], data["exceptions"])
            st.markdown(answer)

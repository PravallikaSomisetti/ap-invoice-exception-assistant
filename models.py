from pydantic import BaseModel
from typing import List, Optional


class InvoiceLineItem(BaseModel):
    line_no: int
    description: str
    quantity: float
    unit_price: float
    tax_amount: float = 0.0
    line_total: float


class InvoiceData(BaseModel):
    invoice_number: str
    vendor_name: str
    po_reference: Optional[str] = None
    invoice_date: Optional[str] = None
    line_items: List[InvoiceLineItem]
    subtotal: Optional[float] = None
    tax_total: Optional[float] = None
    grand_total: Optional[float] = None


class POLineItem(BaseModel):
    line_no: int
    description: str
    quantity: float
    unit_price: float
    tax_rate: float = 0.0  # e.g. 0.08 for 8%


class PurchaseOrder(BaseModel):
    po_number: str
    vendor_name: str
    line_items: List[POLineItem]

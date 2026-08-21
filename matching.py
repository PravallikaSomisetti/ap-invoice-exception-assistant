from difflib import SequenceMatcher
from models import InvoiceData, PurchaseOrder

PRICE_TOLERANCE = 0.01
QTY_TOLERANCE = 0.001
MATCH_THRESHOLD = 0.4


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()


def match_line_items(invoice: InvoiceData, po: PurchaseOrder):
    matches = []
    used_po = set()
    for inv_line in invoice.line_items:
        best_po_line, best_score = None, 0.0
        for po_line in po.line_items:
            if po_line.line_no in used_po:
                continue
            score = similarity(inv_line.description, po_line.description)
            if score > best_score:
                best_score, best_po_line = score, po_line
        if best_po_line and best_score >= MATCH_THRESHOLD:
            used_po.add(best_po_line.line_no)
            matches.append((inv_line, best_po_line, best_score))
        else:
            matches.append((inv_line, None, best_score))
    unmatched_po = [p for p in po.line_items if p.line_no not in used_po]
    return matches, unmatched_po


def evaluate_exceptions(invoice: InvoiceData, po: PurchaseOrder) -> list[dict]:
    matches, unmatched_po = match_line_items(invoice, po)
    exceptions = []

    for inv_line, po_line, score in matches:
        if po_line is None:
            exceptions.append({
                "invoice_number": invoice.invoice_number,
                "line_no": inv_line.line_no,
                "field": "unmatched",
                "severity": "high",
                "invoice_value": f"{inv_line.description} (qty {inv_line.quantity} @ ${inv_line.unit_price})",
                "po_value": None,
                "explanation": (
                    f"Invoice line {inv_line.line_no} ('{inv_line.description}') has no matching "
                    f"line on PO {po.po_number}. Best description match confidence was {score:.0%}, "
                    f"below the {MATCH_THRESHOLD:.0%} threshold used for line matching."
                ),
            })
            continue

        if abs(inv_line.quantity - po_line.quantity) > QTY_TOLERANCE:
            exceptions.append({
                "invoice_number": invoice.invoice_number,
                "line_no": inv_line.line_no,
                "field": "quantity",
                "severity": "high" if inv_line.quantity > po_line.quantity else "medium",
                "invoice_value": str(inv_line.quantity),
                "po_value": str(po_line.quantity),
                "explanation": (
                    f"Invoice line {inv_line.line_no} ('{inv_line.description}') bills "
                    f"{inv_line.quantity} units, but PO {po.po_number} line {po_line.line_no} "
                    f"authorizes {po_line.quantity} — a difference of "
                    f"{inv_line.quantity - po_line.quantity:+g} units."
                ),
            })

        if abs(inv_line.unit_price - po_line.unit_price) > PRICE_TOLERANCE:
            delta = inv_line.unit_price - po_line.unit_price
            exceptions.append({
                "invoice_number": invoice.invoice_number,
                "line_no": inv_line.line_no,
                "field": "price",
                "severity": "high",
                "invoice_value": f"${inv_line.unit_price:.2f}",
                "po_value": f"${po_line.unit_price:.2f}",
                "explanation": (
                    f"Invoice line {inv_line.line_no} ('{inv_line.description}') bills at "
                    f"${inv_line.unit_price:.2f}/unit vs. ${po_line.unit_price:.2f}/unit on "
                    f"PO {po.po_number} line {po_line.line_no} — a difference of ${delta:+.2f}/unit "
                    f"(${delta * inv_line.quantity:+.2f} total impact)."
                ),
            })

        expected_tax = po_line.unit_price * inv_line.quantity * po_line.tax_rate
        if abs(inv_line.tax_amount - expected_tax) > max(0.5, expected_tax * 0.02):
            exceptions.append({
                "invoice_number": invoice.invoice_number,
                "line_no": inv_line.line_no,
                "field": "tax",
                "severity": "medium",
                "invoice_value": f"${inv_line.tax_amount:.2f}",
                "po_value": f"${expected_tax:.2f} (at {po_line.tax_rate:.1%})",
                "explanation": (
                    f"Invoice line {inv_line.line_no} charges ${inv_line.tax_amount:.2f} tax, but "
                    f"applying the PO's {po_line.tax_rate:.1%} rate to this line implies "
                    f"${expected_tax:.2f} — a difference of ${inv_line.tax_amount - expected_tax:+.2f}."
                ),
            })

    for po_line in unmatched_po:
        exceptions.append({
            "invoice_number": invoice.invoice_number,
            "line_no": None,
            "field": "unbilled_po_line",
            "severity": "low",
            "invoice_value": None,
            "po_value": f"{po_line.description} (qty {po_line.quantity} @ ${po_line.unit_price})",
            "explanation": (
                f"PO {po.po_number} line {po_line.line_no} ('{po_line.description}') was not "
                f"billed on this invoice — may indicate a partial shipment rather than an error."
            ),
        })

    return exceptions

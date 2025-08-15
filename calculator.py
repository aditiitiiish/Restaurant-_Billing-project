
from datetime import datetime

def calculate_bill(quantity_vars, menu, payment_method="Cash", mode="Dine-In", table="Table 1", discount_percent=0):
    subtotal = 0
    orders = []
    lines = []
    lines.append("------ Restaurant Bill ------")
    lines.append(f"Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Mode: {mode} | Table: {table} | Payment: {payment_method}")
    lines.append("-----------------------------")
    for item, var in quantity_vars.items():
        try:
            qty = var.get()
        except Exception:
            qty = int(var) if isinstance(var, (int, float)) else 0
        if qty and qty > 0:
            price = menu.get(item, 0)
            line_total = qty * price
            subtotal += line_total
            orders.append({"item": item, "quantity": qty, "price": price, "line_total": line_total})
            lines.append(f"{item} x {qty} = ₹{line_total}")

    gst = round(subtotal * 0.05, 2)
    discount = round(subtotal * (discount_percent/100), 2) if discount_percent else 0
    grand = round(subtotal + gst - discount, 2)
    lines.append("-----------------------------")
    lines.append(f"Subtotal: ₹{subtotal:.2f}")
    lines.append(f"GST (5%): ₹{gst:.2f}")
    if discount > 0:
        lines.append(f"Discount ({discount_percent}%): -₹{discount:.2f}")
    lines.append(f"Grand Total: ₹{grand:.2f}")
    lines.append("-----------------------------")
    receipt = "\n".join(lines)

    return {
        "receipt": receipt,
        "orders": orders,
        "subtotal": subtotal,
        "gst": gst,
        "discount": discount,
        "grand_total": grand,
        "payment_method": payment_method,
        "mode": mode,
        "table": table
    }

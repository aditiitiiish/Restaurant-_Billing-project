
import os
from datetime import datetime
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    REPORTLAB_OK = True
except Exception:
    REPORTLAB_OK = False

def export_pdf(receipt_text):
    os.makedirs("bills", exist_ok=True)
    filename = f"bills/bill_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    if REPORTLAB_OK:
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        y = height - 40
        for line in receipt_text.splitlines():
            c.drawString(40, y, line[:100])
            y -= 14
            if y < 40:
                c.showPage()
                y = height - 40
        c.save()
    else:
        # Fallback to .txt if reportlab missing
        filename = filename.replace(".pdf", ".txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(receipt_text)
    return filename

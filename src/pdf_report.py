from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_pdf(path: str, total_overdue: int, sent_count: int):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    c = canvas.Canvas(path, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "Invoice Reminder Summary")

    c.setFont("Helvetica", 12)
    c.drawString(50, 700, f"Total overdue invoices: {total_overdue}")
    c.drawString(50, 680, f"Emails sent: {sent_count}")

    c.showPage()
    c.save()

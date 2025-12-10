import os
from datetime import datetime
import argparse
from dotenv import load_dotenv
from colorama import Fore, init

from csv_helper import load_invoices, parse_due_date
from log_helper import load_sent_log, save_sent_invoice
from email_helper import send_reminder
from pdf_report import create_pdf

# Color output
init(autoreset=True)

# Load .env
load_dotenv()

SENDER = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")

CSV_PATH = "data/invoices_updated.csv"
LOG_PATH = "logs/sent_log.txt"
PDF_PATH = "logs/summary.pdf"

# Dry run flag
parser = argparse.ArgumentParser()
parser.add_argument("--dry", action="store_true", help="Run without sending emails")
args = parser.parse_args()

today = datetime.today().date()

# Load data
invoices = load_invoices(CSV_PATH)
sent_log = load_sent_log(LOG_PATH)

total_overdue = 0
sent_count = 0

for row in invoices:
    invoice_id = row["invoice_id"]
    client_name = row["client_name"]
    client_email = row["client_email"]
    amount = row["amount"]
    due_str = row["due_date"]
    status = row["status"].lower()

    # Parse DD-MM-YYYY
    due_date = parse_due_date(due_str)

    # Overdue + pending only
    if due_date < today and status == "pending":
        total_overdue += 1

        # Skip if already sent
        if invoice_id in sent_log:
            print(Fore.YELLOW + f"Already sent reminder for {invoice_id}")
            continue

        days_overdue = (today - due_date).days

        subject = f"Payment Reminder for Invoice {invoice_id}"
        body = f"""
Hello {client_name},

Your invoice of amount {amount} was due on {due_str}.
It is now {days_overdue} days overdue.

Please complete the payment soon.

Regards,
Sahil Automation
"""

        if args.dry:
            print(Fore.CYAN + f"[DRY RUN] Would send reminder to {client_email}")
        else:
            send_reminder(SENDER, PASSWORD, client_email, subject, body)
            print(Fore.GREEN + f"Sent reminder for {invoice_id}")
            save_sent_invoice(LOG_PATH, invoice_id)
            sent_count += 1

# Summary
print("---------------")
print(f"Total overdue invoices: {total_overdue}")
print(f"Emails sent: {sent_count}")

# PDF summary
create_pdf(PDF_PATH, total_overdue, sent_count)
print(Fore.GREEN + f"PDF summary saved to {PDF_PATH}")

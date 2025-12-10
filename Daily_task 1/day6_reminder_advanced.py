import csv
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import os

today = datetime.today().date()

sender_email = "sahillad96@zohomail.in"
app_password = "xA3b25S76eRK"
receiver_email = "sahillad96@zohomail.in"

log_file = "logs/sent_log.txt"

# Counters for summary
total_overdue = 0
emails_sent = 0

# Create log file if missing
if not os.path.exists(log_file):
    open(log_file, "w").close()

# Load existing log entries
with open(log_file, "r") as f:
    sent_invoices = set(line.strip() for line in f)

# READ FROM UPDATED CSV FILE
with open("data/invoices_updated.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        invoice_id = row["invoice_id"]
        client_name = row["client_name"]
        client_email = row["due_date"]
        amount = row["amount"]
        due_str = row["due_date"]
        status = row["status"].lower()

        due_date = datetime.strptime(row["due_date"], "%d-%m-%Y")
        due_date = due_date.date()

        # Check overdue + pending
        if due_date < today and status == "pending":
            total_overdue += 1

            # Skip duplicate reminders
            if invoice_id in sent_invoices:
                print("Already sent reminder for Invoice", invoice_id)
                continue

            days_overdue = (today - due_date).days

            subject = f"Payment Reminder for Invoice {invoice_id}"
            body = f"""
Hello {client_name},

This is a reminder that your invoice amount {amount} was due on {due_str}.
It is now {days_overdue} days overdue.

Please complete the payment.

Regards,
Sahil Automation
"""

            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = sender_email
            msg["To"] = client_email

            # Send email using Zoho SMTP
            server = smtplib.SMTP_SSL("smtp.zoho.in", 465)
            server.login(sender_email, app_password)
            server.sendmail(sender_email, client_email, msg.as_string())
            server.quit()

            print(f"Email sent for Invoice {invoice_id} to {client_email}")
            emails_sent += 1

            # Log invoice ID to avoid duplicates
            with open(log_file, "a") as f:
                f.write(invoice_id + "\n")

# Summary
print("---------------")
print("Summary for today:")
print("Total overdue invoices:", total_overdue)
print("Emails sent today:", emails_sent)

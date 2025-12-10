import csv
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import os


today = datetime.today().date()

sender_email = "sahillad96@zohomail.in"
app_password = "xA3b25S76eRK"
receiver_email = "sahillad96@zohomail.in"

log_file = "sent_log.txt"

# Create log file if missing
if not os.path.exists(log_file):
    open(log_file, "w").close()

# Load existing log entries
with open(log_file, "r") as f:
    sent_invoices = set(line.strip() for line in f)

with open("invoices.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        invoice_id = row["InvoiceID"]
        due_date = datetime.strptime(row["DueDate"], "%Y-%m-%d").date()

        # Check overdue + pending
        if due_date < today and row["Status"].lower() == "pending":

            # Check duplicate reminder
            if invoice_id in sent_invoices:
                print("Already sent reminder for Invoice", invoice_id)
                continue

            # Email details
            subject = f"Payment Reminder for Invoice {invoice_id}"
            body = f"""
Hello {row['ClientName']},

This is a reminder that your invoice amount {row['Amount']} was due on {row['DueDate']}.

Please complete the payment.

Regards,
Sahil Automation
"""

            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = sender_email
            msg["To"] = receiver_email

            # Send email using Zoho SMTP
            server = smtplib.SMTP_SSL("smtp.zoho.in", 465)
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()

            print("Email sent for Invoice", invoice_id)

            # Log invoice ID so it won't resend later
            with open(log_file, "a") as f:
                f.write(invoice_id + "\n")
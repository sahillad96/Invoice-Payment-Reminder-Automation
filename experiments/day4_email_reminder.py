import csv
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

today = datetime.today().date()

sender_email = "sahillad96@zohomail.in"
app_password = "xA3b25S76eRK"
receiver_email = "sahillad96@zohomail.in"

with open("invoices.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        due_date = datetime.strptime(row["DueDate"], "%Y-%m-%d").date()

        if due_date < today and row["Status"].lower() == "pending":
            subject = f"Payment Reminder for Invoice {row['InvoiceID']}"
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

            server = smtplib.SMTP_SSL("smtp.zoho.in", 465)
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()

            print("Email sent for Invoice", row["InvoiceID"])

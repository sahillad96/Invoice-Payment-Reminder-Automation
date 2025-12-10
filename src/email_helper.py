import smtplib
from email.mime.text import MIMEText

def send_reminder(sender: str, password: str, receiver: str, subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.zoho.in", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())

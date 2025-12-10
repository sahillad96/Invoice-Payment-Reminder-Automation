import os
import schedule
import time
from datetime import datetime
from openai import OpenAI
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# ---- CONFIGURATION ----
SENDER_EMAIL = "sahillad96@gmail.com"       # Your verified SendGrid sender email
RECEIVER_EMAIL = "sahillad96@zohomail.in"  # Recipient email

# ---- AI CLIENT ----
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_quote():
    """Generate a motivational quote using AI."""
    prompt = "Write a short motivational quote about learning and self-improvement."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    quote = response.choices[0].message.content.strip()
    return quote

def send_email(quote):
    """Send the quote using SendGrid."""
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=RECEIVER_EMAIL,
        subject="🌅 Your AI Daily Quote",
        plain_text_content=quote
    )

    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(f"Email sent successfully! Status: {response.status_code}")
    except Exception as e:
        print("Email failed:", e)

def save_quote(quote):
    """Save quote locally with date and time."""
    with open("ai_motivation_journal.txt", "a", encoding="utf-8") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timestamp} - {quote}\n\n")
    print("Quote saved locally.")

def job():
    """Main automation job."""
    quote = generate_quote()
    send_email(quote)
    save_quote(quote)
    print("Quote generated, emailed, and saved.\n")

# ---- SCHEDULER ----
schedule.every().day.at("22:08").do(job)  # Change time if needed
print("AI Quote Automation started... waiting for next scheduled time.")

while True:
    schedule.run_pending()
    time.sleep(60)

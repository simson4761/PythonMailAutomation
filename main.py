import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime

# --- SMTP Provider Settings ---
# Use Port 587 for STARTTLS (Standard)
# Use Port 465 for SSL (More secure/Older protocol)
SMTP_CONFIGS = {
    "gmail": {"server": "smtp.gmail.com", "port": 587},
    "outlook": {"server": "smtp-mail.outlook.com", "port": 587},
    "yahoo": {"server": "smtp.mail.yahoo.com", "port": 465},
    "icloud": {"server": "smtp.mail.me.com", "port": 587}
}

# --- Configuration ---
# Choose your provider settings from the dictionary above
SMTP_SERVER = SMTP_CONFIGS["gmail"]["server"]
SMTP_PORT = SMTP_CONFIGS["gmail"]["port"]

SENDER_EMAIL = "senderMail@gmail.com"
SENDER_PASSWORD = "generatedMailAppPassword"

RECIPIENT_EMAIL = "recipientMail@gmail.com"

data_payloads = [
    {
        "type": "Mail Type",
        "subject": "Mail Subject",
        "body": "Mail Body"
    },
    {
        "type": "2nd Mail Type",
        "subject": "2nd Mail Subject",
        "body": "2nd Mail Body"
    }
]


def send_data_driven_batch(payloads):
    context = ssl.create_default_context()
    server = None

    try:
        print(f"Connecting to {SMTP_SERVER}...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
        server.starttls(context=context)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        print("Login successful! Sending batch...")

        for i, email_data in enumerate(payloads, 1):
            # 2. Construct the unique message using the data
            msg = EmailMessage()
            msg['Subject'] = f"[{email_data['type']}] {email_data['subject']}"
            msg['To'] = RECIPIENT_EMAIL
            msg['From'] = SENDER_EMAIL
            msg.set_content(email_data['body'])

            server.send_message(msg)
            print(f"[{i}/{len(payloads)}] Sent report for {email_data['subject']}")

    except Exception as e:
        print(f"❌ Connection Error: {e}")
    finally:
        if server:
            server.quit()
            print("Connection closed.")


# Run it
send_data_driven_batch(data_payloads)

import mimetypes
import os
import random
import smtplib
import ssl
import time
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

# --- Common folder with all attachments ---
ATTACHMENTS_DIR =  r"C:\Users\<your-name>\Downloads"

# --- Step 1: Create lists of files by type ---
all_files = os.listdir(ATTACHMENTS_DIR)

pdf_files = [os.path.join(ATTACHMENTS_DIR, f) for f in all_files if f.lower().endswith(".pdf")]
jpeg_files = [os.path.join(ATTACHMENTS_DIR, f) for f in all_files if f.lower().endswith((".jpg", ".jpeg"))]
png_files = [os.path.join(ATTACHMENTS_DIR, f) for f in all_files if f.lower().endswith(".png")]
xcel_files = [os.path.join(ATTACHMENTS_DIR, f) for f in all_files if f.lower().endswith((".xlsx", ".csv"))]

# You can add more types if needed
all_types = pdf_files + jpeg_files + png_files + xcel_files

# --- Step 2: Randomly attach 1-3 files per email ---
for email_data in data_payloads:
    num_attachments = random.randint(1, 2)  # 1 to 2 files per email
    email_data["attachments"] = random.sample(all_types, min(num_attachments, len(all_types)))

# --- Step 3: Now `data_payloads` contains random attachments per email ---
for e in data_payloads:
    print(f"{e['subject']} -> {e['attachments']}")

def send_data_driven_batch(payloads):
    context = ssl.create_default_context()
    server = None

    try:
        print(f"Connecting to {SMTP_SERVER}...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=3600)
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

            attachments = email_data.get("attachments", [])

            for file_path in attachments:
                try:
                    mime_type, _ = mimetypes.guess_type(file_path)

                    if mime_type is None:
                        mime_type = "application/octet-stream"

                    maintype, subtype = mime_type.split("/", 1)

                    with open(file_path, "rb") as f:
                        msg.add_attachment(
                            f.read(),
                            maintype=maintype,
                            subtype=subtype,
                            filename=file_path.split("/")[-1]
                        )

                    print(f"   Attached: {file_path}")

                except Exception as att_err:
                    print(f"   ⚠️ Failed to attach {file_path}: {att_err}")

            server.send_message(msg)
            print(f"[{i}/{len(payloads)}] Sent report for {email_data['subject']}")
            time.sleep(1)

    except smtplib.SMTPServerDisconnected:
        print("⚠️ Server disconnected. Reconnecting...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        print("Reconnected. Retrying email...")
        server.send_message(msg)
        print(f"[{i}/{len(payloads)}] Sent report for {email_data['subject']} after reconnect\n")

    except Exception as e:
        print(f"❌ Connection Error: {e}")
    finally:
        if server:
            try:
                server.quit()
                print("Connection closed.")
            except Exception:
                print("Server already disconnected, skipping quit.")


# Run it
send_data_driven_batch(data_payloads)

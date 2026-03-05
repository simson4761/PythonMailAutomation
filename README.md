# 📧 Data-Driven Batch Email Sender

A lightweight Python script for sending automated, personalized batch emails via SMTP. This tool is designed to handle multiple mail providers and security protocols efficiently.

---

## 🚀 Features

- **Batch Processing:** Connects once and sends multiple emails to reduce overhead.
- **Provider Presets:** Pre-configured settings for Gmail, Outlook, Yahoo, and iCloud.
- **Protocol Flexibility:** Supports both **STARTTLS** (Port 587) and **Implicit SSL** (Port 465).
- **Data-Driven:** Define unique subjects and bodies for every recipient in a single list.

---

## ⚙️ SMTP Configuration Reference

Depending on your email provider, use the following settings in the script:

| Provider | SMTP Server | Port | Security Type |
| :--- | :--- | :--- | :--- |
| **Gmail** | `smtp.gmail.com` | 587 | STARTTLS |
| **Outlook** | `smtp-mail.outlook.com` | 587 | STARTTLS |
| **Yahoo** | `smtp.mail.yahoo.com` | 465 | SSL |
| **iCloud** | `smtp.mail.me.com` | 587 | STARTTLS |

---

## 📂 Feed Your Data

Open the script and locate the `data_payloads` list.  
Replace the sample data with your own message content using the structure below:

```python
data_payloads = [
    {
        "type": "Mail Type",
        "subject": "Mail Subject",
        "body": "Mail Body"
    },
    {
        "type": "Reminder",
        "subject": "Weekly Sync",
        "body": "Don't forget the meeting tomorrow at 9 AM."
    }
]
```

---


# 🔎 Field Descriptions

- **type** → Category of the email (e.g., Reminder, Alert, Notification)  
- **subject** → Subject line of the email  
- **body** → Main email message content  

You can add as many message objects as needed inside the list.

---

## ⚠️ Security Warning

🚨 **Never commit your email credentials to Git!**

Hardcoding passwords inside your script can lead to:

- Account compromise
- Unauthorized email usage
- Security breaches

---


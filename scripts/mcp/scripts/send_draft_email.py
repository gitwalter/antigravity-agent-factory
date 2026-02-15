import os
import re

# Import send_email from the existing script (assuming it's in the same dir)
from send_gmail import send_email

DRAFT_PATH = r"C:\Users\wpoga\.gemini\antigravity\brain\9803b5fa-661a-48fc-bc2f-20490e0a6280\draft_email_to_andreas.md"
RECIPIENT = "andreas.graeber@gmail.com"


def send_draft():
    if not os.path.exists(DRAFT_PATH):
        print(f"Draft file not found: {DRAFT_PATH}")
        return

    with open(DRAFT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract Subject
    subject_match = re.search(r"^Subject: (.+)", content, re.MULTILINE)
    if subject_match:
        subject = subject_match.group(1).strip()
        # Remove the subject line from the body to avoid duplication
        body = content.replace(f"Subject: {subject}\n", "").strip()
        # Also remove potential extra newlines at start
        body = body.lstrip()
    else:
        subject = "Antigravity Agent Factory Update"
        body = content

    print(f"Sending email to: {RECIPIENT}")
    print(f"Subject: {subject}")
    print(f"Body length: {len(body)} chars")

    success = send_email(RECIPIENT, subject, body)
    if success:
        print("Draft sent successfully.")
    else:
        print("Failed to send draft.")


if __name__ == "__main__":
    send_draft()

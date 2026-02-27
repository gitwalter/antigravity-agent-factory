---
agents:
- none
category: routing
description: Send emails using the cached Google Workspace credentials.
knowledge:
- none
name: sending-emails
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---

# Send Email Skill

This skill allows agents to send emails via the user's Gmail account using a Python script.

## When to Use
Use this skill when you need to perform automated email communication, such as sending reports, notifications, or project updates.

## Prerequisites
- Valid Gmail credentials stored in `.gemini/antigravity/brain/...` (configured).
- `google-api-python-client` installed.

## Process
1. Prepare the email recipient, subject, and body.
2. Formulate the python command with the appropriate arguments.
3. Execute the command and monitor for success or failure logs.

## Best Practices
- Always verify recipient email addresses before sending.
- Keep email bodies concise and professional.
- Use descriptive subjects to ensure clarity for the recipient.

## Tools

### Send Email

Send an email to a specific recipient.

**Usage:**

```python
# To send an email
run_command(
    CommandLine='python scripts/send_gmail.py --to "recipient@example.com" --subject "Subject Line" --body "Message body goes here"',
    Cwd='d:/Users/wpoga/Documents/Python Scripts/antigravity-agent-factory',
    SafeToAutoRun=False, # User should confirm email sending usually
    WaitMsBeforeAsync=5000
)
```

## Security
- The script uses hardcoded paths to credentials stored outside the git repository.
- Do not modify the credential paths in `scripts/send_gmail.py`.

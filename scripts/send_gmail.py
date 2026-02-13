import os
import json
import base64
import argparse
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Paths to credentials (HARDCODED for security isolation)
GAUTH_PATH = r"C:\Users\wpoga\.gemini\antigravity\brain\a93caf4d-b65d-451f-b60a-50033eac1db7\mcp-google-workspace\.gauth.json"
TOKEN_PATH = r"C:\Users\wpoga\.gemini\antigravity\brain\a93caf4d-b65d-451f-b60a-50033eac1db7\mcp-google-workspace\.oauth2.w.pogantsch@googlemail.com.json"

def get_credentials():
    if not os.path.exists(GAUTH_PATH):
        raise FileNotFoundError(f"Client config not found at {GAUTH_PATH}")
    if not os.path.exists(TOKEN_PATH):
        raise FileNotFoundError(f"Token not found at {TOKEN_PATH}")

    with open(GAUTH_PATH, 'r') as f:
        gauth_data = json.load(f)
        client_config = gauth_data['installed']

    with open(TOKEN_PATH, 'r') as f:
        token_data = json.load(f)

    scopes = token_data['scope'].split()
    
    creds = Credentials(
        token=None, 
        refresh_token=token_data['refresh_token'],
        token_uri=client_config['token_uri'],
        client_id=client_config['client_id'],
        client_secret=client_config['client_secret'],
        scopes=scopes
    )
    return creds

def send_email(to, subject, body):
    try:
        creds = get_credentials()
        if not creds.valid:
            creds.refresh(Request())

        service = build('gmail', 'v1', credentials=creds)

        message = EmailMessage()
        message.set_content(body)
        message['To'] = to
        message['From'] = 'w.pogantsch@googlemail.com'
        message['Subject'] = subject

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'raw': encoded_message}

        sent = service.users().messages().send(userId="me", body=create_message).execute()
        print(f"Email sent successfully! Message Id: {sent['id']}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send email via Gmail API.')
    parser.add_argument('--to', required=True, help='Recipient email address')
    parser.add_argument('--subject', required=True, help='Email subject')
    parser.add_argument('--body', required=True, help='Email body')
    
    args = parser.parse_args()
    
    send_email(args.to, args.subject, args.body)

import os
import json
import base64
import argparse
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
        # We need to handle potential scope mismatches, but let's try with the existing token
    
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

def search_messages(query):
    try:
        creds = get_credentials()
        if not creds.valid:
            creds.refresh(Request())

        service = build('gmail', 'v1', credentials=creds)

        # List messages matching the query
        results = service.users().messages().list(userId='me', q=query, maxResults=5).execute()
        messages = results.get('messages', [])

        if not messages:
            print(f"No messages found for query: {query}")
            return None

        print(f"Found {len(messages)} messages. Checking headers...")
        
        for msg in messages:
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = txt.get('payload', {})
            headers = payload.get('headers', [])

            subject = ""
            sender = ""
            recipient = ""

            for h in headers:
                name = h.get('name')
                if name == 'Subject':
                    subject = h.get('value')
                if name == 'From':
                    sender = h.get('value')
                if name == 'To':
                    recipient = h.get('value')
            
            print(f"Evaluating Message: Subject='{subject}' | From='{sender}' | To='{recipient}'")
            
            # Simple heuristic: if query is in From, return From. If in To, return To.
            if "Andreas Graeber" in sender:
                print(f"FOUND EMAIL: {sender}")
                return sender
            if "Andreas Graeber" in recipient:
                 print(f"FOUND EMAIL: {recipient}")
                 return recipient

        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search Gmail messages.')
    parser.add_argument('--query', required=True, help='Search query')
    args = parser.parse_args()
    
    search_messages(args.query)

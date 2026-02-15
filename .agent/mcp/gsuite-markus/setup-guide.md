# MarkusPfundstein GSuite MCP Setup Guide

This server provides advanced interaction with Google Docs, Sheets, and Calendar.

## Installation
```powershell
uvx mcp-gsuite
```

## Configuration
Requires two JSON files in the working directory:
1. `.gauth.json`: OAuth2 client credentials.
2. `.accounts.json`: Account mapping.

### Example .gauth.json
```json
{
  "web": {
    "client_id": "...",
    "client_secret": "...",
    "redirect_uris": ["http://localhost:4100/code"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token"
  }
}
```

### Example .accounts.json
```json
{
  "accounts": [
    {
      "email": "user@example.com",
      "account_type": "personal",
      "extra_info": "Main account"
    }
  ]
}
```

## Tools
- `gsuite_search_emails`
- `gsuite_get_document`
- `gsuite_update_sheet`
- `gsuite_create_event`

# Gmail MCP Setup Guide (Auto-Auth)

This server provides high-fidelity Gmail integration with support for attachments and automated authentication.

## Prerequisites
1.  **Google Cloud Project**: [Console](https://console.cloud.google.com)
2.  **Enabled API**: Gmail API
3.  **OAuth Credentials**: Desktop App
4.  **Key File**: `gcp-oauth.keys.json` in the working directory.

## Configuration
Add the following to your `mcp_config.json`:

```json
"gmail": {
  "command": "npx",
  "args": ["-y", "@gongrzhe/server-gmail-autoauth-mcp"]
}
```

## Features
- **Send Emails**: `send_email` with attachments.
- **Drafts**: `draft_email`.
- **Search**: `search_emails` with advanced syntax.
- **Labels**: `list_labels`, `create_label`.
- **Filters**: Advanced filter management.

## Support
See [GongRzhe/Gmail-MCP-Server](https://github.com/GongRzhe/Gmail-MCP-Server) for full documentation.

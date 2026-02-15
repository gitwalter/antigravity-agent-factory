# IsaacPhi GDrive MCP Setup Guide

Integrates Google Drive and Sheets functionality for file operations and spreadsheet manipulation.

## Installation
```powershell
npx -y github:isaacphi/mcp-gdrive
```

## Configuration
Required environment variables:
- `GDRIVE_CREDS_DIR`: Path to the directory containing OAuth keys.
- `CLIENT_ID`: Google OAuth Client ID.
- `CLIENT_SECRET`: Google OAuth Client Secret.

Place `gcp-oauth.keys.json` in the directory specified by `GDRIVE_CREDS_DIR`.

## Features
- **Drive**: Search and read files (automatically exports Docs to Markdown).
- **Sheets**: Read and update spreadsheet data.

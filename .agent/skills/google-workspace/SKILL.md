---
description: Integration with Google Workspace (Drive, Gmail, Calendar) via MCP
name: google-workspace
type: skill
---
# Google Workspace Integration

Use Google Workspace MCP servers to manage files, emails, and calendar events.

## Capabilities

- **Google Drive**: List, read, and search files.
- **Gmail**: Send, read, and manage emails (if supported by specific server implementation).
- **Google Calendar**: List, create, and update events.

## Process

1.  **Authentication**: Ensure specific environment variables (like OAuth tokens or `GOOGLE_APPLICATION_CREDENTIALS`) are set if required by the specific server implementation (often interactive on first use).
2.  **Selection**: Choose the correct tool for the task (e.g., `gdrive` for files, `google-calendar` for events).
3.  **Execution**: Run the tool with appropriate parameters.

## Example Usage

### Google Drive: List Files
```python
response = await client.chat.completions.create(
    messages=[{"role": "user", "content": "List files in the 'Project X' folder"}],
    tools=[{
        "type": "mcp",
        "name": "gdrive",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-gdrive"]
    }]
)
```

### Google Calendar: Create Event
```python
response = await client.chat.completions.create(
    messages=[{"role": "user", "content": "Schedule a meeting with the team on Friday at 2 PM"}],
    tools=[{
        "type": "mcp",
        "name": "google-calendar",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-google-calendar"]
    }]
)
```

### Gmail: Draft Email
```python
response = await client.chat.completions.create(
    messages=[{"role": "user", "content": "Draft an email to john@example.com about the update"}],
    tools=[{
        "type": "mcp",
        "name": "gmail",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-gmail"]
    }]
)
```

## Best Practices

- **Privacy**: Be cautious when reading personal emails or files.
- **Authentication**: These servers usually require an initial OAuth handshake. Ensure this is completed.
- **Rate Limits**: Respcet Google API rate limits.

## Alternative: Local Mount Access

If you have **Google Drive for Desktop** installed, the agent can access files directly via the file system without using the MCP server.

**Path Examples (Windows):**
- `G:\My Drive\`
- `C:\Users\Username\Google Drive\`

**When to use Mount vs MCP:**
- **Use Mount (File System)**: When you need to read/write large files, perform complex file operations (unzip, move), or treat it as a standard directory.
- **Use MCP (API)**: For searching metadata, listing files without syncing, managing permissions, or when Drive is not mounted locally.

### Example: Reading from Mounted Drive
```python
# specific file path
file_content = open("G:\\My Drive\\Project Docs\\specs.docx", "r").read()
```

## Related
- MCP Servers: `gdrive`, `gmail`, `google-calendar`

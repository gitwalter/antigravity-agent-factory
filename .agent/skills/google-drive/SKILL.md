---
name: google-drive
description: Manage files in Google Drive using the Google Drive MCP server.
type: skill
---

# Google Drive Skill

This skill provides access to Google Drive file management capabilities via the `gdrive` MCP server.

## When to Use
Use this skill when you need to manage files and folders on Google Drive, including searching, reading content, and uploading new data.

## Prerequisites
- Google Drive MCP server configured and authorized.
- Active Google account with Drive access.

## Capabilities
- List files and folders.
- Search for files.
- Read file content.
- Upload/Create files.

## Process
1. Determine the file or folder operation required.
2. Use `gdrive_search_files` or `gdrive_list_files` to find targets.
3. Perform the read/write operation using the appropriate tool.
4. Verify the operation's success via metadata or content check.

## Best Practices
- Use specific search queries (MIME types, names) to minimize data transfer.
- Always handle potential authentication errors gracefully.
- Validate file paths and permissions before attempting writes.

## Tools (MCP)
These tools are provided by the `gdrive` MCP server:
- `gdrive_list_files`
- `gdrive_search_files`
- `gdrive_read_file`
- `gdrive_upload_file`

## Usage Examples

### Listing Files
```python
# List files in root
results = await gdrive_list_files()
```

### Searching Files
```python
# Search for PDFs
results = await gdrive_search_files(query="mimeType = 'application/pdf'")
```

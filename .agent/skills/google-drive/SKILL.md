---
name: google-drive
description: Manage files in Google Drive using the Google Drive MCP server.
type: skill
---

# Google Drive Skill

This skill provides access to Google Drive file management capabilities via the `gdrive` MCP server.

## Capabilities
- List files and folders.
- Search for files.
- Read file content.
- Upload/Create files.

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

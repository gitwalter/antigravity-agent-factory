# Filesystem MCP Server Setup Guide

## Overview

The Filesystem MCP Server provides secure file operations with configurable access controls. It's part of the official Model Context Protocol reference implementations.

## Prerequisites

- Node.js 18+ installed
- npm or npx available

## Installation

No separate installation required. The server runs via npx:

```bash
npx @modelcontextprotocol/server-filesystem /path/to/allowed/directory
```

## Configuration

### Antigravity MCP Config (`.agent/mcp.json`)

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/project"
      ]
    }
  }
}
```

### Multiple Allowed Directories

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/project",
        "/path/to/docs",
        "/path/to/config"
      ]
    }
  }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `read_file` | Read contents of a file |
| `read_multiple_files` | Read multiple files at once |
| `write_file` | Write content to a file |
| `edit_file` | Make line-based edits with diff output |
| `create_directory` | Create a new directory |
| `list_directory` | List directory contents |
| `directory_tree` | Get recursive tree structure |
| `move_file` | Move or rename files |
| `search_files` | Search for files by pattern |
| `get_file_info` | Get file metadata |
| `list_allowed_directories` | List configured allowed directories |

## Security

- **Access Control**: Operations are restricted to specified directories
- **Path Validation**: Prevents path traversal attacks
- **Read/Write Permissions**: All operations respect filesystem permissions

## Verification

Test the server is working:

1. Add configuration to `.agent/mcp.json`
2. Restart Antigravity
3. Ask the AI to "list files in the project directory"

## Troubleshooting

### Server not responding
- Ensure Node.js 18+ is installed: `node --version`
- Check npx is available: `npx --version`

### Permission denied
- Verify the path in args is accessible
- Check filesystem permissions on the directory

### Files not found
- Ensure the path is absolute, not relative
- Verify the directory exists

## Official Documentation

- GitHub: https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem
- NPM: https://www.npmjs.com/package/@modelcontextprotocol/server-filesystem

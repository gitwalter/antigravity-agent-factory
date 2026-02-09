# Git MCP Server Setup Guide

## Overview

The Git MCP Server provides Git repository operations - commits, branches, diffs, and logs. It's part of the official Model Context Protocol reference implementations.

## Prerequisites

- Node.js 18+ installed
- Git installed and configured
- Repository to work with

## Installation

No separate installation required. The server runs via npx:

```bash
npx @modelcontextprotocol/server-git --repository /path/to/repo
```

## Configuration

### Cursor MCP Config (`.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-git",
        "--repository",
        "/path/to/repository"
      ]
    }
  }
}
```

### Current Directory (Project Root)

```json
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-git",
        "--repository",
        "."
      ]
    }
  }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `git_status` | Get current repository status |
| `git_diff` | Show changes between commits, working tree, etc. |
| `git_log` | View commit history |
| `git_show` | Show commit details |
| `git_branch` | List, create, or delete branches |
| `git_checkout` | Switch branches or restore files |
| `git_commit` | Create a new commit |
| `git_add` | Stage files for commit |
| `git_reset` | Unstage files |
| `git_stash` | Stash changes |

## Security Notes

- This server can modify the repository (commits, branches, etc.)
- Use with caution in production repositories
- Consider read-only mode for sensitive repos

## Verification

Test the server is working:

1. Add configuration to `.cursor/mcp.json`
2. Restart Cursor
3. Ask the AI "show git status" or "show recent commits"

## Troubleshooting

### Repository not found
- Ensure the path points to a valid Git repository
- Check that `.git` directory exists in the path

### Permission denied
- Verify you have write access to the repository
- Check Git credentials are configured

### Command failed
- Ensure Git is installed: `git --version`
- Check Git configuration: `git config --list`

## Official Documentation

- GitHub: https://github.com/modelcontextprotocol/servers/tree/main/src/git
- NPM: https://www.npmjs.com/package/@modelcontextprotocol/server-git

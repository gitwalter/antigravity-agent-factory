# Fetch MCP Setup Guide

Retrieve and process web content, converting HTML to markdown for LLM consumption.

## Installation
```powershell
uvx mcp-server-fetch
```

## Configuration
Add to your `mcp_config.json`:

```json
"fetch": {
  "command": "uvx",
  "args": ["mcp-server-fetch"]
}
```

## Tools
- `fetch`: Takes a URL and returns markdown.

## Arguments
- `--ignore-robots-txt`: Bypass robots restrictions.
- `--user-agent`: Custom User-Agent string.

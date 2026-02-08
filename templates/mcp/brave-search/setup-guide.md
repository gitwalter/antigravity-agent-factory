# Brave Search MCP Server Setup Guide

## Overview

The Brave Search MCP Server provides web and local search capabilities through Brave's Search API. It offers 2,000 free queries per month, making it ideal for development and moderate usage.

## Prerequisites

- Node.js 18+ installed
- Brave Search API key (free tier available)

## Getting an API Key

1. Go to https://brave.com/search/api/
2. Click "Get started for free"
3. Create an account or sign in
4. Generate an API key
5. Free tier includes 2,000 queries/month

## Installation

No separate installation required. The server runs via npx:

```bash
BRAVE_API_KEY=your-api-key npx @anthropics/mcp-server-brave-search
```

## Configuration

### Environment Variables

Create a `.env` file or set in your environment:

```bash
BRAVE_API_KEY=your-brave-api-key-here
```

### Antigravity MCP Config (`.agent/mcp.json`)
```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": [
        "-y",
        "@anthropics/mcp-server-brave-search"
      ],
      "env": {
        "BRAVE_API_KEY": "${BRAVE_API_KEY}"
      }
    }
  }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `brave_web_search` | Search the web with pagination and filtering |
| `brave_local_search` | Search local businesses (falls back to web if unavailable) |

### Web Search Parameters

- `query` (required): Search query
- `count`: Number of results (1-20, default 10)
- `offset`: Pagination offset

### Local Search Parameters

- `query` (required): Search query
- `count`: Number of results (1-5 for local, default 5)

## Use Cases

- Research and fact-checking
- Finding documentation and tutorials
- Discovering local businesses and services
- Real-time information retrieval
- Competitive analysis

## Example Usage

Once configured, you can ask the AI to:

- "Search for the latest React documentation"
- "Find restaurants near Times Square"
- "Look up best practices for Python async programming"

## Rate Limits

### Free Tier
- 2,000 queries per month
- Basic web search

### Paid Tiers
- Higher query limits
- Local search
- Additional features

## Verification

Test the server is working:

1. Set BRAVE_API_KEY in your environment
2. Add configuration to `.agent/mcp.json`
3. Restart Antigravity4. Ask the AI to "search for MCP server documentation"

## Troubleshooting

### Authentication failed
- Verify your API key is correct
- Check the key hasn't expired
- Ensure you haven't exceeded rate limits

### No results returned
- Try a different search query
- Check your internet connection
- Verify the API is available

### Rate limit exceeded
- Wait for the rate limit to reset (monthly)
- Consider upgrading to a paid plan

## Official Documentation

- Brave Search API: https://brave.com/search/api/
- GitHub: https://github.com/brave/brave-search-mcp-server
- API Documentation: https://api.search.brave.com/app/documentation

# Memory MCP Server Setup Guide

## Overview

The Memory MCP Server provides a persistent knowledge graph for maintaining context across sessions. It stores entities, relationships, and observations that persist between conversations.

## Prerequisites

- Node.js 18+ installed
- npm or npx available

## Installation

No separate installation required. The server runs via npx:

```bash
npx @modelcontextprotocol/server-memory
```

## Configuration

### Antigravity MCP Config (`.agent/mcp.json`)
```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    }
  }
}
```

### With Custom Storage Path

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ],
      "env": {
        "MEMORY_FILE_PATH": "/path/to/memory.json"
      }
    }
  }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `create_entities` | Create new entities in the knowledge graph |
| `create_relations` | Create relationships between entities |
| `add_observations` | Add observations about entities |
| `delete_entities` | Remove entities from the graph |
| `delete_observations` | Remove specific observations |
| `delete_relations` | Remove relationships |
| `read_graph` | Read the entire knowledge graph |
| `search_nodes` | Search for entities by query |
| `open_nodes` | Open specific nodes by name |

## Use Cases

### Project Context
- Store project architecture decisions
- Remember team conventions
- Track ongoing tasks and their status

### Personal Assistant
- Remember user preferences
- Track conversation history topics
- Store learned information

### Agent Memory
- Persistent memory for AI agents
- Cross-session context retention
- Knowledge accumulation over time

## Example Usage

Once configured, you can ask the AI to:

- "Remember that we're using PostgreSQL for the database"
- "What do you know about this project's architecture?"
- "Store that the API uses JWT authentication"

## Data Persistence

- Memory is stored in a JSON file
- Default location: `~/.mcp-memory/memory.json`
- Persists across Antigravity restarts
## Verification

Test the server is working:

1. Add configuration to `.agent/mcp.json`
2. Restart Antigravity3. Ask the AI to "remember that this is a test project"
4. In a new conversation, ask "what do you know about this project?"

## Troubleshooting

### Memory not persisting
- Check write permissions for the memory file location
- Verify the MEMORY_FILE_PATH is accessible

### Server not responding
- Ensure Node.js 18+ is installed
- Check npx is available

## Official Documentation

- GitHub: https://github.com/modelcontextprotocol/servers/tree/main/src/memory
- NPM: https://www.npmjs.com/package/@modelcontextprotocol/server-memory

---
name: mcp-integration
description: Model Context Protocol overview, server creation, tool exposure, and common integrations
type: skill
agents: [code-reviewer, test-generator]
knowledge: [api-integration-patterns.json]
---

# MCP Integration Skill

Build and integrate Model Context Protocol (MCP) servers to expose tools and resources to AI agents.

## When to Use

- Creating MCP servers for tool exposure
- Integrating existing services via MCP
- Using MCP servers in agent workflows
- Exposing filesystem, database, or API access via MCP
- Building provider-agnostic integrations with aisuite

## Prerequisites

```bash
pip install mcp aisuite
```

## Process

### Step 1: Understand MCP Architecture

Model Context Protocol enables standardized communication between AI applications and external resources:

- **Servers**: Expose tools, resources, and prompts
- **Clients**: Consume server capabilities
- **Tools**: Executable functions with typed inputs/outputs
- **Resources**: Read-only data sources
- **Prompts**: Template-based prompt generation

### Step 2: Create Basic MCP Server

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio

# Initialize server
server = Server("my-mcp-server")

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="get_weather",
            description="Get current weather for a location",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name or coordinates"
                    }
                },
                "required": ["location"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute a tool call."""
    if name == "get_weather":
        location = arguments.get("location", "Unknown")
        return [TextContent(
            type="text",
            text=f"Sunny, 72°F in {location}"
        )]
    raise ValueError(f"Unknown tool: {name}")

# Run server
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

### Step 3: Register MCP Server

Register server in Cursor or MCP client configuration:

**Cursor Settings** (`settings.json`):
```json
{
  "mcp.servers": {
    "my-server": {
      "command": "python",
      "args": ["path/to/server.py"]
    }
  }
}
```

**MCP Client Configuration**:
```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def connect_to_server():
    server_params = StdioServerParameters(
        command="python",
        args=["path/to/server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")
            
            # Call tool
            result = await session.call_tool("get_weather", {"location": "NYC"})
            print(result.content)
```

### Step 4: Expose Tools via MCP

```python
from mcp.server import Server
from mcp.types import Tool, TextContent
from pydantic import BaseModel

server = Server("tool-server")

class CalculatorInput(BaseModel):
    expression: str

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="calculate",
            description="Evaluate a mathematical expression",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression like '2 + 2'"
                    }
                },
                "required": ["expression"]
            }
        ),
        Tool(
            name="search_files",
            description="Search for files matching a pattern",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {"type": "string"},
                    "directory": {"type": "string", "default": "."}
                },
                "required": ["pattern"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "calculate":
        expr = arguments["expression"]
        try:
            result = eval(expr)  # In production, use safe evaluator
            return [TextContent(type="text", text=str(result))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]
    
    elif name == "search_files":
        import glob
        pattern = arguments["pattern"]
        directory = arguments.get("directory", ".")
        matches = glob.glob(f"{directory}/{pattern}")
        return [TextContent(type="text", text="\n".join(matches))]
    
    raise ValueError(f"Unknown tool: {name}")
```

### Step 5: aisuite MCP Integration

Integrate MCP with aisuite for provider-agnostic LLM access:

```python
import aisuite as ai
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("aisuite-mcp")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="chat_completion",
            description="Generate chat completion using aisuite",
            inputSchema={
                "type": "object",
                "properties": {
                    "model": {
                        "type": "string",
                        "description": "Model identifier (e.g., 'google:gemini-2.5-flash')"
                    },
                    "messages": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "role": {"type": "string"},
                                "content": {"type": "string"}
                            }
                        }
                    }
                },
                "required": ["model", "messages"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "chat_completion":
        client = ai.Client()
        
        response = client.chat.completions.create(
            model=arguments["model"],
            messages=arguments["messages"]
        )
        
        return [TextContent(
            type="text",
            text=response.choices[0].message.content
        )]
    
    raise ValueError(f"Unknown tool: {name}")
```

### Step 6: Filesystem MCP Server

```python
from mcp.server import Server
from mcp.types import Tool, TextContent, Resource
import os
from pathlib import Path

server = Server("filesystem")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="read_file",
            description="Read file contents",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="list_directory",
            description="List directory contents",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "default": "."}
                }
            }
        )
    ]

@server.list_resources()
async def list_resources() -> list[Resource]:
    """List available file resources."""
    return [
        Resource(
            uri="file:///etc/hosts",
            name="Hosts file",
            description="System hosts file",
            mimeType="text/plain"
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "read_file":
        path = arguments["path"]
        # Security: validate path is in allowed directory
        allowed_base = Path("/data")
        full_path = Path(path).resolve()
        
        if not str(full_path).startswith(str(allowed_base)):
            return [TextContent(type="text", text="Error: Access denied")]
        
        try:
            with open(path, 'r') as f:
                return [TextContent(type="text", text=f.read())]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]
    
    elif name == "list_directory":
        path = arguments.get("path", ".")
        try:
            items = os.listdir(path)
            return [TextContent(type="text", text="\n".join(items))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]
    
    raise ValueError(f"Unknown tool: {name}")
```

### Step 7: Database MCP Server

```python
from mcp.server import Server
from mcp.types import Tool, TextContent
import sqlite3
import json

server = Server("database")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="execute_query",
            description="Execute SQL query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "database": {"type": "string", "default": "default.db"}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_schema",
            description="Get database schema",
            inputSchema={
                "type": "object",
                "properties": {
                    "database": {"type": "string", "default": "default.db"},
                    "table": {"type": "string"}
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "execute_query":
        query = arguments["query"]
        db_path = arguments.get("database", "default.db")
        
        # Security: only allow SELECT queries
        if not query.strip().upper().startswith("SELECT"):
            return [TextContent(type="text", text="Error: Only SELECT queries allowed")]
        
        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query)
            rows = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return [TextContent(
                type="text",
                text=json.dumps(rows, indent=2)
            )]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]
    
    elif name == "get_schema":
        db_path = arguments.get("database", "default.db")
        table = arguments.get("table")
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.execute(
                "SELECT sql FROM sqlite_master WHERE type='table'"
                + (f" AND name='{table}'" if table else "")
            )
            schema = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            return [TextContent(
                type="text",
                text="\n".join(schema) if schema else "No tables found"
            )]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]
    
    raise ValueError(f"Unknown tool: {name}")
```

### Step 8: LangSmith MCP Integration

```python
from mcp.server import Server
from mcp.types import Tool, TextContent
from langsmith import Client

server = Server("langsmith")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_trace",
            description="Get LangSmith trace details",
            inputSchema={
                "type": "object",
                "properties": {
                    "trace_id": {"type": "string"}
                },
                "required": ["trace_id"]
            }
        ),
        Tool(
            name="search_runs",
            description="Search LangSmith runs",
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {"type": "string"},
                    "query": {"type": "string"}
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    client = Client()
    
    if name == "get_trace":
        trace_id = arguments["trace_id"]
        trace = client.read_run(trace_id)
        return [TextContent(
            type="text",
            text=json.dumps(trace.dict(), indent=2, default=str)
        )]
    
    elif name == "search_runs":
        project = arguments.get("project")
        query = arguments.get("query", "")
        
        runs = client.list_runs(
            project_name=project,
            filter=query
        )
        
        results = [{"id": r.id, "name": r.name} for r in runs]
        return [TextContent(
            type="text",
            text=json.dumps(results, indent=2)
        )]
    
    raise ValueError(f"Unknown tool: {name}")
```

## Common MCP Servers

| Server | Purpose | Tools |
|--------|---------|-------|
| Filesystem | File operations | read_file, write_file, list_directory |
| Database | SQL queries | execute_query, get_schema |
| LangSmith | Tracing/debugging | get_trace, search_runs |
| Web | HTTP requests | fetch_url, scrape_page |
| Git | Version control | get_status, create_branch |

## Best Practices

- Always validate inputs and sanitize paths
- Implement proper error handling
- Use async/await for I/O operations
- Document tools with clear descriptions
- Restrict access to sensitive operations
- Use typed schemas for tool inputs
- Handle resource cleanup properly
- Log tool invocations for debugging

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| No input validation | Validate all inputs with schemas |
| Synchronous I/O | Use async/await for all I/O |
| Unrestricted file access | Validate paths against allowed directories |
| No error handling | Wrap operations in try/except |
| Hardcoded credentials | Use environment variables or secure config |
| Missing tool descriptions | Write clear, detailed descriptions |
| Blocking operations | Use async patterns throughout |

## Related

- Knowledge: `knowledge/api-integration-patterns.json`
- Skill: `tool-usage`
- Skill: `langchain-usage`
- Skill: `langsmith-tracing`
"""
Anthropic MCP Server Template

This template demonstrates how to create a Model Context Protocol (MCP) server
that exposes resources, tools, and prompts to Claude and other MCP clients.

Usage:
    server = MCPServerTemplate()
    asyncio.run(server.run())
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent, Prompt, PromptArgument
import json


class MCPServerTemplate:
    """
    MCP server exposing resources, tools, and prompts.

    Components:
    - Resources: Data sources (files, databases, APIs)
    - Tools: Functions that can be called
    - Prompts: Reusable prompt templates
    """

    def __init__(self, name: str = "example-server"):
        """
        Initialize the MCP server.

        Args:
            name: Name of the MCP server
        """
        self.server = Server(name)
        self._setup_handlers()

    def _setup_handlers(self):
        """Set up all MCP handlers."""

        # Resources
        @self.server.list_resources()
        async def list_resources() -> list[Resource]:
            """List available resources."""
            return [
                Resource(
                    uri="file:///data/users.json",
                    name="User Database",
                    description="Database of user information",
                    mimeType="application/json",
                ),
                Resource(
                    uri="file:///data/products.json",
                    name="Product Catalog",
                    description="Catalog of available products",
                    mimeType="application/json",
                ),
            ]

        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            """Read a resource by URI."""
            if uri == "file:///data/users.json":
                return json.dumps(
                    [
                        {"id": 1, "name": "Alice", "email": "alice@example.com"},
                        {"id": 2, "name": "Bob", "email": "bob@example.com"},
                    ],
                    indent=2,
                )
            elif uri == "file:///data/products.json":
                return json.dumps(
                    [
                        {"id": 1, "name": "Widget", "price": 9.99},
                        {"id": 2, "name": "Gadget", "price": 19.99},
                    ],
                    indent=2,
                )
            else:
                raise ValueError(f"Unknown resource: {uri}")

        # Tools
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available tools."""
            return [
                Tool(
                    name="search_users",
                    description="Search for users by name or email",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Search query"}
                        },
                        "required": ["query"],
                    },
                ),
                Tool(
                    name="calculate",
                    description="Perform mathematical calculations",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "Mathematical expression to evaluate",
                            }
                        },
                        "required": ["expression"],
                    },
                ),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            """Execute a tool."""
            if name == "search_users":
                query = arguments["query"]
                # Implement actual search
                results = [{"id": 1, "name": "Alice", "email": "alice@example.com"}]
                return [TextContent(type="text", text=json.dumps(results, indent=2))]

            elif name == "calculate":
                expression = arguments["expression"]
                try:
                    result = eval(expression)
                    return [TextContent(type="text", text=f"Result: {result}")]
                except Exception as e:
                    return [TextContent(type="text", text=f"Error: {str(e)}")]

            else:
                raise ValueError(f"Unknown tool: {name}")

        # Prompts
        @self.server.list_prompts()
        async def list_prompts() -> list[Prompt]:
            """List available prompts."""
            return [
                Prompt(
                    name="code-review",
                    description="Review code for quality and security",
                    arguments=[
                        PromptArgument(
                            name="language",
                            description="Programming language",
                            required=True,
                        ),
                        PromptArgument(
                            name="code", description="Code to review", required=True
                        ),
                    ],
                ),
                Prompt(
                    name="data-analysis",
                    description="Analyze data and provide insights",
                    arguments=[
                        PromptArgument(
                            name="data_type",
                            description="Type of data to analyze",
                            required=True,
                        )
                    ],
                ),
            ]

        @self.server.get_prompt()
        async def get_prompt(name: str, arguments: dict) -> str:
            """Get a prompt template."""
            if name == "code-review":
                language = arguments["language"]
                code = arguments["code"]
                return f"""Review this {language} code for:
1. Code quality and best practices
2. Security vulnerabilities
3. Performance issues
4. Maintainability

Code:
```{language}
{code}
```

Provide detailed feedback with specific recommendations."""

            elif name == "data-analysis":
                data_type = arguments["data_type"]
                return f"""Analyze this {data_type} data:
1. Identify key patterns and trends
2. Calculate relevant statistics
3. Provide actionable insights
4. Suggest next steps

Please be thorough and data-driven in your analysis."""

            else:
                raise ValueError(f"Unknown prompt: {name}")

    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream, write_stream, self.server.create_initialization_options()
            )


# Example usage
if __name__ == "__main__":
    import asyncio

    server = MCPServerTemplate(name="example-mcp-server")

    print("Starting MCP server...")
    print("Configure your MCP client to connect to this server.")

    asyncio.run(server.run())

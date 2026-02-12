---
description: Tool design, binding, and error handling patterns for LangChain agents
name: tool-usage
type: skill
---

# Tool Usage

Tool design, binding, and error handling patterns for LangChain agents

## 
# Tool Usage Patterns Skill

Design, implement, and manage tools for LangChain/LangGraph agents.

## 
# Tool Usage Patterns Skill

Design, implement, and manage tools for LangChain/LangGraph agents.

## Process
### Step 1: Create Basic Tools

```python
from langchain_core.tools import tool
from pydantic import BaseModel, Field

@tool
def get_weather(location: str) -> str:
    """Get current weather for a location.
    
    Args:
        location: City name or coordinates
    """
    # Implementation
    return f"Sunny, 72°F in {location}"

@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression safely.
    
    Args:
        expression: Math expression like '2 + 2' or 'sqrt(16)'
    """
    import ast
    import operator
    
    ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }
    
    def eval_expr(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return ops[type(node.op)](eval_expr(node.left), eval_expr(node.right))
        raise ValueError("Unsupported expression")
    
    tree = ast.parse(expression, mode='eval')
    return str(eval_expr(tree.body))
```

### Step 2: Structured Tool Inputs

```python
from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool

class SearchInput(BaseModel):
    """Input for web search."""
    query: str = Field(description="Search query")
    num_results: int = Field(default=5, ge=1, le=20)
    domain: str | None = Field(default=None, description="Limit to domain")

def search_web(query: str, num_results: int = 5, domain: str | None = None) -> str:
    """Search the web for information."""
    # Implementation
    return f"Found {num_results} results for '{query}'"

search_tool = StructuredTool.from_function(
    func=search_web,
    name="web_search",
    description="Search the web for current information",
    args_schema=SearchInput,
)
```

### Step 3: Async Tools

```python
from langchain_core.tools import tool
import httpx

@tool
async def fetch_api(url: str, method: str = "GET") -> str:
    """Fetch data from an API endpoint.
    
    Args:
        url: The API endpoint URL
        method: HTTP method (GET, POST)
    """
    async with httpx.AsyncClient() as client:
        response = await client.request(method, url)
        response.raise_for_status()
        return response.text
```

### Step 4: Bind Tools to LLM

```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Bind tools
tools = [get_weather, calculate, search_tool]
llm_with_tools = llm.bind_tools(tools)

# Invoke
response = await llm_with_tools.ainvoke("What's the weather in NYC?")

# Check for tool calls
if response.tool_calls:
    for tool_call in response.tool_calls:
        print(f"Tool: {tool_call['name']}")
        print(f"Args: {tool_call['args']}")
```

### Step 5: Execute Tool Calls

```python
from langchain_core.messages import ToolMessage

async def execute_tools(response, tools_map: dict):
    """Execute tool calls and return results."""
    results = []
    
    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_id = tool_call["id"]
        
        if tool_name in tools_map:
            tool = tools_map[tool_name]
            try:
                if asyncio.iscoroutinefunction(tool.func):
                    result = await tool.ainvoke(tool_args)
                else:
                    result = tool.invoke(tool_args)
            except Exception as e:
                result = f"Error: {str(e)}"
        else:
            result = f"Unknown tool: {tool_name}"
        
        results.append(ToolMessage(
            content=str(result),
            tool_call_id=tool_id
        ))
    
    return results

# Usage
tools_map = {t.name: t for t in tools}
tool_results = await execute_tools(response, tools_map)
```

### Step 6: Tool Error Handling

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@tool
@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
async def reliable_api_call(endpoint: str) -> str:
    """Call an API with automatic retry on failure."""
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(endpoint)
        response.raise_for_status()
        return response.json()

# Tool with explicit error handling
@tool
def safe_file_read(path: str) -> str:
    """Read a file safely with error handling.
    
    Args:
        path: Path to the file (must be in allowed directories)
    """
    import os
    
    # Security check
    allowed_dirs = ["/data", "/tmp"]
    abs_path = os.path.abspath(path)
    
    if not any(abs_path.startswith(d) for d in allowed_dirs):
        return "Error: Access denied - path not in allowed directories"
    
    if not os.path.exists(path):
        return f"Error: File not found - {path}"
    
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"
```

### Step 7: Tool Permissions and Validation

```python
from enum import Enum
from pydantic import BaseModel, field_validator

class ToolPermission(str, Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    NETWORK = "network"

class SecureTool(BaseModel):
    """Tool with permission management."""
    name: str
    permissions: list[ToolPermission]
    allowed_users: list[str] = []
    
    def can_execute(self, user: str, required_perms: list[ToolPermission]) -> bool:
        if self.allowed_users and user not in self.allowed_users:
            return False
        return all(p in self.permissions for p in required_perms)

# Decorator for permission checking
def require_permissions(*perms: ToolPermission):
    def decorator(func):
        func._required_permissions = list(perms)
        return func
    return decorator

@tool
@require_permissions(ToolPermission.WRITE)
def write_file(path: str, content: str) -> str:
    """Write content to a file (requires WRITE permission)."""
    # Implementation
    pass
```

```python
from langchain_core.tools import tool
from pydantic import BaseModel, Field

@tool
def get_weather(location: str) -> str:
    """Get current weather for a location.
    
    Args:
        location: City name or coordinates
    """
    # Implementation
    return f"Sunny, 72°F in {location}"

@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression safely.
    
    Args:
        expression: Math expression like '2 + 2' or 'sqrt(16)'
    """
    import ast
    import operator
    
    ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }
    
    def eval_expr(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return ops[type(node.op)](eval_expr(node.left), eval_expr(node.right))
        raise ValueError("Unsupported expression")
    
    tree = ast.parse(expression, mode='eval')
    return str(eval_expr(tree.body))
```

```python
from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool

class SearchInput(BaseModel):
    """Input for web search."""
    query: str = Field(description="Search query")
    num_results: int = Field(default=5, ge=1, le=20)
    domain: str | None = Field(default=None, description="Limit to domain")

def search_web(query: str, num_results: int = 5, domain: str | None = None) -> str:
    """Search the web for information."""
    # Implementation
    return f"Found {num_results} results for '{query}'"

search_tool = StructuredTool.from_function(
    func=search_web,
    name="web_search",
    description="Search the web for current information",
    args_schema=SearchInput,
)
```

```python
from langchain_core.tools import tool
import httpx

@tool
async def fetch_api(url: str, method: str = "GET") -> str:
    """Fetch data from an API endpoint.
    
    Args:
        url: The API endpoint URL
        method: HTTP method (GET, POST)
    """
    async with httpx.AsyncClient() as client:
        response = await client.request(method, url)
        response.raise_for_status()
        return response.text
```

```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Bind tools
tools = [get_weather, calculate, search_tool]
llm_with_tools = llm.bind_tools(tools)

# Invoke
response = await llm_with_tools.ainvoke("What's the weather in NYC?")

# Check for tool calls
if response.tool_calls:
    for tool_call in response.tool_calls:
        print(f"Tool: {tool_call['name']}")
        print(f"Args: {tool_call['args']}")
```

```python
from langchain_core.messages import ToolMessage

async def execute_tools(response, tools_map: dict):
    """Execute tool calls and return results."""
    results = []
    
    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_id = tool_call["id"]
        
        if tool_name in tools_map:
            tool = tools_map[tool_name]
            try:
                if asyncio.iscoroutinefunction(tool.func):
                    result = await tool.ainvoke(tool_args)
                else:
                    result = tool.invoke(tool_args)
            except Exception as e:
                result = f"Error: {str(e)}"
        else:
            result = f"Unknown tool: {tool_name}"
        
        results.append(ToolMessage(
            content=str(result),
            tool_call_id=tool_id
        ))
    
    return results

# Usage
tools_map = {t.name: t for t in tools}
tool_results = await execute_tools(response, tools_map)
```

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@tool
@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
async def reliable_api_call(endpoint: str) -> str:
    """Call an API with automatic retry on failure."""
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(endpoint)
        response.raise_for_status()
        return response.json()

# Tool with explicit error handling
@tool
def safe_file_read(path: str) -> str:
    """Read a file safely with error handling.
    
    Args:
        path: Path to the file (must be in allowed directories)
    """
    import os
    
    # Security check
    allowed_dirs = ["/data", "/tmp"]
    abs_path = os.path.abspath(path)
    
    if not any(abs_path.startswith(d) for d in allowed_dirs):
        return "Error: Access denied - path not in allowed directories"
    
    if not os.path.exists(path):
        return f"Error: File not found - {path}"
    
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"
```

```python
from enum import Enum
from pydantic import BaseModel, field_validator

class ToolPermission(str, Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    NETWORK = "network"

class SecureTool(BaseModel):
    """Tool with permission management."""
    name: str
    permissions: list[ToolPermission]
    allowed_users: list[str] = []
    
    def can_execute(self, user: str, required_perms: list[ToolPermission]) -> bool:
        if self.allowed_users and user not in self.allowed_users:
            return False
        return all(p in self.permissions for p in required_perms)

# Decorator for permission checking
def require_permissions(*perms: ToolPermission):
    def decorator(func):
        func._required_permissions = list(perms)
        return func
    return decorator

@tool
@require_permissions(ToolPermission.WRITE)
def write_file(path: str, content: str) -> str:
    """Write content to a file (requires WRITE permission)."""
    # Implementation
    pass
```

## Tool Categories
| Category | Examples |
|----------|----------|
| Data Retrieval | web_search, database_query, api_fetch |
| Computation | calculate, analyze_data, transform |
| I/O Operations | read_file, write_file, upload |
| External Services | send_email, create_ticket, notify |
| System | execute_command, manage_process |

## Best Practices
- Write clear, detailed docstrings (LLM uses these)
- Use Pydantic for input validation
- Implement proper error handling
- Make tools async when doing I/O
- Add permission checks for sensitive operations
- Return structured data when possible
- Log tool invocations for debugging

## Anti-Patterns
| Anti-Pattern | Fix |
|--------------|-----|
| Vague docstrings | Be specific about inputs/outputs |
| No error handling | Always catch and return errors |
| Sync I/O in async | Use async for all I/O |
| No input validation | Use Pydantic schemas |
| Unrestricted access | Add permission checks |

## Related
- Knowledge: `knowledge/tool-patterns.json`
- Skill: `mcp-integration`
- Skill: `langchain-usage`

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Packages: langchain-core, langchain
> - Knowledge: tool-patterns.json

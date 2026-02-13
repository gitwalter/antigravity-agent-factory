---
description: Input validation and sanitization, output filtering, code execution safety,
  and permission management
name: security-sandboxing
type: skill
---
# Security Sandboxing

Input validation and sanitization, output filtering, code execution safety, and permission management

Implement security measures for agents: input validation, output filtering, safe code execution, and permission management.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Input Validation with Pydantic

```python
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional
import re

class UserInput(BaseModel):
    """Validated user input schema."""
    query: str = Field(
        min_length=1,
        max_length=1000,
        description="User query"
    )
    user_id: str = Field(
        pattern=r"^[a-zA-Z0-9_-]+$",
        description="Alphanumeric user ID"
    )
    context: Optional[dict] = Field(default=None)
    
    @field_validator("query")
    @classmethod
    def validate_query(cls, v: str) -> str:
        """Validate and sanitize query."""
        # Remove potentially dangerous characters
        v = re.sub(r'[<>"\']', '', v)
        
        # Check for SQL injection patterns
        sql_patterns = [
            r'(\bOR\b|\bAND\b).*=',  # SQL injection
            r';\s*(DROP|DELETE|UPDATE)',  # SQL commands
        ]
        for pattern in sql_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError("Invalid input detected")
        
        return v.strip()
    
    @field_validator("context")
    @classmethod
    def validate_context(cls, v: Optional[dict]) -> Optional[dict]:
        """Validate context dictionary."""
        if v is None:
            return None
        
        # Limit context size
        if len(str(v)) > 5000:
            raise ValueError("Context too large")
        
        # Ensure no code execution attempts
        context_str = str(v).lower()
        dangerous = ['eval', 'exec', '__import__', 'open(']
        for keyword in dangerous:
            if keyword in context_str:
                raise ValueError("Dangerous context detected")
        
        return v

# Usage
try:
    validated = UserInput(
        query="What is Python?",
        user_id="user_123"
    )
except ValidationError as e:
    print(f"Validation error: {e}")
```

### Step 2: Output Filtering and Sanitization

```python
from typing import Optional
import html
import re

class OutputFilter:
    """Filter and sanitize agent outputs."""
    
    @staticmethod
    def sanitize_html(text: str) -> str:
        """Escape HTML characters."""
        return html.escape(text)
    
    @staticmethod
    def remove_code_blocks(text: str) -> str:
        """Remove code blocks that might contain executable code."""
        # Remove markdown code blocks
        text = re.sub(r'```[\s\S]*?```', '[Code block removed]', text)
        text = re.sub(r'`[^`]+`', '[Code removed]', text)
        return text
    
    @staticmethod
    def filter_secrets(text: str) -> str:
        """Filter potential secrets."""
        # API keys pattern
        text = re.sub(
            r'[A-Za-z0-9]{32,}',
            '[Potential secret removed]',
            text
        )
        # Email addresses
        text = re.sub(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            '[Email removed]',
            text
        )
        return text
    
    @staticmethod
    def sanitize_output(text: str, strict: bool = False) -> str:
        """Comprehensive output sanitization."""
        # Basic sanitization
        text = OutputFilter.sanitize_html(text)
        
        if strict:
            # Strict mode: remove code
            text = OutputFilter.remove_code_blocks(text)
            text = OutputFilter.filter_secrets(text)
        
        # Remove control characters
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        
        return text

# Usage
filtered = OutputFilter.sanitize_output(
    agent_response,
    strict=True
)
```

### Step 3: Safe Code Execution

```python
from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins
from RestrictedPython.transformer import RestrictingNodeTransformer
import ast

class SafeCodeExecutor:
    """Safely execute Python code in a restricted environment."""
    
    def __init__(self):
        # Allowed builtins
        self.allowed_builtins = {
            'abs', 'all', 'any', 'bool', 'dict', 'enumerate',
            'float', 'int', 'len', 'list', 'max', 'min',
            'range', 'reversed', 'round', 'set', 'sorted',
            'str', 'sum', 'tuple', 'type', 'zip'
        }
        
        # Restricted builtins
        self.restricted_builtins = {
            name: getattr(safe_builtins, name)
            for name in self.allowed_builtins
            if hasattr(safe_builtins, name)
        }
    
    def execute(self, code: str, globals_dict: dict = None) -> tuple[bool, any, str]:
        """Execute code safely.
        
        Returns:
            (success, result, error_message)
        """
        if globals_dict is None:
            globals_dict = {}
        
        # Compile with restrictions
        try:
            byte_code = compile_restricted(code, '<inline>', 'exec')
        except SyntaxError as e:
            return False, None, f"Syntax error: {e}"
        except Exception as e:
            return False, None, f"Compilation error: {e}"
        
        # Prepare restricted globals
        restricted_globals = {
            '__builtins__': self.restricted_builtins,
            **globals_dict
        }
        
        # Execute
        try:
            exec(byte_code, restricted_globals)
            return True, restricted_globals.get('_result'), None
        except Exception as e:
            return False, None, f"Execution error: {e}"

# Usage
executor = SafeCodeExecutor()

success, result, error = executor.execute("""
_result = sum([1, 2, 3, 4, 5])
""")

if success:
    print(f"Result: {result}")
else:
    print(f"Error: {error}")
```

### Step 4: Permission Management

```python
from enum import Enum
from typing import Set, Optional
from dataclasses import dataclass

class Permission(str, Enum):
    """Agent permissions."""
    READ_FILE = "read_file"
    WRITE_FILE = "write_file"
    EXECUTE_CODE = "execute_code"
    NETWORK_ACCESS = "network_access"
    DATABASE_ACCESS = "database_access"
    SYSTEM_COMMANDS = "system_commands"

@dataclass
class AgentPermissions:
    """Agent permission set."""
    user_id: str
    permissions: Set[Permission]
    allowed_paths: Set[str] = None
    max_execution_time: int = 30  # seconds
    
    def __post_init__(self):
        if self.allowed_paths is None:
            self.allowed_paths = set()
    
    def has_permission(self, permission: Permission) -> bool:
        """Check if agent has permission."""
        return permission in self.permissions
    
    def can_access_path(self, path: str) -> bool:
        """Check if agent can access path."""
        if not self.allowed_paths:
            return False
        
        import os
        abs_path = os.path.abspath(path)
        
        for allowed in self.allowed_paths:
            if abs_path.startswith(os.path.abspath(allowed)):
                return True
        
        return False

class PermissionManager:
    """Manage agent permissions."""
    
    def __init__(self):
        self.permissions: dict[str, AgentPermissions] = {}
    
    def grant(self, user_id: str, permission: Permission) -> None:
        """Grant permission to user."""
        if user_id not in self.permissions:
            self.permissions[user_id] = AgentPermissions(
                user_id=user_id,
                permissions=set()
            )
        self.permissions[user_id].permissions.add(permission)
    
    def revoke(self, user_id: str, permission: Permission) -> None:
        """Revoke permission from user."""
        if user_id in self.permissions:
            self.permissions[user_id].permissions.discard(permission)
    
    def check(self, user_id: str, permission: Permission) -> bool:
        """Check if user has permission."""
        if user_id not in self.permissions:
            return False
        return self.permissions[user_id].has_permission(permission)
    
    def get_permissions(self, user_id: str) -> Optional[AgentPermissions]:
        """Get user permissions."""
        return self.permissions.get(user_id)

# Usage
pm = PermissionManager()
pm.grant("user_123", Permission.READ_FILE)
pm.grant("user_123", Permission.EXECUTE_CODE)

if pm.check("user_123", Permission.READ_FILE):
    # Allow file read
    pass
```

### Step 5: Sandboxed Tool Execution

```python
from langchain_core.tools import tool
from typing import Optional
import os

class SandboxedTool:
    """Tool wrapper with permission checking."""
    
    def __init__(self, tool_func, required_permission: Permission):
        self.tool_func = tool_func
        self.required_permission = required_permission
        self.permission_manager: Optional[PermissionManager] = None
    
    def set_permission_manager(self, pm: PermissionManager):
        """Set permission manager."""
        self.permission_manager = pm
    
    async def execute(self, user_id: str, *args, **kwargs):
        """Execute tool with permission check."""
        if self.permission_manager:
            if not self.permission_manager.check(user_id, self.required_permission):
                raise PermissionError(
                    f"User {user_id} lacks permission: {self.required_permission}"
                )
        
        return await self.tool_func(*args, **kwargs)

@tool
async def safe_file_read(path: str, user_id: str) -> str:
    """Read file with permission checking."""
    pm = PermissionManager()  # Get from context
    
    # Check permission
    if not pm.check(user_id, Permission.READ_FILE):
        return "Error: Permission denied"
    
    # Check path access
    user_perms = pm.get_permissions(user_id)
    if user_perms and not user_perms.can_access_path(path):
        return "Error: Path not allowed"
    
    # Safe file read
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error: {str(e)}"
```

### Step 6: Rate Limiting

```python
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Optional

class RateLimiter:
    """Rate limiting for agent requests."""
    
    def __init__(
        self,
        max_requests: int = 100,
        window_seconds: int = 60
    ):
        self.max_requests = max_requests
        self.window = timedelta(seconds=window_seconds)
        self.requests: dict[str, list[datetime]] = defaultdict(list)
    
    def is_allowed(self, user_id: str) -> bool:
        """Check if request is allowed."""
        now = datetime.now()
        
        # Clean old requests
        cutoff = now - self.window
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id]
            if req_time > cutoff
        ]
        
        # Check limit
        if len(self.requests[user_id]) >= self.max_requests:
            return False
        
        # Record request
        self.requests[user_id].append(now)
        return True
    
    def get_remaining(self, user_id: str) -> int:
        """Get remaining requests in window."""
        now = datetime.now()
        cutoff = now - self.window
        
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id]
            if req_time > cutoff
        ]
        
        return max(0, self.max_requests - len(self.requests[user_id]))

# Usage
rate_limiter = RateLimiter(max_requests=10, window_seconds=60)

if rate_limiter.is_allowed("user_123"):
    # Process request
    pass
else:
    # Rate limit exceeded
    raise Exception("Rate limit exceeded")
```

### Step 7: Input Size Limits

```python
from pydantic import BaseModel, Field, field_validator

class SizeLimitedInput(BaseModel):
    """Input with size limits."""
    query: str = Field(max_length=1000)
    context: Optional[str] = Field(default=None, max_length=5000)
    
    @field_validator("query", "context")
    @classmethod
    def validate_size(cls, v: Optional[str]) -> Optional[str]:
        """Validate input size."""
        if v is None:
            return None
        
        # Check character count
        if len(v) > 10000:
            raise ValueError("Input too large")
        
        # Check token estimate (rough: 1 token ≈ 4 chars)
        estimated_tokens = len(v) / 4
        if estimated_tokens > 2000:
            raise ValueError("Input exceeds token limit")
        
        return v

# Usage in agent
async def process_with_limits(input_data: dict):
    """Process input with size limits."""
    try:
        validated = SizeLimitedInput(**input_data)
        # Process validated input
        return await agent.ainvoke(validated.model_dump())
    except ValueError as e:
        return f"Error: {str(e)}"
```

### Step 8: Content Moderation

```python
from typing import List, Optional
import re

class ContentModerator:
    """Moderate agent inputs and outputs."""
    
    def __init__(self):
        # Blocked patterns
        self.blocked_patterns = [
            r'\b(hack|exploit|bypass|vulnerability)\b',
            r'<script[^>]*>.*?</script>',  # Script tags
            r'javascript:',  # JavaScript protocol
            r'on\w+\s*=',  # Event handlers
        ]
        
        # Suspicious patterns (warn but allow)
        self.suspicious_patterns = [
            r'eval\s*\(',
            r'exec\s*\(',
            r'__import__',
        ]
    
    def moderate_input(self, text: str) -> tuple[bool, Optional[str]]:
        """Moderate input text.
        
        Returns:
            (is_safe, reason_if_blocked)
        """
        text_lower = text.lower()
        
        # Check blocked patterns
        for pattern in self.blocked_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return False, f"Blocked pattern detected: {pattern}"
        
        return True, None
    
    def moderate_output(self, text: str) -> tuple[bool, str]:
        """Moderate output text.
        
        Returns:
            (is_safe, sanitized_text)
        """
        # Check for blocked content
        is_safe, reason = self.moderate_input(text)
        if not is_safe:
            return False, "[Content blocked by moderation]"
        
        # Sanitize suspicious patterns
        sanitized = text
        for pattern in self.suspicious_patterns:
            sanitized = re.sub(pattern, '[removed]', sanitized, flags=re.IGNORECASE)
        
        return True, sanitized

# Usage
moderator = ContentModerator()

is_safe, reason = moderator.moderate_input(user_input)
if not is_safe:
    return f"Input rejected: {reason}"

is_safe, sanitized = moderator.moderate_output(agent_output)
if not is_safe:
    return "[Output blocked]"
```

## Security Layers

| Layer | Purpose | Implementation |
|-------|---------|----------------|
| Input Validation | Validate user inputs | Pydantic schemas |
| Output Filtering | Sanitize outputs | OutputFilter class |
| Code Execution | Safe code running | RestrictedPython |
| Permissions | Access control | PermissionManager |
| Rate Limiting | Prevent abuse | RateLimiter |
| Content Moderation | Filter harmful content | ContentModerator |

## Best Practices

- Validate all inputs with Pydantic
- Sanitize all outputs before returning
- Use sandboxed execution for code
- Implement least-privilege permissions
- Set rate limits per user
- Log security events
- Monitor for suspicious patterns
- Keep security libraries updated

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Trusting user input | Always validate |
| No output filtering | Sanitize outputs |
| Unsafe code execution | Use RestrictedPython |
| No permission checks | Implement permission system |
| No rate limiting | Add rate limits |
| Ignoring security warnings | Address security issues |
| Hardcoded secrets | Use environment variables |
| No logging | Log security events |

## Related

- Skill: `error-handling`
- Skill: `logging-monitoring`
- Skill: `tool-usage`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

---
name: filesystem-ops
description: File reading/writing tools, directory traversal, file type detection, and security sandboxing
type: skill
agents: [code-reviewer, test-generator]
knowledge: [api-integration-patterns.json]
---

# Filesystem Operations Skill

Build secure file and directory operations for AI agents with proper sandboxing, validation, and error handling.

## When to Use

- Creating file reading/writing tools
- Building directory traversal utilities
- Implementing file search and filtering
- Adding filesystem access to agents
- Building document processing pipelines

## Prerequisites

```bash
pip install pathlib python-magic mimetypes
```

## Process

### Step 1: Basic File Operations

```python
from pathlib import Path
from typing import Optional, List
import os

class FileOperations:
    """Basic file operations with validation."""
    
    def __init__(self, allowed_directories: List[str] = None):
        """
        Args:
            allowed_directories: List of allowed directory paths (None = all)
        """
        self.allowed_dirs = [Path(d).resolve() for d in allowed_directories] if allowed_directories else None
    
    def _validate_path(self, file_path: str) -> Path:
        """Validate and resolve file path."""
        path = Path(file_path).resolve()
        
        # Check if path is in allowed directories
        if self.allowed_dirs:
            if not any(path.is_relative_to(allowed) for allowed in self.allowed_dirs):
                raise PermissionError(f"Path {path} is not in allowed directories")
        
        return path
    
    def read_file(self, file_path: str, encoding: str = "utf-8") -> str:
        """Read file contents."""
        path = self._validate_path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")
        
        try:
            with open(path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            raise ValueError(f"Cannot decode file {path} as {encoding}")
    
    def write_file(self, file_path: str, content: str, encoding: str = "utf-8") -> None:
        """Write content to file."""
        path = self._validate_path(file_path)
        
        # Create parent directories if needed
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding=encoding) as f:
            f.write(content)
    
    def file_exists(self, file_path: str) -> bool:
        """Check if file exists."""
        try:
            path = self._validate_path(file_path)
            return path.exists() and path.is_file()
        except (PermissionError, ValueError):
            return False
    
    def get_file_size(self, file_path: str) -> int:
        """Get file size in bytes."""
        path = self._validate_path(file_path)
        return path.stat().st_size

# Usage
fs = FileOperations(allowed_directories=["/data", "/tmp"])
content = fs.read_file("/data/document.txt")
fs.write_file("/tmp/output.txt", "Hello, World!")
```

### Step 2: Directory Traversal and Search

```python
from pathlib import Path
from typing import List, Optional, Callable
import fnmatch

class DirectoryOperations:
    """Directory traversal and search operations."""
    
    def __init__(self, allowed_directories: List[str] = None, max_depth: int = 10):
        """
        Args:
            allowed_directories: List of allowed directory paths
            max_depth: Maximum recursion depth
        """
        self.allowed_dirs = [Path(d).resolve() for d in allowed_directories] if allowed_directories else None
        self.max_depth = max_depth
    
    def _validate_path(self, directory_path: str) -> Path:
        """Validate directory path."""
        path = Path(directory_path).resolve()
        
        if self.allowed_dirs:
            if not any(path.is_relative_to(allowed) for allowed in self.allowed_dirs):
                raise PermissionError(f"Path {path} is not in allowed directories")
        
        if not path.exists():
            raise FileNotFoundError(f"Directory not found: {path}")
        
        if not path.is_dir():
            raise ValueError(f"Path is not a directory: {path}")
        
        return path
    
    def list_directory(self, directory_path: str, recursive: bool = False) -> List[dict]:
        """List directory contents."""
        path = self._validate_path(directory_path)
        results = []
        
        if recursive:
            for item in path.rglob("*"):
                if item.is_file():
                    results.append({
                        "path": str(item),
                        "type": "file",
                        "size": item.stat().st_size
                    })
                elif item.is_dir():
                    results.append({
                        "path": str(item),
                        "type": "directory"
                    })
        else:
            for item in path.iterdir():
                if item.is_file():
                    results.append({
                        "name": item.name,
                        "path": str(item),
                        "type": "file",
                        "size": item.stat().st_size
                    })
                elif item.is_dir():
                    results.append({
                        "name": item.name,
                        "path": str(item),
                        "type": "directory"
                    })
        
        return results
    
    def find_files(
        self,
        directory_path: str,
        pattern: str = "*",
        file_type: Optional[str] = None,
        max_results: int = 100
    ) -> List[str]:
        """Find files matching pattern."""
        path = self._validate_path(directory_path)
        results = []
        
        for item in path.rglob(pattern):
            if item.is_file():
                # Filter by file type if specified
                if file_type:
                    if item.suffix.lower() != f".{file_type.lower()}":
                        continue
                
                results.append(str(item))
                
                if len(results) >= max_results:
                    break
        
        return results
    
    def search_content(
        self,
        directory_path: str,
        search_text: str,
        file_pattern: str = "*",
        case_sensitive: bool = False
    ) -> List[dict]:
        """Search for text in files."""
        path = self._validate_path(directory_path)
        results = []
        
        if not case_sensitive:
            search_text = search_text.lower()
        
        for file_path in path.rglob(file_pattern):
            if not file_path.is_file():
                continue
            
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                search_content = content if case_sensitive else content.lower()
                
                if search_text in search_content:
                    # Find line numbers
                    lines = content.split("\n")
                    matching_lines = [
                        i + 1 for i, line in enumerate(lines)
                        if search_text in (line if case_sensitive else line.lower())
                    ]
                    
                    results.append({
                        "file": str(file_path),
                        "matches": len(matching_lines),
                        "lines": matching_lines[:10]  # First 10 matches
                    })
            except Exception:
                # Skip files that can't be read as text
                continue
        
        return results

# Usage
dir_ops = DirectoryOperations(allowed_directories=["/data"])
files = dir_ops.find_files("/data", pattern="*.py", max_results=50)
results = dir_ops.search_content("/data", "def main", file_pattern="*.py")
```

### Step 3: File Type Detection

```python
import mimetypes
import magic
from pathlib import Path
from typing import Optional, Dict

class FileTypeDetector:
    """Detect file types and MIME types."""
    
    def __init__(self):
        mimetypes.init()
        try:
            self.magic = magic.Magic(mime=True)
        except:
            self.magic = None
    
    def detect_by_extension(self, file_path: str) -> Dict[str, Optional[str]]:
        """Detect file type by extension."""
        path = Path(file_path)
        ext = path.suffix.lower()
        
        mime_type, encoding = mimetypes.guess_type(str(path))
        
        return {
            "extension": ext,
            "mime_type": mime_type,
            "encoding": encoding,
            "category": self._categorize_extension(ext)
        }
    
    def detect_by_content(self, file_path: str) -> Optional[str]:
        """Detect file type by content (requires python-magic)."""
        if not self.magic:
            return None
        
        try:
            return self.magic.from_file(file_path)
        except Exception:
            return None
    
    def _categorize_extension(self, ext: str) -> str:
        """Categorize file extension."""
        categories = {
            ".py": "code",
            ".js": "code",
            ".ts": "code",
            ".java": "code",
            ".cpp": "code",
            ".c": "code",
            ".html": "markup",
            ".xml": "markup",
            ".json": "data",
            ".csv": "data",
            ".xlsx": "data",
            ".pdf": "document",
            ".docx": "document",
            ".txt": "text",
            ".md": "text",
            ".jpg": "image",
            ".png": "image",
            ".gif": "image",
            ".mp4": "video",
            ".mp3": "audio"
        }
        return categories.get(ext, "unknown")
    
    def is_text_file(self, file_path: str) -> bool:
        """Check if file is likely a text file."""
        detection = self.detect_by_extension(file_path)
        mime_type = detection.get("mime_type", "")
        
        text_types = [
            "text/",
            "application/json",
            "application/xml",
            "application/javascript"
        ]
        
        return any(mime_type.startswith(t) for t in text_types) or \
               detection["category"] in ["code", "text", "markup", "data"]

# Usage
detector = FileTypeDetector()
info = detector.detect_by_extension("/path/to/file.py")
print(f"Type: {info['mime_type']}, Category: {info['category']}")
```

### Step 4: Secure Sandboxed Filesystem

```python
from pathlib import Path
from typing import List, Set
import os

class SandboxedFilesystem:
    """Secure filesystem operations with sandboxing."""
    
    def __init__(
        self,
        base_directory: str,
        allowed_extensions: Set[str] = None,
        max_file_size: int = 10 * 1024 * 1024,  # 10MB default
        read_only: bool = False
    ):
        """
        Args:
            base_directory: Base directory for all operations
            allowed_extensions: Set of allowed file extensions (None = all)
            max_file_size: Maximum file size in bytes
            read_only: If True, disable write operations
        """
        self.base_dir = Path(base_directory).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.allowed_extensions = allowed_extensions
        self.max_file_size = max_file_size
        self.read_only = read_only
    
    def _sanitize_path(self, file_path: str) -> Path:
        """Sanitize and resolve path within sandbox."""
        # Resolve relative to base directory
        if Path(file_path).is_absolute():
            # If absolute, check if it's within base_dir
            path = Path(file_path).resolve()
            if not path.is_relative_to(self.base_dir):
                raise PermissionError(f"Path outside sandbox: {file_path}")
        else:
            # Relative path - resolve within base_dir
            path = (self.base_dir / file_path).resolve()
        
        # Ensure still within base_dir (prevent .. attacks)
        if not path.is_relative_to(self.base_dir):
            raise PermissionError(f"Path escape attempt: {file_path}")
        
        return path
    
    def _validate_file(self, path: Path, for_write: bool = False) -> None:
        """Validate file before operation."""
        if for_write and self.read_only:
            raise PermissionError("Filesystem is read-only")
        
        if self.allowed_extensions:
            if path.suffix.lower() not in self.allowed_extensions:
                raise ValueError(f"Extension not allowed: {path.suffix}")
        
        if path.exists() and path.is_file():
            size = path.stat().st_size
            if size > self.max_file_size:
                raise ValueError(f"File too large: {size} bytes (max: {self.max_file_size})")
    
    def read_file(self, file_path: str) -> str:
        """Read file from sandbox."""
        path = self._sanitize_path(file_path)
        self._validate_file(path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        return path.read_text(encoding="utf-8", errors="ignore")
    
    def write_file(self, file_path: str, content: str) -> None:
        """Write file to sandbox."""
        path = self._sanitize_path(file_path)
        self._validate_file(path, for_write=True)
        
        # Create parent directories
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check content size
        content_size = len(content.encode("utf-8"))
        if content_size > self.max_file_size:
            raise ValueError(f"Content too large: {content_size} bytes")
        
        path.write_text(content, encoding="utf-8")
    
    def list_files(self, directory: str = ".") -> List[dict]:
        """List files in sandbox directory."""
        dir_path = self._sanitize_path(directory)
        
        if not dir_path.exists():
            raise FileNotFoundError(f"Directory not found: {dir_path}")
        
        if not dir_path.is_dir():
            raise ValueError(f"Not a directory: {dir_path}")
        
        results = []
        for item in dir_path.iterdir():
            if item.is_file():
                results.append({
                    "name": item.name,
                    "size": item.stat().st_size,
                    "modified": item.stat().st_mtime
                })
        
        return results
    
    def delete_file(self, file_path: str) -> None:
        """Delete file from sandbox."""
        if self.read_only:
            raise PermissionError("Filesystem is read-only")
        
        path = self._sanitize_path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        if not path.is_file():
            raise ValueError(f"Not a file: {path}")
        
        path.unlink()

# Usage
sandbox = SandboxedFilesystem(
    base_directory="/tmp/sandbox",
    allowed_extensions={".txt", ".md", ".json"},
    max_file_size=1024 * 1024,  # 1MB
    read_only=False
)

sandbox.write_file("test.txt", "Hello, World!")
content = sandbox.read_file("test.txt")
files = sandbox.list_files()
```

### Step 5: LangChain Tool Integration

```python
from langchain_core.tools import tool
from typing import Optional

class FilesystemTools:
    """LangChain tools for filesystem operations."""
    
    def __init__(self, sandbox: SandboxedFilesystem):
        self.sandbox = sandbox
    
    @tool
    def read_file_tool(file_path: str) -> str:
        """Read contents of a file.
        
        Args:
            file_path: Path to the file (relative to sandbox)
        """
        return self.sandbox.read_file(file_path)
    
    @tool
    def write_file_tool(file_path: str, content: str) -> str:
        """Write content to a file.
        
        Args:
            file_path: Path to the file (relative to sandbox)
            content: Content to write
        """
        self.sandbox.write_file(file_path, content)
        return f"Successfully wrote to {file_path}"
    
    @tool
    def list_files_tool(directory: str = ".") -> str:
        """List files in a directory.
        
        Args:
            directory: Directory path (relative to sandbox)
        """
        files = self.sandbox.list_files(directory)
        if not files:
            return "No files found"
        
        result = f"Files in {directory}:\n"
        for f in files:
            result += f"  - {f['name']} ({f['size']} bytes)\n"
        
        return result
    
    @tool
    def search_files_tool(pattern: str, directory: str = ".") -> str:
        """Search for files matching a pattern.
        
        Args:
            pattern: File pattern (e.g., "*.py")
            directory: Directory to search (relative to sandbox)
        """
        dir_ops = DirectoryOperations(
            allowed_directories=[str(self.sandbox.base_dir)]
        )
        matches = dir_ops.find_files(
            str(self.sandbox.base_dir / directory),
            pattern=pattern
        )
        
        if not matches:
            return f"No files matching '{pattern}' found"
        
        return "\n".join([Path(m).name for m in matches])
    
    def get_tools(self):
        """Get all filesystem tools."""
        return [
            self.read_file_tool,
            self.write_file_tool,
            self.list_files_tool,
            self.search_files_tool
        ]

# Usage with LangChain agent
sandbox = SandboxedFilesystem("/tmp/agent_workspace")
fs_tools = FilesystemTools(sandbox)
tools = fs_tools.get_tools()

# Bind to LLM
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
llm_with_tools = llm.bind_tools(tools)
```

### Step 6: File Processing Pipeline

```python
from typing import List, Callable, Dict
from pathlib import Path

class FileProcessor:
    """Process files through a pipeline."""
    
    def __init__(self, sandbox: SandboxedFilesystem):
        self.sandbox = sandbox
        self.processors: List[Callable] = []
    
    def add_processor(self, processor: Callable[[str], str]):
        """Add a processing step."""
        self.processors.append(processor)
    
    def process_file(self, file_path: str, output_path: Optional[str] = None) -> str:
        """Process file through pipeline."""
        content = self.sandbox.read_file(file_path)
        
        # Apply processors
        for processor in self.processors:
            content = processor(content)
        
        # Write output
        if output_path is None:
            path = Path(file_path)
            output_path = str(path.parent / f"{path.stem}_processed{path.suffix}")
        
        self.sandbox.write_file(output_path, content)
        return output_path

# Example processors
def remove_whitespace(content: str) -> str:
    """Remove extra whitespace."""
    lines = [line.strip() for line in content.split("\n")]
    return "\n".join(line for line in lines if line)

def add_line_numbers(content: str) -> str:
    """Add line numbers."""
    lines = content.split("\n")
    return "\n".join(f"{i+1:4d} | {line}" for i, line in enumerate(lines))

# Usage
sandbox = SandboxedFilesystem("/tmp/workspace")
processor = FileProcessor(sandbox)
processor.add_processor(remove_whitespace)
processor.add_processor(add_line_numbers)

output = processor.process_file("input.txt", "output.txt")
```

## File Operation Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| Read-only | Document analysis | Read config files |
| Sandboxed write | Agent workspaces | Create temporary files |
| Recursive search | Code analysis | Find all Python files |
| Content search | Text mining | Search for keywords |
| Batch processing | Data pipelines | Process multiple files |

## Best Practices

- Always validate and sanitize file paths
- Use sandboxing for untrusted operations
- Set maximum file size limits
- Restrict allowed file extensions
- Use pathlib for cross-platform compatibility
- Handle encoding errors gracefully
- Implement proper error handling
- Log file operations for auditing
- Use read-only mode when possible
- Validate file types before processing

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| No path validation | Always validate and sanitize paths |
| Allowing absolute paths | Resolve relative to base directory |
| No size limits | Set max_file_size limits |
| Ignoring encoding | Handle encoding errors |
| No sandboxing | Use SandboxedFilesystem |
| Synchronous I/O | Use async for large files |
| No error handling | Wrap operations in try/except |
| Hardcoded paths | Use configurable base directories |
| No permission checks | Validate read/write permissions |
| Ignoring file types | Check file types before processing |

## Related

- Knowledge: `knowledge/api-integration-patterns.json`
- Skill: `tool-usage`
- Skill: `mcp-integration`
- Skill: `web-browsing`

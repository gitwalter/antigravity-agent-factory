---
description: GitHub operations and repository management using the GitHub MCP Server
name: github-operations
type: skill
---
# GitHub Operations

Use the GitHub MCP Server to manage repositories, issues, pull requests, and file operations.

## When to Use
Use this skill when you need to automate GitHub-related tasks such as managing issues, reviewing pull requests, or performing remote file commits.

## Prerequisites
- GitHub MCP server installed and configured.
- Valid `GITHUB_TOKEN` with appropriate scopes available in the environment.

## Capabilities

- **Repository Management**: Search, fork, and configure repositories.
- **Issue Tracking**: Create, list, search, and comment on issues.
- **Pull Requests**: Create, review, merge, and update PRs.
- **File Operations**: Read, write (commit), and delete files remotely.
- **Branch Management**: Create, list, and delete branches.

## Process

1.  **Authentication**: Ensure `GITHUB_TOKEN` is available in the environment.
2.  **Context Loading**: Use `search_repositories` or `list_repositories` to find the target.
3.  **Operation**: Execute the specific tool (e.g., `create_issue`, `get_file_contents`).
4.  **Verification**: Check operations (e.g., verify PR creation).

## Example Usage

### Creating an Issue
```python
response = await client.chat.completions.create(
    messages=[{"role": "user", "content": "Create a bug report for the login crash"}],
    tools=[{
        "type": "mcp",
        "name": "github",
        "command": "docker", # Managed by MCP config
        "args": ["run", ...] 
    }]
)
```

### Reading a File
```python
# Get content of README.md
content = await github.get_file_contents(
    owner="owner-name",
    repo="repo-name",
    path="README.md"
)
```

## Best Practices

- **Security**: Never hardcode tokens; use environment variables.
- **Scope**: Verify the token has appropriate permissions (repo, read:org, etc.).
- **Rate Limiting**: Be mindful of API limits when performing bulk operations.

## Related
- MCP Server: `github-mcp-server`

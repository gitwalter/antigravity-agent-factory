# Configuration Guide

This document describes how to configure the Antigravity Agent Factory for your development environment.

## Tool Paths Configuration

The factory uses a hierarchical system to resolve paths for external tools like `git` and `gh`.

### Configuration Files

| File | Purpose |
|------|---------|
| `.agent/cache/session-paths.json` | **Session overrides** - Machine-specific paths (not committed) |
| `.agent/config/tools.json` | **Tool definitions** - Defaults and fallback paths |

### Resolution Order (Single Point of Truth)

To ensure consistency and reliability, Antigravity Agent/Skill Factory uses a **Single Point of Truth (SPoT)** architecture. **Configuration is the definitive source for all environment-specific values.**

#### Core Philosophy

> **"If it's an absolute path, a URL, or a machine-specific setting, it belongs in configuration."**

Every parameter that varies between environments MUST be externalized to the configuration hierarchy. Hardcoded values are only permitted as **fallbacks/defaults** within the configuration files themselves (`tools.json`), never in the instructions or logic of agents and skills.

1.  **Session Cache** (`.agent/cache/session-paths.json`): Checked first. Machine-specific overrides.
2.  **Project Configuration** (`.agent/config/tools.json`): Shared project defaults.
3.  **Environment Variables**: `PYTHON_PATH`, `GIT_PATH`, etc.
4.  **System Defaults**: Fallback only (Discouraged for automated procedures).

### Configuration Variables

Agents use the following placeholders in instructions. These are resolved at runtime from the configuration hierarchy.

| Variable | Description | Default (Fallback) |
|----------|-------------|-------------------|
| `{PYTHON_PATH}` | Python interpreter | `C:\App\Anaconda\python.exe` |
| `{GIT_PATH}` | Git executable | `C:\Program Files\Git\cmd\git.exe` |
| `{GH_CLI_PATH}` | GitHub CLI (`gh`) | `C:\App\gh\bin\gh.exe` |
| `{PIP_PATH}` | Python package manager | `C:\App\Anaconda\Scripts\pip.exe` |
| `{CONDA_PATH}` | Conda environment manager | `C:\App\Anaconda\Scripts\conda.exe` |
| `{PYTEST_PATH}` | Testing framework | `C:\App\Anaconda\Scripts\pytest.exe` |
| `{ATLASSIAN_MCP_URL}` | Atlassian MCP SSE URL | `https://mcp.atlassian.com/v1/sse` |
| `{JIRA_BASE_URL}` | Jira Cloud base URL | `https://company.atlassian.net` |
| `{LINEAR_BASE_URL}` | Linear App base URL | `https://linear.app` |

## Dynamic Shell Execution Protocol (REQUIRED)

All automated procedures MUST follow these standards for reliability across different Windows environments:

- **No Hardcoding**: NEVER hardcode absolute paths or URLs in instructions, scripts, or documentation.
- **Variable Placeholders**: Use `{VARIABLE_NAME}` notation in instructions. Agents will resolve these at runtime.
- **Configurable Endpoints**: Every external API or GitHub URL must be configurable in `tools.json` or environment variables.
- **Relative Repo Paths**: Always use relative paths for files inside the repository (e.g., `scripts/validation/sync_artifacts.py`).
- **PowerShell Syntax**: Use the semi-colon (`;`) for chaining multiple commands. Do not use `&&`.

### Example Command

`{PYTHON_PATH} scripts/validation/sync_artifacts.py --sync ; {PYTHON_PATH} -m pytest tests/`


### Customizing Your Environment

To use specific paths for tools on your machine without affecting other users, create or edit `.agent/cache/session-paths.json`:

```json
{
  "tools": {
    "gh": {
      "path": "C:\\Custom\\Path\\gh.exe"
    }
  }
}
```

This file is ignored by git, so your local configuration remains private.

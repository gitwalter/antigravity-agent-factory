# Configuration Guide

This document describes how to configure the Antigravity Agent Factory for your development environment.

## Tool Paths Configuration

The factory uses a hierarchical system to resolve paths for external tools like `git` and `gh`.

### Configuration Files

| File | Purpose |
|------|---------|
| `.agent/cache/session-paths.json` | **Session overrides** - Machine-specific paths (not committed) |
| `.agent/config/tools.json` | **Tool definitions** - Defaults and fallback paths |

### Resolution Order

1.  **Session Cache** (`.agent/cache/session-paths.json`): Checked first. Use this for local overrides.
2.  **Environment Variables**: `GH_CLI_PATH`, `GIT_PATH`, etc.
3.  **System PATH**: Standard system path lookup.
4.  **Defaults** (`.agent/config/tools.json`): Verified fallback paths.

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

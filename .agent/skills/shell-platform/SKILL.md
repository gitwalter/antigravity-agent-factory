---
description: Platform-specific shell command considerations for Windows PowerShell and Unix shells
---

# Shell Platform

Platform-specific shell command considerations for Windows PowerShell and Unix shells

## 
# Shell Platform Skill

Handle platform-specific shell syntax differences when executing commands.

## 
# Shell Platform Skill

Handle platform-specific shell syntax differences when executing commands.

## CRITICAL: PowerShell Command Chaining Warning
> **NEVER USE `&&` IN WINDOWS POWERSHELL 5.x!**
>
> The following pattern DOES NOT WORK and will ALWAYS fail:
> ```bash
> cd "path" && git pull
> ```
> Error: `Das Token "&&" ist in dieser Version kein gültiges Anweisungstrennzeichen`
>
> **USE THIS INSTEAD:**
> ```powershell
> cd "path"; & "C:\Program Files\Git\cmd\git.exe" pull
> ```
>
> The `&&` operator only works in PowerShell 7+ (pwsh.exe), NOT in Windows PowerShell 5.x (powershell.exe).

This is a **recurring error** - check `user_info.Shell` to detect PowerShell version.

```bash
> cd "path" && git pull
>
```

```powershell
> cd "path"; & "C:\Program Files\Git\cmd\git.exe" pull
>
```

## CRITICAL: PowerShell Heredoc Warning
> **NEVER USE HEREDOC SYNTAX IN POWERSHELL!**
>
> The following pattern DOES NOT WORK and will ALWAYS fail:
> ```bash
> git commit -m "$(cat <<'EOF'
> message
> EOF
> )"
> ```
>
> **USE THIS INSTEAD:**
> ```powershell
> git commit -m "Single line message"
> ```
>
> Or for multi-line:
> ```powershell
> git commit -m "Title" -m "Body paragraph"
> ```

This is a **recurring error** - always use simple string syntax on Windows.

```bash
> git commit -m "$(cat <<'EOF'
> message
> EOF
> )"
>
```

```powershell
> git commit -m "Single line message"
>
```

```powershell
> git commit -m "Title" -m "Body paragraph"
>
```

## Scope
**This skill is LOCAL to this machine only.** Do not apply automatically - always ask the user before applying platform-specific command adjustments.

## Process
### Step 1: Detect Platform
Check `user_info.OS` to determine if running on Windows (`win32`), macOS (`darwin`), or Linux (`linux`).

### Step 2: Check Shell Type
If on Windows, check `user_info.Shell` to determine if using PowerShell 5.x (`powershell.exe`) or PowerShell 7+ (`pwsh.exe`).

### Step 3: Apply Platform-Specific Syntax
- **PowerShell 5.x**: Replace `&&` with `;`, avoid heredoc syntax, use multiple `-m` flags for git commits
- **PowerShell 7+**: `&&` works, but prefer `;` for compatibility
- **Unix shells**: Use standard bash syntax

### Step 4: Use Session Cache
Read `.cursor/cache/session-paths.json` first to get verified tool paths before executing commands.

### Step 5: Execute Command
Run the platform-adapted command with appropriate syntax and tool paths.

## Activation
**First-time activation only:** If this skill has not been confirmed yet, ask the user:

> "I notice you're on Windows/PowerShell. Should I enable PowerShell-compatible syntax for shell commands? This setting will persist in your Cursor configuration."

Once the user confirms:
1. The skill remains **permanently active** in Cursor settings
2. No need to ask again in future sessions
3. Apply PowerShell-compatible syntax automatically from then on

**Status:** ✅ ACTIVE (confirmed by user)

## Platform Detection
Check the user's OS from `user_info`:
- `win32` → Windows (PowerShell)
- `darwin` → macOS (zsh/bash)
- `linux` → Linux (bash)

## Critical: PowerShell Limitations
### Heredoc Syntax NOT Supported

PowerShell does NOT support bash-style heredoc syntax:

```bash
# THIS DOES NOT WORK IN POWERSHELL:
git commit -m "$(cat <<'EOF'
Multi-line
commit message
EOF
)"
```

### PowerShell Alternatives

**Option 1: Multiple -m flags (recommended for git commits)**
```powershell
git commit -m "Title line" -m "Body paragraph 1" -m "Body paragraph 2"
```

**Option 2: Backtick for line continuation**
```powershell
git commit -m "Title line`n`nBody with newlines"
```

**Option 3: Here-string (PowerShell native)**
```powershell
$message = @"
Title line

Body paragraph
"@
git commit -m $message
```

### Command Chaining

PowerShell uses different operators:

| Bash | PowerShell | Purpose |
|------|------------|---------|
| `&&` | `;` or `-and` | Run if previous succeeds |
| `||` | `-or` | Run if previous fails |
| `\|` | `\|` | Pipe (same) |

**Note:** `&&` and `||` work in PowerShell 7+ but NOT in Windows PowerShell 5.x.

```bash
# THIS DOES NOT WORK IN POWERSHELL:
git commit -m "$(cat <<'EOF'
Multi-line
commit message
EOF
)"
```

```powershell
git commit -m "Title line" -m "Body paragraph 1" -m "Body paragraph 2"
```

```powershell
git commit -m "Title line`n`nBody with newlines"
```

```powershell
$message = @"
Title line

Body paragraph
"@
git commit -m $message
```

## Git Commit Message Best Practices
For cross-platform compatibility, use multiple `-m` flags:

```powershell
git commit -m "feat: Short title" -m "Longer description of the change." -m "Additional details if needed."
```

This works on all platforms and produces proper multi-paragraph commit messages.

```powershell
git commit -m "feat: Short title" -m "Longer description of the change." -m "Additional details if needed."
```

## Tool Paths Configuration
Tool paths are **configurable** via `.cursor/config/tools.json` with environment variable fallbacks.

See [Configuration Guide](../../docs/CONFIGURATION.md) for full details.

### ⚡ Session Path Cache (CRITICAL)

**ALWAYS read the session cache first** before running commands:

```
.cursor/cache/session-paths.json
```

This file contains **verified working paths** for the current machine. Reading this file ONCE at session start prevents repeated path resolution failures.

**Resolution Priority:**
1. **Session Cache** (`.cursor/cache/session-paths.json`) - FASTEST, already verified
2. **Environment Variable** (e.g., `$env:PYTHON_PATH`)
3. **Config File** (`.cursor/config/tools.json`)
4. **Auto-detect** (via PATH)
5. **Fallbacks** (hardcoded paths)

**Agent Behavior:**
- At session start: Read `session-paths.json` to get working paths
- When a path fails: Try next in resolution order, then UPDATE the cache
- Cache is machine-specific - do not commit to git

### Session Cache Format

```json
{
  "paths": {
    "python": "{PYTHON_PATH}",
    "pip": "{PIP_PATH}",
    "conda": "{CONDA_PATH}",
    "pytest": "{PYTEST_PATH}",
    "git": null
  },
  "workspace": {
    "root": "{WORKSPACE_ROOT}",
    "shell": "powershell"
  }
}
```

**Usage in Commands:**
```powershell
# Read from cache - path is already verified
{PYTHON_PATH} scripts/validation/validate_yaml_frontmatter.py
```

### Default Tool Paths (Windows)

| Tool | Default Path | Env Variable | Notes |
|------|--------------|--------------|-------|
| **Python** | `{PYTHON_PATH}` | `PYTHON_PATH` | Anaconda installation |
| **Pip** | `{PIP_PATH}` | `PIP_PATH` | Anaconda pip |
| **Conda** | `{CONDA_PATH}` | `CONDA_PATH` | Anaconda conda |
| **GitHub CLI** | `{GH_CLI_PATH}` | `GH_CLI_PATH` | **CONFIGURABLE** |
| **Pytest** | `{PYTEST_PATH}` | `PYTEST_PATH` | Anaconda pytest |

### GitHub CLI Configuration

The GitHub CLI (`gh`) is installed at `{GH_CLI_DIR}` on this machine.

**Usage:**
```powershell
# Full path (always works)
{GH_CLI_PATH} pr list

# Or via environment variable
& $env:GH_CLI_PATH pr list
```

**Common Commands:**
```powershell
# List recent workflow runs
{GH_CLI_PATH} run list --limit 5

# View specific run
{GH_CLI_PATH} run view <run-id> --json jobs

# Create pull request
{GH_CLI_PATH} pr create --title "Title" --body "Description"

# List issues
{GH_CLI_PATH} issue list

# Create repository
{GH_CLI_PATH} repo create my-repo --public
```

### Updating the Session Cache

When a path is verified to work, update the cache:

```powershell
# After verifying {PYTHON_PATH} works, update cache
# The agent should read_file, modify, and write back
```

### GitHub CLI Examples

```powershell
# Using environment variable (recommended)
& $env:GH_CLI_PATH run list --limit 5

# Or with default path
{GH_CLI_PATH} run list --limit 5

# View specific run details
{GH_CLI_PATH} run view <run-id> --json jobs

# Check job status
{GH_CLI_PATH} run view <run-id> --json jobs --jq ".jobs[] | {name, conclusion}"

# Create a pull request
{GH_CLI_PATH} pr create --title "Title" --body "Description"

# List open issues
{GH_CLI_PATH} issue list
```

### Cross-Platform Paths

For Linux/macOS, paths typically use forward slashes and may be simpler:

| Tool | Linux/macOS Path |
|------|------------------|
| **Python** | `python3` or `/usr/bin/python3` |
| **Pip** | `pip3` or `/usr/bin/pip3` |
| **GitHub CLI** | `gh` or `/usr/local/bin/gh` |

```
.cursor/cache/session-paths.json
```

```json
{
  "paths": {
    "python": "{PYTHON_PATH}",
    "pip": "{PIP_PATH}",
    "conda": "{CONDA_PATH}",
    "pytest": "{PYTEST_PATH}",
    "git": null
  },
  "workspace": {
    "root": "{WORKSPACE_ROOT}",
    "shell": "powershell"
  }
}
```

```powershell
# Read from cache - path is already verified
{PYTHON_PATH} scripts/validation/validate_yaml_frontmatter.py
```

```powershell
# Full path (always works)
{GH_CLI_PATH} pr list

# Or via environment variable
& $env:GH_CLI_PATH pr list
```

```powershell
# List recent workflow runs
{GH_CLI_PATH} run list --limit 5

# View specific run
{GH_CLI_PATH} run view <run-id> --json jobs

# Create pull request
{GH_CLI_PATH} pr create --title "Title" --body "Description"

# List issues
{GH_CLI_PATH} issue list

# Create repository
{GH_CLI_PATH} repo create my-repo --public
```

```powershell
# After verifying {PYTHON_PATH} works, update cache
# The agent should read_file, modify, and write back
```

```powershell
# Using environment variable (recommended)
& $env:GH_CLI_PATH run list --limit 5

# Or with default path
{GH_CLI_PATH} run list --limit 5

# View specific run details
{GH_CLI_PATH} run view <run-id> --json jobs

# Check job status
{GH_CLI_PATH} run view <run-id> --json jobs --jq ".jobs[] | {name, conclusion}"

# Create a pull request
{GH_CLI_PATH} pr create --title "Title" --body "Description"

# List open issues
{GH_CLI_PATH} issue list
```

## Important Rules
1. **NEVER use `&&`** in Windows PowerShell 5.x - use `;` instead (e.g., `cd path; git pull`)
2. **NEVER use heredoc** (`<<EOF`) in PowerShell - it ALWAYS fails
3. **Use simple strings** for git commit messages: `git commit -m "message"`
4. **Use multiple -m flags** for multi-line commits: `-m "Title" -m "Body"`
5. **Use full tool paths** on Windows to avoid PATH issues
6. **Prefer simple commands** that work across platforms
7. **Check user_info.Shell** - if `powershell.exe`, apply Windows PowerShell 5.x rules

### Git Commit - Quick Reference

```powershell
# CORRECT - Simple message
git commit -m "feat: Add new feature"

# CORRECT - Multi-line with multiple -m
git commit -m "feat: Add new feature" -m "Detailed description here"

# WRONG - NEVER DO THIS IN POWERSHELL
git commit -m "$(cat <<'EOF'
message
EOF
)"
```

```powershell
# CORRECT - Simple message
git commit -m "feat: Add new feature"

# CORRECT - Multi-line with multiple -m
git commit -m "feat: Add new feature" -m "Detailed description here"

# WRONG - NEVER DO THIS IN POWERSHELL
git commit -m "$(cat <<'EOF'
message
EOF
)"
```

## Prerequisites
> [!IMPORTANT]
> Requirements:

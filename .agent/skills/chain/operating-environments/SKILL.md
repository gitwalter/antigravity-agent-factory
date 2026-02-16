---
description: Config-driven operating environment skill for shell commands, tool path
  resolution, and platform-specific syntax across all platforms
name: operating-environments
type: skill
---
# Operating Environment

Config-driven operating environment skill for shell commands, tool path resolution, and platform-specific syntax across all platforms

**Scope:** `always` -- auto-loaded for every agent session. Do not skip.

This skill defines how to discover tool paths, detect the platform, and apply
shell syntax rules. All paths come from configuration files; nothing is
hardcoded in this skill.

## Configuration Files (Source of Truth)

| File | Purpose | Committed |
|------|---------|-----------|
| `{directories.cache}/session-paths.json` | Verified tool paths for this machine | No (gitignored) |
| `{directories.config}/tools.json` | Resolution order, fallbacks, env vars per tool | Yes |
| `{directories.config}/settings.json` | Platform rules, directories, credentials refs | Yes |

**Rule:** Paths live ONLY in these config files. Skills and `.cursorrules` must never contain hardcoded tool paths.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Load Verified Paths

Read `{directories.cache}/session-paths.json`:

```json
{
  "paths": { "python": "...", "pip": "...", "conda": "...", "git": "...", "pytest": "..." },
  "workspace": { "root": "...", "shell": "powershell" },
  "verified": "2026-02-10"
}
```

If the file exists and `verified` is recent, use these paths directly. This is
the fastest resolution -- one read, zero lookups.

If the file is missing, empty, or stale, proceed to Step 4 (Tool Path Resolution).

### Step 2: Detect Platform

Read `user_info.Shell` from the IDE context (provided automatically in every
message). Cross-reference with the `platforms` section in `{directories.config}/settings.json`:

```json
{
  "platforms": {
    "windows": { "shell": "powershell", "path_separator": "\\", "env_syntax": "%VAR%" },
    "linux":   { "shell": "bash",       "path_separator": "/",  "env_syntax": "$VAR" },
    "darwin":  { "shell": "zsh",        "path_separator": "/",  "env_syntax": "$VAR" }
  }
}
```

Use the detected shell to select the correct syntax rules below.

### Step 3: Apply Shell Syntax Rules

#### PowerShell 5.x (`powershell`)

1. **No `&&` chaining** -- use `;` to chain commands sequentially.

```powershell
# WRONG -- parse error in PowerShell 5.x
cd "path" && git pull

# CORRECT
cd "path"; git pull
```

2. **No heredoc (`<<EOF`)** -- use simple strings or multiple `-m` flags.

```powershell
# WRONG
git commit -m "$(cat <<'EOF'
message
EOF
)"

# CORRECT
git commit -m "feat: Add new feature"

# CORRECT -- multi-line
git commit -m "feat: Add new feature" -m "Detailed description here"

# CORRECT -- PowerShell here-string
$message = @"
Title line

Body paragraph
"@
git commit -m $message
```

3. **Always use full tool paths** -- bare `python` or `git` may not resolve.
   Use the verified path from session cache.

4. **Set `working_directory`** on Shell tool calls instead of `cd`.

5. **Verify paths** with `Glob` or `LS` before referencing in commands.

#### Bash (`bash`) / Zsh (`zsh`)

1. `&&` chaining works normally.
2. Heredoc (`<<EOF`) works normally.
3. Bare tool names usually resolve via PATH, but prefer verified paths when available.
4. Set `working_directory` on Shell tool calls instead of `cd`.

#### Command Chaining Reference

| Bash / Zsh | PowerShell 5.x | Purpose |
|------------|----------------|---------|
| `&&` | `;` | Sequential execution |
| `\|\|` | `; if ($LASTEXITCODE -ne 0) { ... }` | Run on failure |
| `\|` | `\|` | Pipe (same on all platforms) |

### Step 4: Tool Path Resolution

When a path is not in session cache or fails, resolve using the order defined
in `{directories.config}/tools.json` under `resolution_order`:

1. **Session Cache** -- `{directories.cache}/session-paths.json` (already tried in Step 1)
2. **Environment Variable** -- Check the `env_var` field for the tool (e.g., `$env:PYTHON_PATH` on Windows, `$PYTHON_PATH` on Unix)
3. **Local Config** -- Read `tools` section of `{directories.config}/tools.json` for `fallbacks` array; try each path in order
4. **Auto-detect** -- Run `where.exe <tool>` (Windows) or `which <tool>` (Unix)
5. **Platform Defaults** -- Read `defaults.<platform>` in `{directories.config}/tools.json`

For each tool, `tools.json` defines:

```json
{
  "python": {
    "env_var": "PYTHON_PATH",
    "conda_env": "cursor-factory",
    "auto_detect": ["python", "python3", "python.exe"],
    "fallbacks": ["<paths from tools.json>"],
    "min_version": "3.10"
  }
}
```

**Do not repeat these paths here.** Read them from `tools.json` at resolution time.

### Step 5: Verify and Cache

After resolving a tool path:

1. **Verify** -- Run a quick check (e.g., `<path> --version`) to confirm the tool works.
2. **Update cache** -- Write the verified path to `{directories.cache}/session-paths.json` so future calls skip resolution.
3. **On failure** -- Move to the next resolution level. If all levels fail, report the error with the list of attempted paths.

## Conda Environment Management

When Python operations require a specific conda environment:

1. Read the `conda_env` field from `{directories.config}/tools.json` for the `python` tool.
2. Activate using the conda path from session cache: `<conda_path> activate <env_name>`.
3. On Windows PowerShell, use: `& <conda_path> activate <env_name>` or the `activate.bat` script.
4. For package installs, prefer `<conda_path> install -n <env_name> <package>` over bare `conda install`.

## Important Rules

1. **NEVER hardcode tool paths** in skills, agents, or `.cursorrules` -- always read from config.
2. **ALWAYS read session cache first** -- it is the fastest path to verified tools.
3. **ALWAYS use full tool paths** when executing commands, especially on Windows.
4. **ALWAYS set `working_directory`** on Shell tool calls instead of using `cd`.
5. **ALWAYS verify file paths** with `Glob` or `LS` before referencing them in commands.
6. **Check `user_info.Shell`** to determine which syntax rules to apply.
7. **On path failure**, fall through resolution order -- do not stop at the first failure.
8. **Update session cache** whenever a new path is verified, so subsequent calls are fast.

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

## Best Practices
- Always follow the established guidelines.
- Document any deviations or exceptions.
- Regularly review and update the skill documentation.

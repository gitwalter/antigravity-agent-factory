---
description: Interactive configuration and onboarding skill for Cursor Agent Factory
  settings
name: configuring-systems
type: skill
---
# System Configuration

Interactive configuration and onboarding skill for Cursor Agent Factory settings

# System Configuration Skill

## Overview

This skill provides interactive configuration and onboarding for the Cursor Agent Factory. It guides users through setting up all system settings including tool paths, credentials, knowledge evolution preferences, and platform-specific configurations.

## Purpose

Provide a single, unified configuration experience that:
- Detects and configures tool paths (Python, Git, etc.)
- Sets up API credentials securely (GitHub, NPM, PyPI)
- Configures knowledge evolution preferences
- Validates all settings before saving
- Migrates from legacy configuration formats

## Axiom Alignment

- **A1 (Verifiability)**: All configurations are validated against schema
- **A3 (Transparency)**: Clear explanation of what each setting does
- **A4 (Adaptability)**: Flexible configuration for different environments

## Trigger

This skill is activated when:
- User says "configure system", "setup factory", "configure settings"
- First run of the factory (no settings.json exists)
- User requests "update credentials" or "change settings"
- Migration from legacy tools.json is needed

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Environment Detection

Automatically detect the current environment:

```yaml
detection_tasks:
  platform:
    action: Detect operating system (Windows, Linux, macOS)
    output: Platform identifier and shell type

  python:
    action: Find Python installation
    checks:
      - PYTHON_PATH environment variable
      - cursor-factory conda environment
      - System Python (python3, python.exe)
    output: Python path and version

  git:
    action: Find Git installation
    checks:
      - GIT_PATH environment variable
      - git in PATH
      - Common installation paths
    output: Git path and version

  other_tools:
    action: Detect additional tools
    tools: [conda, pip, pytest, gh]
    output: Tool availability status
```

### Step 2: Present Current Configuration

Show the user what has been detected:

```markdown

## Detected Configuration

| Setting | Value | Source |
|---------|-------|--------|
| Platform | {platform} | Auto-detected |
| Python | {python_path} | {source} |
| Git | {git_path} | {source} |
| ...

## Missing or Unverified

- [ ] GitHub Token (required for knowledge updates)
- [ ] NPM Token (optional, for JS/TS updates)
```

### Step 3: Interactive Configuration

Guide user through configuring each section:

#### 3.1 Tool Paths

```yaml
tool_configuration:
  python:
    question: "Python path detected: {path}. Is this correct?"
    options:
      - Use detected path
      - Specify different path
      - Use conda environment
    validation: Check Python version >= 3.10

  git:
    question: "Git path detected: {path}. Is this correct?"
    options:
      - Use detected path
      - Specify different path
    validation: Check git --version works
```

#### 3.2 Credentials

```yaml
credential_configuration:
  github_token:
    question: "Enter GitHub Personal Access Token for knowledge updates"
    hint: "Create at https://github.com/settings/tokens"
    required_scopes: [public_repo, read:org]
    storage: Environment variable reference (${GITHUB_TOKEN})
    validation: Test API access

  npm_token:
    question: "Enter NPM token (optional, for JS/TS package updates)"
    hint: "Create at https://www.npmjs.com/settings/tokens"
    optional: true
    storage: Environment variable reference (${NPM_TOKEN})
```

#### 3.3 Knowledge Evolution Settings

```yaml
knowledge_evolution_configuration:
  mode:
    question: "How should knowledge updates be handled?"
    options:
      - name: Stability First
        value: stability_first
        description: Lock versions, explicit updates only
      - name: Awareness Hybrid (Recommended)
        value: awareness_hybrid
        description: Notify of updates, user approves
      - name: Freshness First
        value: freshness_first
        description: Auto-update with rollback option
      - name: Subscription
        value: subscription
        description: Subscribe to specific stacks/topics

  sources:
    question: "Which knowledge sources should be enabled?"
    multi_select: true
    options:
      - GitHub Trending & Releases
      - Official Framework Documentation
      - Package Registries (PyPI, NPM)
      - Community Curated Sources
      - User Feedback from Projects

  subscriptions:
    when: mode == subscription
    question: "Which topics should you subscribe to?"
    hint: "Use glob patterns like python-*, ai-*"
    examples: ["python-*", "fastapi-*", "ai-*", "react-*"]
```

### Step 4: Validation

Validate all settings before saving:

```yaml
validation_steps:
  schema_validation:
    action: Validate against settings-schema.json
    on_error: Show specific validation errors

  tool_validation:
    action: Test each tool path
    tests:
      - python --version
      - git --version
    on_error: Warn but allow save

  credential_validation:
    action: Test API credentials
    tests:
      - GitHub: GET /rate_limit
      - NPM: npm whoami (if token provided)
    on_error: Warn but allow save

  knowledge_validation:
    action: Verify knowledge evolution settings
    checks:
      - Mode is valid
      - Sources have at least one enabled
      - Subscriptions are valid patterns
```

### Step 5: Save Configuration

Save validated configuration:

```yaml
save_actions:
  backup:
    action: Backup existing settings.json if exists
    path: settings.json.bak.{timestamp}

  save:
    action: Write new settings.json
    path: {directories.config}/settings.json

  migrate_legacy:
    when: tools.json exists
    action: Rename to tools.json.migrated

  report:
    action: Show configuration summary
    include:
      - What was configured
      - What credentials are set
      - Knowledge evolution mode
      - Next steps
```

## Configuration File Structure

The skill creates/updates `{directories.config}/settings.json`:

```json
{
  "$schema": "./settings-schema.json",
  "version": "1.0.0",
  "system": {
    "factory_version": "2.0.0",
    "platform": "windows"
  },
  "tools": {
    "python": {
      "path": "C:\\App\\Anaconda\\envs\\cursor-factory\\python.exe",
      "env_var": "PYTHON_PATH",
      "min_version": "3.10",
      "description": "Python 3.10+ interpreter"
    },
    "git": {
      "path": "C:\\Program Files\\Git\\bin\\git.exe",
      "env_var": "GIT_PATH",
      "description": "Git version control"
    }
  },
  "credentials": {
    "github_token": "${GITHUB_TOKEN}",
    "npm_token": "${NPM_TOKEN}"
  },
  "knowledge_evolution": {
    "mode": "awareness_hybrid",
    "check_on_startup": true,
    "auto_update": false,
    "notify_updates": true,
    "update_channel": "stable",
    "sources": {
      "github_trending": true,
      "official_docs": true,
      "package_registries": true,
      "community_curated": true,
      "user_feedback": true
    }
  },
  "llm": {
    "primary_model": "gemini-2.5-flash",
    "preview_model": "gemini-3-flash-preview",
    "fallback_model": "gemini-2.5-flash-lite",
    "default_temperature": 0.0
  }
}
```

## Environment Variable Setup

Provide instructions for setting environment variables:

### Windows (PowerShell)

```powershell
# Set GitHub token
[Environment]::SetEnvironmentVariable("GITHUB_TOKEN", "ghp_xxx...", "User")

# Set NPM token (optional)
[Environment]::SetEnvironmentVariable("NPM_TOKEN", "npm_xxx...", "User")

# Verify
$env:GITHUB_TOKEN
```

### Linux/macOS (Bash/Zsh)

```bash
# Add to ~/.bashrc or ~/.zshrc
export GITHUB_TOKEN="ghp_xxx..."
export NPM_TOKEN="npm_xxx..."

# Apply changes
source ~/.bashrc
```

## Outputs

1. **settings.json** - Unified configuration file
2. **Configuration Summary** - Report of what was configured
3. **Environment Instructions** - How to set required env vars
4. **Validation Report** - Results of all validation checks

## Important Rules

1. **Never store raw credentials** - Always use environment variable references
2. **Always validate before saving** - Ensure configuration is valid
3. **Create backups** - Backup existing config before overwriting
4. **Be transparent** - Explain what each setting does
5. **Provide defaults** - Sensible defaults for all optional settings

## Error Handling

| Error | Resolution |
|-------|------------|
| Python not found | Provide installation instructions |
| Git not found | Provide installation instructions |
| Invalid token | Show how to create valid token |
| Schema validation failed | Show specific errors, offer correction |
| Permission denied | Request elevated permissions |

## Success Criteria

Configuration is complete when:
- [ ] All required tools are configured and validated
- [ ] At least GitHub token is configured (for knowledge updates)
- [ ] Knowledge evolution mode is selected
- [ ] settings.json is created and valid
- [ ] User understands next steps

## Related Skills

- `update-knowledge` - Uses configuration to fetch updates
- `grounding-verification` - May need tool paths
- `requirements-gathering` - May trigger configuration if not set

---

*This skill ensures the Cursor Agent Factory is properly configured for optimal operation.*

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

## Best Practices
- Always follow the established guidelines.
- Document any deviations or exceptions.
- Regularly review and update the skill documentation.

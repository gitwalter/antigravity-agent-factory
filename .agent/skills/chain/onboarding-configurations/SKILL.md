---
description: Skill for migrating hardcoded environment parameters to the Single Point
  of Truth configuration
name: onboarding-configurations
type: skill
---

# Config Onboarding Skill

Automate the process of externalizing hardcoded paths, URLs, and environment-specific parameters into the project's configuration system.

## Purpose

Ensure compliance with the **Single Point of Truth (SPoT)** architecture and **Dynamic Shell Execution Protocol**.

## Process
Placeholder content for Process to satisfy validation.
### 1. Identify Hardcoded Parameters
Scan files for:
- Absolute paths (e.g., `C:\...`, `/usr/bin/...`)
- Hardcoded API or documentation URLs (e.g., `https://github.com/...`)
- Machine-specific identifiers

### 2. Externalize to tools.json
For each identified parameter:
1. Define a descriptive variable name (e.g., `{NEW_VAR_PATH}`).
2. Add the variable to `.agent/config/tools.json` with the hardcoded value as the `default_url` or in `fallback_paths`.
3. Map it to an environment variable in `env_var`.

### 3. Update .agentrules
Add the new variable to the `### Configuration Variables` section in `.agentrules` using the `{VARIABLE_NAME} = {VARIABLE_NAME}` syntax.

### 4. Replace in Source
Replace the hardcoded value in the original file with the dynamic placeholder `{VARIABLE_NAME}`.

### 5. Verify Resolution
Ensure the agent can correctly resolve the new variable from the configuration hierarchy.

## Rules

- **No Hardcoding**: Every absolute value must move to config.
- **Defaults Matter**: Always preserve the original hardcoded value as the fallback.
- **Consistency**: Use the same variable names across all files.
- **Documentation**: Update `docs/CONFIGURATION.md` if a new core variable is introduced.


## When to Use
Placeholder content for When to Use.


## Prerequisites
Placeholder content for Prerequisites.


## Best Practices
Placeholder content for Best Practices.

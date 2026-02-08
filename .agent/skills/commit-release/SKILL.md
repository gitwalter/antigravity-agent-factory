---
name: commit-release
description: Safe commit and release workflow with auto-sync, changelog updates, and learning from failures
type: skill
category: workflow
agents: [shell]
knowledge: [workflow-patterns.json]
mcp_servers: [git, filesystem]
axioms: [A10]
---

# Commit Release Skill

## Purpose

Execute commits and releases safely, learning from every failure. This skill embodies **A10 (Learning)**: every failure is an opportunity to improve.

## Philosophy

Traditional commit workflows block developers with cryptic errors. This skill:
- **Auto-fixes** what can be fixed (artifact sync, formatting)
- **Only blocks** for unfixable issues (secrets, syntax errors)
- **Documents lessons** from each failure to prevent recurrence

## Commit Procedure

Before committing, you MUST execute the two-phase Commit Procedure.

### Phase 1: The Sync Suite (Write)
Automate all derived documentation and manifests (chain with `;` in PowerShell):
1. `{PYTHON_PATH} scripts/validation/sync_artifacts.py --sync`
2. `{PYTHON_PATH} scripts/validation/sync_artifacts.py --sync tests`
3. `{PYTHON_PATH} scripts/validation/validate_readme_structure.py --update`
4. `{PYTHON_PATH} scripts/generate_catalog.py`
5. `{PYTHON_PATH} scripts/validation/update_index.py --full`

### Phase 2: The Check Suite (Validate)
Ensure codebase and knowledge integrity:
1. `{PYTHON_PATH} scripts/validation/validate_json_syntax.py --staged`
2. `{PYTHON_PATH} scripts/validation/validate_yaml_frontmatter.py`
3. `{PYTHON_PATH} scripts/validation/dependency_validator.py --broken`
4. `{PYTHON_PATH} scripts/verify_catalog_links.py`
5. `{PYTHON_PATH} scripts/validation/scan_secrets.py --staged`

## Stage and Commit Workflow

```powershell
# 1. Stage your implementation changes
git add -A

# 2. Execute Phase 1: Sync
{PYTHON_PATH} scripts/validation/sync_artifacts.py --sync ; {PYTHON_PATH} scripts/validation/sync_artifacts.py --sync tests ; {PYTHON_PATH} scripts/validation/validate_readme_structure.py --update ; {PYTHON_PATH} scripts/generate_catalog.py

# 3. Restage all auto-generated changes
git add README.md docs/*.md knowledge/manifest.json

# 4. Execute Phase 2: Check Suite
{PYTHON_PATH} scripts/validation/validate_json_syntax.py --staged ; {PYTHON_PATH} scripts/validation/validate_yaml_frontmatter.py ; {PYTHON_PATH} scripts/validation/dependency_validator.py --broken ; {PYTHON_PATH} scripts/verify_catalog_links.py

# 5. Finalize Commit with Conventional Message
git commit -m "feat(scope): your summary" -m "Detailed body if needed"
```

> [!IMPORTANT]
> **Dynamic Path Resolution**: ALWAYS use the configuration variables for executables (e.g., `{PYTHON_PATH}`, `{GIT_PATH}`). These MUST be resolved from the configuration files at runtime. Configuration is the **Single Point of Truth** for all tool paths. Chain commands with `;` in PowerShell.


## Conventional Commits Format

```
<type>(<scope>): <description>

<body>

<footer>
```

| Type | When |
|------|------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `test` | Adding tests |
| `refactor` | Code change |
| `chore` | Maintenance |

## Learning From Failures (A10)

When a commit fails:
1. **Capture the error**
2. **Identify root cause**
3. **Implement fix**
4. **Document lesson** in this skill or relevant knowledge file.

##Related Skills

| Skill | Use When |
|-------|----------|
| `ci-monitor` | Watch CI after push |
| `shell-platform` | Platform-specific commands |

## Axiom Alignment

| Axiom | Application |
|-------|-------------|
| **A10 (Learning)** | Failures are feedback |
| A1 (Verifiability) | Automated sync ensures truth |
| A3 (Transparency) | Clear catalogs and READMEs |

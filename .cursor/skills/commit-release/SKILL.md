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

> "A failed commit teaches us more than a successful one - if we pay attention."

Traditional commit workflows block developers with cryptic errors. This skill:
- **Auto-fixes** what can be fixed (artifact sync, formatting)
- **Only blocks** for unfixable issues (secrets, syntax errors)
- **Documents lessons** from each failure to prevent recurrence

## When to Use

| Trigger | Example |
|---------|---------|
| After implementation | "Commit all changes with a meaningful message" |
| Feature complete | "Commit and push to remote" |
| Multiple files changed | "Stage, sync, and commit" |
| After CI failure | "Fix and recommit" |

## Prerequisites

| Tool | Purpose | Check |
|------|---------|-------|
| `git` | Version control | `git --version` |
| Python | Pre-commit scripts | Anaconda environment |
| Pre-commit hook | Auto-sync | `scripts/git/install_hooks.py` |

## Workflow

```mermaid
flowchart TD
    Start([Commit Request]) --> CheckFiles[Check Staged Files]
    CheckFiles --> HasChanges{Changes?}
    
    HasChanges -->|No| NoChanges([Nothing to commit])
    HasChanges -->|Yes| RunSync[Run Artifact Sync]
    
    RunSync --> SyncOK{Sync OK?}
    SyncOK -->|No| AutoFix[Auto-fix & Restage]
    AutoFix --> RunSync
    SyncOK -->|Yes| ValidateSecrets[Validate No Secrets]
    
    ValidateSecrets --> SecretsFound{Secrets?}
    SecretsFound -->|Yes| Block([BLOCKED - Remove Secrets])
    SecretsFound -->|No| ValidateSyntax[Validate JSON/YAML]
    
    ValidateSyntax --> SyntaxOK{Syntax OK?}
    SyntaxOK -->|No| FixSyntax[Fix Syntax Errors]
    FixSyntax --> ValidateSyntax
    SyntaxOK -->|Yes| UpdateChangelog[Update CHANGELOG]
    
    UpdateChangelog --> CreateMessage[Generate Commit Message]
    CreateMessage --> Commit[git commit]
    
    Commit --> CommitOK{Success?}
    CommitOK -->|No| LearnFailure[Document Failure Lesson]
    LearnFailure --> RetryOrEscalate{Can Retry?}
    RetryOrEscalate -->|Yes| RunSync
    RetryOrEscalate -->|No| Escalate([Escalate to Human])
    
    CommitOK -->|Yes| PushRequested{Push Requested?}
    PushRequested -->|Yes| Push[git push]
    PushRequested -->|No| Complete([Commit Complete])
    
    Push --> PushOK{Push OK?}
    PushOK -->|Yes| Complete
    PushOK -->|No| LearnFailure
```

## Pre-Commit Checklist

Before committing, use the **unified pre-commit runner**:

### Unified Pre-Commit Runner (Recommended)
```powershell
# Full sync mode - runs all validations in parallel and auto-fixes
{PYTHON_PATH} scripts/git/pre_commit_runner.py --sync

# Check mode - validate only, no modifications  
{PYTHON_PATH} scripts/git/pre_commit_runner.py --check

# Fast mode - skip slow validation checks
{PYTHON_PATH} scripts/git/pre_commit_runner.py --sync --fast

# Full mode - sync + run all tests in parallel
{PYTHON_PATH} scripts/git/pre_commit_runner.py --sync --full

# Sequential mode - disable parallel execution
{PYTHON_PATH} scripts/git/pre_commit_runner.py --sync --sequential
```

The unified runner executes in **2 parallel execution groups** (optimized for maximum parallelism):

| Group | Scripts (Parallel) | Time |
|-------|-------------------|------|
| 0 | `sync_manifest`, `sync_knowledge`, `validate_yaml`, `dependency_validator`, `sync_artifacts`, `generate_test_catalog`, `changelog_check` | ~1.2s (7 parallel) |
| 1 | `validate_readme`, `update_index` | ~0.5s (2 parallel) |

**Total: ~3-5 seconds** (optimized with fast file-based test counting)

**Workflow steps:**
1. **Cleanup** - Removes temp files (`__pycache__`, `.pytest_cache`, etc.)
2. **JSON Validation** - Validates all JSON syntax (excludes `data/` and `fixtures/`)
3. **Parallel Sync** - Runs 9 scripts across 4 groups in parallel
4. **Auto-Stage** - Stages files modified by sync scripts

### Changelog Helper (Automatic)
```powershell
# Check if changelog needs update (run by pre_commit_runner)
{PYTHON_PATH} scripts/docs/changelog_helper.py --check

# Get suggested entries if update needed
{PYTHON_PATH} scripts/docs/changelog_helper.py --suggest

# Validate changelog format
{PYTHON_PATH} scripts/docs/changelog_helper.py --validate
```

The changelog helper triggers when **3+ significant files** are staged:
- Blueprints (`blueprints/`)
- Knowledge files (`knowledge/*.json`)
- Templates (`templates/`)
- Agents (`.cursor/agents/`)
- Skills (`.cursor/skills/`)

### Legacy Individual Scripts
For debugging or specific tasks:

```powershell
# Artifact sync only
{PYTHON_PATH} scripts/validation/sync_artifacts.py --sync

# Secrets check
{PYTHON_PATH} scripts/validation/scan_secrets.py --staged
```

## Commit Message Format

Use Conventional Commits:

```
<type>(<scope>): <description>

<body>

<footer>
```

### Types
| Type | When |
|------|------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change, no feature/fix |
| `test` | Adding tests |
| `chore` | Maintenance tasks |

### Example
```
feat(workflows): expand workflow system from 1 to 21 workflows

Add 20 new workflows across 8 categories:
- Universal: feature-development, bugfix-resolution, code-review, tdd-cycle, release-management
- Quality: quality-gate, bdd-driven-development, security-audit
- Agile: sprint-planning, sprint-closure, daily-standup, backlog-refinement
- Blockchain: smart-contract-audit
- Trading: trading-strategy-pipeline
- SAP: rap-development, cap-service-development
- AI/ML: multi-agent-orchestration, rag-pipeline-development
- Operations: cicd-pipeline, incident-response

Includes validation tests and documentation updates.
```

## PowerShell Commit Command

For multi-line commit messages on Windows:

```powershell
# Option 1: Multiple -m flags
git commit -m "feat(scope): description" -m "Body paragraph" -m "Footer"

# Option 2: Single quoted string with backtick-n
git commit -m "feat(scope): description`n`nBody paragraph"

# AVOID: Heredoc syntax (Bash only, fails in PowerShell)
```

### Using --no-verify (CAUTION)

**PREFERRED: Use `safe_commit.py` instead** - it handles everything correctly:

```powershell
# safe_commit.py automatically runs pre-commit, then commits with --no-verify
{PYTHON_PATH} scripts/git/safe_commit.py "feat(scope): description" --push
```

**Manual --no-verify (only if you've already run pre-commit):**

```powershell
# ONLY use --no-verify if you've ALREADY run pre-commit:
{PYTHON_PATH} scripts/git/pre_commit_runner.py --sync

# Then commit with --no-verify to avoid running twice:
git commit --no-verify -m "feat(scope): description"
```

**WARNING:** Never use `--no-verify` without running pre-commit first. This bypasses all validation and can cause CI failures.

## Changelog Update

Before committing significant changes, update `CHANGELOG.md`:

```markdown
## [Unreleased]

### Added
- New workflow system with 21 workflows across 8 categories

### Changed
- Pre-commit hook now auto-syncs instead of blocking

### Fixed
- PowerShell commit message handling
```

## Learning From Failures (A10)

When a commit fails:

1. **Capture the error** - Save exact error message
2. **Identify root cause** - Why did it fail?
3. **Implement fix** - Resolve the issue
4. **Document lesson** - Add to this skill or create rule
5. **Prevent recurrence** - Update pre-commit hook if applicable

### Known Failure Patterns

| Pattern | Cause | Solution |
|---------|-------|----------|
| Heredoc error | PowerShell doesn't support `<<EOF` | Use multiple `-m` flags |
| Artifact out of sync | Files changed after staging | Run `sync_artifacts.py --sync --fast` |
| Secret detected | API key in file | Remove secret, use env var |
| JSON syntax error | Invalid JSON | Fix syntax before commit |
| JSON BOM error | PowerShell writes UTF-16 BOM | Use `utf-8-sig` encoding in Python |
| Pre-commit timeout | Slow artifact sync | Simplified hook: skip artifact sync |
| `set -e` silent fail | Shell exits on any error | Removed `set -e`, explicit error handling |

## Stage and Commit Flow

### Recommended: Use safe_commit.py (Enforced Validation)

```powershell
# Single command - ALWAYS runs pre-commit, then commits
{PYTHON_PATH} scripts/git/safe_commit.py "feat(scope): description"

# With push
{PYTHON_PATH} scripts/git/safe_commit.py "feat(scope): description" --push

# With body text
{PYTHON_PATH} scripts/git/safe_commit.py "feat(scope): description" --body "Detailed body"

# Fast mode (skip slow checks)
{PYTHON_PATH} scripts/git/safe_commit.py "fix(scope): quick fix" --fast --push

# Dry run (validate without committing)
{PYTHON_PATH} scripts/git/safe_commit.py --dry-run "feat(scope): test"
```

**Why safe_commit.py?**
- CANNOT be bypassed - pre-commit always runs first
- Prevents accidental `--no-verify` without validation
- Single command does everything correctly
- Used by shell agents for reliable commits

### Manual Flow (Legacy)

```powershell
# 1. Stage all changes
git add -A

# 2. Run unified pre-commit (auto-syncs and auto-stages)
{PYTHON_PATH} scripts/git/pre_commit_runner.py --sync

# 3. If changelog warning appears, review suggestions
{PYTHON_PATH} scripts/docs/changelog_helper.py --suggest
# Then manually update CHANGELOG.md with curated entries

# 4. Restage if changelog was updated
git add CHANGELOG.md

# 5. Commit with proper message format
git commit -m "feat(scope): description" -m "Detailed body"

# 6. Push if requested
git push origin HEAD
```

## Integration with Pre-Commit Hook

The Factory's pre-commit hook (`.git/hooks/pre-commit`) now:
- **Auto-syncs** all artifacts instead of blocking
- **Auto-stages** synced files
- **Checks changelog** and warns if significant changes need documentation
- Only **blocks** for secrets and syntax errors

Install the hook with:
```powershell
{PYTHON_PATH} scripts/git/install_hooks.py
```

This aligns with A10: failures are learning opportunities, not punishment.

## Output

After successful commit:

```
[OK] Pre-commit complete (auto-fixed and staged any sync updates)
[main abc1234] feat(workflows): expand workflow system
 25 files changed, 3000 insertions(+)
```

## Related Skills

| Skill | Use When |
|-------|----------|
| `ci-monitor` | Watch CI after push |
| `pipeline-error-fix` | CI failures after push |
| `shell-platform` | Platform-specific commands |

## Axiom Alignment

| Axiom | Application |
|-------|-------------|
| **A10 (Learning)** | Every failure teaches us something |
| A1 (Verifiability) | Commit messages explain changes |
| A3 (Transparency) | Clear changelog entries |
| A5 (Consistency) | Conventional commit format |

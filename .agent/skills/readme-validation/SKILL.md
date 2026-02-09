---
description: Validates that project structure documented in README.md accurately reflects the actual filesystem structure
---

# Readme Validation

Validates that project structure documented in README.md accurately reflects the actual filesystem structure

## 
# README Structure Validation Skill

> **Tool Paths:** Commands in this skill use default Windows paths from `.cursor/config/tools.json`.
> See [Configuration Guide](../../docs/CONFIGURATION.md) to customize for your environment.

## 
# README Structure Validation Skill

> **Tool Paths:** Commands in this skill use default Windows paths from `.cursor/config/tools.json`.
> See [Configuration Guide](../../docs/CONFIGURATION.md) to customize for your environment.

## Purpose
Validates that the project structure documented in README.md accurately reflects the actual filesystem structure. This skill ensures documentation stays synchronized with the codebase as the project evolves.

## Process
### Step 1: Run Validation Check

Execute the validation script to check if README matches actual structure:

```powershell
C:\App\Anaconda\python.exe scripts/validate_readme_structure.py --check
```

**Expected output if valid:**
```
✓ README project structure is up to date
  agents: 7
  skills: 18
  blueprints: 14
  patterns: 48
  knowledge: 42
  templates: 163
```

**Expected output if invalid:**
```
✗ README project structure is OUT OF DATE

Discrepancies found:
  - skills: README says 14, actual is 18
  - blueprints: README says 7, actual is 14
```

### Step 2: Review Discrepancies

If discrepancies are found, review what changed:

```powershell
# Generate current structure to see what's different
C:\App\Anaconda\python.exe scripts/validate_readme_structure.py --generate
```

### Step 3: Update README

If discrepancies are legitimate (new components added), update the README:

```powershell
C:\App\Anaconda\python.exe scripts/validate_readme_structure.py --update
```

This automatically updates the Project Structure section in README.md.

### Step 4: Verify Update

Run validation again to confirm the update was successful:

```powershell
C:\App\Anaconda\python.exe scripts/validate_readme_structure.py --check
```

```powershell
C:\App\Anaconda\python.exe scripts/validate_readme_structure.py --check
```

```
✓ README project structure is up to date
  agents: 7
  skills: 18
  blueprints: 14
  patterns: 48
  knowledge: 42
  templates: 163
```

```
✗ README project structure is OUT OF DATE

Discrepancies found:
  - skills: README says 14, actual is 18
  - blueprints: README says 7, actual is 14
```

```powershell
# Generate current structure to see what's different
C:\App\Anaconda\python.exe scripts/validate_readme_structure.py --generate
```

```powershell
C:\App\Anaconda\python.exe scripts/validate_readme_structure.py --update
```

```powershell
C:\App\Anaconda\python.exe scripts/validate_readme_structure.py --check
```

## Integration Points
### Pre-Commit Hook

Add to `.git/hooks/pre-commit` (or use pre-commit framework):

```bash
#!/bin/bash
python scripts/validate_readme_structure.py --check
if [ $? -ne 0 ]; then
    echo "README structure validation failed. Run: python scripts/validate_readme_structure.py --update"
    exit 1
fi
```

### CI/CD Integration

The validation is integrated into `.github/workflows/ci.yml`:

```yaml
- name: Validate README Structure
  run: python scripts/validate_readme_structure.py --check
```

### Manual Workflow

When extending the factory with new components:

1. Add your new agent/skill/blueprint/etc.
2. Run `--check` to see the discrepancy
3. Run `--update` to fix README
4. Commit both the new component AND the updated README

```bash
#!/bin/bash
python scripts/validate_readme_structure.py --check
if [ $? -ne 0 ]; then
    echo "README structure validation failed. Run: python scripts/validate_readme_structure.py --update"
    exit 1
fi
```

```yaml
- name: Validate README Structure
  run: python scripts/validate_readme_structure.py --check
```

## Command Reference
| Command | Description |
|---------|-------------|
| `--check` | Validate README against actual structure (default) |
| `--generate` | Print the correct structure markdown |
| `--update` | Update README.md in place |
| `--json` | Output scan results as JSON (for tooling) |
| `--root PATH` | Specify project root directory |

## What Gets Scanned
| Component | Location | Counted |
|-----------|----------|---------|
| Agents | `.cursor/agents/*.md` | Number of .md files |
| Skills | `.cursor/skills/*/SKILL.md` | Directories with SKILL.md |
| Blueprints | `blueprints/*/blueprint.json` | Directories with blueprint.json |
| Patterns | `patterns/**/*.json` | All JSON files in subdirectories |
| Knowledge | `knowledge/*.json` | All JSON files |
| Templates | `templates/**/*.tmpl` | All .tmpl files |

## Error Handling
- **README not found**: Script reports error and exits with code 1
- **Structure section not found**: Script warns and exits with code 1
- **Permission errors**: Standard Python permission error handling

## Relationship to Factory Components
This skill supports the factory's documentation-first approach:

- **Agents** use this skill via the `onboarding-architect` when validating project state
- **CI/CD** runs this automatically on every pull request
- **Developers** run this before commits to catch documentation drift

## Best Practices
- Run validation before every commit to catch drift early
- Integrate validation into pre-commit hooks for automated checks
- Keep README structure section as single source of truth
- Update README immediately when adding new components
- Use `--check` in CI to fail builds with outdated documentation
- Document any intentional discrepancies with comments
- Review structure changes during code review

## References
- Script: `scripts/validate_readme_structure.py`
- CI Config: `.github/workflows/ci.yml`
- README: `README.md` (Project Structure section)

## Prerequisites
> [!IMPORTANT]
> Requirements:

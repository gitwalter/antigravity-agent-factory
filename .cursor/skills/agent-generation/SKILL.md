---
name: agent-generation
description: Agent definition file generation skill
type: skill
knowledge: [best-practices.json]
templates: [patterns/agents/]
---

# Agent Generation Skill

Generates agent definition files from patterns for target projects.

## When to Use

- When generating agents for a new project
- When customizing agent behavior
- When creating new agent types

## Process

### Step 1: Load Agent Pattern
For each requested agent:
1. Load pattern from `patterns/agents/{agent-id}.json`
2. Parse metadata, frontmatter, and sections
3. Identify customization points

### Step 2: Apply Customizations
If customizations specified:
- Override frontmatter values
- Modify skill references
- Update knowledge file references

### Step 3: Render Markdown
Convert pattern to markdown format:

```markdown
---
name: {name}
description: {description}
type: agent
skills: [{skills}]
knowledge: [{knowledge}]
---

# {title}

## Purpose
{purpose}

## When Activated
{whenActivated}

## Workflow
{workflow steps}

## Skills Used
{skills table}

## Important Rules
{rules}
```

### Step 4: Write File
Write to target location:
- Path: `{TARGET}/.cursor/agents/{name}.md`
- Encoding: UTF-8
- Validate markdown structure

### Step 5: Update README Counts (Factory Only)

**CRITICAL:** When creating agents in the Cursor Agent Factory itself, ALWAYS run:

```powershell
{PYTHON_PATH} scripts/validation/validate_readme_structure.py --update
```

This updates the agent count in README.md to prevent CI failures.

## Output Format

Agent markdown file with:
- YAML frontmatter with metadata
- Purpose section
- When Activated section
- Workflow steps
- Skills Used table
- Important Rules list

## Fallback Procedures

- **If pattern not found**: Report error, skip agent
- **If customization fails**: Use default pattern values

## Important Rules

1. **Always update README counts** when adding agents to the factory
2. Run `validate_readme_structure.py --update` after creating any new agent
3. Commit the README update along with the new agent
4. This prevents CI pipeline failures

## References

- `patterns/agents/*.json`
- `knowledge/best-practices.json`
- `scripts/validation/validate_readme_structure.py`

---
name: skill-generation
description: Skill definition file generation skill
type: skill
knowledge: [best-practices.json]
templates: [patterns/skills/]
---

# Skill Generation Skill

Generates skill definition files from patterns for target projects.

## When to Use

- When generating skills for a new project
- When customizing skill behavior
- When creating new skill types

## Process

### Step 1: Load Skill Pattern
For each requested skill:
1. Load pattern from `patterns/skills/{skill-id}.json`
2. Parse metadata, frontmatter, and sections
3. Identify customization points

### Step 2: Apply Customizations
If customizations specified:
- Override frontmatter values
- Modify knowledge references
- Update MCP tool references

### Step 3: Render Markdown
Convert pattern to markdown format:

```markdown
---
name: {name}
description: {description}
type: skill
skills: [{skills}]
knowledge: [{knowledge}]
---

# {title}

{introduction}

## When to Use
{whenToUse}

## Process
{process steps}

## Fallback Procedures
{fallbacks}

## Important Rules
{rules}
```

### Step 4: Create Skill Directory
Create skill directory structure:

```
{TARGET}/.cursor/skills/{skill-name}/
├── SKILL.md           # Main skill definition
└── references/        # Optional reference docs
```

### Step 5: Update README Counts (Factory Only)

**CRITICAL:** When creating skills in the Cursor Agent Factory itself, ALWAYS run:

```powershell
{PYTHON_PATH} scripts/validation/validate_readme_structure.py --update
```

This updates the skill count in README.md to prevent CI failures.

**Why:** The README displays skill counts that must match actual files. Adding a skill without updating the README causes the CI pipeline to fail.

**Automation:** This step should be automatic - never skip it when adding skills to the factory.

## Output Format

Skill markdown file with:
- YAML frontmatter with metadata
- Introduction
- When to Use section
- Process steps with actions
- Fallback Procedures
- Important Rules

## Fallback Procedures

- **If pattern not found**: Report error, skip skill
- **If customization fails**: Use default pattern values

## Important Rules

1. **Always update README counts** when adding skills to the factory
2. Run `validate_readme_structure.py --update` after creating any new skill
3. Commit the README update along with the new skill
4. This prevents CI pipeline failures

## References

- `patterns/skills/*.json`
- `knowledge/best-practices.json`
- `scripts/validation/validate_readme_structure.py`

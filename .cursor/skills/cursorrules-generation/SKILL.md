---
name: cursorrules-generation
description: .cursorrules file generation skill
type: skill
knowledge: [best-practices.json]
templates: [templates/factory/cursorrules-template.md]
---

# Cursorrules Generation Skill

Generates the `.cursorrules` file that governs AI agent behavior in generated projects.

## When to Use

- When generating a new project
- When updating project configuration
- When customizing agent behavior rules

## Process

### Step 1: Load Template
Load the cursorrules template from:
`templates/factory/cursorrules-template.md`

### Step 2: Replace Variables
Replace all template variables with project values:

| Variable | Source |
|----------|--------|
| `{PROJECT_NAME}` | config.project_name |
| `{PROJECT_DESCRIPTION}` | config.project_description |
| `{PRIMARY_LANGUAGE}` | config.primary_language |
| `{STYLE_GUIDE}` | config.style_guide |
| `{DOMAIN}` | config.domain |
| `{GENERATED_DATE}` | Current date |

### Step 3: Generate Agent List
Create agent table from configured agents:

```markdown
| Agent | Purpose |
|-------|---------|
| `code-reviewer` | Reviews code quality |
| `test-generator` | Creates test cases |
```

### Step 4: Generate Skill List
Create skill table from configured skills:

```markdown
| Skill | Description |
|-------|-------------|
| `bugfix-workflow` | Ticket-based bug fixes |
| `feature-workflow` | Spec-based features |
```

### Step 5: Generate MCP Section
Create MCP server configuration:

```markdown
| Server | Purpose | URL |
|--------|---------|-----|
| `atlassian` | Jira/Confluence | https://mcp.atlassian.com/v1/sse |
```

### Step 6: Write File
Write to target location:
- Path: `{TARGET}/.cursorrules`
- Encoding: UTF-8

## Output

Complete `.cursorrules` file with:
- Project Context section
- Configuration Variables
- Available Agents table
- Available Skills table
- MCP Server Integration
- Autonomous Behavior Rules
- Response Behavior Guidelines

## Important Rules

1. **Complete variables** - Replace ALL placeholders
2. **Valid markdown** - Ensure proper formatting
3. **Working tables** - Tables must render correctly
4. **Accurate lists** - List actual configured items

## Fallback Procedures

- **If template not found**: Use embedded default template
- **If variable undefined**: Use empty or default value

## References

- `templates/factory/cursorrules-template.md`
- `knowledge/best-practices.json`

---
description: .cursorrules file generation skill
name: cursorrules-generation
type: skill
---
# Cursorrules Generation

.cursorrules file generation skill

Generates the `.cursorrules` file that governs AI agent behavior in generated projects.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Load Template
Load the cursorrules template from:
`{directories.templates}/factory/cursorrules-template.md`

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

1. **Use `{directories.XXX}` path variables** — NEVER hardcode directory paths in generated `.cursorrules` files. Always use configured path variables (e.g. `{directories.skills}`, `{directories.agents}`, `{directories.config}`). See `{directories.config}/settings.json` for the full mapping.
2. **Complete variables** - Replace ALL placeholders
3. **Valid markdown** - Ensure proper formatting
4. **Working tables** - Tables must render correctly
5. **Accurate lists** - List actual configured items

## Fallback Procedures

- **If template not found**: Use embedded default template
- **If variable undefined**: Use empty or default value

## References

- `{directories.templates}/factory/cursorrules-template.md`
- `{directories.knowledge}/best-practices.json`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

## Best Practices
- Always follow the established guidelines.
- Document any deviations or exceptions.
- Regularly review and update the skill documentation.

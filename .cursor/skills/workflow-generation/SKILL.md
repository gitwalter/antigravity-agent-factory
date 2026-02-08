---
name: workflow-generation
description: Workflow pattern generation and customization skill
type: skill
knowledge: [workflow-patterns.json, mcp-servers-catalog.json]
---

# Workflow Generation Skill

Generates workflow configurations and documentation based on methodology and trigger sources.

## When to Use

- When configuring project workflows
- When setting up MCP server integrations
- When generating workflow documentation

## Process

### Step 1: Parse Workflow Requirements
- Identify methodology (Agile, Kanban, etc.)
- List trigger sources (Jira, Confluence, etc.)
- List required output artifacts

### Step 2: Select Workflow Patterns
Match triggers to workflow patterns:

| Trigger | Patterns |
|---------|----------|
| Jira | `bugfix-workflow` |
| Confluence | `feature-workflow` |
| GitHub Issue | `bugfix-workflow` |
| GitHub PR | `code-review` |
| Manual | `code-templates` |

### Step 3: Configure MCP Servers
For each trigger, configure required MCP server:

| Trigger | MCP Server | Authentication |
|---------|------------|----------------|
| Jira | `atlassian` | OAuth |
| Confluence | `atlassian` | OAuth |
| GitHub | `deepwiki` | None |
| SAP Docs | `sap-documentation` | None |

Generate MCP configuration:

```yaml
mcpServers:
  atlassian:
    url: "https://mcp.atlassian.com/v1/sse"
    headers: {}
```

### Step 4: Generate Workflow Files
For each selected pattern, generate documentation:

- `workflows/{pattern_name}.md`
- Include trigger conditions
- Include step-by-step process
- Include artifact outputs

### Step 5: Output Configuration

```yaml
workflows:
  methodology: "{METHODOLOGY}"
  patterns: ["bugfix-workflow", "feature-workflow"]
  triggers:
    - type: "jira"
      pattern: "{PROJECT_KEY}-{NUMBER}"
    - type: "confluence"
      pagePattern: "Page ID or URL"
  mcpServers: [...]
```

## Fallback Procedures

- **If trigger not supported**: Ask user for manual workflow design
- **If MCP server unavailable**: Document manual fallback procedure

## References

- `knowledge/workflow-patterns.json`
- `knowledge/mcp-servers-catalog.json`

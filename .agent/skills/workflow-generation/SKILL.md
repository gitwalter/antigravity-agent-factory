---
description: Workflow pattern generation and customization skill
name: workflow-generation
type: skill
---

# Workflow Generation

Workflow pattern generation and customization skill

## 
# Workflow Generation Skill

Generates workflow configurations and documentation based on methodology and trigger sources.

## 
# Workflow Generation Skill

Generates workflow configurations and documentation based on methodology and trigger sources.

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
- **REQUIRED:** Include `**Version:** x.x.x` in the file (typically in the Overview/metadata block). This is validated by CI tests and will fail the build if missing.
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

```yaml
mcpServers:
  atlassian:
    url: "https://mcp.atlassian.com/v1/sse"
    headers: {}
```

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

## Best Practices
- **Match workflow patterns to actual team processes**: Don't force-fit patterns; customize workflows to match how the team actually works rather than imposing theoretical processes
- **Validate MCP server availability before workflow creation**: Check that required MCP servers are accessible and properly configured before generating workflows that depend on them
- **Design workflows with clear trigger conditions**: Define specific, testable conditions for when workflows activate to avoid ambiguity and false triggers
- **Include manual fallback procedures**: Always document what to do when automated steps fail, ensuring workflows remain useful even when integrations break
- **Test workflow execution paths**: Validate that all decision branches and escalation paths work correctly before marking workflows as production-ready
- **Document workflow dependencies**: Clearly list all external systems, credentials, and prerequisites needed for workflow execution in the workflow documentation

## Fallback Procedures
- **If trigger not supported**: Ask user for manual workflow design
- **If MCP server unavailable**: Document manual fallback procedure

## References
- `knowledge/workflow-patterns.json`
- `knowledge/mcp-servers-catalog.json`

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Knowledge: workflow-patterns.json, mcp-servers-catalog.json

---
description: Workflow pattern generation and customization skill with mandatory schema
  validation against schemas/workflow.schema.json
name: workflow-generation
type: skill
---
# Workflow Generation

Workflow pattern generation and customization skill with mandatory schema validation against schemas/workflow.schema.json

Generates workflow configurations and documentation based on methodology and trigger sources, with mandatory schema validation against `schemas/workflow.schema.json`.

## Canonical Schema Reference

Workflow frontmatter MUST validate against `schemas/workflow.schema.json`. Required fields:

| Field | Type | Constraints |
|-------|------|-------------|
| `name` | string | Min 3 chars |
| `description` | string | Min 20 chars |
| `version` | string | Semantic version |
| `type` | enum | ONLY: supervisor, sequential, parallel, hierarchical, iterative, pipeline |
| `domain` | enum | ONLY: ai-ml, agile, blockchain, dotnet, java, operations, python, quality, sap, trading, typescript, universal |
| `steps` | array | Min 2 items, each with required `name` and `description` |
| `agents` | array | Min 1 item |
| `blueprints` | array | Min 1 item (use `["none"]` if not applicable) |

**Domain mapping:** data-science → `python` or `ai-ml`, automation → `operations`, general → `universal`

## Validation Checklist

- [ ] All required frontmatter fields present
- [ ] `type` and `domain` use allowed enum values
- [ ] At least 2 steps, each with `name` and `description`
- [ ] At least 1 agent listed
- [ ] `blueprints` has min 1 item (use `["none"]` when no blueprint)
- [ ] `**Version:** x.x.x` included in file body (CI validation)

## Common Violations

| Violation | Fix |
|-----------|-----|
| Missing `blueprints` | Add `blueprints: ["none"]` if no blueprint |
| Invalid `domain` | Map to allowed enum or use mapping table |
| Only 1 step | Add at least 2 steps |
| Step missing `description` | Every step needs `name` and `description` |
| Missing `**Version:**` in body | Add version line for CI validation |

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
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

- `{directories.workflows}/{pattern_name}.md`
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

## Best Practices

- **Match workflow patterns to actual team processes**: Don't force-fit patterns; customize workflows to match how the team actually works
- **Validate MCP server availability before workflow creation**: Check that required MCP servers are accessible and properly configured
- **Design workflows with clear trigger conditions**: Define specific, testable conditions for when workflows activate
- **Include manual fallback procedures**: Always document what to do when automated steps fail
- **Test workflow execution paths**: Validate that all decision branches and escalation paths work correctly
- **Document workflow dependencies**: Clearly list all external systems, credentials, and prerequisites

## Important Rules

1. **Use `{directories.XXX}` path variables** — NEVER hardcode directory paths like `workflows/` or `knowledge/` in generated workflow content. See `{directories.config}/settings.json` for the full mapping.
2. **Lowercase kebab-case filenames** — All workflow files must use lowercase kebab-case (e.g. `feature-development.md`).
3. **Validate against schema** — Ensure frontmatter validates against `schemas/workflow.schema.json`.

## Fallback Procedures

- **If trigger not supported**: Ask user for manual workflow design
- **If MCP server unavailable**: Document manual fallback procedure

## References

- `{directories.knowledge}/workflow-patterns.json`
- `{directories.knowledge}/mcp-servers-catalog.json`
- `{directories.knowledge}/knowledge-cross-reference.json`
- `schemas/workflow.schema.json`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

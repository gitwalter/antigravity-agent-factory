---
agents:
- none
category: chain
description: Code and document template generation skill with mandatory schema validation
  against schemas/template.schema.json
knowledge:
- none
name: generating-templates
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# Template Generation

Code and document template generation skill with mandatory schema validation against schemas/template.schema.json

Generates code and document templates for target projects with mandatory schema validation against `schemas/template.schema.json`.

## Canonical Schema Reference

Template metadata (embedded in .j2/.tmpl files as comment) MUST validate against `schemas/template.schema.json`. Required fields:

| Field | Type | Constraints |
|-------|------|-------------|
| `name` | string | Min 3 chars |
| `description` | string | Min 20 chars |
| `version` | string | Semantic version |
| `category` | enum | ONLY: agents, graphs, memory, rag, tests, tools, ai, python, docs, config, trading, sap, dotnet, java, web |
| `variables` | array | Min 1 item, each with name, type, description, required |
| `produces` | string | What file type is generated |
| `used_by_skills` | array | Min 1 item |
| `used_by_blueprints` | array | Min 1 item |

## Validation Checklist

- [ ] All required metadata fields present
- [ ] `category` uses allowed enum value
- [ ] Each variable has `name`, `type`, `description`, `required`
- [ ] At least 1 skill in `used_by_skills`
- [ ] At least 1 blueprint in `used_by_blueprints` (use `["none"]` if not applicable)
- [ ] `produces` clearly describes output file type

## Common Violations

| Violation | Fix |
|-----------|-----|
| Missing `used_by_blueprints` | Add `used_by_blueprints: ["none"]` if no blueprint |
| Variable missing `required` | Each variable needs name, type, description, required |
| Empty `variables` | Add at least 1 variable |
| Invalid `category` | Use one of the allowed enum values |
| Short `description` | Min 20 chars |

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Determine Template Categories
Based on stack, identify template categories:

| Stack | Categories |
|-------|------------|
| Python | service-class, repository, model, schema, test-class |
| TypeScript | component, hook, service, test |
| Java | controller, service, repository, entity, dto, test |
| ABAP | global-class, service-class, test-class, enhancement |

### Step 2: Generate Code Templates
For each category:
1. Create template file with variable placeholders
2. Apply stack naming conventions
3. Include proper imports/dependencies
4. Add documentation comments
5. Embed metadata header validating against `schemas/template.schema.json`

Template structure:
```
{directories.templates}/{language}/{category}/{template-name}.{ext}
```

### Step 3: Generate Document Templates
Create standard document templates:

| Template | Purpose |
|----------|---------|
| `implementation_plan.md` | Implementation planning |
| `technical_spec.md` | Technical specification |
| `test_plan.md` | Test planning |

### Step 4: Variable Placeholders
Use consistent variable placeholders:

| Variable | Description |
|----------|-------------|
| `{CLASS_NAME}` | Class name |
| `{METHOD_NAME}` | Method name |
| `{FILE_NAME}` | File name |
| `{DESCRIPTION}` | Description text |
| `{TICKET_ID}` | Ticket identifier |

## Output

Templates in project structure:

```
{TARGET}/
├── {directories.templates}/
│   ├── {language}/
│   │   ├── service-class/
│   │   ├── test-class/
│   │   └── ...
│   └── docs/
│       ├── implementation_plan.md
│       └── technical_spec.md
```

## Best Practices

- **Follow stack-specific conventions**: Research and apply naming conventions, file structure, and code style patterns specific to the target technology stack
- **Use consistent placeholder naming**: Establish a clear convention for template variables (e.g., `{CLASS_NAME}`, `{METHOD_NAME}`) and document all placeholders
- **Include helpful comments in templates**: Add comments explaining template structure, required variables, and usage examples
- **Validate templates with real examples**: Generate sample outputs from templates using realistic values to ensure they produce correct, runnable code
- **Organize templates by category**: Group templates logically (by language, by pattern type, by use case)
- **Version templates when patterns change**: Update template version numbers and changelogs when modifying templates

## Important Rules

1. **Use `{directories.XXX}` path variables** — NEVER hardcode directory paths like `templates/` or `knowledge/` in generated template content. See `{directories.config}/settings.json` for the full mapping.
2. **Validate against schema** — Template metadata must validate against `schemas/template.schema.json`.

## Fallback Procedures

- **If template category unknown**: Create minimal generic template
- **If style guide unavailable**: Use default conventions

## References

- `{directories.knowledge}/stack-capabilities.json`
- `{directories.knowledge}/knowledge-cross-reference.json`
- `{directories.patterns}/templates/template-pattern.json`
- `schemas/template.schema.json`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

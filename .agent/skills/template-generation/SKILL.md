---
name: template-generation
description: Code and document template generation skill
type: skill
knowledge: [stack-capabilities.json, best-practices.json]
---

# Template Generation Skill

Generates code and document templates for target projects.

## When to Use

- When creating templates for a new project
- When adding new template categories
- When customizing existing templates

## Process

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

Template structure:
```
templates/{language}/{category}/{template-name}.{ext}
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
├── templates/
│   ├── {language}/
│   │   ├── service-class/
│   │   ├── test-class/
│   │   └── ...
│   └── docs/
│       ├── implementation_plan.md
│       └── technical_spec.md
```

## Fallback Procedures

- **If template category unknown**: Create minimal generic template
- **If style guide unavailable**: Use default conventions

## References

- `knowledge/stack-capabilities.json`
- `patterns/templates/template-pattern.json`

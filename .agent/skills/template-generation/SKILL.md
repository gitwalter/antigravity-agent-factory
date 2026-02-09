---
description: Code and document template generation skill
---

# Template Generation

Code and document template generation skill

## 
# Template Generation Skill

Generates code and document templates for target projects.

## 
# Template Generation Skill

Generates code and document templates for target projects.

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

```
templates/{language}/{category}/{template-name}.{ext}
```

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

## Best Practices
- **Follow stack-specific conventions**: Research and apply naming conventions, file structure, and code style patterns specific to the target technology stack
- **Use consistent placeholder naming**: Establish a clear convention for template variables (e.g., `{CLASS_NAME}`, `{METHOD_NAME}`) and document all placeholders
- **Include helpful comments in templates**: Add comments explaining template structure, required variables, and usage examples to guide future users
- **Validate templates with real examples**: Generate sample outputs from templates using realistic values to ensure they produce correct, runnable code
- **Organize templates by category**: Group templates logically (by language, by pattern type, by use case) to make them easy to discover and maintain
- **Version templates when patterns change**: Update template version numbers and changelogs when modifying templates to track evolution and breaking changes

## Fallback Procedures
- **If template category unknown**: Create minimal generic template
- **If style guide unavailable**: Use default conventions

## References
- `knowledge/stack-capabilities.json`
- `patterns/templates/template-pattern.json`

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Knowledge: stack-capabilities.json, best-practices.json

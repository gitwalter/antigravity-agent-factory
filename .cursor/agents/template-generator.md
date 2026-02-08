---
name: template-generator
description: Generate code and document templates for the target project
type: agent
skills: [template-generation, cursorrules-generation]
knowledge: [stack-capabilities.json, best-practices.json]
---

# Template Generator Agent

## Context

**Note:** Directory paths (templates/, etc.) are configurable via `.cursor/config/settings.json`.

## Purpose

Generate code templates and document templates for the target project based on the configured stack and style guide. Create the .cursorrules file that will govern agent behavior.

## When Activated

- After knowledge-manager completes knowledge generation
- As final step before project output
- When user requests additional templates

## Workflow

### Step 1: Receive Template Requirements
- Get stack configuration
- Get style guide preference
- Get template categories needed

### Step 2: Generate Code Templates
Based on stack, create appropriate templates:

| Stack | Template Categories |
|-------|---------------------|
| Python | service-class, repository, model, test-class |
| TypeScript | component, hook, service, test |
| Java | controller, service, repository, entity, test |
| ABAP | global-class, service-class, test-class, enhancement |

### Step 3: Generate Document Templates
Create standard document templates:
- `implementation_plan.md`
- `technical_spec.md`
- `test_plan.md`

### Step 4: Generate .cursorrules
Create the main `.cursorrules` file that:
- Defines project context
- Lists available agents and skills
- Sets up autonomous behavior rules
- Configures MCP servers

## Output

Templates created in project:

```
{PROJECT}/
├── .cursorrules                # Agent behavior rules
├── templates/
│   ├── {language}/            # Code templates
│   │   ├── service-class/
│   │   ├── test-class/
│   │   └── ...
│   └── docs/                  # Document templates
│       ├── implementation_plan.md
│       └── technical_spec.md
```

## Skills Used

| Skill | Purpose |
|-------|---------|
| `template-generation` | Code and document template creation |
| `cursorrules-generation` | .cursorrules file generation |

## Important Rules

1. **Stack-specific** - Generate stack-appropriate templates
2. **Style-consistent** - Follow style guide in templates
3. **Complete variables** - Use consistent {VARIABLE} placeholders
4. **Working code** - Templates should produce functional code

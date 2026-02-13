# template-generator

Generate code and document templates for the target project

- **Role**: Agent
- **Model**: default

## Purpose
Generate code templates and document templates for the target project based on the configured stack and style guide. Create the .cursorrules file that will govern agent behavior.

## Philosophy
"Templates are the DNA of generated projects - they must be complete, correct, and customizable."

## Activation
**Triggers:**
- After knowledge-manager completes knowledge generation
- As final step before project output
- When user requests additional templates

## Skills
- [[template-generation]]
- [[cursorrules-generation]]

## Knowledge
- [stack-capabilities.json](../knowledge/stack-capabilities.json)
- [best-practices.json](../knowledge/best-practices.json)

---
name: automated-code-generation
type: skill
description: 'Uses the Factory project generation engine to create core file structures and basic implementation logic from parsed PRD requirements. Orchestrates the ProjectGenerator and uses builder agents for initial implementation.'
license: MIT
allowed-tools: Read, Write, Execute
metadata:
  version: 1.0.0
  phase: implementation
  llm-preference: gemini
  standard: agentic-code-gen
agents:
- python-ai-specialist
knowledge:
- none
templates:
- none
related_skills:
- prd-parsing-logic
- repository-maintenance
---

# Automated Code Generation

Triggers the Factory generation engine and populates implementation files with code derived from PRD acceptance criteria.

## Prerequisites

- Verified `ProjectConfig` object from `prd-parsing-logic`.
- Active environment with `ProjectGenerator` dependencies.
- Plane issue ID for traceability.


## Process

1. **Initialize Config**: Create a `ProjectConfig` object using data from the `prd-parsing-logic` skill.
2. **Structural Generation**: Invoke `ProjectGenerator` to create the scaffolding (directories, rules, workflows).
3. **Requirement Mapping**: For each Story extracted from the PRD:
   - Identify the target file(s) in `src/` or `scripts/`.
   - Pass the Story's acceptance criteria and AI component specs to a "Builder Agent".
   - Use `write_to_file` to populate the target files with the generated implementation.
4. **Consistency Check**: Verify that all generated files adhere to the project's Layer 0-4 standards.

## Guidelines

- **Minimal Placeholders**: Avoid generating "TODO" comments. Aim for functional, if minimal, implementation logic.
- **TDD Integration**: Generate corresponding unit test stubs (`tests/`) simultaneously with implementation.
- **Traceability**: Add a header to generated files linking back to the Plane issue and Story ID.

## Best Practices

- **Incremental Generation**: Generate and verify structural foundations before adding complex implementation logic.
- **Fail-Fast**: Validate the input configuration strictly before initiating file writes.
- **Root Cleanliness**: Ensure all temporary generational artifacts are stored in `tmp/`.


## When to Use

- After a PRD has been successfully parsed into a configuration.
- To bootstrap a new feature or project with Factory-standard foundations.

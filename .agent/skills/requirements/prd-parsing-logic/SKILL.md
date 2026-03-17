---
name: prd-parsing-logic
type: skill
description: 'Parses an Agentic PRD (knowledge/prd.md) to extract structured configuration for automated project generation. Extracts Epics, Stories (with JSON acceptance criteria), NFRs, and AI components. Use when initializing a project or feature implementation from a verified PRD.'
license: MIT
allowed-tools: Read
metadata:
  version: 1.0.0
  phase: requirements
  llm-preference: claude
  standard: agentic-prd-parsing
agents:
- system-architecture-specialist
knowledge:
- none
templates:
- none
related_skills:
- writing-prd
- automated-code-generation
---

# PRD Parsing Logic

Extracts machine-readable signals from the Factory standard PRD format.

## Prerequisites

- A valid `knowledge/prd.md` file following the Factory PRD template.
- Target PRD must be in `READY` state.


## Process

1. **Load PRD**: Read `knowledge/prd.md`.
2. **Identify JSON Blocks**: Locate all ```json blocks within the "Functional Requirements" section. These contain machine-executable acceptance criteria.
3. **Extract Metadata**:
   - Extract `project_name` from H1.
   - Extract `description` from Executive Summary.
4. **Extract AI Components**: Parse Section 5 "AI Component Specifications" to identify model requirements and grounding strategies.
5. **Map to Config**: Convert the extracted data into a `ProjectConfig` schema.

## Guidelines

- **Regex Precision**: Use robust regex to find the start and end of specific sections (Functional Requirements, NFRs, etc.).
- **Validation**: Ensure that every extracted JSON block is valid and follows the `story_id` / `acceptance` structure.
- **Error Handling**: If a required section is missing, flag it as a warning but continue if possible.

## Best Practices

- **Schema Strictness**: Validate extracted JSON blocks against `story_id` and `acceptance` criteria schemas.
- **Context Preservation**: Ensure AI component specs include all necessary grounding and model parameters.
- **Idempotency**: Parsing the same PRD multiple times should yield identical `ProjectConfig` objects.


## When to Use

- When a `knowledge/prd.md` exists and is marked as READY.
- Before running the `automated-code-generation` skill.

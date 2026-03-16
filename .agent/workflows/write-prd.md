---
description: Comprehensive workflow for writing the Product Requirements Document
  (PRD).
version: 1.0.0
tags:
- write
- prd
- standardized
---


# /writing-prd Workflow

**Version:** 1.0.0


**Goal:** Transform an approved Prototype Brief into a formal, structured PRD with functional requirements and user stories.

## Phases

### Phase 1: PRD Generation
- **Goal**: Transform an approved Prototype Brief into a formal, structured PRD.
- **Agent**: `project-operations-specialist`
- **Skills**: writing-prd
- **Tools**: write_to_file
- **Actions**:
    - Load `knowledge/prototype-brief.md`.
    - Trigger `.agent/skills/requirements/writing-prd/SKILL.md`.
    - Write to `knowledge/prd.md` using `knowledge/templates/prd.md`.

### Phase 2: Story Slicing
- **Goal**: Ensure user stories are vertically sliced and ready for development.
- **Agent**: `project-operations-specialist`
- **Skills**: slicing-stories
- **Tools**: replace_file_content
- **Actions**:
    - Trigger `.agent/skills/requirements/slicing-stories/SKILL.md`.
    - Prompt user to run `/eliciting-nfr` to complete technical requirements.


## Trigger Conditions
- Triggered by user context or meta-orchestrator.


## Trigger Examples:
- "Execute this workflow."


## Best Practices
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.


## Related
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)

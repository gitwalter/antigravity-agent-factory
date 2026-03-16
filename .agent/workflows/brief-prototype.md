---
description: Formalizes a selected opportunity into a Prototype Brief (Phase 1 Gate).
version: 1.0.0
tags:
- brief
- prototype
- standardized
---


# /briefing-prototypes Workflow

**Version:** 1.0.0


**Goal:** Transform a prioritized opportunity cluster into a formal, human-approvable Prototype Brief.

## Phases

### Phase 1: Prototype Brief Extraction
- **Goal**: Research potential opportunities and formalize the one with the highest ROI.
- **Agent**: `project-operations-specialist`
- **Skills**: brainstorming-ideas, researching-first
- **Tools**: search_web, deepwiki
- **Actions**:
    - Load `knowledge/opportunities.md`.
    - Trigger `.agent/skills/ideation/briefing-prototypes/SKILL.md`.
    - Write to `knowledge/prototype-brief.md` using `knowledge/templates/prototype-brief.md`.


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

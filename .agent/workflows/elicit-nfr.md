---
description: Structured Socratic elicitation session to surface all non-functional
  requirements.
version: 1.0.0
tags:
- elicit
- nfr
- standardized
---


# /eliciting-nfr Workflow

**Version:** 1.0.0


**Goal:** Identify and document critical NFRs (Performance, Security, Reliability) that standard templates often miss.

## Steps:
1. **Target**: Load `knowledge/prd.md` (or draft).
2. **Execute**: Trigger `.agent/skills/requirements/eliciting-nfr/SKILL.md`.
3. **Capture**: Update `knowledge/nfr.md` (or section in PRD).
4. **Follow-up**: Recommend running `/reviewing-requirements` to validate the combined requirements set.


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

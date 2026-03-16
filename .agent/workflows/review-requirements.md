---
description: Adversarial review of requirements using 3 personas + a judge to improve
  F1 quality.
version: 1.0.0
tags:
- review
- requirements
- standardized
---


# /reviewing-requirements Workflow

**Version:** 1.0.0


**Goal:** Improve requirement quality through Multi-Agent Debate (MAD), detecting ambiguities, contradictions, and missing edge cases.

## Steps:
1. **Target**: Load `knowledge/prd.md`.
2. **Execute**: Trigger `.agent/skills/requirements/reviewing-requirements/SKILL.md`.
3. **Logic**: Run 3 personas (Optimist, Pessimist, Realist) followed by a Judge synthesis.
4. **Output**: Append review findings to `knowledge/prd.md` or a separate `review_report.md`.
5. **Phase Gate**: Ask the user for final sign-off on the Requirements phase.


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

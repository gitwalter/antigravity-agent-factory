---
description: Convergent synthesis of raw ideas into opportunity clusters.
version: 1.0.0
tags:
- cluster
- standardized
---


# /cluster Workflow

**Version:** 1.0.0


**Goal:** Group raw ideas into meaningful themes and prioritize them using the Prioritization Matrix.

## Steps:
1. **Target**: Load all `knowledge/ideas/raw/*.md`.
2. **Execute**: Trigger `.agent/skills/ideation/clustering-opportunities/SKILL.md`.
3. **Output**: Write to `knowledge/opportunities.md`.
4. **Follow-up**: Recommend the top-scoring clusters and prompt user to run `/brief` on a specific selection.


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

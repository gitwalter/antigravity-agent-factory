---
description: High-volume divergent ideation session. Generates 20+ raw ideas.
version: 1.0.0
tags:
- brainstorming-ideas
- standardized
---


# /brainstorming-ideas Workflow

**Version:** 1.0.0


**Goal:** Generate a wide range of creative solutions and features anchored to the current problem frame.

## Steps:
1. **Target**: Load `knowledge/problem-frame.md`.
2. **Execute**: Trigger `.agent/skills/ideation/brainstorming-ideas/SKILL.md`.
3. **Capture**: Append results to `knowledge/ideas/raw/YYYY-MM-DD-session.md`.
4. **Follow-up**: Prompt user to run `/cluster` next to synthesize ideas.


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

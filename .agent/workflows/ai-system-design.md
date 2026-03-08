---
description: Comprehensive workflow for designing AI systems including requirements analysis, architecture selection, cost estimation, and detailed design documentation.
version: 1.0.0
---

# /ai-system-design Workflow

**Version:** 1.0.0


**Goal:** Transform approved requirements (PRD) into a robust, scalable, and cost-effective AI system architecture.

## Steps:
1. **Target**: Load `knowledge/prd.md`.
2. **Execute**: Trigger `.agent/skills/parallel/designing-ai-systems/SKILL.md`.
3. **API Design**: Trigger `.agent/skills/parallel/designing-apis/SKILL.md` if external interfaces are required.
4. **Template**: Use `knowledge/templates/ai-design.md`.
5. **Output**: Write to `knowledge/ai-design.md`.
6. **Follow-up**: Prompt user to run `/agent-development` (Phase 4) once the design is approved.


## Trigger Conditions
- Triggered by user context or meta-orchestrator.


## Trigger Examples:
- "Execute this workflow."

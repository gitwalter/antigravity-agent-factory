---
description: Multi-step workflow for developing AI agents from design through deployment.
version: 1.0.0
---

# /agent-development Workflow (SDLC Phase 4)

**Version:** 1.0.0
**Created:** 2026-03-06
**Agent:** `project-operations-specialist`

**Goal:** Implement the approved AI System Design, ensuring all code and agent logic are production-ready.

## Trigger Conditions

This workflow is activated when:
- Phase 3 (Architecture) is marked complete.
- A user explicitly requests to build an agent based on the AI design.
- The `sdlc-meta-orchestrator` transitions to Phase 4.

## Trigger Examples:
- "Start agent development based on the design."
- "Build the feature agent."
- "Execute Phase 4 of SDLC."

## Steps:
1. **Target**: Load `knowledge/ai-design.md` and `knowledge/prd.md`.
2. **Execute**: Trigger `.agent/skills/parallel/agent-generation/SKILL.md` (if building agents).
3. **Build**: Iterate on implementation based on `implementation_plan.md`.
4. **Walkthrough**: Generate `walkthrough.md` using the `/documentation-workflow`.
5. **Output**: Write implementation to the repository and ensure all technical docs are updated.
6. **Follow-up**: Prompt user to run `/agent-testing` (Phase 5) to verify the build.

## Phase Gate (Build):
- Mandatory generation of `walkthrough.md`.
- Code must pass initial "Green" verification.

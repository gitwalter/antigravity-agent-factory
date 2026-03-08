---
description: Agent testing workflow covering unit tests with mocks, integration tests, and LLM evaluation. Ensures agents behave c...
version: 1.0.0
---

# /agent-testing Workflow (SDLC Phase 5)

**Version:** 1.0.0


**Goal:** Verify implementation against requirements using rigorous unit, integration, and LLM-based evaluation.

## Steps:
1. **Target**: Load `knowledge/walkthrough.md`, `knowledge/prd.md`, and `knowledge/ai-design.md`.
2. **Execute**: Trigger `.agent/skills/verification/verifying-artifact-structures/SKILL.md`.
3. **Unit Tests**: Run project-specific test suites (e.g., `pytest`, `npm test`).
4. **Eval**: Trigger LLM-based evaluation of agentic outputs if applicable.
5. **Report**: Generate `eval-report.md` using `knowledge/templates/eval-report.md`.
6. **Output**: Write report to `knowledge/eval-report.md`.
7. **Follow-up**: Prompt user to run `/release-management` (Phase 6) if the report is "Green".

## Phase Gate (Test & Eval):
- Mandatory generation of `eval-report.md`.
- No P0 issues; 100% requirements coverage validated.


## Trigger Conditions
- Triggered by user context or meta-orchestrator.


## Trigger Examples:
- "Execute this workflow."

---
description: Agent testing-agents workflow covering unit tests with mocks, integration tests,
  and LLM evaluation. Ensures agents behave c...
version: 1.0.0
tags:
- agent
- testing-agents
- standardized
---


# /agent-testing-agents Workflow (SDLC Phase 5)

**Version:** 1.0.0


**Goal:** Verify implementation against requirements using rigorous unit, integration, and LLM-based evaluation.

## Phases

### Phase 1: Artifact & Structure Verification
- **Goal**: Verify implemented structures against architectural definitions.
- **Agents**: `workflow-quality-specialist`
- **Skills**: verifying-artifact-structures, analyzing-code
- **Tools**: view_file
- **Actions**:
    - Load `knowledge/walkthrough.md`, `knowledge/prd.md`, and `knowledge/ai-design.md`.
    - Trigger `.agent/skills/verification/verifying-artifact-structures/SKILL.md`.

### Phase 2: Unit & Integration Testing
- **Goal**: Execute codebase-specific verification suites.
- **Agents**: `workflow-quality-specialist`
- **Skills**: verifying-artifact-structures
- **Tools**: run_command
- **Actions**:
    - Run project-specific test suites (e.g., `pytest`, `npm test`).

### Phase 3: LLM Evaluation & Reporting
- **Goal**: Perform qualitative assessment and generate final report.
- **Agents**: `workflow-quality-specialist`, `knowledge-operations-specialist`
- **Skills**: evaluating-llms, writing-prd
- **Tools**: write_to_file
- **Actions**:
    - Trigger LLM-based evaluation of agentic outputs if applicable.
    - Generate `eval-report.md` using `knowledge/templates/eval-report.md`.
    - Prompt user to run `/committing-releases` (Phase 6) if the report is "Green".

## Phase Gate (Test & Eval):
- Mandatory generation of `eval-report.md`.
- No P0 issues; 100% requirements coverage validated.


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

---
agents:
- workflow-quality-specialist
- knowledge-operations-specialist
blueprints:
- universal
description: Antigravity workflow for agent-testing. Standardized for IDX Visual Editor.
domain: universal
name: agent-testing
steps:
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Load `knowledge/walkthrough.md`, `knowledge/prd.md`, and `knowledge/ai-design.md`.
  - Trigger `.agent/skills/verification/verifying-artifact-structures/SKILL.md`.
  agents:
  - workflow-quality-specialist
  goal: Verify implemented structures against architectural definitions.
  name: Artifact & Structure Verification
  skills:
  - verifying-artifact-structures
  - analyzing-code
  tools:
  - view_file
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Run project-specific test suites (e.g., `pytest`, `npm test`).
  agents:
  - workflow-quality-specialist
  goal: Execute codebase-specific verification suites.
  name: Unit & Integration Testing
  skills:
  - verifying-artifact-structures
  tools:
  - run_command
- actions:
  - '**Agents**: `workflow-quality-specialist`, `knowledge-operations-specialist`'
  - '**Actions**:'
  - Trigger LLM-based evaluation of agentic outputs if applicable.
  - Generate `eval-report.md` using `knowledge/templates/eval-report.md`.
  - Prompt user to run `/committing-releases` (Phase 6) if the report is "Green".
  - Mandatory generation of `eval-report.md`.
  - No P0 issues; 100% requirements coverage validated.
  - Triggered by user context or meta-orchestrator.
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - workflow-quality-specialist
  - knowledge-operations-specialist
  goal: Perform qualitative assessment and generate final report.
  name: LLM Evaluation & Reporting
  skills:
  - evaluating-llms
  - writing-prd
  tools:
  - write_to_file
tags: []
type: sequential
version: 2.0.0
---
# /agent-testing-agents Workflow (SDLC Phase 5)

**Version:** 1.0.0

## Overview
This workflow governs the qualitative and quantitative evaluation of AI agents, ensuring they meet architectural standards and functional requirements before release.

## Trigger Conditions
- Completion of agent implementation.
- Regression testing required after updates.
- Periodic quality audit of agent performance.

**Trigger Examples:**
- "Verify the new specialist agent implementation."
- "Run the LLM evaluation suite for the SYARCH persona."

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
- Mandatory generation of `eval-report.md`.
- No P0 issues; 100% requirements coverage validated.
- Triggered by user context or meta-orchestrator.
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)

## Best Practices
- Ensure the test environment matches the production configuration exactly.
- Use diverse and edge-case inputs for LLM evaluation.
- Document all manual intervention steps if required.

## Related
- [/agent-development](file:///.agent/workflows/agent-development.md)
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)

---
description: Coordinating meta-workflow that sequentially orchestrates the 7 SDLC
  phases, managing the transition of artifacts, agents, and state.
tags:
- sdlc
- orchestration
- meta-workflow
- factory-management
version: 2.0.0
---


# SDLC Meta-Orchestrator Workflow (v2.0)

**Version:** 1.0.0


**Goal:** Coordinate the 7-phase AI-Engineering SDLC, enforcing phase gates and artifact transitions.

## Trigger Conditions
- When transitioning an Epic or high-level issue through the full factory SDLC phases.

## Trigger Examples:
- "Start the SDLC for AGENT-101"
- "Trigger Phase 2 for the new memory integration task"

## Phases
### Phase 1: Ideation
- **Goal**: Formalize a vague request into a high-fidelity Prototype Brief.
- **Agents**: `project-operations-specialist`, `system-architecture-specialist`
- **Skills**: brainstorming-ideas, researching-first, briefing-prototypes
- **Tools**: search_web, deepwiki
- **Actions**:
    - Execute `/brainstorming-ideas`, `/cluster`, and `/briefing-prototypes`.
    - Validate `knowledge/prototype-brief.md` gate artifact.
    - Run `python scripts/orchestration/verify_phase_1.py`.

### Phase 2: Requirements
- **Goal**: Formalize constraints, functional requirements, and adversarial quality review.
- **Agents**: `project-operations-specialist`, `workflow-quality-specialist`
- **Skills**: writing-prd, slicing-stories, reviewing-requirements
- **Tools**: replace_file_content, write_to_file
- **Actions**:
    - Execute `/writing-prd`, `/eliciting-nfr`, and `/reviewing-requirements`.
    - Validate `knowledge/prd.md` and `knowledge/nfr.md` gate artifacts.
    - Run `python scripts/orchestration/verify_phase_2.py`.

### Phase 3: Architecture
- **Goal**: Establish ADRs, data flow, and API contracts.
- **Agents**: `system-architecture-specialist`, `python-ai-specialist`
- **Skills**: designing-ai-systems, designing-apis
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Execute `/ai-designing-ai-systems`.
    - Validate `knowledge/ai-design.md` gate artifact.

### Phase 4: Build
- **Goal**: Core implementation using stack-specific tools and patterns.
- **Agents**: `python-ai-specialist`, `sap-systems-specialist`, `project-operations-specialist`
- **Skills**: developing-ai-agents, developing-rap-objects, developing-ai-agents
- **Tools**: conda-run, write_to_file
- **Actions**:
    - Route dynamically based on project stack (e.g., `/developing-ai-agents` or `/developing-rap-objects`).
    - Validate `knowledge/walkthrough.md` gate artifact.
    - Run `python scripts/orchestration/verify_phase_4.py`.

### Phase 5: Test & Eval
- **Goal**: Quantitative and qualitative verification using the stack's test runner.
- **Agents**: `workflow-quality-specialist`, `project-operations-specialist`
- **Skills**: testing-agents, verifying-artifact-structures, securing-ai-systems
- **Tools**: run_command
- **Actions**:
    - Route dynamically based on project stack (e.g., `/agent-testing-agents` or `/verifying-artifact-structures`).
    - Validate `knowledge/eval-report.md` gate artifact.
    - Run `python scripts/orchestration/verify_phase_5.py`.

### Phase 6: Deploy
- **Goal**: Version bumping, changelog updates, documentation generation, and env rollout.
- **Agents**: `project-operations-specialist`, `knowledge-operations-specialist`
- **Skills**: committing-releases, generating-documentation
- **Tools**: safe_release.py
- **Actions**:
    - Execute `/committing-releases` and `/generating-documentation`.
    - Validate `knowledge/release-notes.md` and `knowledge/walkthrough.md` gate artifacts.

### Phase 7: Monitor
- **Goal**: Post-deployment health tracking and feeding feedback back to Phase 1.
- **Agents**: `project-operations-specialist`
- **Skills**: logging-and-monitoring
- **Tools**: search_web
- **Actions**:
    - Execute `/logging-and-monitoring`.
    - Validate `knowledge/monitor-report.md` gate artifact.

## Meta-Orchestration Logic:
1. **State Persistence**: The current SDLC phase is tracked in `docs/architecture/sdlc-architecture-spec.json`.
2. **Gatekeeping**: A subagent MUST verify the existence and "READY" status of the current phase's Gate Artifact before initiating the next phase.
3. **Plane Sync**: Each phase transition requires updating the corresponding Child Issue (AGENT-85 to AGENT-91) in Plane to 'Done' and moving the Parent Issue (AGENT-56) forward.


## Best Practices
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.


## Related
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)

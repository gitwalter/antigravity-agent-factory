---
description: Coordinating meta-workflow that sequentially orchestrates the 7 SDLC phases, managing the transition of artifacts, agents, and state.
tags: [sdlc, orchestration, meta-workflow, factory-management]
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
### P1: Ideation (Divergent & Convergent Thinking)
- **Goal**: Formalize a vague request into a high-fidelity Prototype Brief.
- **Workflow**: `/brainstorm`, `/cluster`, `/brief-prototype`
- **Gate Artifact**: `knowledge/prototype-brief.md`
- **Automation**: `python scripts/orchestration/verify_phase_1.py`
- **State Transition**: Moves to **P2: Requirements** upon success.

## 2. Requirements (Convergent)
- **Workflows**: `/write-prd`, `/elicit-nfr`, `/review-requirements`
- **Gate Artifact**: `knowledge/prd.md`, `knowledge/nfr.md`
- **Automation**: `python scripts/orchestration/verify_phase_2.py`
- **Action**: Formalize constraints, functional需求, and adversarial quality review.

## 3. Architecture
- **Workflows**: `/ai-system-design`
- **Gate Artifact**: `knowledge/ai-design.md`
- **Action**: Establish ADRs, data flow, and API contracts.

## 4. Build
- **Routing**: This phase is **Stack-Aware**. The orchestrator queries `stack-configurations.json` based on the active project stack.
- **Workflows**:
  - *Default*: `/feature-development`
  - *Stack-Specific*: Routed dynamically (e.g., `/agent-development` for AI, `/rap-development` for SAP).
- **Gate Artifact**: `knowledge/walkthrough.md`
- **Action**: Core implementation using stack-specific tools and patterns.
- **Automation**: `python scripts/orchestration/verify_phase_4.py`

## 5. Test & Eval
- **Routing**: This phase is **Stack-Aware**.
- **Workflows**:
  - *Default*: `/quality-gate`
  - *Stack-Specific*: Routed dynamically (e.g., `/agent-testing` for Agentic, `/smart-contract-audit` for Web3).
- **Gate Artifact**: `knowledge/eval-report.md`
- **Action**: Quantitative and qualitative verification using the stack's `test_runner`.
- **Automation**: `python scripts/orchestration/verify_phase_5.py`

## 6. Deploy
- **Workflows**: `/release-management`, `/documentation-workflow`
- **Gate Artifact**: `knowledge/release-notes.md`, `knowledge/walkthrough.md`
- **Action**: Version bumping, changelog updates, documentation generation, and environment rollout.

## 7. Monitor
- **Workflows**: `/monitor`
- **Gate Artifact**: `knowledge/monitor-report.md`
- **Action**: Post-deployment health tracking and feeding feedback back to Phase 1.

## Meta-Orchestration Logic:
1. **State Persistence**: The current SDLC phase is tracked in `docs/architecture/sdlc-architecture-spec.json`.
2. **Gatekeeping**: A subagent MUST verify the existence and "READY" status of the current phase's Gate Artifact before initiating the next phase.
3. **Plane Sync**: Each phase transition requires updating the corresponding Child Issue (AGENT-85 to AGENT-91) in Plane to 'Done' and moving the Parent Issue (AGENT-56) forward.

---
description: Standard Feature Delivery Cycle (SFDC) for developing new features from specifications through to completion.
tags: [feature, development, sdlc, sfdc]
version: 2.0.0
---

# Standard Feature Delivery Cycle (SFDC)

**Version:** 2.0.0

The formal process for developing and delivering new features within the Antigravity Agent Factory.

## Trigger Conditions
- New feature request in Plane or via user prompt.
- Transition from Phase 3 (Architecture) to Phase 4 (Build).

**Trigger Examples:**
- "Build a new agent for sentiment analysis."
- "Implement the user profile feature as described in the PRD."
- "Add a new skill for database migration."
- "Execute the feature development workflow for the 'Payment Integration' ticket."

## Phases

The documentation generation process follows a structured path from harvesting context to artifact verification and system induction.

### 1. Requirements & Analysis
- **Goal**: Deep understanding of the PRD and technical constraints.
- **Action**: Review `knowledge/prd.md` and `knowledge/nfr.md`.

### 2. Implementation & Unit Testing
- **Goal**: Safe and axiomatic code generation.
- **Action**: Use the appropriate builder agent (e.g., `python-ai-specialist`).
- **Standard**: Follow the `tdd-cycle.md` where applicable.

### 3. Integration & System Testing
- **Goal**: Verify the feature works within the larger system.
- **Action**: Run integration tests and check for side effects.

### 4. Quality Gate & Documentation
- **Goal**: High-fidelity proof of work and documentation.
- **Action 1**: Invoke `/quality-gate`.
- **Action 2**: Invoke `/documentation-workflow` to generate `walkthrough.md` and update `README.md`.

### 5. Deployment & Release
- **Goal**: Formalized rollout.
- **Action**: Invoke `/release-management`.

### 6. Memory Induction
- **Goal**: Persist new patterns/knowledge.
- **Action**: Update `knowledge-manifest.json` via the `documentation-workflow`.

## Best Practices
- **Phase Gates**: Never skip a phase without explicit justification in the `walkthrough.md`.
- **Relative Links**: All documented links must use root-relative paths.
- **Evidence First**: Use screenshots/logs in documentation.

## Related
- `sdlc-meta-orchestrator.md`
- `documentation-workflow.md`

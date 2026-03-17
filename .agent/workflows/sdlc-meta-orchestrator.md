---
agents:
- system-architecture-specialist
- workflow-quality-specialist
- sap-systems-specialist
- project-operations-specialist
- python-ai-specialist
- knowledge-operations-specialist
blueprints:
- universal
description: Antigravity workflow for sdlc-meta-orchestrator. Standardized for IDX
  Visual Editor.
domain: universal
name: sdlc-meta-orchestrator
steps:
- actions:
  - '**Agents**: `project-operations-specialist`, `system-architecture-specialist`'
  - '**Actions**:'
  - Execute `/brainstorming-ideas`, `/cluster`, and `/briefing-prototypes`.
  - Validate `knowledge/prototype-brief.md` gate artifact.
  - Run `python scripts/orchestration/verify_phase_1.py`.
  agents:
  - project-operations-specialist
  - system-architecture-specialist
  goal: Formalize a vague request into a high-fidelity Prototype Brief.
  name: Ideation
  skills:
  - brainstorming-ideas
  - researching-first
  - briefing-prototypes
  tools:
  - search_web
  - deepwiki
- actions:
  - '**Agents**: `project-operations-specialist`, `workflow-quality-specialist`'
  - '**Actions**:'
  - Execute `/writing-prd`, `/eliciting-nfr`, and `/reviewing-requirements`.
  - Validate `knowledge/prd.md` and `knowledge/nfr.md` gate artifacts.
  - Run `python scripts/orchestration/verify_phase_2.py`.
  agents:
  - project-operations-specialist
  - workflow-quality-specialist
  goal: Formalize constraints, functional requirements, and adversarial quality review.
  name: Requirements
  skills:
  - writing-prd
  - slicing-stories
  - reviewing-requirements
  tools:
  - replace_file_content
  - write_to_file
- actions:
  - '**Agents**: `system-architecture-specialist`, `python-ai-specialist`'
  - '**Actions**:'
  - Execute `/ai-designing-ai-systems`.
  - Validate `knowledge/ai-design.md` gate artifact.
  agents:
  - system-architecture-specialist
  - python-ai-specialist
  goal: Establish ADRs, data flow, and API contracts.
  name: Architecture
  skills:
  - designing-ai-systems
  - designing-apis
  tools:
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `python-ai-specialist`, `sap-systems-specialist`, `project-operations-specialist`'
  - '**Actions**:'
  - Route dynamically based on project stack (e.g., `/developing-ai-agents` or `/developing-rap-objects`).
  - Validate `knowledge/walkthrough.md` gate artifact.
  - Run `python scripts/orchestration/verify_phase_4.py`.
  agents:
  - python-ai-specialist
  - sap-systems-specialist
  - project-operations-specialist
  goal: Core implementation using stack-specific tools and patterns.
  name: Build
  skills:
  - developing-ai-agents
  - developing-rap-objects
  - developing-ai-agents
  tools:
  - conda-run
  - write_to_file
- actions:
  - '**Agents**: `workflow-quality-specialist`, `project-operations-specialist`'
  - '**Actions**:'
  - Route dynamically based on project stack (e.g., `/agent-testing-agents` or `/verifying-artifact-structures`).
  - Validate `knowledge/eval-report.md` gate artifact.
  - Run `python scripts/orchestration/verify_phase_5.py`.
  agents:
  - workflow-quality-specialist
  - project-operations-specialist
  goal: Quantitative and qualitative verification using the stack's test runner.
  name: Test & Eval
  skills:
  - testing-agents
  - verifying-artifact-structures
  - securing-ai-systems
  tools:
  - run_command
- actions:
  - '**Agents**: `project-operations-specialist`, `knowledge-operations-specialist`'
  - '**Actions**:'
  - Execute `/committing-releases` and `/generating-documentation`.
  - Validate `knowledge/release-notes.md` and `knowledge/walkthrough.md` gate artifacts.
  agents:
  - project-operations-specialist
  - knowledge-operations-specialist
  goal: Version bumping, changelog updates, documentation generation, and env rollout.
  name: Deploy
  skills:
  - committing-releases
  - generating-documentation
  tools:
  - safe_release.py
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Execute `/logging-and-monitoring`.
  - Validate `knowledge/monitor-report.md` gate artifact.
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - project-operations-specialist
  goal: Post-deployment health tracking and feeding feedback back to Phase 1.
  name: Monitor
  skills:
  - logging-and-monitoring
  tools:
  - search_web
tags: []
type: sequential
version: 2.0.0
---
# SDLC Meta-Orchestrator Workflow (v2.0)

**Version:** 2.0.0

## Overview
Antigravity workflow for end-to-end SDLC orchestration, coordinating ideation, requirements, architecture, build, test, and deployment. Standardized for IDX Visual Editor.

## Trigger Conditions
- Complex feature request requiring full SDLC lifecycle.
- Strategic project initiative requiring multi-phase orchestration.
- User request: `/sdlc-meta-orchestrator`.

**Trigger Examples:**
- "Orchestrate the development of the 'Enterprise Knowledge Hub' from ideation to deployment."
- "Execute the full SDLC for the new 'Cross-Chain Payment Protocol' module."

## Phases

### 1. Ideation
- **Goal**: Formalize a vague request into a high-fidelity Prototype Brief.
- **Agents**: `project-operations-specialist`, `system-architecture-specialist`
- **Skills**: brainstorming-ideas, researching-first, briefing-prototypes
- **Tools**: search_web, deepwiki
- **Agents**: `project-operations-specialist`, `system-architecture-specialist`
- **Actions**:
- Execute `/brainstorming-ideas`, `/cluster`, and `/briefing-prototypes`.
- Validate `knowledge/prototype-brief.md` gate artifact.
- Run `python scripts/orchestration/verify_phase_1.py`.

### 2. Requirements
- **Goal**: Formalize constraints, functional requirements, and adversarial quality review.
- **Agents**: `project-operations-specialist`, `workflow-quality-specialist`
- **Skills**: writing-prd, slicing-stories, reviewing-requirements
- **Tools**: replace_file_content, write_to_file
- **Agents**: `project-operations-specialist`, `workflow-quality-specialist`
- **Actions**:
- Execute `/writing-prd`, `/eliciting-nfr`, and `/reviewing-requirements`.
- Validate `knowledge/prd.md` and `knowledge/nfr.md` gate artifacts.
- Run `python scripts/orchestration/verify_phase_2.py`.

### 3. Architecture
- **Goal**: Establish ADRs, data flow, and API contracts.
- **Agents**: `system-architecture-specialist`, `python-ai-specialist`
- **Skills**: designing-ai-systems, designing-apis
- **Tools**: mcp_memory_search_nodes
- **Agents**: `system-architecture-specialist`, `python-ai-specialist`
- **Actions**:
- Execute `/ai-designing-ai-systems`.
- Validate `knowledge/ai-design.md` gate artifact.

### 4. Build
- **Goal**: Core implementation using stack-specific tools and patterns.
- **Agents**: `python-ai-specialist`, `sap-systems-specialist`, `project-operations-specialist`
- **Skills**: developing-ai-agents, developing-rap-objects, developing-ai-agents
- **Tools**: conda-run, write_to_file
- **Agents**: `python-ai-specialist`, `sap-systems-specialist`, `project-operations-specialist`
- **Actions**:
- Route dynamically based on project stack (e.g., `/developing-ai-agents` or `/developing-rap-objects`).
- Validate `knowledge/walkthrough.md` gate artifact.
- Run `python scripts/orchestration/verify_phase_4.py`.

### 5. Test & Eval
- **Goal**: Quantitative and qualitative verification using the stack's test runner.
- **Agents**: `workflow-quality-specialist`, `project-operations-specialist`
- **Skills**: testing-agents, verifying-artifact-structures, securing-ai-systems
- **Tools**: run_command
- **Agents**: `workflow-quality-specialist`, `project-operations-specialist`
- **Actions**:
- Route dynamically based on project stack (e.g., `/agent-testing-agents` or `/verifying-artifact-structures`).
- Validate `knowledge/eval-report.md` gate artifact.
- Run `python scripts/orchestration/verify_phase_5.py`.

### 6. Deploy
- **Goal**: Version bumping, changelog updates, documentation generation, and env rollout.
- **Agents**: `project-operations-specialist`, `knowledge-operations-specialist`
- **Skills**: committing-releases, generating-documentation
- **Tools**: safe_release.py
- **Agents**: `project-operations-specialist`, `knowledge-operations-specialist`
- **Actions**:
- Execute `/committing-releases` and `/generating-documentation`.
- Validate `knowledge/release-notes.md` and `knowledge/walkthrough.md` gate artifacts.

### 7. Monitor
- **Goal**: Post-deployment health tracking and feeding feedback back to Phase 1.
- **Agents**: `project-operations-specialist`
- **Skills**: logging-and-monitoring
- **Tools**: search_web
- **Agents**: `project-operations-specialist`
- **Actions**:
- Execute `/logging-and-monitoring`.
- Validate `knowledge/monitor-report.md` gate artifact.
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)

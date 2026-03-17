---
agents:
- workflow-quality-specialist
- system-architecture-specialist
- project-operations-specialist
- python-ai-specialist
blueprints:
- universal
description: Antigravity workflow for sdlc-usage-guide. Standardized for IDX Visual
  Editor.
domain: universal
name: sdlc-usage-guide
steps:
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Identify a high-value opportunity.
  - Create a [Prototype Brief](file:///knowledge/prototype-brief.md).
  agents:
  - project-operations-specialist
  goal: Research potential opportunities and formalize the one with the highest ROI.
  name: Ideation (`/briefing-prototypes`)
  skills:
  - brainstorming-ideas
  - researching-first
  tools:
  - search_web
  - deepwiki
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Create the [PRD](file:///knowledge/prd.md).
  - Run `/eliciting-nfr` for technical constraints.
  agents:
  - project-operations-specialist
  goal: Breakdown the Brief into functional requirements and user stories.
  name: Requirements (`/writing-prd`)
  skills:
  - generating-documentation
  tools:
  - write_to_file
- actions:
  - '**Agents**: `system-architecture-specialist`'
  - '**Actions**:'
  - Create the [AI Design Document](file:///knowledge/ai-design.md) with C4 diagrams.
  agents:
  - system-architecture-specialist
  goal: Design the system architecture based on the PRD.
  name: Architecture (`/ai-designing-ai-systems`)
  skills:
  - designing-ai-systems
  tools:
  - view_file
  - write_to_file
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Implement the feature using builder agents and TDD.
  - Generate [Walkthrough](file:///knowledge/walkthrough.md).
  agents:
  - python-ai-specialist
  goal: Axiomatic implementation of the feature.
  name: Build (`/developing-ai-agents`)
  skills:
  - developing-ai-agents
  - analyzing-code
  tools:
  - run_command
  - replace_file_content
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Run unit, integration, and LLM evaluations.
  - Produce [Evaluation Report](file:///knowledge/eval-report.md).
  agents:
  - workflow-quality-specialist
  goal: Verify correctness and quality.
  name: Test & Eval (`/agent-testing-agents`)
  skills:
  - testing-agents
  tools:
  - pytest
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Merge, tag, and update `CHANGELOG.md`.
  agents:
  - project-operations-specialist
  goal: Version control and formal release.
  name: Deploy (`/committing-releases`)
  skills:
  - governing-repositories
  tools:
  - git
  - committing-releases
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Gather production metrics.
  - Generate [Monitor Report](file:///knowledge/monitor-report.md).
  agents:
  - project-operations-specialist
  goal: Close the feedback loop.
  name: Monitor (`/logging-and-monitoring`)
  skills:
  - logging-and-monitoring
  tools:
  - log_analysis
tags: []
type: sequential
version: 2.0.0
---
# Antigravity SDLC Usage Guide

**Version:** 1.0.0

## Overview
Antigravity workflow serving as a comprehensive guide for utilizing the standard SDLC phases in the Agent Factory. Standardized for IDX Visual Editor.

## Trigger Conditions
- User seeking guidance on how to follow the project's SDLC.
- New team members onboarding or learning the workflow standards.
- User request: `/sdlc-usage-guide`.

**Trigger Examples:**
- "How do I use the Antigravity SDLC for my new feature?"
- "Provide a guide on the standard phases of our development lifecycle."

## Phases

### 1. Ideation (`/briefing-prototypes`)
- **Goal**: Research potential opportunities and formalize the one with the highest ROI.
- **Agents**: `project-operations-specialist`
- **Skills**: brainstorming-ideas, researching-first
- **Tools**: search_web, deepwiki
- **Agents**: `project-operations-specialist`
- **Actions**:
- Identify a high-value opportunity.
- Create a [Prototype Brief](file:///knowledge/prototype-brief.md).

### 2. Requirements (`/writing-prd`)
- **Goal**: Breakdown the Brief into functional requirements and user stories.
- **Agents**: `project-operations-specialist`
- **Skills**: generating-documentation
- **Tools**: write_to_file
- **Agents**: `project-operations-specialist`
- **Actions**:
- Create the [PRD](file:///knowledge/prd.md).
- Run `/eliciting-nfr` for technical constraints.

### 3. Architecture (`/ai-designing-ai-systems`)
- **Goal**: Design the system architecture based on the PRD.
- **Agents**: `system-architecture-specialist`
- **Skills**: designing-ai-systems
- **Tools**: view_file, write_to_file
- **Agents**: `system-architecture-specialist`
- **Actions**:
- Create the [AI Design Document](file:///knowledge/ai-design.md) with C4 diagrams.

### 4. Build (`/developing-ai-agents`)
- **Goal**: Axiomatic implementation of the feature.
- **Agents**: `python-ai-specialist`
- **Skills**: developing-ai-agents, analyzing-code
- **Tools**: run_command, replace_file_content
- **Agents**: `python-ai-specialist`
- **Actions**:
- Implement the feature using builder agents and TDD.
- Generate [Walkthrough](file:///knowledge/walkthrough.md).

### 5. Test & Eval (`/agent-testing-agents`)
- **Goal**: Verify correctness and quality.
- **Agents**: `workflow-quality-specialist`
- **Skills**: testing-agents
- **Tools**: pytest
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Run unit, integration, and LLM evaluations.
- Produce [Evaluation Report](file:///knowledge/eval-report.md).

### 6. Deploy (`/committing-releases`)
- **Goal**: Version control and formal release.
- **Agents**: `project-operations-specialist`
- **Skills**: governing-repositories
- **Tools**: git, committing-releases
- **Agents**: `project-operations-specialist`
- **Actions**:
- Merge, tag, and update `CHANGELOG.md`.

### 7. Monitor (`/logging-and-monitoring`)
- **Goal**: Close the feedback loop.
- **Agents**: `project-operations-specialist`
- **Skills**: logging-and-monitoring
- **Tools**: log_analysis
- **Agents**: `project-operations-specialist`
- **Actions**:
- Gather production metrics.
- Generate [Monitor Report](file:///knowledge/monitor-report.md).

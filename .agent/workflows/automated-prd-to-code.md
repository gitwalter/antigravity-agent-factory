---
name: automated-prd-to-code
type: sequential
version: 2.0.0
description: Autonomous bridge that transforms a verified Agentic PRD into structural
  boilerplate and core implementation logic. Use when a READY prd.md exists and you
  want to bootstrap the implementation phase.
agents:
- system-architecture-specialist
- python-ai-specialist
steps:
- name: Requirements Parsing
  goal: Extract structured configuration from knowledge/prd.md.
  agents:
  - system-architecture-specialist
  skills:
  - prd-parsing-logic
  tools:
  - prd_to_code_bridge.py
  actions:
  - Run `prd_to_code_bridge.py --prd knowledge/prd.md` to parse requirements.
- name: Structural Generation
  goal: Create the project scaffolding and factory-standard directories.
  agents:
  - system-architecture-specialist
  skills:
  - automated-code-generation
  tools:
  - ProjectGenerator
  actions:
  - Invoke `ProjectGenerator` via the bridge script to create .agent/, workflows/,
    and scripts/.
- name: Logic Implementation
  goal: Generate initial implementation files based on PRD acceptance criteria.
  agents:
  - python-ai-specialist
  skills:
  - automated-code-generation
  tools:
  - write_to_file
  actions:
  - Populate src/ or scripts/ with implementation stubs derived from Story JSON blocks.
- name: Verification
  goal: Validate the generated structure and initial code.
  agents:
  - workflow-quality-specialist
  skills:
  - testing-agents
  tools:
  - pytest-cli
  actions:
  - Run linting and basic structure checks on generated assets.
---
# Automated PRD to Code Bridge

**Version:** 1.0.0

## Overview
This workflow implements an autonomous bridge that transforms a verified PRD into structural boilerplate and core implementation logic, ensuring alignment with Factory Layer 0-4 standards.

## Trigger Conditions
- Verified PRD exists in `knowledge/prd.md` (READY status).
- User request: `/automated-prd-to-code`.

**Trigger Examples:**
- "Run the bridge on our new PRD."
- "Execute automated-prd-to-code for the dashboard feature."

## Phases

### 1. Requirements Parsing
- **Goal**: Extract structured configuration from `knowledge/prd.md`.
- **Agents**: `system-architecture-specialist`
- **Skills**: `prd-parsing-logic`
- **Tools**: `prd_to_code_bridge.py`
- **Actions**:
  - Run `python scripts/orchestration/prd_to_code_bridge.py --prd knowledge/prd.md` to parse requirements and prepare the configuration.

### 2. Structural Generation
- **Goal**: Create the project scaffolding and factory-standard directories.
- **Agents**: `system-architecture-specialist`
- **Skills**: `automated-code-generation`
- **Tools**: `ProjectGenerator`
- **Actions**:
  - The bridge script invokes `ProjectGenerator` to establish the `.agent/`, `workflows/`, `scripts/`, and `knowledge/` directories.

### 3. Logic Implementation
- **Goal**: Generate initial implementation files based on PRD acceptance criteria.
- **Agents**: `python-ai-specialist`
- **Skills**: `automated-code-generation`
- **Tools**: `write_to_file`
- **Actions**:
  - For each user story extracted, generate an implementation stub in `src/` or `scripts/` following the acceptance criteria.

### 4. Verification
- **Goal**: Validate the generated structure and initial code.
- **Agents**: `workflow-quality-specialist`
- **Skills**: `testing-agents`
- **Tools**: `pytest-cli`
- **Actions**:
  - Verify that all generated files pass basic linting and structural checks.

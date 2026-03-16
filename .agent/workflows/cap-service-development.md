---
agents:
- workflow-quality-specialist
- project-operations-specialist
- python-ai-specialist
blueprints:
- universal
description: Antigravity workflow for cap-service-development. Standardized for IDX
  Visual Editor.
domain: universal
name: cap-service-development
steps:
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Create entity definitions and add aspects.
  agents:
  - python-ai-specialist
  goal: Design the application data model using CDS entity definitions and aspects.
  name: Data Modeling & Entity Definition
  skills:
  - modeling-cds
  - analyzing-code
  tools:
  - write_to_file
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Create service definitions and implement event handlers.
  agents:
  - python-ai-specialist
  goal: Implement service logic and event handlers for business logic.
  name: Service Definition & Handler Implementation
  skills:
  - modeling-cds
  tools:
  - write_to_file
- actions:
  - '**Agents**: `workflow-quality-specialist`, `project-operations-specialist`'
  - '**Actions**:'
  - Perform unit and integration testing-agents.
  - Add UI annotations and create Fiori app.
  agents:
  - workflow-quality-specialist
  - project-operations-specialist
  goal: Add UI annotations, create the Fiori app, and perform tests.
  name: UI & Integration Testing
  skills:
  - developing-fiori-apps
  - testing-agents
  tools:
  - run_tests.py
  - fiori-tools-cli
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Configure MTA and build/deploy.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - project-operations-specialist
  goal: Configure MTA and deploy the application to SAP BTP.
  name: BTP Configuration & Deployment
  skills:
  - deploying-to-btp
  - committing-releases
  tools:
  - mta-tool
  - cf-cli
tags: []
type: sequential
version: 1.0.0
---

# CAP Service Development

**Version:** 1.0.0

## Overview
Antigravity workflow for CAP service development. Standardized for IDX Visual Editor.

## Trigger Conditions
- Requirement for a new SAP CAP microservice.
- Modification of existing CDS entity definitions or service logic.
- User request: `/cap-service-development`.

**Trigger Examples:**
- "Develop a new CAP service for order management."
- "Update the entity model in the sales service."

## Phases

### 1. Data Modeling & Entity Definition
- **Goal**: Design the application data model using CDS entity definitions and aspects.
- **Agents**: `python-ai-specialist`
- **Skills**: modeling-cds, analyzing-code
- **Tools**: write_to_file
- **Agents**: `python-ai-specialist`
- **Actions**:
- Create entity definitions and add aspects.

### 2. Service Definition & Handler Implementation
- **Goal**: Implement service logic and event handlers for business logic.
- **Agents**: `python-ai-specialist`
- **Skills**: modeling-cds
- **Tools**: write_to_file
- **Agents**: `python-ai-specialist`
- **Actions**:
- Create service definitions and implement event handlers.

### 3. UI & Integration Testing
- **Goal**: Add UI annotations, create the Fiori app, and perform tests.
- **Agents**: `workflow-quality-specialist`, `project-operations-specialist`
- **Skills**: developing-fiori-apps, testing-agents
- **Tools**: run_tests.py, fiori-tools-cli
- **Agents**: `workflow-quality-specialist`, `project-operations-specialist`
- **Actions**:
- Perform unit and integration testing-agents.
- Add UI annotations and create Fiori app.

### 4. BTP Configuration & Deployment
- **Goal**: Configure MTA and deploy the application to SAP BTP.
- **Agents**: `project-operations-specialist`
- **Skills**: deploying-to-btp, committing-releases
- **Tools**: mta-tool, cf-cli
- **Agents**: `project-operations-specialist`
- **Actions**:
- Configure MTA and build/deploy.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)

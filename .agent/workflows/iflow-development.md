---
agents:
- system-architecture-specialist
- workflow-quality-specialist
- project-operations-specialist
- python-ai-specialist
blueprints:
- universal
description: Antigravity workflow for iflow-development. Standardized for IDX Visual
  Editor.
domain: universal
name: iflow-development
steps:
- actions:
  - '**Agents**: `system-architecture-specialist`'
  - '**Actions**:'
  - Identify systems (S/4HANA, Salesforce, etc.) and communication protocols (SOAP,
    REST, OData).
  agents:
  - system-architecture-specialist
  goal: Define the source and target systems and the integration pattern.
  name: Integration Design
  skills:
  - designing-ai-systems
  tools:
  - search_web
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Create iFlow and add adapters (Request-Reply, Content Modifier).
  - Model XML/JSON transformations.
  agents:
  - python-ai-specialist
  goal: Create the iFlow and model the message flow and transformations.
  name: iFlow Modeling
  skills:
  - iflow-development
  tools:
  - write_to_file
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Write Groovy scripts for custom header/body manipulation.
  agents:
  - python-ai-specialist
  goal: Implement complex logic using Groovy or custom scripts.
  name: Groovy Scripting & Logic
  skills:
  - iflow-development
  tools:
  - write_to_file
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Test iFlow with sample payloads and verify transformations.
  agents:
  - workflow-quality-specialist
  goal: Validate the iFlow in the simulation environment and CPI tenant.
  name: Verification & Testing
  skills:
  - testing-agents
  tools:
  - run_tests.py
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Deploy iFlow and configure message logging.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - project-operations-specialist
  goal: Deploy the iFlow to production and set up logging-and-monitoring.
  name: Deployment & Monitoring
  skills:
  - committing-releases
  - logging-and-monitoring
  tools:
  - cpi-dashboard
  - grafana
tags: []
type: sequential
version: 1.0.0
---

# iFlow Development

**Version:** 1.0.0

## Overview
Antigravity workflow for SAP Integration Suite (CPI) iFlow development. Standardized for IDX Visual Editor.

## Trigger Conditions
- Need to integrate different software systems (e.g., S/4HANA to Salesforce).
- Requirement for a complex message transformation or routing logic.
- User request: `/iflow-development`.

**Trigger Examples:**
- "Develop an iFlow to synchronize customer data from S/4HANA to Salesforce."
- "Model a message transformation for converting XML orders to JSON format."

## Phases

### 1. Integration Design
- **Goal**: Define the source and target systems and the integration pattern.
- **Agents**: `system-architecture-specialist`
- **Skills**: designing-ai-systems
- **Tools**: search_web
- **Agents**: `system-architecture-specialist`
- **Actions**:
- Identify systems (S/4HANA, Salesforce, etc.) and communication protocols (SOAP, REST, OData).

### 2. iFlow Modeling
- **Goal**: Create the iFlow and model the message flow and transformations.
- **Agents**: `python-ai-specialist`
- **Skills**: iflow-development
- **Tools**: write_to_file
- **Agents**: `python-ai-specialist`
- **Actions**:
- Create iFlow and add adapters (Request-Reply, Content Modifier).
- Model XML/JSON transformations.

### 3. Groovy Scripting & Logic
- **Goal**: Implement complex logic using Groovy or custom scripts.
- **Agents**: `python-ai-specialist`
- **Skills**: iflow-development
- **Tools**: write_to_file
- **Agents**: `python-ai-specialist`
- **Actions**:
- Write Groovy scripts for custom header/body manipulation.

### 4. Verification & Testing
- **Goal**: Validate the iFlow in the simulation environment and CPI tenant.
- **Agents**: `workflow-quality-specialist`
- **Skills**: testing-agents
- **Tools**: run_tests.py
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Test iFlow with sample payloads and verify transformations.

### 5. Deployment & Monitoring
- **Goal**: Deploy the iFlow to production and set up logging-and-monitoring.
- **Agents**: `project-operations-specialist`
- **Skills**: committing-releases, logging-and-monitoring
- **Tools**: cpi-dashboard, grafana
- **Agents**: `project-operations-specialist`
- **Actions**:
- Deploy iFlow and configure message logging.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)

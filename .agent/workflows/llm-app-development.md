---
agents:
- workflow-quality-specialist
- system-architecture-specialist
- project-operations-specialist
- python-ai-specialist
blueprints:
- universal
description: Antigravity workflow for llm-app-development. Standardized for IDX Visual
  Editor.
domain: universal
name: llm-app-development
steps:
- actions:
  - '**Agents**: `system-architecture-specialist`, `project-operations-specialist`'
  - '**Actions**:'
  - Gather functional and non-functional requirements.
  - Select the architecture (RAG, Agentic, Chain).
  - Set up the project structure and LangChain environment.
  agents:
  - system-architecture-specialist
  - project-operations-specialist
  goal: Define the LLM application scope and choose the optimal orchestration stack
    (LangChain, LangGraph, etc.).
  name: Requirements & Architecture Selection
  skills:
  - designing-ai-systems
  - brainstorming-ideas
  tools:
  - search_web
  - deepwiki
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Implement core functionality and design the state graph.
  - Implement nodes and add checkpointing for persistence.
  agents:
  - python-ai-specialist
  goal: Build the core reasoning logic, state graphs, and node functions.
  name: Implementation & Logic Definition
  skills:
  - developing-ai-agents
  - designing-apis
  tools:
  - conda-run
  - write_to_file
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Create evaluation datasets and run automated evals.
  - Iterate on prompts and logic based on evaluation results.
  agents:
  - workflow-quality-specialist
  goal: Rigorously test the LLM performance using quantitative and qualitative metrics.
  name: Evaluation & Refinement
  skills:
  - testing-agents
  - evaluating-llms
  tools:
  - run_tests.py
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Implement input validation and output filtering.
  - Configure guardrails (e.g., NeMo Guardrails, custom filters).
  agents:
  - workflow-quality-specialist
  goal: Implement safety measures, input validation, and output filtering.
  name: Security & Guardrails
  skills:
  - securing-ai-systems
  tools:
  - view_file
  - replace_file_content
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Prepare for deployment and roll out to production.
  - Set up logging-and-monitoring and implement cost tracking.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - project-operations-specialist
  goal: Deploy the application and establish logging-and-monitoring for performance
    and cost.
  name: Deployment & Operational Readiness
  skills:
  - committing-releases
  - logging-and-monitoring
  tools:
  - safe_release.py
tags: []
type: sequential
version: 1.0.0
---

# LLM App Development

**Version:** 1.0.0

## Overview
Antigravity workflow for developing LLM-powered applications. Standardized for IDX Visual Editor.

## Trigger Conditions
- Requirement for building an application using Large Language Models (LLMs).
- Need to implement RAG, Agentic, or Chain-based architectures.
- User request: `/llm-app-development`.

**Trigger Examples:**
- "Develop a RAG-based application for querying internal documentation."
- "Implement an agentic assistant for automating customer support tasks."

## Phases

### 1. Requirements & Architecture Selection
- **Goal**: Define the LLM application scope and choose the optimal orchestration stack (LangChain, LangGraph, etc.).
- **Agents**: `system-architecture-specialist`, `project-operations-specialist`
- **Skills**: designing-ai-systems, brainstorming-ideas
- **Tools**: search_web, deepwiki
- **Agents**: `system-architecture-specialist`, `project-operations-specialist`
- **Actions**:
- Gather functional and non-functional requirements.
- Select the architecture (RAG, Agentic, Chain).
- Set up the project structure and LangChain environment.

### 2. Implementation & Logic Definition
- **Goal**: Build the core reasoning logic, state graphs, and node functions.
- **Agents**: `python-ai-specialist`
- **Skills**: developing-ai-agents, designing-apis
- **Tools**: conda-run, write_to_file
- **Agents**: `python-ai-specialist`
- **Actions**:
- Implement core functionality and design the state graph.
- Implement nodes and add checkpointing for persistence.

### 3. Evaluation & Refinement
- **Goal**: Rigorously test the LLM performance using quantitative and qualitative metrics.
- **Agents**: `workflow-quality-specialist`
- **Skills**: testing-agents, evaluating-llms
- **Tools**: run_tests.py
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Create evaluation datasets and run automated evals.
- Iterate on prompts and logic based on evaluation results.

### 4. Security & Guardrails
- **Goal**: Implement safety measures, input validation, and output filtering.
- **Agents**: `workflow-quality-specialist`
- **Skills**: securing-ai-systems
- **Tools**: view_file, replace_file_content
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Implement input validation and output filtering.
- Configure guardrails (e.g., NeMo Guardrails, custom filters).

### 5. Deployment & Operational Readiness
- **Goal**: Deploy the application and establish logging-and-monitoring for performance and cost.
- **Agents**: `project-operations-specialist`
- **Skills**: committing-releases, logging-and-monitoring
- **Tools**: safe_release.py
- **Agents**: `project-operations-specialist`
- **Actions**:
- Prepare for deployment and roll out to production.
- Set up logging-and-monitoring and implement cost tracking.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)

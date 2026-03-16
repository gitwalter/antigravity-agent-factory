---
description: Comprehensive workflow for developing production-ready LLM applications
  from prototype to production, including evalu...
version: 1.0.0
tags:
- llm
- app
- development
- standardized
---


# Llm App Development

Comprehensive workflow for developing production-ready LLM applications from prototype to production, including evaluation, security, and logging-and-monitoring.

**Version:** 1.0.0
**Created:** 2026-02-09
**Agent:** template-creator

> **Note:** Directory paths referenced in this workflow ({directories.knowledge}/, {directories.skills}/, {directories.patterns}/, etc.) are configurable via `{directories.config}/settings.json`.

## Trigger Conditions

This workflow is activated when:

- User requests "create LLM app", "build chatbot", "RAG application"
- User mentions "LangChain", "LangGraph", "LLM application"
- User requests "AI assistant" or "conversational AI"
- User asks to "build AI-powered feature"

**Trigger Examples:**
- "Create a RAG application for document Q&A"
- "Build a chatbot using LangChain"
- "Develop an LLM-powered assistant"
- "Create an AI application with evaluation"

## Phases

### Phase 1: Requirements & Architecture Selection
- **Goal**: Define the LLM application scope and choose the optimal orchestration stack (LangChain, LangGraph, etc.).
- **Agents**: `system-architecture-specialist`, `project-operations-specialist`
- **Skills**: designing-ai-systems, brainstorming-ideas
- **Tools**: search_web, deepwiki
- **Actions**:
    - Gather functional and non-functional requirements.
    - Select the architecture (RAG, Agentic, Chain).
    - Set up the project structure and LangChain environment.

### Phase 2: Implementation & Logic Definition
- **Goal**: Build the core reasoning logic, state graphs, and node functions.
- **Agents**: `python-ai-specialist`
- **Skills**: developing-ai-agents, designing-apis
- **Tools**: conda-run, write_to_file
- **Actions**:
    - Implement core functionality and design the state graph.
    - Implement nodes and add checkpointing for persistence.

### Phase 3: Evaluation & Refinement
- **Goal**: Rigorously test the LLM performance using quantitative and qualitative metrics.
- **Agents**: `workflow-quality-specialist`
- **Skills**: testing-agents, evaluating-llms
- **Tools**: run_tests.py
- **Actions**:
    - Create evaluation datasets and run automated evals.
    - Iterate on prompts and logic based on evaluation results.

### Phase 4: Security & Guardrails
- **Goal**: Implement safety measures, input validation, and output filtering.
- **Agents**: `workflow-quality-specialist`
- **Skills**: securing-ai-systems
- **Tools**: view_file, replace_file_content
- **Actions**:
    - Implement input validation and output filtering.
    - Configure guardrails (e.g., NeMo Guardrails, custom filters).

### Phase 5: Deployment & Operational Readiness
- **Goal**: Deploy the application and establish logging-and-monitoring for performance and cost.
- **Agents**: `project-operations-specialist`
- **Skills**: committing-releases, logging-and-monitoring
- **Tools**: safe_release.py
- **Actions**:
    - Prepare for deployment and roll out to production.
    - Set up logging-and-monitoring and implement cost tracking.


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...


## Trigger Examples
- "Execute this workflow."


## Best Practices
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.


## Related
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)

# Rule: Workflow Execution

## Context
Rules for creating, extending, and executing workflows in `.agent/workflows/`.

## Requirements
- **Schema Adherence**: MUST follow `schemas/workflow.schema.json`.
- **Workflow Primacy**: All major system operations MUST be orchestrated by a designated workflow.
- **Phased Execution**:
    - Break workflows into logical, verifiable phases.
    - Define clear entry and exit criteria for each phase.
- **Automation (Turbo)**:
    - Use `// turbo` for safe, repetitive commands.
    - Use `// turbo-all` ONLY for highly standardized, verified automation paths.
- **Complex Logic**: For workflows with >3 dependent steps, use the `sequential-thinking` MCP to validate the execution path.
- **PMS Integration**:
    - **Intelligence over Polling**: Do NOT poll for Plane states. Refer to the standard mapping (`Todo`, `In Progress`, `Done`, `Backlog`, `Triage`).
    - **Closure Requirement**: Every workflow execution MUST terminate with a PMS status update (typically to `Done`) upon successful verification.
    - **Solution Documentation**: Every completed issue MUST include a detailed "Technical Implementation" or "Solution Summary" in the description, explaining *how* the task was solved for full transparency.
    - **Context Retrieval**: Use `scripts/pms/manager.py` for all PMS interactions to ensure consistency.

## Execution Standards
- **Supervisor Role**: Every workflow MUST have a designated Supervisor agent (e.g., MSO).
- **Quality Gates**: Implement quality gates between phases to prevent error propagation.
- **Recovery**: Define fallback procedures for phase failures.

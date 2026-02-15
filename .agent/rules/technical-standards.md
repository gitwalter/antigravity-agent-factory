# Rule: Technical Standards

## Context
Enforces technical best practices and platform-specific reliability standards.

## 1. Execution Environment
- **Python**: ALWAYS use `python` for all Python-based tool calls. NEVER assume the system python is correct.
- **NEVER** modify `.cursorrules` (use `.agent/rules/` instead).
- **Shell**: Consistently use PowerShell syntax.
- **Windows Reliability**:
    - Use `;` for command chaining.
- **Tool Priority**:
    - **Local-First (P0)**: If a command-line tool (`git`, `gh`, `python`) fulfills the requirement, use it.
    - **MCP (P1)**: Use MCP only if local tools are insufficient, missing, or for bridging external services (Drive, Gmail).
- **MCP Usage**:
    - PRIORITIZE `memory` and context-specific MCPs (Drive, Gmail, etc.) for all grounding operations.
    - Use `sequential-thinking` for complex problem-solving (>3 steps).
    - **Dynamic Management**:
        - If an MCP is `disabled: true` in `mcp_config.json` but required for a task, the agent MUST notify the user or propose selective activation.
        - **Resource Guardrail**: Maintain a "Lean Environment". Avoid having more than 5-7 specialist MCPs active simultaneously.
        - **Auto-Cleanup**: If an agent activates an MCP for a specific task, it SHOULD propose deactivating it upon task completion to conserve resources.

## Code Quality
- **Verifiability (A1)**: Every code change SHOULD be accompanied by proof of testing (terminal output or file snapshots).
- **Transparency (A3)**: Comment complex logic; explain rationale for non-obvious choices.
- **Non-Harm (A4)**: Verify destructive operations (PowerShell `Remove-Item`) before execution.

## File & Path Management
- **Broken Links**: DELETE links if the target file does not exist. DO NOT create stub files.
- **Normalization**: Normalize all paths relative to the root `antigravity-agent-factory`.

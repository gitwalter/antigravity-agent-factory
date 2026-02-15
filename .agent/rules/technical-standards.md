# Rule: Technical Standards

## Context
Enforces technical best practices and platform-specific reliability standards.

## 1. Execution Environment
- **Python**: ALWAYS use `python` for all Python-based tool calls. NEVER assume the system python is correct.
- **NEVER** modify `.cursorrules` (use `.agent/rules/` instead).
- **Shell**: Consistently use PowerShell syntax.
- **Windows Reliability**:
    - Use `;` for command chaining.
    - Resolve absolute paths dynamically from configuration.
    - Handle UTF-8 encoding for input/output redirection.

## Code Quality
- **Verifiability (A1)**: Every code change SHOULD be accompanied by proof of testing (terminal output or file snapshots).
- **Transparency (A3)**: Comment complex logic; explain rationale for non-obvious choices.
- **Non-Harm (A4)**: Verify destructive operations (PowerShell `Remove-Item`) before execution.

## File & Path Management
- **Broken Links**: DELETE links if the target file does not exist. DO NOT create stub files.
- **Normalization**: Normalize all paths relative to the root `antigravity-agent-factory`.

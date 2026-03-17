# Rule: Temporary File Governance

## Context
Governs the creation, location, and lifecycle of temporary files and scripts used during the development and operational cycle.

## Requirements

### 1. Location
- **NEVER** create temporary files, scratch scripts, or intermediate data files in the root directory.
- **ALWAYS** use the `tmp/` directory for all temporary assets.

### 2. Lifecycle
- **Cleanup**: All temporary files MUST be deleted immediately after their purpose is served.
- **Persistence**: Do not commit files in `tmp/` to version control (ensure they are Git-ignored).

### 3. Generalization & Reusability
- **Tool-First Mindset**: Before creating a "one-off" scratch script, evaluate if the logic is reusable.
- **Skill Induction**: If a script performs a task that will likely be repeated (e.g., listing metadata, associating entities), refactor it into a permanent tool within a relevant skill's `scripts/` directory.
- **Standardization**: Reusable tools must follow the factory's standards (e.g., using `conda run`, absolute paths, and structured logging/output).

### 4. Enforcement & Self-Correction
- **Pre-Check**: Before running any temporary script, verify it is in `tmp/`.
- **Auto-Cleanup**: Include cleanup logic within temporary scripts (e.g., `atexit` or `try/finally`).
- **Audit**: Run `python scripts/maintenance/enforce_tmp_usage.py` as part of the verification phase to ensure no artifacts were leaked to the root.

## Anti-Patterns
- Leaving `.py`, `.json`, or `.log` files in the root directory after a task.
- Creating duplicate logic in multiple scratch scripts instead of centralizing in a skill-based tool.
- Forgetting to delete temporary files, cluttering the workspace.

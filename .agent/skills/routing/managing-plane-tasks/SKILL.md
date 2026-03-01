---
name: managing-plane-tasks
description: Native management of Plane PMS issues and states using direct backend access via Django ORM.
type: skill
version: 1.0.0
category: routing
agents:
- python-ai-specialist
- ai-app-developer
- master-system-orchestrator
knowledge:
- plane-integration.json
- api-integration-patterns.json
tools:
- run_command
- manager.py
related_skills:
- orchestrating-mcp
- generating-skills
templates:
- ["none"]
axioms:
  A1_verifiability: "Uses direct container execution for verifiable state changes."
  A3_transparency: "Base64 encoding ensures transparent shell-safe payloads."
  A5_evolutionary_design: "Bypasses unstable API layers for stable, direct management."
---

# Native Plane Management

This skill enables agents to manage projects, issues, and states in a local Plane PMS deployment by executing commands directly against the Plane API container. This bypasses the need for an external MCP server and provides 100% reliability.

## When to Use
- When you need to create, update, or track tasks in the Plane Project Management System.
- When existing MCP servers for Plane are unavailable or unauthorized.
- When performing automated project lifecycle updates during a release or development cycle.

## Prerequisites
- **Local Plane Stack**: Plane must be running in Docker (`docker ps` should show `plane-api`).
- **Conda Environment**: The `D:\Anaconda\envs\cursor-factory` environment must be accessible.
- **Project Context**: Project ID and Identifier (e.g., `AGENT`) must be known.

## Process
Follow these procedures to interact with the Plane PMS native integration via shell commands.

### 1. Listing Issues & Filtering
To list components, prefer JSON output for programmatic parsing. **You can combine filters for high-precision discovery**:
```powershell
# List all issues in AGENT project
conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py list --json

# Filter by state (e.g., Backlog, Todo, In Progress, Done, Cancelled)
conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py list --state "In Progress" --json

# Filter by cycle/sprint
conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py list --cycle "sprint 002" --json

# Filter by module
conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py list --module "rag system" --json

# Combined filter: Done issues in sprint 002
conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py list --cycle "sprint 002" --state "Done" --json

# List all projects
conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py projects --json

# List all modules in the project
conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py modules --json
```

### 3. Creating Professional Issues
Always include **Cycle**, **Module**, **Assignee**, **Priority**, and **Dates** for factory-grade orchestration. Use `members`, `labels`, and `modules` commands to find valid metadata values.

**Standard Command:**
```powershell
conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py create `
  --name "FEATURE: Component Name" `
  --description "<b>Description:</b> Detailed HTML or text..." `
  --priority "high" `
  --state "Todo" `
  --cycle "sprint 003" `
  --module "component" `
  --assignee "email@example.com" `
  --start-date "2026-03-01" `
  --target-date "2026-03-08" `
  --estimate 5 `
  --labels feature cleanup
```

**Metadata Lookup:**
```powershell
# Find valid assignees
conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py members --json

# Find valid labels (case-sensitive!)
conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py labels --json

# Find valid modules
conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py modules --json
```

### 4. Updating Issues
Use for status changes or appending technical updates:
```powershell
# Change state
conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py update AGENT-5 --state "Done"

# Append technical update (adds timestamp and separator)
conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py update AGENT-5 --description "Logic verified with tests." --append
```

## Best Commands
- **Professional Creation**: Use all metadata flags (`--cycle`, `--module`, etc.) to ensure issues are correctly bucketed in Plane.
- **JSON for Parsing**: Always use `--json` when reading metadata or issue lists for programmatic use.
- **Append for History**: Use `--append` during updates to maintain a chronological audit trail in the description.

## Anti-Patterns
- **Missing Metadata**: Creating issues without cycle or module (makes them hard to track in PMS).
- **Manual ID Guessing**: Hardcoding sequence IDs instead of listing them first.
- **Generic Titles**: Using titles like "Fix bug" instead of "FIX: [Component] Null pointer in TOC extraction".

### Supported Issue States (DO NOT QUERY DYNAMICALLY)
Plane uses the following hardcoded standard states. **DO NOT run the `states` command to check for states before updating or filtering. Memorize and use these exact strings:**
- `Backlog`
- `Todo`
- `In Progress`
- `Done`
- `Cancelled`

### 2. Creating & Detailed Inspection
To create or inspect a specific issue:
```powershell
# Create task
conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py create --name "Task Title" --description "Details"

# Get full issue metadata (JSON)
conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py details AGENT-1
```

### 3. Precision Updates
Update specific fields with precision:
```powershell
# Update status and description
conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py update AGENT-1 --state "In Progress" --description "Updated scope"

# Rename task (Efficiency: prevents duplicate tasks for minor scope shifts)
conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py update AGENT-1 --name "New Explicit Title"

### 4. Advanced Direct Execution
For custom queries or operations not covered by the CLI:
```powershell
conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py run_django "from plane.db.models import Module; print(list(Module.objects.all().values('name', 'id')))"
```

## Professional Documentation Standards

All issue updates, especially closures, MUST provide high transparency and professional technical details. Do not just state "Fixed" or "Done".

### Mandatory Reporting Components
1. **Technical Summary**: A 1-2 sentence overview of the core problem and the high-level approach taken.
2. **Files Affected**: List the key files modified or created.
3. **Internal Logic/Pattern**: Explain *why* the solution was implemented this way (e.g., "bypassed API due to 401 errors").
4. **Verification Proof**: State exactly which tests were run and the results (e.g., "pytest passed 131/131").
5. **Future Prevention**: Document any new rules, scripts, or quality gates added to prevent regression.

### Example Professional Update
```powershell
conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py update AGENT-16 --state "Done" --description "<b>VERIFIED: Structural Hardening & Sync accomplished.</b><br><ul><li><b>Core Fix:</b> Repaired structural flaws in MD/JSON artifacts to satisfy CI gates.</li><li><b>Files:</b> Patched agent-1-bridge.md, dashboard-knowledge.json, and 12 others.</li><li><b>Logic:</b> Aligned manifest counts (194) with filesystem reality.</li><li><b>Proof:</b> 131/131 pytest passed.</li><li><b>Prevention:</b> Integrated verify_structures.py into the generation lifecycle.</li></ul>"
```

## Best Commands to Use
| Operation | Recommended Command Pattern | Goal |
|-----------|-----------------------------|------|
| **Discovery** | `projects` \| `list --json` \| `list --state "Done" --json` | Mapping current project landscape & filtering |
| **Inspection** | `details <ID>` | Deep understanding of a specific roadblock |
| **Reporting** | `update <ID> --description "<ul><li>Item</li></ul>"` | Professional progress broadcasting |
| **Refactoring** | `update <ID> --name "..."` | Aligning issue titles with evolving goals |
| **Custom Ops** | `run_django "..."` | Bypassing limitations for specific data needs |

## Best Practices
- **Explicit Project IDs**: Always verify the project ID before performing operations.
- **State Name Matching**: Use the exact standard state names (`Backlog`, `Todo`, `In Progress`, `Done`, `Cancelled`). Do NOT query the states list.
- **Filter Issues Efficiently**: If a task requires finding completed or pending work, use the `list --state "..."` capability rather than fetching all issues and filtering in memory.
- **HTML in Description**: ALWAYS use `<ul>`, `<li>`, and `<b>` tags for professional formatting.
- **High Transparency**: Document the *how* and *why*, not just the *what*.
- **Sync Proof**: Include test results or verification command output in the description.
- **JSON First**: Always try to parse `--json` output when making automated decisions.

## Anti-Patterns
- **Using `--title`**: The CLI uses `--name` for the issue title. Using `--title` will cause a crash.
- **Using `--state_name`**: The CLI argument is `--state`. The internal function uses `state_name`, but the subagent must use the CLI flag.
- **Vague Statuses**: Setting state to "Done" without a detailed HTML description is a violation of professional reporting standards.
- **Incorrect Environment**: Running without the `-p D:\Anaconda\envs\cursor-factory` flag will lead to missing dependency errors.

## References
- Plane documentation: [https://docs.plane.so/](https://docs.plane.so/)
- Local PMS Deployment: `apps/pms/docker-compose.yml`

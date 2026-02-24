---
name: managing-tasks-in-plane
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

### 1. Listing Issues
To list issues for a project, use the native `manager.py` script:
```powershell
conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py list --project-id 40ab9f42-6a2a-402b-a3d7-908973557123
```

### 2. Creating an Issue
To create a new task:
```powershell
conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py create --name "Task Title" --description "Detailed description" --priority "high" --state "Todo"
```

### 3. Updating Issue Status
To change the status of an existing issue (use sequence ID like AGENT-5):
```powershell
conda run -p D:\Anaconda\envs\cursor-factory python scripts/pms/manager.py update --id AGENT-5 --state "In Progress"
```

## Best Practices
- **Explicit Project IDs**: Always verify the project ID before performing operations.
- **State Name Matching**: Use the exact state names (Backlog, Todo, In Progress, Done, Cancelled).
- **Environment Awareness**: Ensure the `D:\Anaconda\envs\cursor-factory` environment is active.

## References
- Plane documentation: [https://docs.plane.so/](https://docs.plane.so/)
- Local PMS Deployment: `apps/pms/docker-compose.yml`

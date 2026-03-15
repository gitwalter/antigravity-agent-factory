---
name: managing-stack-context
version: 1.0.0
type: skill
description: Tools for managing the execution environment active SDLC stack (e.g., Python_FastAPI, DotNet_CSharp) to ensure correct workflow routing.
category: workflow
agents:
- orchestrator
knowledge:
- stack-capabilities.json
tools:
- name: get_active_stack
  type: factory
  description: Retrieves the currently active SDLC stack from configuration and memory.
- name: set_active_stack
  type: factory
  description: Sets the active SDLC stack in the configuration for the current project
    session.
related_skills:
- configuring-stacks
templates:
- none
references:
- none
settings:
  auto_approve: false
  retry_limit: 3
  timeout_seconds: 300
  safe_to_parallelize: false
  orchestration_pattern: routing
---

# Managing Stack Context Skill

## Purpose
The Antigravity factory uses a 7-Phase Meta-Orchestration loop that is **stack-agnostic**. However, Phase 4 (Build) and Phase 5 (Test) heavily depend on knowing what language/framework the project uses (e.g., Python vs C#).

This skill provides explicit tooling to query and definitively set the active `SDLC_Stack`.

## When to Use
Use this skill at the beginning of a project session or when switching between different components of a polyglot repository to ensure the AI agent operates with the correct environment context and workflow constraints.

## Prerequisites
- Conda environment `cursor-factory` must be active.
- Access to `.agent/config/stack-configurations.json`.

## Process
To manage stack context effectively, follow these steps. First, perform a comprehensive repository audit to identify key indicator files (e.g., requirements.txt, package.json). Second, query the existing execution context using the get_active_stack tool to detect any state drift. Third, implement stack realignment by running the set_active_stack command with the appropriate stack key. Finally, verify and persist the state by confirming the update with get_active_stack and ensuring the Memory MCP graph is synchronized. This flat process ensures all necessary steps are taken without architectural ambiguity.

## Best Practices
- **Explicit over Implicit**: Always set the stack explicitly when starting work on a new component.
- **Verification**: Run `get_active_stack` after setting to confirm the change was persisted.
- **Memory Sync**: Ensure scripts successfully update the Memory MCP graph for cross-session consistency.

---
name: agent-creator
description: Standardized agent creation and evaluation with mandatory schema validation
type: skill
version: 2.0.0
category: factory
agents:
  - analyzer
  - comparator
  - grader
knowledge:
  - agent-taxonomy.json
tools:
  - none
related_skills:
  - skill-creator
templates:
  - none
---

# Agent Creator

The **Agent Creator** skill is the counterpart to `skill-creator`, specifically designed for the rapid generation and iterative improvement of Cursor agents. It ensures every agent complies with the canonical `schemas/agent.schema.json` and follows the factory core patterns.

## Standard Structure

All agents follow this standardized markdown format in `{directories.agents}/*.md`:

1.  **YAML Frontmatter**: Mandatory fields (name, description, type, version, domain, skills, knowledge, tools, workflows, blueprints).
2.  **Purpose**: High-level goal.
3.  **Philosophy**: Guiding quote or principle.
4.  **Triggers**: When the agent should activate.
5.  **Workflows**: Mermaid diagram of the agent's logic.
6.  **Rules**: Core constraints.

## Iterative Improvement Loop

Like `skill-creator`, this skill supports an evaluation loop:

1.  **Generate**: Draft an agent based on a pattern or requirement.
2.  **Evaluate**: Run the agent against test queries (using `scripts/run_eval.py`).
3.  **Analyze**: Use evaluation agents (`agents/analyzer.md`, etc.) to identify weaknesses.
4.  **Improve**: Refine the agent's description and rules (using `scripts/run_loop.py`).

## Automation Scripts

Located in `scripts/`:
- `run_loop.py`: Orchestrates the improvement cycle.
- `quick_validate.py`: Validates agent frontmatter against `agent.schema.json`.
- `package_skill.py`: (Internal use) Packages agent definitions.

## Usage

Use this skill to refactor existing agents or create new specialized agents for the Factory.

## When to Use

- When creating a new agent definition from scratch
- When updating an existing agent to comply with the Factory schema
- When a user wants to design a domain-specialist agent for a specific use case
- When another agent or workflow requests a properly structured agent definition

## Prerequisites

- Access to Factory schemas in schemas/
- Understanding of available skills and topologies (chain, parallel, routing, etc.)
- The quick_validate.py script must be available for schema validation

## Process

1. Clarify the agent purpose, domain, and target topology
2. Identify relevant skills and knowledge to reference
3. Draft the agent .md file with YAML frontmatter and structured body
4. Validate against the agent schema using quick_validate.py
5. Iterate with user feedback until complete and schema-compliant

## Best Practices

- Always define a clear domain: and 	ype: agent in frontmatter
- Only reference skills that actually exist in the Factory
- Keep agent scope focused — prefer depth over breadth
- Validate the skills: list against the skill catalog
- Document axioms and decision gates for clarity

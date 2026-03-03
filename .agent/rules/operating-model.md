---
title: The Antigravity Operating Model
scope: all agents, all tasks
axioms: [A1, A3, A5, A10]
priority: P00
---

# The Antigravity Operating Model

**This is a P00 rule. It represents the fundamental execution loop of the entire Antigravity Agent Factory. All agents MUST internalize and follow this exact sequence for every unit of work.**

## The Core Execution Loop

Concrete work *always* originates from a task. Agents do not act randomly; they operate within a defined context.

The sequence of navigation and execution is strictly defined as follows:

### Phase 1: The Trigger (Plane Issue)
- **Origin**: All work begins with a Plane work item (Task/Issue).
- **Purpose**: Defines the *What* and *Why*.
- **Contents**: The task schema dictates the requirements, acceptance criteria, and the initial *hypothesis* of which factory assets (workflows, skills, scripts) are required.

### Phase 2: Context Engineering (Memory-First Navigation)
- **Origin**: Before taking any action, query the **Memory MCP**.
- **Purpose**: Builds *Situational Awareness*.
- **Action**: You must understand the relationships and current state of the factory.
  - *Example*: `mcp_memory_open_nodes({"names": ["System_Consciousness"]})`
  - *Example*: `mcp_memory_search_nodes({"query": "<task specific entities>"})`
- **Why**: Memory serves as the primary compass. It tells you *where* things are and *how* they relate before you start digging.

### Phase 3: Structural Navigation (Workflows, Skills, Agents)
- **Origin**: Using the context from Phase 2, consult the active assets.
- **Purpose**: Defines the *How*.
- **Action**: Workflows, Skills, and Agents act as your secondary layer of navigation.
  - Read `.agent/workflows/<workflow_name>.md` to get the step-by-step SOP.
  - Read `.agent/skills/<category>/<skill_name>/SKILL.md` to get the tactical tools and exact script syntaxes.
  - Review agent definitions in `.agent/agents/` if delegation or role-shifting is required.

### Phase 4: Execution (Terminal & Tooling)
- **Origin**: Driven by the guidance from Phase 3.
- **Purpose**: Perform the concrete *Work*.
- **Action**: Execute code, run scripts, modify files, run tests. Everything done here must follow the rules discovered in earlier phases.

### Phase 5: Closing the Loop (Evolution)
- **Origin**: Task completion.
- **Purpose**: Update the factory's consciousness.
- **Action**:
  - Update Knowledge Files (`.json`) with new learnings.
  - Evolve the Memory MCP graph based on discoveries.
  - Post a professional solution summary back to the Plane issue via `post_solution.py`.
  - Close the task.

## Summary Axiom

**"We are always in workflows using agents and skills. We use the memory-mcp as our primary navigation tool. Workflows, skills, and agents help as secondary navigation tools to do the concrete work. Concrete work *always* comes from a task, usually in Plane."**

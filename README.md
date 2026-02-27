# Antigravity Agent Factory

![antigravity-ide](https://img.shields.io/badge/antigravity--ide-blue)
![ai-agents](https://img.shields.io/badge/ai--agents-purple)
![mcp-servers](https://img.shields.io/badge/mcp--servers-green)

This repository demonstrates a **platform-independent system** for building agentic software. It provides a concrete example of how to implement the **Axiomatic Agentic Framework**—a universal methodology for creating verifiable, purposeful, and safe AI systems.

While this implementation uses Python and specific tools, the underlying **System** (Agents, Skills, Workflows, Integrity Layers) can be adapted to any platform or language.

## Quick Start (Example Usage)

This reference implementation allows you to generate a demo project immediately:


**Generate Project:**
```powershell
python cli/factory_cli.py --quickstart
```

## System Architecture

The Framework is built on a **5-Layer Deductive-Inductive Architecture**. It deduces technical implementation (L4) from foundational axioms (L0). This architecture is universally applicable.

### 1. The 5 Layers
- **L0: Integrity & Logic** (Axioms, Formal Verification)
- **L1: Purpose** (Mission, Stakeholders)
- **L2: Principles** (Ethical Boundaries, Quality Standards)
- **L3: Methodology** (Workflows, Collaboration Patterns)
- **L4: Technical** (Code, Agents, Skills)

See [docs/architecture/axiomatic-principles.md](docs/architecture/axiomatic-principles.md) for the deep dive into the system's design philosophy.

### 2. Core Concepts

The system is composed of **8 Key Concepts** that work together:

| Concept | Layer | Definition |
|---------|-------|------------|
| **Agents** | L4 | **The "Who"**: Autonomous entities with a specific role, personality, and instructions (e.g., `git-specialist`). |
| **Skills** | L4 | **The "Recipe"**: Deterministic, executable instruction sets (e.g., `create_pull_request`). |
| **Workflows** | L3 | **The "Process"**: Repeatable work patterns grounded in a defined *Purpose* (e.g., "Feature Dev", "Bug Fix"). |
| **Patterns** | L3/4 | **The "Wisdom"**: Inductive best practices and architectural designs (e.g., "Clean Architecture"). |
| **Knowledge** | L4 | **The "Context"**: Structured data, docs, and rules that ground the agents. |
| **Templates** | L4 | **The "Shape"**: Jinja2 scaffolding for generating consistent code and docs. |
| **RAG** | Sys | **The "Memory"**: Retrieval-Augmented Generation. How agents access *Knowledge*. |
| **MCP** | Sys | **The "Kitchen"**: Model Context Protocol. The standardized environment providing tools (Git, DB, Slack). |

### 3. Interaction & Coordination

The system uses specific protocols to execute tasks reliably.

#### Interaction Models (User ↔ System)
*   **Natural Language ("Intent")**: You describe the goal ("Fix the bug in login"), and the system deduces the necessary steps.
*   **Slash Commands ("Process")**: You invoke deterministic workflows (e.g., `/feature-development`, `/code-review`). This forces the system into a proven path.
*   **CLI ("Scaffolding")**: You use terminal commands (`python cli/factory_cli.py`) for project generation and system updates.

#### Coordination Patterns (Agent ↔ Agent)
*   **Supervisor Pattern**: A high-level agent (e.g., `ProductOwner`) breaks down the task and delegates to worker agents (`Developer`, `Tester`), ensuring the plan is followed.
*   **Handoff Protocol**: Agents explicitly transfer control and context to the next specialist (e.g., `Developer` → `Reviewer`) when a phase is complete.
*   **Guardian Interdiction**: The Layer 0 Guardian monitors *all* interactions and can pause or block agents if they violate safety axioms.

### 4. Workflows: The Engine of Creation

Workflows are more than just lists of steps; they are **dynamic engines** that combine Agents, Skills, Patterns, and Templates to solve complex tasks defined by the user or system. They react to triggers (e.g., a new ticket, a test failure) and orchestrate the entire response.

#### How It Works
> **Workflow = Agents + Skills + Patterns + Templates**

1.  **Trigger**: An event occurs (Slash command, Jira ticket, CI failure).
2.  **Sequence**: The workflow initiates a sequence of steps.
3.  **Reaction**: At each step, it assigns an **Agent**, equips them with **Skills** and **Patterns**, and provides **Templates** for output.

#### Common Workflows
*   **Feature Development**:
    *   *Sequence*: Research → TDD (Test Driven Development) → Implementation → Verification.
    *   *Goal*: Ship new capabilities reliably.
*   **Debugging**:
    *   *Sequence*: Log Analysis → Runtime Inspection → Root Cause Analysis → Fix.
    *   *Goal*: Restore system stability.
*   **Building**:
    *   *Sequence*: Architecture Design → Scaffolding → Compilation.
    *   *Goal*: Create new Agents, Statistical Programs, or entire Software Systems.

### 5. The Orchestration Flow

How a user intent becomes code:

1.  **Workflow (Layer 3)**:
    *   Defines the **Plan**.
    *   Example: "Feature Development" workflow splits a request into *Analysis*, *Implementation*, and *Verification* phases.
    *   It assigns specific **Agents** to each phase.

2.  **Agent (Layer 4)**:
    *   Accepts the **Task** from the Workflow.
    *   Example: `Senior Developer` agent receives the *Implementation* task.
    *   It queries **Knowledge** (RAG) to understand the codebase context.
    *   It selects the appropriate **Skill** ("Recipe") to execute the task.

3.  **Skill (Layer 4)**:
    *   Defines the **Recipe** (Method).
    *   Example: `implement_feature` skill provides the step-by-step logic (create branch, edit files, run tests).
    *   It calls distinct **Tools** to perform actions.

4.  **Tools (System)**:
    *   The **Kitchen** (Environment).
    *   **MCP**: Provides the utensils and appliances (e.g., `git` to branch, `postgres` to migrate).
    *   **Scripts**: Local utilities.
    *   **Reference**: Static blueprints.

**The Result**: A deterministic, verifiable change to the system, born from intent and executed with precision.

### 5. Core Components

The framework's power lies in the interaction between its core components.

#### Current Implementation Stats
This reference implementation currently includes a comprehensive set of verified components:
- **Agents**: 10 active agents in `.agent/agents` (10 agents)
- **Skills**: 191 specialized skills in `.agent/skills` (198 skills)
- **Blueprints**: 34 project blueprints in `.agent/blueprints` (34 blueprints)
- **Knowledge**: 268 JSON knowledge files in `.agent/knowledge` (273 files)
- **Patterns**: 113 architectural patterns in `.agent/patterns` (113 patterns)
- **Templates**: 307 Jinja2 templates in `.agent/templates` (308 templates)
- **Verification**: 76 automated validation tests (76 tests)

#### Integrity Guardian (Layer 0)
An active runtime protection system that monitors all agent operations.
- **Role**: Ensures alignment with Axiom 0 (Love, Truth, Beauty).
- **Function**: Intercepts and blocks destructive commands, secret leaks, or deceptive logic.
- **Status**: Always active. Cannot be disabled by prompts.

#### Memory System (Qdrant-Backed)
A persistent, user-verified knowledge graph utilizing Qdrant for vector search.
- **Semantic Memory**: Long-term fact storage with high-dimensional embeddings.
- **Episodic Memory**: Session-based context for maintaining conversation continuity.
- **User Primacy**: All long-term memories require explicit user approval.

#### Formal Verification (Lean 4)
The system's core logic is formally verified using the Lean 4 theorem prover.
- We prove that the **Guardian** preserves system safety states.
- We prove that high-level **Instructions** cannot violate **Axioms**.

#### Agent Society
A verified communication protocol for multi-agent collaboration.
- Agents verify each other's "contracts" (capabilities and obligations).
- Uses cryptographic event sourcing for immutable audit trails.

## The Factory Workflow

The Factory operates as a meta-agent that guides you from intent to implementation:

1.  **Purpose Definition**: Define *why* you are building this.
2.  **Requirement Deduction**: Derive technical needs from the purpose.
3.  **Agent Assembly**: Select agents and skills based on requirements.
4.  **Code Generation**: Scaffolding the project structure.

## Available Blueprints

The Factory includes **34+ Blueprints** for various domains:

| Blueprint | Stack | Description |
|-----------|-------|-------------|
| `python-fastapi` | Python, FastAPI, Pydantic | Modern, high-performance web API |
| `python-streamlit` | Python, Streamlit | Rapid interactive data applications |
| `python-langgraph` | Python, LangChain, LangGraph | State-of-the-art agent orchestration |
| `python-rag` | Python, Qdrant, sentence-transformers | Retrieval-Augmented Generation system |
| `sap-abap` | ABAP, Clean ABAP | SAP ABAP development |
| `sap-rap` | ABAP, RAP, Fiori | SAP RESTful ABAP Programming |
| `sap-cap` | Node.js/Java, CDS, SAP BTP | SAP Cloud Application Programming |
| `dotnet-api` | C#, ASP.NET Core, EF Core | Enterprise-grade .NET APIs |
| `nextjs-app` | TypeScript, Next.js, Tailwind | Modern full-stack web applications |
| `solidity-contract` | Solidity, Hardhat/Foundry | Ethereum smart contracts |
| `solana-program` | Rust, Anchor | High-performance Solana programs |

See [docs/reference/blueprints.md](docs/reference/blueprints.md) for the complete list of available stacks.

## Project Structure

A generated project looks like this:

```text
my-project/
├── .agent/                 # The "Brain"
│   ├── agents/             # Active Agents
│   ├── skills/             # Executable Skills
│   └── knowledge/          # Domain Knowledge
├── .agentrules             # The 5-Layer Constitution
├── PURPOSE.md              # The L1 Definition
├── workflows/              # L3 Methodologies
├── src/                    # L4 Implementation
└── tests/                  # Verification
```

## Development

### Requirements
- Python 3.10+
- An OpenAI/Anthropic API Key (for the agents)

### Installation

```powershell
pip install -r requirements.txt
```

### Running Tests

```powershell
pytest tests/
```

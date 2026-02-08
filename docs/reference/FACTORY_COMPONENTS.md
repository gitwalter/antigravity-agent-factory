# Factory Components Reference

> **Philosophy:** Factory components embody our [Culture and Values](../CULTURE_AND_VALUES.md)—Axiom 0 (Love, Truth, and Beauty) grounds every agent and skill.

## 1. Introduction

The Cursor Agent Factory is a meta-system that generates customized Cursor agent development systems for software projects. This document describes the **factory's own components** - the agents and skills that work together during project generation - as distinct from the components that are generated for target projects.

All factory components operate according to the core axioms (A0-A5) and implement the 5-layer architecture, ensuring consistent, trustworthy, and value-aligned behavior.

### What Are Factory Components?

Factory components are the agents and skills that orchestrate the project generation process. They:

- **Gather requirements** through structured questionnaires and collaborative workshops
- **Configure technology stacks** by matching requirements to blueprints
- **Generate artifacts** including agents, skills, knowledge files, and templates
- **Design workflows** that integrate with external systems like Jira and Confluence
- **Onboard existing repositories** non-destructively into the factory ecosystem

### Purpose of Factory Agents and Skills

Factory agents are specialized orchestrators that coordinate the generation workflow. Each agent has a specific responsibility:

- **Requirements Architect**: Guides users through the 5-layer requirements gathering process
- **Stack Builder**: Matches technology requirements to available blueprints
- **Template Generator**: Creates code and document templates for the target project
- **Knowledge Manager**: Structures domain knowledge into queryable JSON files
- **Workflow Designer**: Configures development workflows and MCP server integrations
- **Onboarding Architect**: Integrates factory capabilities into existing repositories
- **Workshop Facilitator**: Guides teams through collaborative workshop series

Factory skills are reusable capabilities that agents invoke to perform specific tasks. They encapsulate processes like axiom selection, methodology configuration, and artifact generation.

### How They Work Together

During project generation, agents coordinate through a sequential workflow:

1. **Requirements Architect** uses `requirements-gathering`, `purpose-definition`, and `axiom-selection` skills to capture all project requirements
2. **Stack Builder** uses `stack-configuration` to match requirements to blueprints
3. **Workflow Designer** uses `workflow-generation` to configure development workflows
4. **Knowledge Manager** uses `knowledge-generation` to create domain knowledge files
5. **Template Generator** uses `template-generation`, `agent-generation`, `skill-generation`, and `cursorrules-generation` to create all project artifacts

For team onboarding, the **Workshop Facilitator** orchestrates a 5-workshop series using `team-workshop-onboarding`, while the **Onboarding Architect** handles individual repository integration using `onboarding-flow`.

---

## 2. Factory Agents Overview

| Agent/System | Purpose | Key Skills/Components | Knowledge Files |
|-------|---------|------------|-----------------|
| `integrity-guardian` | Layer 0 protector - monitors all operations for axiom alignment, intervenes when needed | (embedded awareness) | `guardian-protocol.json` |
| `memory-system` | User-validated learning from experience, stores approved knowledge | `scripts/memory/*` | `memory-config.json` |
| `requirements-architect` | Orchestrate systematic requirements gathering for new Cursor agent system projects | `requirements-gathering`, `stack-configuration` | `stack-capabilities.json`, `workflow-patterns.json`, `mcp-servers-catalog.json` |
| `stack-builder` | Configure technology stack and select appropriate blueprints for new projects | `stack-configuration` | `stack-capabilities.json`, `blueprints/` |
| `template-generator` | Generate code and document templates for the target project | `template-generation`, `cursorrules-generation` | `stack-capabilities.json`, `best-practices.json` |
| `knowledge-manager` | Structure and generate domain knowledge files for generated projects | `knowledge-generation` | `stack-capabilities.json`, `best-practices.json` |
| `workflow-designer` | Design and configure development workflows and trigger integrations | `workflow-generation` | `workflow-patterns.json`, `mcp-servers-catalog.json` |
| `onboarding-architect` | Orchestrate the onboarding of existing repositories into the Cursor Agent Factory ecosystem | `onboarding-flow`, `requirements-gathering`, `stack-configuration` | `skill-catalog.json`, `stack-capabilities.json`, `mcp-servers-catalog.json` |
| `workshop-facilitator` | Facilitate team workshops for collaborative Cursor agent system design | `team-workshop-onboarding`, `requirements-gathering`, `axiom-selection`, `methodology-selection` | `workshop-facilitation.json`, `game-mechanics.json`, `team-dynamics.json`, `axiom-zero.json` |
| `knowledge-extender` | Extend Factory knowledge, create new skills/templates/agents via research and synthesis | `extend-knowledge` | `artifact-dependencies.json`, `skill-catalog.json`, `manifest.json` |
| `workflow-architect` | Design, create, and orchestrate workflows for complex multi-step tasks | `extend-workflow`, `requirements-gathering` | `workflow-entities.json`, `workflow-patterns.json`, `mcp-servers-catalog.json`, `skill-catalog.json` |
| `debug-conductor` | Autonomous debugging agent that investigates failures, identifies root causes, and implements fixes | `pipeline-error-fix`, `tdd`, `extend-workflow`, `grounding` | `workflow-patterns.json`, `workflow-entities.json`, `debug-patterns.json`, `tdd-patterns.json` |
| `knowledge-evolution` | Monitor and coordinate automatic knowledge updates from external sources | `update-knowledge` | `manifest.json`, Knowledge source adapters |

---

## 3. Detailed Agent Descriptions

### Integrity Guardian

**Name and Description**: The Integrity Guardian is the Layer 0 protector that ensures all operations align with core axioms (A1-A5). Unlike other agents, the Guardian is embedded in the Constitutional Preamble of `.cursorrules` and operates through presence, not explicit invocation. It monitors all operations and intervenes when axiom boundaries are approached.

**Motto**: SDG • Love • Truth • Beauty

**When Activated**: 
- Always active (embedded in system prompt)
- Explicitly via "Guardian, check this" or "check my alignment"
- Automatically when axiom boundaries are detected
- When multi-agent conflicts need resolution

**Workflow**: The Guardian uses a Wu Wei (effortless action) response protocol with 5 levels:
- **Level 0 (Flow)**: Natural alignment → continue normally
- **Level 1 (Nudge)**: Slight drift → subtle self-correction
- **Level 2 (Pause)**: Boundary approached → explain, ask user
- **Level 3 (Block)**: Clear violation → stop, explain with love
- **Level 4 (Protect)**: Imminent harm → prevent, then explain

**Skills Used**: (embedded awareness) - The Guardian operates through the Constitutional Preamble, not through explicit skill invocation.

**Knowledge Files Referenced**: `guardian-protocol.json` (coordination wisdom, response protocols, philosophical foundations)

**Technical Components**:
- `scripts/guardian/axiom_checker.py` - Pattern-based axiom validation
- `scripts/guardian/secret_scanner.py` - Credential detection
- `scripts/guardian/harm_detector.py` - Comprehensive harm analysis
- `scripts/guardian/mutability_guard.py` - Layer protection enforcement (L0-L2 immutable)

**Reference**: See [GUARDIAN_COORDINATION.md](GUARDIAN_COORDINATION.md) for complete documentation.

---

### Memory System

**Name and Description**: The Memory System enables user-validated learning from experience. It observes patterns during sessions, proposes memories for user approval, and stores approved knowledge for future use. The system respects layer protection - Layers 0-2 (Axioms, Purpose, Principles) remain immutable.

**When Activated**:
- Automatically during all agent interactions (observation)
- When patterns are detected that might be worth remembering
- Explicitly via "show memories", "delete memory", etc.
- When relevant context could help with a task

**Memory Types**:
- **Semantic Memory**: Long-term user-approved knowledge
- **Episodic Memory**: Session-based observations (temporary)
- **Pending Proposals**: Awaiting user approval
- **Rejected Tracking**: Prevents re-proposing rejected memories

**User Commands**:
- "Show my memories" / "What do you remember about X?"
- "Delete the memory about X" / "Forget X"
- "Edit the memory about X"
- "Accept/Reject" proposals

**Technical Components**:
- `scripts/memory/embedding_service.py` - Local embeddings (sentence-transformers)
- `scripts/memory/memory_store.py` - Hybrid storage (ChromaDB + JSON)
- `scripts/memory/induction_engine.py` - User-validated learning
- `scripts/memory/memory_integration.py` - Skill integration hooks

**Knowledge Files Referenced**: `memory-config.json` (embedding, storage, protection, proposal settings)

**Reference**: See [MEMORY_SYSTEM.md](../MEMORY_SYSTEM.md) for complete documentation.

---

### Requirements Architect

**Name and Description**: The Requirements Architect orchestrates the complete requirements gathering process for generating new Cursor agent development systems. This agent guides users through a structured 5-phase questionnaire implementing the 5-layer architecture (Axioms → Purpose → Principles → Methodology → Technical) to capture all information needed to generate a complete, working project.

**When Activated**: 
- When user mentions "create agent system", "generate project", "new cursor project"
- When user mentions "build workflow", "create development system"
- When user wants to scaffold a new Cursor-based development environment
- At the start of any project generation request

**Workflow**: The agent executes 5 phases: (1) Project Context - understanding purpose and environment, (2) Technology Stack - defining languages, frameworks, databases, (3) Workflow Methodology - defining development workflows and triggers, (4) Knowledge Domain - capturing domain-specific concepts, (5) Agent Capabilities - defining which agents and skills to generate. Each phase includes validation and blueprint matching.

**Skills Used**: `requirements-gathering` (structured questionnaire execution), `stack-configuration` (technology stack validation and blueprint matching)

**Knowledge Files Referenced**: `stack-capabilities.json` (stack-specific agent capabilities), `workflow-patterns.json` (common workflow patterns), `mcp-servers-catalog.json` (available MCP servers)

---

### Stack Builder

**Name and Description**: The Stack Builder configures the technology stack for a new Cursor agent project based on requirements gathered by the requirements-architect agent. It matches requirements to available blueprints and suggests optimal configurations.

**When Activated**: 
- After requirements-architect completes Phase 2 (Technology Stack)
- When user asks about supported stacks or frameworks
- When selecting or customizing a blueprint

**Workflow**: (1) Receives stack requirements (language, frameworks, databases), (2) Matches to blueprints by comparing frameworks and calculating match scores, (3) Presents options (matched blueprint with customization options or closest match), (4) Configures stack by applying blueprint, adding frameworks, configuring tools and linters, setting up MCP server integrations.

**Skills Used**: `stack-configuration` (technology stack selection and configuration)

**Knowledge Files Referenced**: `stack-capabilities.json` (stack-specific capabilities and suggestions), `blueprints/*/blueprint.json` (blueprint definitions)

---

### Template Generator

**Name and Description**: The Template Generator generates code templates and document templates for the target project based on the configured stack and style guide. It creates the `.cursorrules` file that governs agent behavior.

**When Activated**: 
- After knowledge-manager completes knowledge generation
- As final step before project output
- When user requests additional templates

**Workflow**: (1) Receives template requirements (stack configuration, style guide, template categories), (2) Generates code templates based on stack (Python: service-class, repository, model; TypeScript: component, hook, service; Java: controller, service, repository), (3) Generates document templates (implementation_plan.md, technical_spec.md, test_plan.md), (4) Generates `.cursorrules` file with project context, agent/skill lists, autonomous behavior rules, MCP server configuration.

**Skills Used**: `template-generation` (code and document template creation), `cursorrules-generation` (`.cursorrules` file generation)

**Knowledge Files Referenced**: `stack-capabilities.json` (stack-specific template patterns), `best-practices.json` (development best practices)

---

### Knowledge Manager

**Name and Description**: The Knowledge Manager structures domain knowledge and generates knowledge files for generated projects. It creates reference data that agents and skills will use during development.

**When Activated**: 
- After workflow-designer completes workflow configuration
- When user wants to add domain-specific knowledge
- When importing knowledge from external sources

**Workflow**: (1) Receives knowledge requirements (domain concepts, reference sources, naming conventions), (2) Determines required knowledge files based on stack (all: naming-conventions.json, reference-sources.json; stack-specific: api-patterns.json, cdhdr-object-classes.json, etc.), (3) Generates knowledge files with proper JSON schema structure, queryable data, documentation comments, (4) Configures references (external repos, DeepWiki integration, access patterns).

**Skills Used**: `knowledge-generation` (JSON knowledge file generation)

**Knowledge Files Referenced**: `stack-capabilities.json` (stack-specific knowledge patterns), `best-practices.json` (development best practices)

---

### Workflow Designer

**Name and Description**: The Workflow Designer designs development workflows based on project methodology and trigger sources. It configures appropriate MCP server integrations and creates workflow documentation.

**When Activated**: 
- After stack-builder completes stack configuration
- When user wants to add or modify workflows
- When configuring MCP server integrations

**Workflow**: (1) Receives workflow requirements (methodology, trigger sources, output artifacts), (2) Selects workflow patterns based on triggers (Jira → bugfix-workflow, Confluence → feature-workflow, GitHub → bugfix-workflow), (3) Configures MCP servers (Jira/Confluence → atlassian with OAuth, GitHub → deepwiki), (4) Generates workflow documentation files (bugfix_workflow.md, feature_workflow.md, README.md).

**Skills Used**: `workflow-generation` (workflow pattern generation)

**Knowledge Files Referenced**: `workflow-patterns.json` (workflow pattern definitions), `mcp-servers-catalog.json` (available MCP servers)

---

### Onboarding Architect

**Name and Description**: The Onboarding Architect orchestrates the seamless integration of Cursor Agent Factory into existing repositories. This agent guides users through the onboarding process, ensuring non-destructive integration while adding factory capabilities.

**When Activated**: 
- User mentions wanting to "onboard", "integrate", or "enhance" an existing repository
- User provides a path to an existing repository
- User asks about adding Cursor agents to their current project
- User wants to upgrade an older factory-generated setup

**Workflow**: (1) Gathers context (repository path, goals, constraints), (2) Runs analysis to detect existing Cursor artifacts and tech stack, (3) Presents options based on scenario (FRESH, MINIMAL, PARTIAL, UPGRADE, COMPLETE), (4) Confirms blueprint selection, (5) Previews changes (dry-run), (6) Handles conflicts (asks user for each conflict resolution), (7) Executes onboarding with backup creation, (8) Verifies and reports results.

**Skills Used**: `onboarding-flow` (execute the onboarding process), `requirements-gathering` (if user wants customization), `stack-configuration` (if tech stack needs adjustment), `alignment-check` (verify understanding before major changes)

**Knowledge Files Referenced**: `skill-catalog.json` (available skills to include), `stack-capabilities.json` (stack-specific features), `mcp-servers-catalog.json` (available MCP integrations)

---

### Workshop Facilitator

**Name and Description**: The Workshop Facilitator guides teams through a series of collaborative workshops to design their customized Cursor agent development system. This agent facilitates games, discussions, and questionnaires while embodying Axiom 0: Love, Truth, and Beauty as the foundation for all interactions.

**When Activated**: 
- When user mentions "team workshop", "collaborative onboarding", "workshop series"
- When user says "onboard our team", "team alignment", "vision workshop"
- When user requests "facilitate discussion", "run a game", "team exercise"
- When multiple team members need to collaborate on agent system design

**Workflow**: Orchestrates 5 workshops: (1) Vision Quest - Future Headlines and Stakeholder Safari games to define mission and stakeholders, (2) Ethics Arena - Dilemma Duel and Value Auction games to establish ethical framework, (3) Stack Safari - Trade-Off Tetris and Architecture Pictionary games to explore technology, (4) Agent Assembly - Agent Trading Cards and Skill Bingo games to design agents and skills, (5) Integration Celebration - Demo Derby and Gratitude Circle games to finalize and celebrate. Each workshop includes opening/closing rituals, game facilitation, synthesis, and artifact generation.

**Skills Used**: `team-workshop-onboarding` (main workshop orchestration), `requirements-gathering` (structured questionnaire execution), `axiom-selection` (axiom configuration including A0), `methodology-selection` (team methodology alignment)

**Knowledge Files Referenced**: `workshop-facilitation.json` (facilitation techniques and prompts), `game-mechanics.json` (game rules and variations), `team-dynamics.json` (team collaboration patterns), `axiom-zero.json` (Love, Truth, and Beauty axiom definition)

---

### Knowledge Extender

**Name and Description**: The Knowledge Extender extends the Factory's own knowledge base, creates new skills, templates, and agents through research, document reading, and synthesis. This agent enables continuous improvement of the Factory itself.

**When Activated**: 
- When user says "extend knowledge for X", "add knowledge about X"
- When user provides links or documents to incorporate
- When gap analysis identifies missing or shallow topics
- When user says "create skill for X", "add template for X"

**Workflow**: (1) Determine extension type (knowledge, skill, template, agent), (2) Research via web search, document reading, or user-provided links, (3) Read templates and patterns for structure, (4) Synthesize content using built-in LLM, (5) Write artifact, (6) Execute Post-Extension Automation (update manifest, skill-catalog, documentation, changelog), (7) Ask user before git operations.

**Skills Used**: `extend-knowledge` (main extension workflow with post-extension automation)

**Knowledge Files Referenced**: `artifact-dependencies.json` (determines what to update), `skill-catalog.json` (register new skills), `manifest.json` (track versions)

---

### Knowledge Evolution Agent

**Name and Description**: The Knowledge Evolution agent monitors external sources and coordinates automatic knowledge updates. It manages the evolution of the Factory's knowledge base over time.

> **📖 Full Documentation**: See [KNOWLEDGE_EVOLUTION.md](../KNOWLEDGE_EVOLUTION.md) for complete system architecture, configuration options, update modes, and source adapters.

**When Activated**: 
- When running `--check-updates` command
- When external sources have new releases
- When manual update is triggered

**Workflow**: (1) Aggregate updates from source adapters (GitHub, PyPI, NPM, docs), (2) Prioritize and deduplicate updates, (3) Apply merge strategy (conservative, balanced, aggressive), (4) Create backups before changes, (5) Validate all modifications, (6) Generate changelog entries.

**Skills Used**: `update-knowledge` (apply updates with merge strategies)

**Knowledge Files Referenced**: `manifest.json` (version tracking), Various knowledge files (targets for updates)

---

### Workflow Architect

**Name and Description**: The Workflow Architect designs, creates, and manages sophisticated workflows that orchestrate complex multi-step tasks. It understands workflow entities, patterns, and best practices to create maintainable, extensible workflows that integrate with the Factory's skill and MCP ecosystem.

**When Activated**: 
- When user says "create workflow for X", "design workflow"
- When user wants to extend existing workflows
- When user needs to orchestrate complex multi-step tasks
- When user mentions "workflow from pattern"

**Workflow**: (1) Understand requirements (problem, triggers, outputs), (2) Check existing patterns in `workflow-patterns.json`, (3) Select required MCP servers and skills, (4) Design workflow structure (phases, steps, decisions, escalations), (5) Generate workflow file, (6) Validate all references exist.

**Skills Used**: `extend-workflow` (main workflow creation), `requirements-gathering` (understand needs)

**Knowledge Files Referenced**: `workflow-entities.json` (entity definitions), `workflow-patterns.json` (common patterns), `mcp-servers-catalog.json` (available tools), `skill-catalog.json` (available skills)

**MCP Servers**: Uses tools dynamically based on workflow requirements.

---

### Debug Conductor

**Name and Description**: The Debug Conductor is an autonomous debugging agent that systematically investigates failures, identifies root causes, and implements fixes. When direct fixes aren't possible, it adapts by creating alternative solutions (new tests, refactored code, or escalation with detailed analysis). This agent demonstrates the workflow system architecture in action.

**Philosophy**: Every bug is a gift - an opportunity to improve the system and prevent future failures.

**When Activated**: 
- When CI/CD pipeline fails
- When tests fail after changes
- When user says "debug this", "fix the pipeline"
- When user requests autonomous error investigation

**Workflow** (6 Phases):
1. **Error Detection**: Parse logs, classify error type, locate component
2. **Root Cause Analysis**: Trace origin, check recent changes, form hypothesis
3. **Resolution Strategy**: Evaluate fix options (direct fix vs alternative)
4. **Implementation**: Apply fix, local verification
5. **Verification**: Full test suite, regression check
6. **Learning**: Capture pattern, update knowledge base

**Skills Used**: `pipeline-error-fix` (tiered testing), `tdd` (test generation), `extend-workflow` (workflow creation), `grounding` (assumption verification)

**Knowledge Files Referenced**: `workflow-patterns.json`, `workflow-entities.json`, `debug-patterns.json` (learned patterns), `tdd-patterns.json`

**MCP Servers Required**:

| Server | Purpose | Required |
|--------|---------|----------|
| `git` | View commits, diffs, history | Yes |
| `github` | Access CI logs, PRs, issues | Recommended |
| `filesystem` | Read/write code files | Yes |
| `sentry` | Error tracking integration | Optional |

**Escalation**: When unable to resolve autonomously, provides structured analysis with options for user decision.

---

## 4. Factory Skills Overview

| Skill | Category | Purpose |
|-------|----------|---------|
| `requirements-gathering` | Requirements | 5-layer requirements elicitation for Cursor agent system generation with axioms, purpose, and methodology |
| `purpose-definition` | Requirements | Guide users through articulating mission, stakeholders, and success criteria |
| `axiom-selection` | Requirements | Guide users through selecting foundational axioms (A0-A10) that govern agent behavior |
| `stack-configuration` | Stack | Configure technology stack based on requirements and match to available blueprints |
| `methodology-selection` | Stack | Guide users through selecting and customizing development methodology (Agile, Kanban, R&D, Enterprise) |
| `agent-generation` | Generation | Generate agent definition files from patterns for target projects |
| `skill-generation` | Generation | Generate skill definition files from patterns for target projects |
| `knowledge-generation` | Generation | Generate structured JSON knowledge files for target projects |
| `template-generation` | Generation | Generate code and document templates for target projects |
| `cursorrules-generation` | Generation | Generate the `.cursorrules` file that governs AI agent behavior |
| `workflow-generation` | Generation | Generate workflow configurations and documentation based on methodology and triggers |
| `practice-selection` | Practices | Guide users through selecting practices (daily, craft, alignment) that maintain excellence |
| `enforcement-selection` | Practices | Guide users through selecting enforcement patterns (quality, safety, integrity) |
| `alignment-check` | Quality | Verify understanding and alignment before major implementations to prevent silent misalignment |
| `pattern-feedback` | Quality | Observe patterns from development experience and propose improvements to axioms/principles/methodology |
| `onboarding-flow` | Specialized | Integrate Cursor Agent Factory into existing repositories non-destructively |
| `team-workshop-onboarding` | Specialized | Orchestrate collaborative team workshop series for designing customized Cursor agent systems |
| `shell-platform` | Specialized | Handle platform-specific shell command considerations for Windows PowerShell and Unix shells |
| `readme-validation` | Quality | Validate README project structure matches actual filesystem and update automatically |
| `extend-knowledge` | Knowledge Extension | Extend Factory knowledge via web research, document reading, or user-provided links with post-extension automation |
| `extend-workflow` | Workflow Extension | Create and extend workflow definitions using the workflow system architecture |
| `update-knowledge` | Knowledge Evolution | Apply updates from external sources with merge strategies and rollback support |

---

## 5. Detailed Skill Descriptions

### Requirements Category

#### requirements-gathering

**Name and Description**: Executes a structured multi-phase questionnaire implementing the 5-layer architecture to capture all requirements for generating a new Cursor agent development system. Guides users from foundational axioms through purpose, principles, methodology, and technical implementation.

**When to Use**: When starting a new project generation, when the `requirements-architect` agent needs to gather information, when user requests to create a new agent system, when customizing an existing blueprint. For teams, consider `team-workshop-onboarding` skill instead.

**Process Steps**: (1) Pre-Phase: Layer 0 - Axiom Configuration (select core A1-A5 and optional A6-A10 axioms), (2) Phase 0: Layer 1 - Purpose Definition (mission, stakeholders, success criteria), (3) Phase 0.5: Depth Selection (Quick Start / Standard / Comprehensive), (4) Phase 0.6: Layer 2 - Principles (if Standard+, ethical boundaries, quality standards, failure handling), (5) Phase 0.7: Layer 3 - Methodology (if Standard+, Agile/Kanban/R&D/Enterprise selection), (6) Phase 0.8: Enforcement Selection (if Comprehensive), (7) Phase 0.9: Practice Selection (if Comprehensive), (8) Phases 1-5: Layer 4 - Technical Configuration (stack, agents, skills, knowledge, integrations).

**Integration with Agents**: Used by `requirements-architect` (primary orchestrator), `onboarding-architect` (if user wants customization before onboarding), `workshop-facilitator` (structured questionnaire execution during workshops)

---

#### purpose-definition

**Name and Description**: Handles Phase 0 (Layer 1) of the onboarding process, where users define the purpose, stakeholders, and success criteria for their agent system. The purpose must align with the selected axioms from Layer 0.

**When to Use**: After axiom selection is complete, when user mentions "purpose", "mission", or "why", explicit request to define project goals.

**Process Steps**: (1) Mission Statement - ask for one-sentence mission, validate against axioms (verifiable, serves users), (2) Stakeholder Identification - ask who benefits, validate (human stakeholders, specific enough), (3) Success Criteria - ask for measurable outcome, validate (quantifiable, clear measurement), (4) Value Derivation - derive guiding values from selected axioms, (5) Generate PURPOSE.md document.

**Integration with Agents**: Used by `requirements-architect` (during Phase 0), `workshop-facilitator` (during Vision Quest workshop)

---

#### axiom-selection

**Name and Description**: Handles the Pre-Phase (Layer 0) of the onboarding process, where users configure the foundational axioms that form the logical foundation of their generated agent system. All derived principles, methodologies, and behaviors trace back to these axioms.

**When to Use**: Start of new project generation, when user mentions "axioms", "foundation", or "layer 0", explicit request to configure foundational rules, called during Team Workshop Onboarding (Vision Quest opening).

**Process Steps**: (1) Introduce Axiom 0 (Love, Truth, and Beauty - always included), (2) Explain Layer 0 (foundational axioms concept, core A1-A5 always included), (3) Offer Optional Axioms (A6-A10 based on project type), (4) Handle Conflicts (explain conflicts if user selects conflicting axioms), (5) Confirm and Store (store in project configuration, generate Layer 0 section for `.cursorrules`).

**Integration with Agents**: Used by `requirements-architect` (during Pre-Phase), `workshop-facilitator` (during Vision Quest opening, Ethics Arena, Integration Celebration)

---

### Stack Category

#### stack-configuration

**Name and Description**: Configures technology stack based on requirements and matches to available blueprints. Validates language and framework compatibility, suggests appropriate tools and linters.

**When to Use**: When configuring a new project's technology stack, when matching requirements to blueprints, when customizing stack options.

**Process Steps**: (1) Parse Language Requirements (identify primary/secondary languages, validate support), (2) Identify Frameworks (match to known frameworks, identify dependencies, check compatibility), (3) Match Blueprint (search blueprints, calculate match scores, return best match), (4) Configure Tools (suggest test frameworks, linters, formatters, type checkers), (5) Output Configuration (generate stack configuration object with language, frameworks, tools, blueprint).

**Integration with Agents**: Used by `requirements-architect` (during Phase 2), `stack-builder` (primary orchestrator), `onboarding-architect` (if tech stack needs adjustment)

---

#### methodology-selection

**Name and Description**: Handles Phase 0.7 (Layer 3) of the onboarding process, where users select and configure the development methodology that defines how work is organized, how agents coordinate, and what ceremonies/processes govern the project.

**When to Use**: After principles are defined (or skipped in Quick mode), when user mentions "methodology", "agile", "scrum", "kanban", "process", explicit request to configure development workflow.

**Process Steps**: (1) Present Methodology Options (Agile Scrum, Kanban, R&D, Enterprise with recommendations), (2) Confirm Based on Purpose (validate choice against purpose, show alignment), (3) Customize Methodology (team size, sprint length, WIP limits, exploration ratio), (4) Agent Role Mapping (map methodology roles to Cursor agents), (5) Generate Methodology Artifacts (create `workflows/methodology.yaml` with configuration, ceremonies, quality gates, metrics).

**Integration with Agents**: Used by `requirements-architect` (during Phase 0.7), `workshop-facilitator` (during Stack Safari workshop)

---

### Generation Category

#### agent-generation

**Name and Description**: Generates agent definition files from patterns for target projects. Creates markdown files with YAML frontmatter, purpose sections, workflow steps, and important rules.

**When to Use**: When generating agents for a new project, when customizing agent behavior, when creating new agent types.

**Process Steps**: (1) Load Agent Pattern (from `patterns/agents/{agent-id}.json`), (2) Apply Customizations (override frontmatter, modify skill references, update knowledge files), (3) Render Markdown (convert pattern to markdown format with frontmatter, sections), (4) Write File (write to `{TARGET}/.cursor/agents/{name}.md` with UTF-8 encoding, validate structure).

**Integration with Agents**: Used by `template-generator` (during final artifact generation), `onboarding-architect` (for generating missing agents)

---

#### skill-generation

**Name and Description**: Generates skill definition files from patterns for target projects. Creates markdown files with YAML frontmatter, introduction, when-to-use sections, process steps, and important rules.

**When to Use**: When generating skills for a new project, when customizing skill behavior, when creating new skill types.

**Process Steps**: (1) Load Skill Pattern (from `patterns/skills/{skill-id}.json`), (2) Apply Customizations (override frontmatter, modify knowledge references, update MCP tool references), (3) Render Markdown (convert pattern to markdown format), (4) Create Skill Directory (create `{TARGET}/.cursor/skills/{skill-name}/` with SKILL.md and optional references/).

**Integration with Agents**: Used by `template-generator` (during final artifact generation), `onboarding-architect` (for generating missing skills)

---

#### knowledge-generation

**Name and Description**: Generates structured JSON knowledge files for target projects. Creates queryable reference data that agents and skills will use during development.

**When to Use**: When creating knowledge files for a new project, when importing domain knowledge, when structuring reference data.

**Process Steps**: (1) Determine Required Files (based on stack: all get naming-conventions.json, reference-sources.json; stack-specific files like api-patterns.json, cdhdr-object-classes.json), (2) Generate File Structure (JSON with `$schema`, title, description, version, queryable data), (3) Populate Data (copy naming conventions from stack definition, add style guide rules, include domain-specific patterns), (4) Write Files (write to `{TARGET}/knowledge/{filename}.json` with UTF-8 encoding, validate JSON structure).

**Integration with Agents**: Used by `knowledge-manager` (primary orchestrator)

---

#### template-generation

**Name and Description**: Generates code and document templates for target projects. Creates stack-specific code templates and standard document templates.

**When to Use**: When creating templates for a new project, when adding new template categories, when customizing existing templates.

**Process Steps**: (1) Determine Template Categories (based on stack: Python gets service-class, repository, model; TypeScript gets component, hook, service; Java gets controller, service, repository), (2) Generate Code Templates (create template files with variable placeholders, apply stack naming conventions, include imports/dependencies, add documentation comments), (3) Generate Document Templates (create implementation_plan.md, technical_spec.md, test_plan.md), (4) Variable Placeholders (use consistent placeholders like {CLASS_NAME}, {METHOD_NAME}, {FILE_NAME}).

**Integration with Agents**: Used by `template-generator` (primary orchestrator)

---

#### cursorrules-generation

**Name and Description**: Generates the `.cursorrules` file that governs AI agent behavior in generated projects. Creates complete configuration with project context, agent/skill lists, MCP server integration, and autonomous behavior rules.

**When to Use**: When generating a new project, when updating project configuration, when customizing agent behavior rules.

**Process Steps**: (1) Load Template (from `templates/factory/cursorrules-template.md`), (2) Replace Variables (project name, description, language, style guide, domain, generated date), (3) Generate Agent List (create agent table from configured agents), (4) Generate Skill List (create skill table from configured skills), (5) Generate MCP Section (create MCP server configuration table), (6) Write File (write to `{TARGET}/.cursorrules` with UTF-8 encoding).

**Integration with Agents**: Used by `template-generator` (during final artifact generation)

---

#### workflow-generation

**Name and Description**: Generates workflow configurations and documentation based on methodology and trigger sources. Configures MCP server integrations and creates workflow documentation files.

**When to Use**: When configuring project workflows, when setting up MCP server integrations, when generating workflow documentation.

**Process Steps**: (1) Parse Workflow Requirements (identify methodology, list trigger sources, list output artifacts), (2) Select Workflow Patterns (match triggers to patterns: Jira → bugfix-workflow, Confluence → feature-workflow, GitHub → bugfix-workflow), (3) Configure MCP Servers (for each trigger, configure required MCP server with authentication), (4) Generate Workflow Files (create `workflows/{pattern_name}.md` with trigger conditions, step-by-step process, artifact outputs), (5) Output Configuration (generate YAML workflow configuration).

**Integration with Agents**: Used by `workflow-designer` (primary orchestrator)

---

### Practices Category

#### practice-selection

**Name and Description**: Guides users through selecting practices (regular disciplines) that will maintain excellence, alignment, and continuous improvement. Practices are rhythms that keep teams aligned with purpose.

**When to Use**: During onboarding after methodology is selected, when user mentions "practices", "rituals", "habits", "ceremonies", request to configure team routines.

**Process Steps**: (1) Explain Practice Philosophy (practices as moments of intentional reflection, opportunities for improvement, rhythms for alignment), (2) Present Practice Categories (Daily Practices: morning intention, evening reflection, focused stand-up; Craft Practices: code as craft review, thoughtful code review, continuous refactoring; Alignment Practices: weekly learning, sprint retrospective, release blessing, quarterly alignment), (3) Customize Practices (for each selected practice, customize to team needs: time, duration, format, checklist), (4) Map Practices to Methodology (align practices with selected methodology, show overlaps, suggest enhancements), (5) Generate Practice Configuration (create `practices.yaml` with enabled practices, schedules, formats, reflection prompts).

**Integration with Agents**: Used by `requirements-architect` (during Phase 0.9 if Comprehensive depth selected)

---

#### enforcement-selection

**Name and Description**: Guides users through selecting enforcement patterns that ensure their agent system lives its values, not just states them. Enforcement translates aspirations into operational reality.

**When to Use**: During onboarding after principles are defined, when user mentions "enforcement", "quality gates", "standards", request to configure automated checks.

**Process Steps**: (1) Explain Enforcement Philosophy (values without enforcement are aspirations; enforcement ensures values are lived), (2) Present Enforcement Categories (Quality Enforcement: test coverage gate, peer review gate, documentation completeness, style consistency; Safety Enforcement: destructive action confirmation, backup before modification, security vulnerability check, production safeguard; Integrity Enforcement: axiom compliance check, purpose alignment check, transparency log), (3) Configure Thresholds (for each selected enforcement, configure thresholds: minimum coverage, reviewers, severity), (4) Configure Override Policies (define when rules can be bypassed: never, with justification, with approval), (5) Generate Enforcement Configuration (create `enforcement.yaml` with enabled enforcements, thresholds, override policies).

**Integration with Agents**: Used by `requirements-architect` (during Phase 0.8 if Comprehensive depth selected)

---

### Quality Category

#### alignment-check

**Name and Description**: Prevents Silent Misalignment by verifying mutual understanding before significant work begins. Implements the Check Alignment pattern from Augmented Coding Patterns.

**When to Use**: Before complex refactoring or architecture changes, when task involves multiple files or components, after receiving ambiguous or complex requirements, when user instructions reference concepts not fully understood, before any implementation that would take more than 10 minutes.

**Process Steps**: (1) Show Understanding (describe current state, proposed changes, questions/assumptions before implementing), (2) Surface Confusion (ask open-ended questions: "What questions do you have?", "What am I missing?"), (3) Validate Assumptions (explicitly check each assumption), (4) Get Explicit Confirmation (before proceeding, get confirmation: "I'll proceed with [summary]. If this doesn't match what you want, please stop me now.").

**Integration with Agents**: Used by `onboarding-architect` (verify understanding before major changes), can be used by any agent before significant implementations

---

#### pattern-feedback

**Name and Description**: Implements the Inductive Learning component of the 5-layer architecture. Observes patterns from development experience, generalizes them, and proposes improvements to axioms, principles, and methodologies. Embodies Axiom A10 (Learning).

**When to Use**: End of sprint/iteration (automatic review), when user mentions "what did we learn", "patterns", "retrospective", multiple similar issues encountered, explicit request to analyze patterns.

**Process Steps**: (1) Observation Collection (gather data from code reviews, test results, user interactions, workflow execution), (2) Pattern Recognition (analyze observations to identify patterns: occurs 3+ times, consistent characteristics, suggests actionable improvement), (3) Generalization (propose general rules from specific patterns: identify commonality, abstract to rule, trace to axiom, validate consistency), (4) Proposal Generation (create improvement proposals with observed pattern, proposed rule, axiom alignment, consistency check, recommended action, validation criteria), (5) Integration (when approved, integrate into appropriate layer: L0 axiom, L2 principle, L3 methodology, L4 technical).

**Integration with Agents**: Can be used by any agent during retrospectives or pattern analysis

---

#### readme-validation

**Name and Description**: Validates that the project structure documented in README.md accurately reflects the actual filesystem structure. Ensures documentation stays synchronized with the codebase as the project evolves.

**When to Use**: Before commits (validate README accuracy), after adding new agents, skills, blueprints, patterns, or templates, during CI/CD pipeline execution, during code review to verify documentation is updated alongside code changes.

**Process Steps**: (1) Scan Filesystem (count agents in `.cursor/agents/`, skills in `.cursor/skills/`, blueprints in `blueprints/`, etc.), (2) Extract README Counts (parse project structure section for documented counts), (3) Compare Counts (identify discrepancies between actual and documented), (4) Report or Update (exit with error if mismatch, or update README in place with `--update` flag).

**Integration with Agents**: Used by `onboarding-architect` (validate project state after changes), integrated into CI/CD via `.github/workflows/ci.yml`

---

### Specialized Category

#### onboarding-flow

**Name and Description**: Integrates Cursor Agent Factory into existing repositories non-destructively, preserving existing artifacts while adding missing components. Enables seamless integration of factory's agent system into repositories that already have code, configurations, and potentially some Cursor artifacts.

**When to Use**: User mentions an existing repository they want to enhance with AI agents, user says "onboard my repo", "integrate into existing project", "add agents to my codebase", user provides a path to a local repository, user wants to upgrade an older factory-generated setup. For teams, consider `team-workshop-onboarding` instead.

**Process Steps**: (1) Gather Repository Information (ask for repository path, validate exists and is directory), (2) Analyze Repository (run `factory_cli.py --analyze` to detect existing artifacts, tech stack, scenario), (3) Confirm Blueprint Selection (suggest blueprint based on tech stack detection), (4) Preview Changes (dry-run to show what will be modified), (5) Resolve Conflicts (for each conflict, ask user: keep existing / replace / rename), (6) Execute Onboarding (create backup, generate missing directories, add missing agents/skills, merge .cursorrules, add missing knowledge files), (7) Provide Summary and Next Steps (report what was created/merged/skipped, provide rollback instructions).

**Integration with Agents**: Used by `onboarding-architect` (primary orchestrator)

---

#### team-workshop-onboarding

**Name and Description**: Orchestrates a series of collaborative workshops that guide teams through vision-setting, ethics definition, technology selection, and agent design - generating a customized Cursor agent system through play and dialogue. Grounded in Axiom 0: Love, Truth, and Beauty.

**When to Use**: When a team (2+ people) wants to collaboratively design their Cursor agent system, when team alignment and shared vision are as important as technical configuration, when user says "team workshop", "collaborative onboarding", "workshop series", when multiple stakeholders need to contribute to agent system design.

**Process Steps**: Orchestrates 5 workshops: (1) Vision Quest (2-3 hours) - Future Headlines and Stakeholder Safari games to define mission and stakeholders, (2) Ethics Arena (2 hours) - Dilemma Duel and Value Auction games to establish ethical framework, (3) Stack Safari (2-3 hours) - Trade-Off Tetris and Architecture Pictionary games to explore technology, (4) Agent Assembly (3-4 hours) - Agent Trading Cards and Skill Bingo games to design agents and skills, (5) Integration Celebration (1.5-2 hours) - Demo Derby and Gratitude Circle games to finalize and celebrate. Each workshop includes opening/closing rituals, game facilitation, synthesis, and artifact generation.

**Integration with Agents**: Used by `workshop-facilitator` (primary orchestrator)

---

#### shell-platform

**Name and Description**: Handles platform-specific shell command considerations for Windows PowerShell and Unix shells. Ensures commands work correctly across different platforms.

**When to Use**: Before executing shell commands that may have platform-specific syntax, when writing git commit messages with multi-line content, when using heredoc, pipes, or other shell-specific constructs.

**Process Steps**: (1) Platform Detection (check user's OS: win32 → PowerShell, darwin/linux → bash/zsh), (2) Apply Platform-Specific Syntax (PowerShell: avoid heredoc, use multiple -m flags for git commits, use ; instead of &&; Unix: use standard bash syntax), (3) Validate Command Syntax (ensure command matches target shell).

**Integration with Agents**: Used automatically by any agent executing shell commands (local scope, asks user before applying)

---

## 5.5 PM System Components

The PM (Project Management) System includes additional agents and skills for project coordination. These are documented separately in the [PM System Documentation](../pm-system/README.md).

### PM Agents (4)

| Agent | Purpose |
|-------|---------|
| `product-owner` | Backlog management, story creation, prioritization |
| `sprint-master` | Sprint planning, standups, retrospectives |
| `task-manager` | Work decomposition, status tracking |
| `reporting-agent` | Metrics, burndown charts, health indicators |

### PM Skills (9)

| Skill | Purpose |
|-------|---------|
| `create-story` | Create user stories with acceptance criteria |
| `create-epic` | Create epics with child story structure |
| `create-task` | Create implementation tasks from stories |
| `plan-sprint` | Pull stories into sprint backlog |
| `run-standup` | Query and report current status |
| `close-sprint` | Complete sprint, calculate velocity |
| `estimate-task` | Suggest story point estimation |
| `generate-burndown` | Create burndown chart data |
| `health-check` | Team health indicators |

See [PM System README](../pm-system/README.md) for complete documentation.

---

## 6. Component Interaction Diagram

The factory components work together in a coordinated workflow during project generation:

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROJECT GENERATION FLOW                      │
└─────────────────────────────────────────────────────────────────┘

1. requirements-architect
   ├─→ requirements-gathering (5-layer questionnaire)
   │   ├─→ axiom-selection (Layer 0: A0-A10)
   │   ├─→ purpose-definition (Layer 1: Mission, Stakeholders)
   │   └─→ methodology-selection (Layer 3: Agile/Kanban/R&D)
   └─→ stack-configuration (Phase 2: Technology Stack)
       └─→ stack-builder

2. stack-builder
   └─→ stack-configuration (Match to blueprints)

3. workflow-designer
   └─→ workflow-generation (Configure workflows & MCP servers)

4. knowledge-manager
   └─→ knowledge-generation (Create JSON knowledge files)

5. template-generator
   ├─→ template-generation (Code & document templates)
   ├─→ agent-generation (Agent definition files)
   ├─→ skill-generation (Skill definition files)
   └─→ cursorrules-generation (.cursorrules file)

┌─────────────────────────────────────────────────────────────────┐
│                    ONBOARDING FLOWS                             │
└─────────────────────────────────────────────────────────────────┘

Individual Onboarding:
onboarding-architect
   ├─→ onboarding-flow (Analyze & integrate existing repo)
   ├─→ requirements-gathering (If customization needed)
   └─→ stack-configuration (If tech stack adjustment needed)

Team Onboarding:
workshop-facilitator
   ├─→ team-workshop-onboarding (5-workshop series)
   │   ├─→ axiom-selection (Vision Quest opening)
   │   ├─→ requirements-gathering (Structured questionnaires)
   │   └─→ methodology-selection (Stack Safari)
   └─→ [Generates complete system through collaborative games]

┌─────────────────────────────────────────────────────────────────┐
│                    QUALITY & IMPROVEMENT                         │
└─────────────────────────────────────────────────────────────────┘

Any Agent (before major work):
   └─→ alignment-check (Verify understanding)

Any Agent (during retrospectives):
   └─→ pattern-feedback (Learn from experience, propose improvements)

┌─────────────────────────────────────────────────────────────────┐
│                    KNOWLEDGE EXTENSION                          │
└─────────────────────────────────────────────────────────────────┘

knowledge-extender
   └─→ extend-knowledge
       ├─→ Research (web_search, read_file, user links)
       ├─→ Synthesize (templates, patterns, LLM)
       ├─→ Post-Extension Automation:
       │   ├─→ Update manifest.json (version, change_history)
       │   ├─→ Update skill-catalog.json (new skills)
       │   ├─→ Update KNOWLEDGE_FILES.md (documentation)
       │   └─→ Update CHANGELOG.md (version entry)
       └─→ Ask before git commit/push

knowledge-evolution
   └─→ update-knowledge
       ├─→ source_aggregator (fetch from adapters)
       ├─→ update_engine (merge with strategies)
       └─→ backup_manager (rollback support)

┌─────────────────────────────────────────────────────────────────┐
│                    WORKFLOW ORCHESTRATION                       │
└─────────────────────────────────────────────────────────────────┘

workflow-architect
   └─→ extend-workflow
       ├─→ Check workflow-patterns.json (existing patterns)
       ├─→ Select MCP servers (mcp-servers-catalog.json)
       ├─→ Map skills (skill-catalog.json)
       ├─→ Design phases, steps, decisions
       └─→ Generate workflow.md

debug-conductor
   └─→ 6-Phase Debugging Workflow
       ├─→ Phase 1: Error Detection (parse logs, classify)
       ├─→ Phase 2: Root Cause Analysis (trace, hypothesize)
       ├─→ Phase 3: Resolution Strategy (evaluate options)
       ├─→ Phase 4: Implementation (fix, verify)
       ├─→ Phase 5: Verification (full suite, regressions)
       └─→ Phase 6: Learning (capture pattern, update knowledge)
       
       MCP Servers: git, github, filesystem, sentry (optional)
       Skills: pipeline-error-fix, tdd, extend-workflow, grounding
```

### Key Integration Points

- **Requirements Architect** orchestrates the initial gathering phase, coordinating `requirements-gathering`, `purpose-definition`, `axiom-selection`, and `stack-configuration` skills
- **Stack Builder** receives requirements and uses `stack-configuration` to match blueprints
- **Workflow Designer** uses `workflow-generation` to configure development workflows and MCP integrations
- **Knowledge Manager** uses `knowledge-generation` to create domain knowledge files
- **Template Generator** coordinates multiple generation skills (`template-generation`, `agent-generation`, `skill-generation`, `cursorrules-generation`) to create all project artifacts
- **Onboarding Architect** uses `onboarding-flow` as primary skill, with optional `requirements-gathering` and `stack-configuration` for customization
- **Workshop Facilitator** orchestrates `team-workshop-onboarding` which internally uses `axiom-selection`, `requirements-gathering`, and `methodology-selection` during workshops
- **Alignment Check** can be invoked by any agent before significant implementations
- **Pattern Feedback** can be invoked by any agent during retrospectives or pattern analysis
- **Knowledge Extender** uses `extend-knowledge` to research, synthesize, and create new Factory artifacts with mandatory post-extension automation
- **Knowledge Evolution** uses `update-knowledge` to apply external updates with merge strategies and rollback support
- **Workflow Architect** uses `extend-workflow` to design and create sophisticated workflows from patterns, integrating MCP servers and skills
- **Debug Conductor** demonstrates the workflow system with autonomous 6-phase debugging (detection → analysis → strategy → implementation → verification → learning)

---

*This reference document describes the factory's own components. For information about components generated for target projects, see the project-specific documentation.*

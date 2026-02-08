# Changelog

All notable changes to the Antigravity Agent Factory project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

No unreleased changes.

## [4.0.0] - 2026-02-08

### Added - Test Conductor Agent & AI Skills Expansion

Major expansion of AI agent development capabilities with proactive test orchestration.

#### Test Conductor Agent
- `.agent/agents/test-conductor.md` - Proactive test orchestration with:
  - Tiered test execution (fast/medium/slow)
  - Parallel execution with pytest-xdist (`-n auto`)
  - Self-correction when tests are too slow
  - Coverage reporting with configurable thresholds
  - Watch mode for TDD workflows
  - Snapshot testing for generated outputs
  - Regression detection across runs
  - Shell-platform aware (PowerShell/bash syntax)

#### New AI Agent Skills (29)
- `advanced-retrieval` - Multi-index RAG, query decomposition
- `agent-testing` - Unit testing with mocks, LangSmith evaluation
- `agentic-loops` - ReAct pattern, reflection, planning
- `anthropic-patterns` - Claude agentic loop patterns
- `caching-optimization` - LLM response caching, memoization
- `crewai-agents` - CrewAI agent design patterns
- `database-agents` - SQL generation, text-to-SQL pipelines
- `error-handling` - Retry strategies, circuit breakers
- `filesystem-ops` - File operations, security sandboxing
- `human-in-the-loop` - Approval workflows, interrupts
- `knowledge-graphs` - Graph RAG, entity extraction
- `langchain-usage` - LangChain 1.x patterns
- `langgraph-agent-building` - LangGraph workflows
- `langsmith-prompts` - Prompt management, versioning
- `langsmith-tracing` - Debugging and tracing
- `logging-monitoring` - Structured logging, metrics
- `mcp-integration` - Model Context Protocol
- `memory-management` - Agent memory patterns
- `ocr-processing` - Image-to-text, PDF extraction
- `rag-patterns` - Document chunking, hybrid retrieval
- `security-sandboxing` - Input validation, permissions
- `speech-processing` - STT/TTS, real-time transcription
- `state-management` - LangGraph state schemas
- `streaming-realtime` - Token streaming, WebSocket
- `subagent-orchestration` - Dynamic subagent spawning
- `tool-usage` - Tool design and binding patterns
- `vision-agents` - Image analysis, visual QA
- `web-browsing` - Web scraping, browser automation

#### New Knowledge Files (23)
- `advanced-rag-patterns.json`, `agent-testing-patterns.json`
- `agentic-loop-patterns.json`, `anthropic-agentic.json`
- `api-integration-patterns.json`, `business-automation-patterns.json`
- `caching-patterns.json`, `data-pipeline-patterns.json`
- `database-agent-patterns.json`, `error-handling-patterns.json`
- `filesystem-patterns.json`, `hitl-patterns.json`
- `langsmith-prompts-patterns.json`, `memory-patterns.json`
- `ocr-patterns.json`, `speech-patterns.json`
- `state-patterns.json`, `streaming-patterns.json`
- `subagent-patterns.json`, `tool-patterns.json`
- `vision-patterns.json`, `web-browsing-patterns.json`

#### New Jinja2 Templates (15)
- `templates/ai/agents/` - base_agent, crew_agent, rag_agent, tool_agent
- `templates/ai/graphs/` - hitl_graph, simple_graph, supervisor_graph
- `templates/ai/memory/` - postgres_memory, redis_memory
- `templates/ai/rag/` - chunker, retriever
- `templates/ai/tests/` - agent_test
- `templates/ai/tools/` - api_tool, database_tool, mcp_tool

#### New Blueprint
- `blueprints/langchain-agent-platform/blueprint.json` - Full LangChain agent platform

### Fixed
- Performance test threshold increased from 5s to 10s to handle parallel execution I/O contention

---

### Added - Agent Society Protocol (ASP) Integration

Complete integration of ASP research into factory blueprints and generated projects.

#### Simplified Society API
- `lib/society/simple.py` - 3-line society creation with verified coordination
- `lib/society/presets.py` - Pattern presets (supervisor-worker, peer, pipeline, hierarchical)
- Updated `lib/society/__init__.py` to export simplified API (v1.2.0)

#### Portable Agent Behavior Protocol (PABP)
- `lib/society/pabp/bundle.py` - Bundle creation with integrity verification
- `lib/society/pabp/manifest.py` - Manifest schema and cryptographic signing
- `lib/society/pabp/transfer.py` - Export/import/verify operations

#### Decision Guidance Knowledge Files
- `knowledge/trust-tier-decision-matrix.json` - Tier selection criteria
- `knowledge/coordination-pattern-selection.json` - Pattern selection guidance
- `knowledge/asp-quick-reference.json` - Quick reference card

#### ASP Skills
- `.agent/skills/society-tier-selection/SKILL.md` - Interactive tier selection
- `.agent/skills/export-agent-bundle/SKILL.md` - Bundle export guidance

#### Society Templates
- `templates/ai/society/context.py.tmpl` - Society context setup
- `templates/ai/society/contracts.py.tmpl` - Contract patterns
- `templates/ai/society/README.md.tmpl` - Module documentation
- `templates/docs/ASP_README_SECTION.md.tmpl` - README section template

#### Documentation
- `docs/ASP_VALUE_PROPOSITION.md` - Value explanation with quantified benefits
- `docs/guides/TRUST_TIER_SELECTION.md` - Tier selection guide
- `docs/guides/SOCIETY_INTEGRATION_GUIDE.md` - Integration guide

#### Tests
- `tests/lib/society/test_simple_api.py` - Simple API unit tests
- `tests/lib/society/pabp/test_bundle.py` - PABP unit tests
- `tests/knowledge/test_tier_selection.py` - Knowledge validation tests
- `tests/integration/test_society_blueprint_generation.py` - Blueprint integration tests

### Changed
- `blueprints/multi-agent-systems/blueprint.json` - Added ASP knowledge, templates, skills
- `blueprints/ai-agent-development/blueprint.json` - Added ASP knowledge, templates, skills

## [3.15.0] - 2026-02-08

### Added - Update System & AI/ML Stack Expansion

Major expansion of the AI/ML stack with comprehensive update infrastructure.

#### Update System Infrastructure
- `knowledge/version-registry.json` - Central source of truth for all package versions
- `.agent/skills/version-check/SKILL.md` - On-demand version audit skill
- `scripts/updates/blueprint_version_updater.py` - Automated blueprint version updates
- `.agent/agents/git-specialist.json` - Git operations and pre-commit automation
- `tests/integration/test_update_system.py` - 44 comprehensive update system tests

#### New AI Blueprints (5)
- `voice-ai-agents` - Voice AI with Whisper, ElevenLabs, Deepgram
- `multimodal-ai` - Vision, audio, text multimodal processing
- `llm-inference-optimization` - vLLM, TensorRT-LLM, llama.cpp
- `synthetic-data-generation` - LLM-powered synthetic data
- `ai-observability-platform` - LangFuse, Arize Phoenix, MLflow

#### New Knowledge Files (12)
- `instructor-patterns.json` - Structured output patterns
- `dspy-patterns.json` - DSPy programming patterns
- `guardrails-patterns.json` - NeMo/Guardrails AI patterns
- `agent-memory-patterns.json` - Mem0, Zep, LangChain memory
- `llamaindex-patterns.json` - LlamaIndex 0.12+ patterns
- `pydantic-ai-patterns.json` - PydanticAI agent patterns
- `embedding-models.json` - Embedding model comparison
- `document-processing-patterns.json` - Docling, Unstructured.io
- `scikit-learn-patterns.json` - ML preprocessing and pipelines
- `tensorflow-patterns.json` - TensorFlow/Keras patterns
- `pandas-patterns.json` - Data manipulation patterns
- `data-engineering-patterns.json` - ETL and pipeline patterns

#### New Templates (46+)
- 8 RAG templates (ingestion, retrieval, reranking, evaluation)
- 6 fine-tuning templates (LoRA, QLoRA, PEFT, SFT)
- 8 agent templates (LangChain, CrewAI, ReAct, multi-agent)
- 4 voice templates (STT, TTS, realtime, voice agent)
- 4 multimodal templates (vision, generation, document, multimodal RAG)
- 10 ML training templates (PyTorch, HPO, distributed)
- 5 model serving templates (FastAPI, vLLM, Triton)

### Changed
- Updated 10+ AI blueprints to LangChain 1.2+, CrewAI 1.9+, current LLM models
- Updated web blueprints to React 19.2+, Next.js 16.1+, FastAPI 0.128+
- Updated enterprise blueprints to Spring 4.0+, .NET 10+
- Updated blockchain blueprints to Anchor 0.32+, Solidity 0.8.30+
- Optimized pytest startup (disabled heavy plugins by default)
- Enhanced pre-commit runner with 8 validation scripts

### Fixed
- Async test failures (installed pytest-asyncio)
- voice-ai-agents blueprint missing standard agents/skills
- Performance test threshold for Windows compatibility
- Unicode encoding in dependency_validator.py

## [3.14.0] - 2026-02-05

### Added - Documentation Excellence

Comprehensive visual and written documentation bringing full transparency to the system architecture.

#### Complete Study Guide: `docs/COMPLETE_GUIDE.md`

A structured 8-12 hour learning journey from zero knowledge to full system understanding:

| Part | Content | Reading Time |
|------|---------|--------------|
| Part 1 | Introduction, Vision, Factory vs Generated | 15-20 min |
| Part 2 | 5-Layer Architecture, Axioms A0-A5 | 1-2 hours |
| Part 3 | Agents, Skills, Knowledge, Blueprints | 2-3 hours |
| Part 4 | Guardian, Memory, Verification, Workflows | 2-3 hours |
| Part 5 | Quickstart, Extension, Troubleshooting | 1-2 hours |
| Part 6 | Lean 4, Society, Research, Contributing | 2+ hours |

Includes Glossary (15 terms), 3 Appendices (Reading Order, Role Paths, Quick Reference Cards).

#### Architecture Diagrams: `diagrams/`

14 comprehensive Mermaid diagram files with 150+ individual diagrams:

| Category | Files |
|----------|-------|
| Formal Verification | `formal-verification.md`, `guardian-state-machine.md` |
| Agent System | `agent-coordination.md`, `memory-system.md` |
| Core System | `knowledge-management.md`, `configuration-resolution.md`, `pattern-library.md` |
| Quality & Learning | `security-pipeline.md`, `quality-gates.md`, `learning-loops.md` |
| Process & Workflow | `onboarding-flows.md`, `cli-architecture.md`, `template-pipeline.md` |
| Supporting Systems | `integrations.md` |

#### Conceptual Mindmaps: `diagrams/mindmaps.md`

12 hierarchical mindmaps providing visual navigation for all major concepts:

1. System Overview
2. 5-Layer Architecture
3. Axiom Derivation
4. Agent Ecosystem (16 agents)
5. Skills Taxonomy (40+ skills)
6. Knowledge Files (89 files)
7. Blueprints (27 blueprints)
8. Guardian System
9. Memory System
10. Workflow System
11. Onboarding Paths
12. Verification Ecosystem

### Added - Agent Society Integration
- Agent Society Integration layer (SocietyContext, AgentSocietyBridge, MessageRouter)
- Verified communication skill with documentation
- Society dashboard CLI for monitoring (`cli/society_dashboard.py`)
- Integration guide (`docs/guides/VERIFIED_AGENT_INTEGRATION.md`)
- Working demo script (`scripts/verified_agents_demo.py`)
- 29 integration tests (1401 total tests)

## [3.13.0] - 2026-02-05

### Added - Agent Society Verification Implementation

Complete implementation of the Agent Society Verification system, bringing the v3.12.0 design to life with a production-ready Python library.

#### Core Library: `lib/society/`

| Module | Purpose |
|--------|---------|
| `events/` | Event sourcing with cryptographic hash chains |
| `verification/` | Axiom compliance monitoring (A0-A5) |
| `contracts/` | Agent contracts with capability/obligation verification |
| `trust/` | Identity, reputation, and trust delegation |
| `society/` | Governance patterns and communication protocols |
| `blockchain/` | Merkle trees, anchoring, Solana integration |
| `hybrid/` | Unified verification system with escalation |

#### Key Features Implemented

- **Event Sourcing**: Append-only event store with SHA-256 hash chains
- **6 Axiom Verifiers**: A0 (SDG), A1 (Love), A2 (Truth), A3 (Beauty), A4 (Guardian), A5 (Memory)
- **Agent Contracts**: Formal agreements with capability, obligation, prohibition verification
- **Cryptographic Identity**: Ed25519-style keypairs for agent signing
- **Reputation System**: Time-decaying reputation based on axiom compliance
- **Trust Graph**: Direct and transitive trust with delegation
- **5 Governance Patterns**: Flat Democracy, Meritocracy, Hierarchy, Federation, DAO
- **3 Communication Protocols**: Direct, Broadcast, Consensus
- **Merkle Tree Anchoring**: Efficient batching with proof generation
- **Solana Integration**: Stub client for blockchain anchoring
- **Attestation Registry**: Cryptographic attestations for verifiable claims
- **Escalation Manager**: Violation tracking with policy-based routing

#### New Files

| Path | Description |
|------|-------------|
| `lib/` | New library root for reusable modules |
| `lib/society/__init__.py` | Society verification library entry point |
| `lib/society/events/` | Event store, hash chain, schema |
| `lib/society/verification/` | Axiom monitor and 6 verifier implementations |
| `lib/society/contracts/` | Contract schema, registry, verifier |
| `lib/society/trust/` | Identity, reputation, trust delegation |
| `lib/society/society/` | Governance patterns, communication protocols |
| `lib/society/blockchain/` | Merkle tree, anchors, Solana client, attestations |
| `lib/society/hybrid/` | Unified system, escalation manager |
| `tests/lib/society/` | Comprehensive test suite (400+ test cases) |

#### CI/CD Updates

- Added society library tests to fast test stage
- Extended linting coverage to `lib/` directory
- Included `lib/` in coverage reporting

#### Usage Example

```python
from lib.society import HybridVerificationSystem, AgentEvent

# Create unified verification system
system = HybridVerificationSystem.create_default(with_blockchain=True)

# Record and verify an agent event
result = system.record_event(event)

if result.overall_pass:
    print("Event verified against all axioms")
else:
    print(f"Violations: {result.axiom_result.violations}")
```

#### Philosophy Alignment

Every component maintains alignment with SDG - Love - Truth - Beauty:
- Events are transparent (Truth) and immutable (Guardian)
- Contracts prioritize user wellbeing (Love)
- Verification is simple and elegant (Beauty)
- Reputation rewards sustainable behavior (SDG)
- Escalation protects against harm (Guardian)

---

## [3.12.0] - 2026-02-05

### Added - Agent Society Verification Architecture

Design documentation and knowledge patterns for extending formal verification to dynamic multi-agent systems with verified communication, contracts, and behavior.

#### Architectural Approaches

| Approach | Description |
|----------|-------------|
| **Event Sourcing + Signed Audit Trail** | Immutable, cryptographically signed event chains |
| **Agent Contracts** | Formal agreements with capabilities, obligations, prohibitions |
| **Blockchain Integration** | On-chain anchoring and smart contract enforcement |
| **Hybrid Architecture** | Local speed with blockchain trust escalation |

#### Society Construction Patterns

| Pattern | Description |
|---------|-------------|
| **Flat Democracy** | All agents equal, consensus voting |
| **Meritocracy** | Trust earned through verified behavior |
| **Hierarchy** | Supervisor-worker with delegated authority |
| **Federation** | Autonomous teams with shared protocols |
| **DAO-style** | Governance by token/stake/contribution |

#### Trust and Reputation

- Cryptographic agent identity (Ed25519)
- Reputation scoring based on axiom compliance
- Trust delegation with decay
- Escalation thresholds for violations

#### New Files

| File | Purpose |
|------|---------|
| `docs/design/AGENT_SOCIETY_VERIFICATION.md` | Comprehensive architecture design document |
| `knowledge/agent-society-verification.json` | Structured knowledge for patterns and schemas |
| `templates/ai/society/event-schema.json.tmpl` | Event schema template for agent actions |
| `templates/ai/society/agent-contract.json.tmpl` | Agent contract template |
| `templates/ai/society/verification-monitor.py.tmpl` | Axiom compliance monitor |
| `templates/ai/society/audit-trail.py.tmpl` | Signed audit trail implementation |

#### Implementation Roadmap

1. **Phase 1 (Complete)**: Static formal verification (Lean 4)
2. **Phase 2 (Planned)**: Event sourcing + local verification
3. **Phase 3 (Planned)**: Agent contracts + breach detection
4. **Phase 4 (Planned)**: Blockchain integration
5. **Phase 5 (Planned)**: Society patterns + reputation
6. **Phase 6 (Planned)**: Full hybrid system

#### Philosophy

All verification patterns maintain alignment with foundational axioms:
- A0 (SDG): Verification serves sustainable development
- A1 (Love): Contracts prioritize user wellbeing
- A2 (Truth): Audit trails ensure transparency
- A3 (Beauty): Simple, elegant verification mechanisms
- A4 (Guardian): Monitor agents embody guardian protocol
- A5 (Memory): Event history requires appropriate consent

---

## [3.11.0] - 2026-02-05

### Added - Formal Verification System

Mathematical proofs using Lean 4 that verify the Factory's core architecture satisfies its foundational axioms. This enables a **trust chain** from Factory to generated projects.

#### Proof System Architecture

| Component | File(s) | What's Proven |
|-----------|---------|---------------|
| **Axioms** | `proofs/Axioms.lean` | A0-A5 formalized with derivation rules |
| **Guardian States** | `proofs/Guardian/States.lean` | State machine with invariants |
| **Guardian Transitions** | `proofs/Guardian/Transitions.lean` | Monotonic escalation, proper de-escalation |
| **Guardian Safety** | `proofs/Guardian/Safety.lean` | State preservation, user notification, harm prevention |
| **Guardian Invariants** | `proofs/Guardian/Invariants.lean` | Inductive invariants preserved by all transitions |
| **Memory Types** | `proofs/Memory/Types.lean` | Layer constraints, memory structure |
| **Memory Consent** | `proofs/Memory/Consent.lean` | User consent required for all permanent memories |
| **Layer Immutability** | `proofs/Layers/Immutability.lean` | L0-L2 (Axioms, Purpose, Principles) are immutable |
| **Project Templates** | `proofs/Project/Templates.lean` | Blueprint-specific state machine examples |

#### Trust Chain

```
Factory Proofs (verified) → Generated Project Proofs → Team Extensions → All Verifiable
```

Every generated project inherits the Factory's proven foundations and can extend with project-specific proofs.

#### Attestation System

| Method | Cost | Description |
|--------|------|-------------|
| **Git + GPG** | Free | SHA-256 checksums with GPG signature |
| **Sigstore/Cosign** | Free | SLSA provenance via transparency logs |

#### New Files

| File | Purpose |
|------|---------|
| `proofs/lean-toolchain` | Lean 4 version lock (v4.17.0) |
| `proofs/lakefile.lean` | Lean 4 project configuration |
| `proofs/Axioms.lean` | Core axiom formalization |
| `proofs/Guardian/*.lean` | State machine proofs (4 files) |
| `proofs/Memory/*.lean` | Consent proofs (2 files) |
| `proofs/Layers/Immutability.lean` | Layer protection proofs |
| `proofs/Project/Templates.lean` | Blueprint templates |
| `proofs/README.md` | Proof system documentation |
| `scripts/verify_proofs.sh` | Unified verification script |
| `scripts/generate_attestation.sh` | Cryptographic attestation generator |
| `docs/VERIFICATION.md` | Complete verification guide |
| `knowledge/formal-verification.json` | Structured knowledge file |

#### CI/CD Integration

New GitHub Actions workflow `.github/workflows/verify-proofs.yml`:

| Job | Purpose |
|-----|---------|
| `verify-proofs` | Install Lean 4, run `lake build`, generate checksums |
| `generate-attestation` | Create JSON attestation with commit metadata |

Runs on push/PR to `main` and `develop` when `proofs/**` files change.

#### Templates for Generated Projects

| Template | Purpose |
|----------|---------|
| `templates/proofs/lakefile.lean.tmpl` | Project-specific Lean configuration |
| `templates/proofs/Project/StateMachines.lean.tmpl` | Blueprint-specific state machines |
| `templates/proofs/README.md.tmpl` | Project proof documentation |
| `templates/scripts/verify_proofs.sh.tmpl` | Project verification script |

#### Philosophy

> "Trust, but verify - mathematically."

- **Love**: Free proofs accessible to all (no paid services required)
- **Truth**: Mathematical certainty that can be verified by anyone
- **Beauty**: Elegant, minimal proofs that capture essential properties

### Changed

- **README.md**: Added Formal Verification section, updated version to 3.11.0
- **Project Structure**: Added `proofs/` directory documentation

---

## [3.10.0] - 2026-02-04

### Added - Configurable Path System

Comprehensive configurable path system enabling cross-platform portability and custom directory structures.

#### PathResolver Utility Class

New `PathResolver` class in `scripts/core/config_manager.py` for consistent path resolution:

| Method | Description |
|--------|-------------|
| `get_directory(name)` | Get configured directory path |
| `get_skill_path(name)` | Get skill directory path |
| `get_agent_path(name)` | Get agent file path |
| `get_knowledge_path(file)` | Get knowledge file path |
| `get_template_path(*parts)` | Get template file path |
| `get_blueprint_path(id)` | Get blueprint directory |
| `get_workflow_path(*parts)` | Get workflow file path |

#### Configurable Directories

New `directories` section in `.agent/config/settings.json`:

| Directory | Default | Environment Variable |
|-----------|---------|---------------------|
| knowledge | `knowledge/` | `FACTORY_KNOWLEDGE_DIR` |
| skills | `.agent/skills/` | `FACTORY_SKILLS_DIR` |
| agents | `.agent/agents/` | `FACTORY_AGENTS_DIR` |
| templates | `templates/` | `FACTORY_TEMPLATES_DIR` |
| workflows | `workflows/` | `FACTORY_WORKFLOWS_DIR` |
| blueprints | `blueprints/` | `FACTORY_BLUEPRINTS_DIR` |
| patterns | `patterns/` | `FACTORY_PATTERNS_DIR` |
| + 7 more | ... | ... |

#### New Documentation

- `docs/PATH_CONFIGURATION.md` - Comprehensive guide for path configuration
- Environment variable override documentation
- Platform-specific guidance (Windows, Linux, macOS, Docker, WSL)
- Migration guide for upgrading from hardcoded paths

### Changed

- **Skills**: 5 priority skills updated to use `{PYTHON_PATH}` placeholder instead of hardcoded Windows paths
  - `shell-platform`, `agent-generation`, `skill-generation`, `commit-release`, `workshop-export`
- **Agents**: 11 agent files updated with configurable path documentation
- **Workflows**: 8 key workflows updated with path configuration notes
- **Templates**: CI/CD templates now use `{{ TEST_PATH | default("tests/") }}` syntax
- **Blueprints**: 4 blueprint JSON files use `${PYTHON_PATH}` instead of `C:\App\Anaconda\python.exe`

### Fixed

- Hardcoded Windows paths (`C:\App\Anaconda\python.exe`) that prevented cross-platform usage
- Inconsistent path references across 100+ files
- Non-portable tool paths in skills and blueprints

---

## [3.8.1] - 2026-02-03

### Added - Skill-First Principle Enforcement

Strengthened commitment to following established skills and workflows.

#### New Rule 0: Skill-First Principle (CRITICAL)

| Requirement | Description |
|-------------|-------------|
| Recognize triggers | Check if request matches skill trigger words |
| Read the skill | Load SKILL.md before executing |
| Follow the workflow | Execute defined steps in order |
| Never skip steps | Every step exists for quality and traceability |

#### Enhanced Available Skills Table

Added "Trigger Words" column to make skill activation explicit:

| Skill | Trigger Words |
|-------|---------------|
| `commit-release` | "commit", "push", "git add" |
| `express-onboarding` | "onboard", "get started" |
| `knowledge-generation` | "create knowledge" |
| ... | (all skills now have triggers) |

#### Strengthened Rule 8

- Added explicit reference to `commit-release` skill
- Added "STOP. Read the skill first" reminder
- Added violation consequence statement

**Lesson Learned (A10):** Skills exist to ensure quality. Skipping them produces incomplete work and wastes time.

---

## [3.9.0] - 2026-02-03

### Added - Advanced AI Agent Workshops and Documentation

Major expansion of AI framework workshops with LangSmith, Anthropic Claude, and Deep Research patterns. Added readable markdown documentation for all workshops.

#### New Learning Workshops (3 new files)

| ID | Workshop | Stack | Level |
|----|----------|-------|-------|
| **L16** | LangSmith Observability | LangSmith | Intermediate |
| **L17** | Anthropic Claude Agents with Tool Use | Claude + MCP | Intermediate |
| **L18** | Deep Research Agents | LangGraph + Research Tools | Advanced |

#### Workshop Documentation System

New human-readable markdown documentation for all 18 workshops:

| Component | Description |
|-----------|-------------|
| `docs/workshops/` | New folder with markdown for all workshops |
| `docs/workshops/README.md` | Index with catalog by category |
| `docs/workshops/L{N}_{name}.md` | Individual workshop docs (18 files) |
| `scripts/docs/generate_workshop_docs.py` | Generator to convert JSON to Markdown |

#### L16: LangSmith Observability

- Tracing and debugging LLM applications
- Dataset creation and management
- Evaluation pipelines with custom evaluators
- Prompt iteration and A/B testing

#### L17: Anthropic Claude Agents

- Anthropic philosophy on safe AI agents
- Tool use with Claude's native API
- Agentic loops with error handling
- Model Context Protocol (MCP) integration

#### L18: Deep Research Agents

- Multi-step research with iterative refinement
- Chain-of-thought and reflection patterns
- Source discovery and credibility scoring
- Synthesis with proper citation

#### Updated Learning Path

AI Engineer path now includes 9 workshops:
```
L7 → L3 → L16 → L8 → L17 → L18 → L5 → L6 → L15
```

#### Workshop Counts

| Category | Count | Workshops |
|----------|-------|-----------|
| Blockchain | 3 | L1, L2, L4 |
| AI Frameworks | 8 | L3, L5, L6, L7, L8, L16, L17, L18 |
| Web Fullstack | 3 | L9, L10, L11 |
| Cloud Native | 2 | L12, L13 |
| Data & ML | 2 | L14, L15 |
| **Total** | **18** | |

---

## [3.8.2] - 2026-02-03

### Added - LangGraph Stateful Workflows Workshop

Added dedicated workshop for LangGraph, the critical framework for building stateful agent workflows.

| ID | Workshop | Stack | Level |
|----|----------|-------|-------|
| **L3** | LangGraph Stateful Agent Workflows | LangGraph 0.2+ | Intermediate |

**Learning Objectives:**
- StateGraph architecture: nodes, edges, conditional routing
- State schemas with TypedDict and Annotated reducers
- Human-in-the-loop with checkpoints and interrupts
- Supervisor-worker multi-agent patterns

**Exercises:**
- State management and routing
- Human approval workflow with MemorySaver

**Prerequisites:** L7 LangChain Fundamentals

---

## [3.8.0] - 2026-02-03

### Added - Learning Workshop Ecosystem

Major expansion: 12 new structured learning workshops covering modern technology stacks, built with parallel agent execution for efficiency.

#### New Learning Workshops (12 new files)

| Category | ID | Workshop | Stack |
|----------|-----|----------|-------|
| **Blockchain** | L1 | Ethereum Smart Contracts | Solidity + Hardhat |
| **Blockchain** | L2 | Bitcoin & Lightning | Bitcoin Script + LND |
| **AI Frameworks** | L5 | CrewAI Multi-Agent | CrewAI |
| **AI Frameworks** | L6 | Hugging Face Transformers | Transformers + PEFT |
| **AI Frameworks** | L7 | LangChain Agent Development | LangChain 0.3+ |
| **AI Frameworks** | L8 | RAG Systems | LangChain + Vector DB |
| **Web Fullstack** | L9 | Modern React | React 18+ |
| **Web Fullstack** | L10 | Next.js Fullstack | Next.js 14+ |
| **Web Fullstack** | L11 | FastAPI Production | FastAPI |
| **Cloud Native** | L12 | Kubernetes Production | Kubernetes |
| **Cloud Native** | L13 | Docker Containerization | Docker |
| **Data & ML** | L14 | PyTorch Deep Learning | PyTorch 2.0+ |
| **Data & ML** | L15 | LLM Fine-Tuning | HuggingFace + PEFT |

#### Workshop Structure

Each workshop follows a 5-phase methodology (2.5 hours total):
- **Concept** (30 min): Theory, architecture diagrams, mental models
- **Demo** (30 min): Live coding walkthrough
- **Exercise** (45 min): Guided hands-on practice with starter code
- **Challenge** (30 min): Independent problem-solving
- **Reflection** (15 min): Key takeaways, self-assessment

#### New Documentation

| File | Description |
|------|-------------|
| `docs/LEARNING_WORKSHOPS.md` | Comprehensive guide with catalog, learning paths, prerequisites, and usage instructions |

#### Parallel Agent Execution

Built using 4 concurrent agents for maximum efficiency:
- Agent 1: Blockchain workshops (L1, L2)
- Agent 2: AI framework workshops (L5, L6, L8)
- Agent 3: Web + Cloud workshops (L9-L13)
- Agent 4: Data/ML workshops (L14, L15)

#### Total Workshop Count

| Category | Count | Workshops |
|----------|-------|-----------|
| Blockchain | 3 | L1, L2, L4 |
| AI Frameworks | 5 | L3, L5, L6, L7, L8 |
| Web Fullstack | 3 | L9, L10, L11 |
| Cloud Native | 2 | L12, L13 |
| Data & ML | 2 | L14, L15 |
| **Total** | **15** | |

---

## [3.7.0] - 2026-02-02

### Added - Comprehensive Workflow System Expansion

Major expansion of the workflow system from 1 to 21 workflows across 8 categories, enabling intelligent automation for all stacks.

#### New Workflows (20 new files)

| Category | Workflows | Description |
|----------|-----------|-------------|
| **Universal** | feature-development, bugfix-resolution, code-review, tdd-cycle, release-management | Core development workflows |
| **Quality** | quality-gate, bdd-driven-development, security-audit | Quality assurance workflows |
| **Agile** | sprint-planning, sprint-closure, daily-standup, backlog-refinement | Agile ceremony automation |
| **Blockchain** | smart-contract-audit | Blockchain security workflow |
| **Trading** | trading-strategy-pipeline | Algo trading development |
| **SAP** | rap-development, cap-service-development | SAP platform workflows |
| **AI/ML** | multi-agent-orchestration, rag-pipeline-development | AI system development |
| **Operations** | cicd-pipeline, incident-response | DevOps workflows |

#### New Skill

| Skill | Description |
|-------|-------------|
| `commit-release` | Safe commit workflow with auto-sync, changelog updates, A10 (Learning) |

#### Pre-commit Hook Improvement

Fixed pre-commit hook to embody A10 (Learning):
- **Targeted sync**: Only syncs artifacts for changed directories (O(changed) not O(all))
- **Auto-syncs** and auto-stages instead of blocking developers
- Only **blocks** for unfixable issues (secrets, syntax errors)
- Uses `--fast` flag for file-based test counting (~100x faster than pytest collection)
- Extracts changed dirs from staged files, passes to `--dirs` flag

#### Documentation Updates

| File | Changes |
|------|---------|
| `docs/reference/WORKFLOW_PATTERNS.md` | Added workflow catalog and selection guide |
| `docs/WORKFLOW_AUTHORING.md` | Added available workflows section |
| `README.md` | Updated to reflect 21 workflows |
| `knowledge/workflow-patterns.json` | Added all 20 new workflow entries |

#### Test Coverage

| Test File | Tests |
|-----------|-------|
| `tests/validation/test_workflow_structure.py` | 14 tests covering structure, naming, sections, and documentation |

---

## [3.6.0] - 2026-02-02

### Added - Commit Routine with Changelog Integration

New Rule 8 in `.agentrules` that ensures changelog updates are part of every significant commit.

| Step | Action |
|------|--------|
| 1 | Analyze changes (git status, git diff) |
| 2 | Determine if changelog entry is required |
| 3 | Update CHANGELOG.md before committing |
| 4 | Stage all related files together |
| 5 | Commit with conventional message |
| 6 | Push to remote |

This ensures atomic commits with proper documentation.

---

### Added - Value Propagation Layers for Generated Projects

Major feature: Every generated project now receives a comprehensive 4-layer value system that enables autonomous operation, self-healing CI/CD, and independent knowledge evolution.

#### Value Propagation Architecture

| Layer | Name | Components | Always Included |
|-------|------|------------|-----------------|
| **Layer 0** | Foundation | grounding-verification, alignment-check, research-first | Yes |
| **Layer 1** | Development Autonomy | ci-monitor, pipeline-error-fix, debug-conductor | Yes |
| **Layer 2** | Knowledge Independence | knowledge-extender, knowledge-evolution | Yes |
| **Layer 3** | PM Integration | PM agents, PM skills, backend adapters | Opt-in |

#### New Pattern Files (5 files)

| File | Purpose |
|------|---------|
| `patterns/agents/debug-conductor-project.json` | Autonomous debugging for CI/CD and test failures |
| `patterns/skills/ci-monitor-project.json` | Continuous CI/CD monitoring with auto-detection |
| `patterns/skills/pipeline-error-fix-project.json` | Systematic pipeline error fixing |
| `patterns/skills/research-first-project.json` | Research existing solutions before building |
| `patterns/skills/alignment-check.json` | Verify understanding before major implementations |

#### Blueprint Updates (27 blueprints)

All blueprints now include:
- `knowledge-extender` and `knowledge-evolution` agents
- `debug-conductor-project` agent
- `grounding-verification`, `alignment-check`, `research-first-project` skills
- `ci-monitor-project`, `pipeline-error-fix-project` skills
- `pmIntegration` section with opt-in PM agents and skills

#### PM Integration (Opt-in)

| Component | Description |
|-----------|-------------|
| **4 PM Agents** | product-owner, sprint-master, task-manager, reporting-agent |
| **6 PM Skills** | create-story, create-epic, create-task, plan-sprint, run-standup, close-sprint |
| **4 Backends** | GitHub, Jira, Linear, Azure DevOps |

#### Test Coverage

| Test File | Tests | Coverage |
|-----------|-------|----------|
| `tests/validation/test_value_propagation.py` | 29 | Blueprint completeness, pattern existence, schema validation, generation script |

#### Documentation Updates

| File | Changes |
|------|---------|
| `docs/ONBOARDING_GUIDE.md` | Added "Value Propagation Features" section |
| `docs/GETTING_STARTED.md` | Added "Understanding Value Propagation" section |
| `docs/QUICKSTART.md` | Added value propagation quick reference |
| `docs/reference/GENERATED_OUTPUT.md` | Added section 3.6 documenting layers |
| `.agent/skills/express-onboarding/SKILL.md` | Added value layers to celebration |
| `.agent/skills/onboarding-flow/SKILL.md` | Added value propagation section |

---

### Added - Workflow System Architecture

Debug-conductor agent and CI/CD monitoring capabilities as a factory-level feature.

#### New Components

| Component | Description |
|-----------|-------------|
| `debug-conductor` agent | Autonomous debugging with 6-phase workflow |
| `ci-monitor` skill | Continuous pipeline monitoring |
| `pipeline-error-fix` skill | Systematic error detection and fixing |
| Workflow patterns | Phase-based workflow with decision points |

#### Workflow Philosophy

> "Every bug is a gift - an opportunity to improve the system and prevent future failures."

6-Phase Debug Workflow:
1. Error Detection - Parse logs, identify failure type
2. Root Cause Analysis - Trace origin, analyze context
3. Direct Fix - Implement targeted fix
4. Alternative Resolution - Refactor or create new tests
5. Verification - Test fix, validate
6. Learning - Document patterns for future prevention

---

### Added - Reactive Artifact Indexing

Performance optimization for instant pre-commit validation.

#### Features

| Feature | Description |
|---------|-------------|
| Reactive indexing | Index artifacts on change, not on every commit |
| Instant validation | Pre-commit checks complete in <1 second |
| Directory-based triggers | Only re-index changed directories |

---

### Added - Research-First Behavior Integration

Anthropic-aligned research-first pattern embedded in agent behavior.

#### Pattern

| Step | Action |
|------|--------|
| 1 | Recognize trigger (is this something others have solved?) |
| 2 | Research existing solutions |
| 3 | Document findings |
| 4 | Test existing solution |
| 5 | Build on top (not from scratch) |
| 6 | Contribute back |

#### Philosophy

> "Each researched pattern benefits all future work in this project and potentially other projects."

---

## [3.5.0] - 2026-01-31

### Added - Unified Artifact Sync System & YAML Validation

Comprehensive automation for keeping documentation synchronized with codebase artifacts, plus enhanced pre-commit validation.

#### Unified Artifact Sync System

| Component | Description |
|-----------|-------------|
| `sync_config.json` | Configuration-driven artifact definitions |
| `sync_artifacts.py` | Unified sync engine with multiple strategies |
| Pre-commit Integration | Intelligent directory-based sync triggers |

##### Artifacts Synchronized

| Artifact | Source | Synced To |
|----------|--------|-----------|
| Agents | `.agent/agents/*.md` | README.md (count + tree) |
| Skills | `.agent/skills/*/SKILL.md` | README.md (count) |
| Blueprints | `blueprints/*/blueprint.json` | README.md, BLUEPRINTS.md |
| Patterns | `patterns/**/*.json` | README.md (count) |
| Knowledge | `knowledge/*.json` | README.md, manifest.json, KNOWLEDGE_FILES.md |
| Templates | `templates/**/*` | README.md (count) |
| Tests | `tests/**/*.py` | TESTING.md (counts by category) |

##### Sync Strategies

| Strategy | Purpose |
|----------|---------|
| `count` | Update numeric counts in markdown |
| `json_field` | Update JSON file fields |
| `category_counts` | Sync categorized counts (tests) |
| `tree_annotation` | Update directory tree annotations |

#### YAML Frontmatter Validation

| Feature | Description |
|---------|-------------|
| Pre-commit hook | Validates YAML frontmatter in staged markdown files |
| Standalone validator | `scripts/validation/validate_yaml_frontmatter.py` |
| Error messages | Clear, actionable validation errors |
| Test coverage | 25 tests covering all edge cases |

##### New Files

| File | Purpose |
|------|---------|
| `scripts/validation/sync_config.json` | Artifact sync configuration |
| `scripts/validation/sync_artifacts.py` | Unified sync engine |
| `scripts/validation/validate_yaml_frontmatter.py` | YAML frontmatter validator |
| `tests/unit/test_sync_artifacts.py` | Sync engine tests (23 tests) |
| `tests/validation/test_yaml_frontmatter.py` | Frontmatter tests (25 tests) |

#### Session Path Cache

Performance optimization for tool path resolution.

| Feature | Description |
|---------|-------------|
| Location | `.agent/cache/session-paths.json` |
| Purpose | Cache verified tool paths to skip resolution |
| Auto-update | Automatically updates when paths are resolved |
| Machine-specific | Gitignored, adapts to each developer |

##### Resolution Order (Updated)

```
1. Session Cache     → Fastest, already verified
2. Environment Var   → $env:PYTHON_PATH, etc.
3. Auto-detect       → shutil.which() / PATH lookup
4. Fallback Paths    → Try each until one exists
```

#### Pre-commit Hook Enhancements

| Step | Description |
|------|-------------|
| 1 | Secret scanning (blocks commits) |
| 2 | JSON syntax validation |
| 3 | **NEW**: YAML frontmatter validation |
| 4 | Version sync across files |
| 5 | **NEW**: Unified artifact sync |
| 6 | README structure update |

### Changed

| Change | Description |
|--------|-------------|
| `ConfigManager` | Added session cache integration |
| `install_hooks.py` | Added YAML validation and unified sync steps |
| `docs/CONFIGURATION.md` | Documented session cache and artifact sync |
| `docs/TESTING.md` | Updated test counts and structure |

### Documentation

| File | Changes |
|------|---------|
| `docs/CONFIGURATION.md` | Session cache section, artifact sync section |
| `docs/TESTING.md` | Test count sync documentation |
| `.gitignore` | Added `.agent/cache/` for session paths |

---

## [3.4.0] - 2026-01-31

### Added - Inductive Memory System

User-validated learning system that enables the Factory to learn from experience while protecting core axioms.

#### Architecture

| Component | Description |
|-----------|-------------|
| Semantic Memory | Long-term validated knowledge (ChromaDB) |
| Episodic Memory | Session-based observations |
| Proposal Queue | Pending memories awaiting user approval |
| Rejection Tracking | Prevents re-proposing rejected memories |

#### New Files

| File | Purpose |
|------|---------|
| `scripts/memory/__init__.py` | Memory module initialization |
| `scripts/memory/embedding_service.py` | Local embeddings with sentence-transformers |
| `scripts/memory/memory_store.py` | Hybrid storage (ChromaDB + JSON) |
| `scripts/memory/induction_engine.py` | User-validated learning engine |
| `scripts/memory/memory_integration.py` | Integration hooks for skills |
| `scripts/guardian/mutability_guard.py` | Layer protection enforcement |
| `knowledge/memory-config.json` | Memory system configuration |
| `tests/memory/test_embedding_service.py` | Embedding tests |
| `tests/memory/test_memory_store.py` | Memory store tests |
| `tests/memory/test_induction_engine.py` | Induction engine tests |
| `tests/guardian/test_mutability_guard.py` | Mutability guard tests |
| `tests/guardian/test_no_axiom_drift.py` | Critical axiom protection tests |

#### User-Validated Learning Flow

```
Observe → Propose → User Decides → Store/Skip
              ↓
   "I noticed you prefer X.
    Should I remember this?"
    [Accept] [Reject] [Edit]
```

#### Layer Protection

| Layer | Content | Status |
|-------|---------|--------|
| L0 | Axioms (A1-A5), Guardian | IMMUTABLE |
| L1 | Purpose (mission, stakeholders) | IMMUTABLE |
| L2 | Principles (ethical boundaries) | IMMUTABLE |
| L3-L4 | Knowledge, Blueprints | Mutable (with approval) |

#### Dependencies Added

| Package | Purpose |
|---------|---------|
| `sentence-transformers>=2.2.0` | Local embeddings (no API key) |
| `chromadb>=0.4.0` | Vector database for memory |

#### Phased Implementation

| Phase | Status | Features |
|-------|--------|----------|
| Phase 1 | Active | User validates all memories |
| Phase 2 | Pending | Confidence-based automation (after 2+ weeks) |

#### New Documentation

| File | Description |
|------|-------------|
| `docs/MEMORY_SYSTEM.md` | Complete memory system guide with chat commands |
| `requirements.txt` | User requirements (separate from dev) |

#### Modified Files

| File | Changes |
|------|---------|
| `.gitignore` | Added memory data directories |
| `requirements-dev.txt` | Added memory system dependencies |
| `requirements.txt` | Created user requirements file |
| `scripts/guardian/__init__.py` | Added mutability_guard reference |
| `knowledge/manifest.json` | Registered memory-config.json |
| `docs/reference/FACTORY_COMPONENTS.md` | Added Memory System section, MutabilityGuard to Guardian |
| `docs/KNOWLEDGE_EVOLUTION.md` | Added Memory System comparison section |
| `docs/GETTING_STARTED.md` | Added Memory System to "What You'll Get" |
| `README.md` | Added Memory System section with chat commands |
| `docs/reference/KNOWLEDGE_FILES.md` | Registered memory-config.json |

---

## [3.3.0] - 2026-01-31

### Added - Layer 0 Integrity Guardian

Major feature: Active constitutional protection for all Factory operations.

#### Philosophy and Foundation

| Element | Description |
|---------|-------------|
| Motto | SDG - Love - Trust |
| Pattern | "Sleeping Dragon" - lightweight but powerful when awakened |
| Inspiration | Sun Tzu (Art of War), Lao Tzu (Tao Te Ching) |
| Principle | Wu Wei - minimum intervention for maximum alignment |

#### New Files

| File | Purpose |
|------|---------|
| `.agent/agents/integrity-guardian.md` | Guardian agent definition (awakened state) |
| `knowledge/guardian-protocol.json` | Coordination wisdom, response protocols |
| `patterns/agents/guardian-aware-agent.json` | Base template with Guardian awareness |
| `docs/reference/GUARDIAN_COORDINATION.md` | Complete Guardian reference |
| `scripts/guardian/__init__.py` | Guardian module initialization |
| `scripts/guardian/axiom_checker.py` | Core axiom violation detection |
| `scripts/guardian/secret_scanner.py` | Credential/secret detection |
| `scripts/guardian/harm_detector.py` | Comprehensive harm analysis |

#### Modified Files

| File | Changes |
|------|---------|
| `.agentrules` | Added Constitutional Preamble as FIRST section |
| `docs/research/AXIOM_BASED_AGENT_ARCHITECTURE.md` | Added Section 9: Active Layer 0 |

#### Wu Wei Response Levels

| Level | Name | Trigger | Action |
|-------|------|---------|--------|
| 0 | Flow | Natural alignment | Continue normally |
| 1 | Nudge | Slight drift | Subtle self-correction |
| 2 | Pause | Boundary approached | Explain, ask user |
| 3 | Block | Clear violation | Stop, explain, present options |
| 4 | Protect | Imminent harm | Prevent harm, then explain |

#### Efficiency Guarantees

| State | API Calls | Latency | Token Overhead |
|-------|-----------|---------|----------------|
| Normal | 0 extra | 0ms | ~500-800 tokens |
| Awakened | 0 extra | Variable | Uses existing context |
| Scripts | 0 | <50ms | 0 |

#### Test Coverage (163 tests)

| Suite | Tests | Purpose |
|-------|-------|---------|
| Unit: Axiom Checker | 55 | Pattern matching correctness |
| Unit: Secret Scanner | 37 | Secret detection accuracy |
| Unit: Harm Detector | 30 | Combined harm analysis |
| Integration: Behavior | 26 | Wu Wei levels trigger correctly |
| Integration: Real Effect | 15 | Guardian ACTUALLY prevents harm |

#### Generated Projects

| Change | Description |
|--------|-------------|
| `.agentrules` template | Constitutional Preamble now included |
| `guardian-protocol.json` template | Lightweight Guardian for generated projects |
| `generate_project.py` | Generates Guardian knowledge file |

#### Onboarding Integration

| Skill | Changes |
|-------|---------|
| `express-onboarding` | Guardian introduced in Steps 2 and 7 |
| `team-huddle-onboarding` | Guardian introduced in Activity 8 |

#### Documentation Updates

| File | Changes |
|------|---------|
| `README.md` | Added Layer 0: Integrity Guardian section |
| `docs/GETTING_STARTED.md` | Added Guardian to "What You'll Get" sections |
| `docs/reference/FACTORY_COMPONENTS.md` | Added integrity-guardian agent details |
| `docs/reference/KNOWLEDGE_FILES.md` | Added guardian-protocol.json |
| `knowledge/manifest.json` | Registered guardian-protocol.json |

---

## [3.2.5] - 2026-01-31

### Added - External Resources and Workshop Integration

Integrated external educational and reflective resources into the Factory's workshop ecosystem.

#### New Reference Documentation

| File | Purpose |
|------|---------|
| `docs/reference/EXTERNAL_RESOURCES.md` | Catalog of external resources for workshops |

#### External Resources Catalog

| Resource | Type | Workshop Use |
|----------|------|--------------|
| AI-Powered Software Dev | Educational | Multi-agent systems reference |
| AI Agent Dev Start | Educational | Agentic patterns foundation |
| Generated Art Technokrat | Entertainment | Icebreaker/discussion prompt |
| IT Strategy VantageX | Example | Cautionary example of AI output |
| Commit 118 | Origin Story | Meaningful milestones reflection |

#### Workshop Skill Updates

| Skill | Enhancement |
|-------|-------------|
| `express-onboarding` | Added optional deep-dive resource link in Step 6 (Magic Preview) |
| `team-huddle-onboarding` | Added "Meaningful Milestones" optional section in Gratitude Close |

#### Research Documentation

| Document | Enhancement |
|----------|-------------|
| `SACRED_PSYCHOLOGY_SOFTWARE_ENGINEERING.md` | Added Appendix D: Commit 118 case study on synchronicity in development |

The Commit 118 case study documents the convergence of technical (Temporal Trust Rule commit), scientific (Element 118 Oganesson), spiritual (Psalm 118), and celestial (planetary alignment) significance on September 5, 2025.

---

## [3.2.4] - 2026-01-31

### Added - Team-Independent Knowledge Management for Generated Projects

Generated projects now include a complete, self-sufficient knowledge management system that allows teams to extend, evolve, and receive updates independently.

#### Three Knowledge Capabilities

| Capability | Agent | Direction | Commands |
|------------|-------|-----------|----------|
| **Extend** | `knowledge-extender` | Team → Project | "extend knowledge for [topic]" |
| **Evolve** | `knowledge-evolution` | Project → Future | "check knowledge status" |
| **Receive** | `factory-updates` | Factory → Project | "check for Factory updates" |

#### New Pattern Files

| File | Purpose |
|------|---------|
| `patterns/agents/knowledge-extender.json` | Add new knowledge to projects |
| `patterns/agents/knowledge-evolution.json` | Track and manage project knowledge |
| `patterns/agents/factory-updates.json` | Receive updates from Factory |
| `patterns/skills/extend-knowledge.json` | Core extension workflow |
| `patterns/skills/receive-updates.json` | Core update workflow |

#### New Knowledge & Templates

| File | Purpose |
|------|---------|
| `knowledge/factory-updates.json` | Update feed for generated projects |
| `templates/knowledge/manifest.json.tmpl` | Project manifest template |
| `templates/knowledge/project-info.json.tmpl` | Project origin tracking |

#### Updated Blueprints (5)

All major blueprints now include knowledge management:
- `python-fastapi`
- `typescript-react`
- `ai-agent-development`
- `java-spring`
- `csharp-dotnet`

Each blueprint now includes:
- `knowledge-extender` agent
- `knowledge-evolution` agent
- `factory-updates` agent
- `extend-knowledge` skill
- `receive-updates` skill

#### Documentation Updates

| Document | Changes |
|----------|---------|
| `docs/USAGE_GUIDE.md` | Added "Knowledge Management (Team-Independent)" and "Receiving Factory Updates" sections |
| `docs/reference/GENERATED_OUTPUT.md` | Updated section 3.5 with full knowledge system |
| `docs/EXTENSION_GUIDE.md` | Added chat-based extension workflow |
| `README.md` | Added "Factory → Generated Project Updates" section |

#### Factory Update Channel

Generated projects can now receive updates from the Factory:
- Update feed at `knowledge/factory-updates.json`
- Channels: `stable` (production) and `latest` (early adopters)
- Updates are filtered by blueprint applicability
- User confirms before applying updates

---

## [3.2.3] - 2026-01-31

### Improved - Comprehensive Artifact Dependency Tracking

Enhanced the artifact-dependencies.json to include documentation as dependent artifacts, enabling reliable detection of what needs updating.

#### Dependency Map Improvements (v1.1.0)

| Feature | Description |
|---------|-------------|
| `documentation_map` | Maps artifact types to their doc sections with regex patterns |
| `factory_artifact_detection` | Lists all Factory agents (9) and skills (21) for reliable detection |
| `post_extension_checklist` | 9-step checklist with specific conditions for each step |
| `factory_agent_created` rule | Explicit rule for Factory agents → FACTORY_COMPONENTS.md |
| `factory_skill_created` rule | Explicit rule for Factory skills → FACTORY_COMPONENTS.md |

#### Updated Artifacts

- `knowledge/artifact-dependencies.json` - Version 1.1.0 with comprehensive documentation tracking
- `.agentrules` - Rule 6 now includes explicit documentation steps
- `.agent/skills/extend-knowledge/SKILL.md` - Step 0 updated with Factory detection logic

---

## [3.2.2] - 2026-01-31

### Added - Algorithmic Trading Knowledge Extension

Extended trading patterns with advanced technical indicators, fundamental data fetching, backtesting frameworks, and strategy building patterns.

#### Knowledge Updates

| File | Version | Changes |
|------|---------|---------|
| `knowledge/trading-patterns.json` | 1.1.0 | Added 5 major sections |

#### New Sections

| Section | Description |
|---------|-------------|
| `technical_indicators_advanced` | Ichimoku, Fibonacci, VWAP, ATR stops, Heikin-Ashi, Elder Ray |
| `fundamental_data_fetching` | yfinance, Alpha Vantage, SEC EDGAR, Piotroski F-Score |
| `backtesting_frameworks` | VectorBT, Backtrader, walk-forward optimization, Monte Carlo |
| `strategy_building_patterns` | Base strategy, multi-factor, regime-aware, portfolio construction |
| `data_sources` | Free and paid data providers with caching patterns |

#### New Skill

| Skill | Description |
|-------|-------------|
| `.agent/skills/algo-trading/SKILL.md` | Complete guide for building trading systems |

#### Updated Artifacts

- `knowledge/manifest.json` - Added trading-patterns.json entry (v1.1.0), updated file count to 67
- `knowledge/skill-catalog.json` - Registered algo-trading skill
- `docs/reference/KNOWLEDGE_FILES.md` - Added Trading/Quant category, updated count to 67
- `docs/reference/FACTORY_COMPONENTS.md` - Added knowledge-extender agent, knowledge-evolution agent, extend-knowledge skill, update-knowledge skill, Knowledge Extension flow diagram

---

## [3.2.1] - 2026-01-31

### Added - CrewAI Knowledge Extension & Post-Extension Automation

Extended CrewAI patterns with advanced orchestration features and integrated mandatory post-extension automation into the Factory system.

#### Knowledge Updates

| File | Changes |
|------|---------|
| `knowledge/crewai-patterns.json` | Added 5 new pattern sections (v1.1.0) |

#### New Sections in CrewAI Patterns

| Section | Description |
|---------|-------------|
| `flow_patterns` | State management with Flows (basic, conditional, parallel) |
| `pipeline_patterns` | Pipeline orchestration for chaining crews |
| `knowledge_patterns` | Adding knowledge sources (string, file, PDF) |
| `training_patterns` | Training crews for improved outputs |
| `kickoff_patterns` | Async and batch execution patterns |

#### New Skill

| Skill | Description |
|-------|-------------|
| `.agent/skills/crewai-workflow/SKILL.md` | Step-by-step guide for CrewAI workflows |

#### Post-Extension Automation (MANDATORY)

Integrated systematic post-extension workflow into Factory rules (`.agentrules` Rule 6):

| Step | Artifact | Action |
|------|----------|--------|
| 1 | `knowledge/manifest.json` | Bump version, update timestamp, add change_history |
| 2 | `knowledge/skill-catalog.json` | Register new skills, update category lists |
| 3 | `docs/reference/KNOWLEDGE_FILES.md` | Update descriptions for modified knowledge |
| 4 | `CHANGELOG.md` | Add version entry with change tables |
| 5 | JSON validation | Run `python -c "import json; json.load(...)"` |
| 6 | Git operations | Ask user before commit/push |

#### Artifact Dependency Map

Created `knowledge/artifact-dependencies.json` for systematic detection of what to update:

| Artifact Type | Must Update |
|---------------|-------------|
| New knowledge file | manifest.json, KNOWLEDGE_FILES.md, CHANGELOG.md |
| Extended knowledge | manifest.json (bump version), CHANGELOG.md |
| New skill | skill-catalog.json, CHANGELOG.md |
| New agent | CHANGELOG.md |
| New template | CHANGELOG.md |
| New blueprint | BLUEPRINTS.md, CHANGELOG.md |

#### Updated Artifacts

- `.agentrules` - Added Rule 6: Post-Extension Automation
- `.agent/skills/extend-knowledge/SKILL.md` - Added Post-Extension Automation section with detection
- `.agent/agents/knowledge-extender.md` - Updated workflow diagram and rules
- `knowledge/artifact-dependencies.json` - NEW: Dependency mapping for automation
- `knowledge/manifest.json` - Version bumped to 1.1.0 for crewai-patterns.json, added artifact-dependencies
- `knowledge/skill-catalog.json` - Registered crewai-workflow skill
- `docs/reference/KNOWLEDGE_FILES.md` - Updated CrewAI description

---

## [3.2.0] - 2026-01-31

### Added - Knowledge Evolution System

This release introduces a comprehensive **Knowledge Evolution System** that automatically keeps the Factory's knowledge base current with the latest best practices from multiple trusted sources.

#### Core Components

| Component | Description |
|-----------|-------------|
| **Source Adapters** | GitHub, PyPI, NPM, official docs, community, user feedback |
| **Configuration Manager** | Unified settings with environment variable support |
| **Update Engine** | Merge, backup, rollback, conflict resolution |
| **Notification System** | Configurable alerts for available updates |
| **Changelog Generator** | Automatic documentation of all changes |

#### New Files

##### Scripts (`scripts/`)
- `config_manager.py` - Centralized configuration management
- `source_aggregator.py` - Multi-source update aggregation
- `update_engine.py` - Update processing and merging
- `conflict_resolver.py` - Conflict detection and resolution
- `notification_system.py` - User notification system
- `changelog_generator.py` - Automatic changelog generation

##### Adapters (`scripts/adapters/`)
- `base_adapter.py` - Abstract adapter interface
- `github_adapter.py` - GitHub releases and trending
- `pypi_adapter.py` - Python package updates
- `npm_adapter.py` - JavaScript/TypeScript packages
- `docs_adapter.py` - Official documentation
- `community_adapter.py` - Community sources
- `feedback_adapter.py` - User feedback learning

##### Schemas (`knowledge/schemas/`)
- `versioning-schema.json` - Knowledge file versioning
- `changelog-schema.json` - Changelog format

##### Configuration
- `.agent/config/settings.json` - Unified configuration (migrates from tools.json)
- `.agent/config/settings-schema.json` - Configuration schema

##### Skills
- `.agent/skills/system-configuration/SKILL.md` - Interactive system configuration
- `.agent/skills/update-knowledge/SKILL.md` - Knowledge update management

##### Agents
- `.agent/agents/knowledge-evolution.md` - Orchestrates knowledge updates

##### Documentation
- `docs/KNOWLEDGE_EVOLUTION.md` - Complete system documentation
- `knowledge/manifest.json` - Central version tracking

#### Update Modes

| Mode | Description |
|------|-------------|
| `stability_first` | Lock versions, explicit approval required |
| `awareness_hybrid` | Notify of updates, user approves (default) |
| `freshness_first` | Auto-apply non-breaking changes |
| `subscription` | Subscribe to specific knowledge files |

#### Features

- **Multi-source aggregation** - Parallel fetching from all configured sources
- **Configurable merge strategies** - Conservative, balanced, aggressive
- **Full rollback support** - Backup before update, easy restore
- **Conflict resolution** - Detect and resolve merge conflicts
- **User customization preservation** - Don't overwrite user changes
- **Schema validation** - All updates validated
- **Source traceability** - Full attribution for every change

#### Tests

- `tests/unit/test_config_manager.py` - Configuration tests
- `tests/unit/test_adapters.py` - Adapter unit tests

---

## [3.1.0] - 2026-01-31

### Added - Enhanced Onboarding Experience

This release transforms the onboarding experience into a more delightful, professional journey that captures team spirit and wisdom.

#### New Onboarding Paths

- **Unified Portal** (`docs/GETTING_STARTED.md`) - Single entry point that guides users to their ideal onboarding path
- **Express Lane** (`.agent/skills/express-onboarding/SKILL.md`) - 10-15 minute individual onboarding with guided prompts and celebrations
- **Team Huddle** (`.agent/skills/team-huddle-onboarding/SKILL.md`) - 1-2 hour condensed workshop for small teams (2-5 people)
- **Wisdom Harvest** (`.agent/skills/wisdom-harvest/SKILL.md`) - Structured knowledge capture for team lessons learned and best practices

#### New Documentation

- `docs/GETTING_STARTED.md` - Unified onboarding portal with path selection guide
- `docs/FIRST_WEEK_GUIDE.md` - Post-onboarding coaching for days 1-5
- `templates/factory/celebration-messages.json` - Celebration moments and visual elements

#### New Skills

| Skill | Duration | Description |
|-------|----------|-------------|
| `express-onboarding` | 10-15 min | Fast individual setup with values, stack, and wisdom capture |
| `team-huddle-onboarding` | 1-2 hours | Condensed team workshop with mini-games |
| `wisdom-harvest` | 5-30 min | Structured capture of team knowledge and lessons |

#### Improvements

- Added celebration moments throughout onboarding flows
- Updated README.md with new onboarding paths
- Updated QUICKSTART.md with cross-references
- Updated USAGE_GUIDE.md with new quick links
- Updated .agentrules with new skills

### Path Comparison

| Path | Team Size | Duration | Best For |
|------|-----------|----------|----------|
| Express Lane | 1 person | 10-15 min | Quick personal setup |
| Team Huddle | 2-5 people | 1-2 hours | Small team alignment |
| Workshop Series | 6+ people | 11-15 hours | Enterprise transformation |

## [3.0.0] - 2026-01-31

### Added - AI/ML Factory Expansion

This major release adds comprehensive AI/ML capabilities with 12 new knowledge files and 8 new blueprints.

#### New Knowledge Files (12 files)

**Foundational ML:**
- `ml-workflow-patterns.json` - Framework-agnostic ML patterns (train/test, cross-validation, pipelines)
- `deep-learning-patterns.json` - PyTorch/TensorFlow training, optimization, checkpointing
- `mlops-patterns.json` - MLflow, Weights & Biases, TensorBoard experiment tracking
- `llm-provider-comparison.json` - OpenAI, Anthropic, Google, Ollama comparison with pricing

**AI Application Patterns:**
- `vector-database-patterns.json` - ChromaDB, Qdrant, Pinecone, FAISS, pgvector
- `huggingface-patterns.json` - Transformers, Datasets, PEFT, Hub integration
- `rag-patterns.json` - RAG architecture, chunking, retrieval, RAGAS evaluation
- `multi-agent-patterns.json` - Consolidated CrewAI, AutoGen, LangGraph patterns

**Advanced AI:**
- `llm-evaluation-patterns.json` - RAGAS, LLM-as-judge, automated testing
- `model-serving-patterns.json` - FastAPI, vLLM, BentoML deployment
- `llm-fine-tuning-patterns.json` - LoRA, QLoRA, DPO, ORPO patterns
- `prompt-library.json` - Reusable prompt templates for common tasks

#### New Blueprints (8 blueprints)

**Production AI/ML:**
- `python-ml-experimentation` - ML research with PyTorch, scikit-learn, MLflow
- `python-deep-learning` - Deep learning with Transformers, PEFT, Accelerate
- `python-rag-system` - Production RAG with LangChain, vector databases
- `python-multi-agent` - Multi-agent systems with CrewAI, AutoGen, LangGraph
- `python-fine-tuning` - LLM fine-tuning with LoRA, QLoRA, TRL

**Starter/Onboarding Blueprints:**
- `starter-ml-classification` - Beginner ML classification (notebooks + patterns)
- `starter-chatbot` - Beginner LLM chatbot with OpenAI and Streamlit
- `starter-rag` - Beginner RAG application with LangChain and ChromaDB

#### Enhanced Blueprints

- `ai-agent-development` - Updated to v2.0.0 with expanded knowledge files and latest LLM models

### Framework Coverage

**Foundational Frameworks:** PyTorch, TensorFlow/Keras, scikit-learn, Hugging Face  
**Orchestration Frameworks:** LangChain, LangGraph, CrewAI, AutoGen  
**Infrastructure:** MLflow, W&B, ChromaDB, Qdrant, Pinecone, vLLM, BentoML  
**LLM Providers:** OpenAI (GPT-4o, o1), Anthropic (Claude 3.5), Google (Gemini), Ollama

### Documentation

- Updated `docs/reference/BLUEPRINTS.md` with new AI/ML blueprints
- Updated `docs/reference/KNOWLEDGE_FILES.md` with new AI/ML knowledge
- Updated `README.md` with AI/ML blueprint listings
- Updated `docs/QUICKSTART.md` with new blueprint options

---

## [2.8.0] - 2026-01-30

### Added

- **Generalized Grounding Verification System** - Universal two-pass verification for all LLM grounding scenarios
  - Base pattern `grounding-verification.json` with confidence delta algorithm
  - 5 verification profiles: strawberry, code, documentation, data, security
  - Configurable thresholds per profile (standard, relaxed, strict, very strict)
  - Trigger options: always, on_medium_confidence, on_critical_claim, on_conflict, manual

- **Grounding Verification Skill** - New base skill for unified verification
  - `.agent/skills/grounding-verification/SKILL.md` - Comprehensive skill documentation
  - Profile-based verification with domain-specific scrubbing rules
  - Error handling with fallbacks for parse failures and conflicting verdicts

- **Profile-Specific Scrubbing Rules**
  - `strawberry`: Tables, fields, classes, functions, numbers, strings, paths, URLs
  - `code`: Classes, functions, methods, variables, types, paths, line numbers, modules
  - `documentation`: Versions, endpoints, config keys, parameters, values, commands
  - `data`: Tables, columns, data types, constraints, indexes, schemas
  - `security`: CVEs, vulnerabilities, attack vectors, algorithms, keys, permissions

### Changed

- **Strawberry Verification Pattern** - Refactored to extend base pattern (v3.0.0)
  - Now references `grounding-verification.json` as base
  - Profile-specific implementation with strawberry defaults
  - Reduced duplication by inheriting shared components

- **Grounding Skill** - Now opts into verification with data profile (v1.1.0)
  - Added `verification.enabled: true, profile: data, trigger: on_medium_confidence`
  - New Step 5: Run Grounding Verification before handling unverified claims

- **Security Audit Skill** - Now opts into verification with security profile (v1.1.0)
  - Added `verification.enabled: true, profile: security, trigger: always`
  - New Step 8: Verify Security Claims with very strict thresholds (delta >= 0.4)
  - Report now includes verification summary section

### Philosophy

This release generalizes the Pythea/Strawberry verification concept into a **universal grounding verification system**:

> "If removing specific identifiers from evidence doesn't significantly change LLM confidence, the evidence may not have been used - indicating potential confabulation."

Key design principles:
- **Configurable** - Skills opt-in by selecting a profile matching their domain
- **DRY** - Core algorithm defined once, reused across all profiles
- **Extensible** - New profiles can be added without modifying base pattern
- **Non-breaking** - Existing skills work unchanged; verification is opt-in

### Credits

- [Leon Chlon](https://github.com/leochlon) - Original Pythea/Strawberry concept

---

## [2.7.0] - 2026-01-30

### Added

- **BDD/TDD Translation and Traceability System** - Configurable testing modes with bidirectional translation
  - 6 testing modes: `tdd-only`, `bdd-only`, `layered`, `bdd-drives-tdd`, `tdd-documents-bdd`, `synchronized`
  - Bidirectional translation between Gherkin scenarios and unit tests
  - Full traceability linking with `@trace-id`, `@implements`, `@scenario` metadata
  - Coverage matrix and orphan detection reports

- **Test Translation Skill** - New skill for BDD/TDD conversion
  - `patterns/skills/test-translation.json` - Translation workflow and modes
  - `knowledge/test-traceability.json` - Traceability metadata schemas and patterns

- **Translation Templates** - Templates for generated artifacts
  - `templates/translation/generated-test-python.py.tmpl` - BDD→TDD test generation
  - `templates/translation/generated-feature.feature.tmpl` - TDD→BDD feature generation
  - `templates/translation/traceability-report.md.tmpl` - Coverage and traceability reports

### Changed

- **Updated test-generator agent** - Now supports all 6 testing modes with translation workflow
- **Updated BDD skill** - Added traceability and translation sections
- **Updated TDD skill** - Added traceability and translation sections
- **Updated stack-configuration skill** - Expanded mode selection UI with all 6 options
- **Updated 5 blueprints** - python-fastapi, typescript-react, java-spring, csharp-dotnet, kotlin-spring
  - All now include `test-translation` skill and 6-mode configuration
- **Updated PATTERNS.md** - Documented Test Translation skill and all modes

---

## [2.6.0] - 2026-01-30

### Added

- **Comprehensive MCP Server Catalog** - Expanded from 10 to 50+ servers across 6 categories
  - Core: filesystem, git, memory, time, fetch, brave-search, exa, sequentialthinking
  - Code: github, gitlab, sentry, playwright, puppeteer, openapi, context7, deepwiki
  - Data: postgresql, sqlite, mongodb, prisma, supabase, firebase, bigquery, snowflake, pinecone, qdrant, chromadb
  - Cloud: docker, terraform, pulumi, datadog
  - Collab: atlassian, linear, asana, todoist, notion, slack, discord, gmail, google-calendar, figma, canva
  - AI/ML: huggingface, mlflow, wandb, langsmith, jupyter, langgraph, knowledge-graph, neo4j, ollama

- **MCP Starter Packs** - Pre-configured server bundles for quick setup
  - Minimal (3 servers): filesystem, git, memory
  - Web Developer (6 servers): + github, postgresql, playwright
  - Data Science (6 servers): + jupyter, bigquery, pinecone
  - AI Agent (6 servers): + langgraph, knowledge-graph, chromadb
  - Enterprise (7 servers): + atlassian, slack, sentry
  - DevOps (6 servers): + docker, terraform, github, datadog

- **Role-Based MCP Recommendations** - Smart server suggestions for 8 developer roles
  - Full-Stack Developer, Frontend Developer, Backend Developer
  - Data Scientist, ML Engineer, Agent Developer
  - DevOps Engineer, SAP Developer

- **MCP Selection Skill** - Interactive skill for guided server selection
  - `.agent/skills/mcp-selection/SKILL.md`
  - Role-based recommendations
  - Category browsing
  - Custom/local server support

- **MCP Server Templates** - Setup guides and configuration templates
  - `templates/mcp/filesystem/setup-guide.md`
  - `templates/mcp/git/setup-guide.md`
  - `templates/mcp/memory/setup-guide.md`
  - `templates/mcp/brave-search/setup-guide.md` + env.template

- **MCP Documentation** - Comprehensive guide for all servers
  - `docs/MCP-SERVERS.md` - Quick start, catalog, and setup instructions

- **AISuite Integration Guide** - Andrew Ng's unified LLM library with MCP support
  - `knowledge/aisuite-integration.json` - Configuration and usage guide
  - Multi-provider LLM access (OpenAI, Anthropic, Google, etc.)
  - Native MCP client support for tool calling

- **MCP Selection Guide Knowledge File** - Decision tree and recommendations
  - `knowledge/mcp-selection-guide.json`
  - Role-to-category mappings
  - Stack recommendations
  - Authentication summaries

### Changed

- **CLI Phase 6** - Enhanced MCP server selection in interactive mode
  - Starter pack selection (6 options)
  - Category browsing for custom selection
  - Auto-add based on PM backend and triggers
  - Custom/local server input support

- **MCP Catalog Schema** - Enhanced with new fields
  - `setupDocs`: Link to official documentation
  - `setupSteps`: Step-by-step setup instructions
  - `envVariables`: Required environment variables
  - `category`: Server category grouping
  - `transport`: stdio, sse, or http

### Documentation

- Added `docs/MCP-SERVERS.md` - Comprehensive MCP server guide
- All server entries now include setup documentation links
- Role-based recommendations table in docs

## [2.5.0] - 2026-01-30

### Added

- **Project Management System** - Complete PM system as optional factory product
  - Multi-backend support: GitHub, Jira, Confluence, Azure DevOps, Linear
  - Methodology support: Scrum, Kanban, Hybrid, Waterfall, SAFe
  - Backend abstraction layer with unified PM operations interface
  - Questionnaire-driven configuration (8 adaptive questions)

- **PM Agents** - Four specialized agents for project management
  - `product-owner` - Creates/refines stories, prioritizes backlog, accepts work
  - `sprint-master` - Facilitates planning, standups, retros, sprint transitions
  - `task-manager` - Breaks down stories, extracts TODOs, updates status
  - `reporting-agent` - Generates burndowns, velocity reports, health indicators

- **PM Skills** - Nine backend-agnostic project management skills
  - `create-epic`, `create-story`, `create-task` - Work item creation
  - `estimate-task` - Story point estimation suggestions
  - `plan-sprint`, `close-sprint` - Sprint lifecycle management
  - `run-standup` - Daily standup status reporting
  - `generate-burndown` - Sprint burndown chart data
  - `health-check` - Team health indicators and metrics

- **CLI PM Flags** - New command-line options for PM configuration
  - `--pm-enabled` - Enable project management system
  - `--pm-backend` - Select PM backend (github/jira/azure-devops/linear)
  - `--pm-doc-backend` - Select documentation backend
  - `--pm-methodology` - Select methodology (scrum/kanban/hybrid/waterfall)

- **MCP Server Templates** - Configuration templates for all backends
  - GitHub: npx @modelcontextprotocol/server-github
  - Atlassian: Remote (mcp.atlassian.com) and local (mcp-atlassian)
  - Azure DevOps: @mcp-apps/azure-devops-mcp-server
  - Linear: Remote (mcp.linear.app/sse)
  - Multi-backend combined configurations

- **PM Metrics System** - Comprehensive metrics with formulas
  - Velocity metrics: velocity, trend, completion rate, carry-over
  - Flow metrics: lead time, cycle time, throughput, WIP
  - Quality metrics: bug ratio, rework rate, escaped defects
  - Predictive metrics: sprint forecast, release prediction, risk score
  - Team health metrics: blocker frequency, stale items, assignment balance

- **PM Documentation** - Complete user and reference documentation
  - `docs/pm-system/README.md` - Overview and quick start
  - `docs/pm-system/USER_GUIDE.md` - Setup and daily usage
  - `docs/pm-system/METHODOLOGY_REFERENCE.md` - Links to official sources
  - `docs/pm-system/METRICS_REFERENCE.md` - Formulas and interpretation
  - Backend-specific setup guides (6 guides)
  - Agent reference documentation (4 agents)

- **PM Tests** - 73 tests covering the PM system
  - Schema validation tests for all PM JSON files
  - Unit tests for PM configuration and adapters
  - Integration tests for CLI PM flags

### Changed

- **ProjectConfig** - Added PM fields (pm_enabled, pm_backend, pm_doc_backend, pm_methodology)
  - New `get_all_agents()` method returns agents including PM agents when enabled
  - New `get_all_skills()` method returns skills including PM skills when enabled

- **onboarding-flow skill** - Added Step 3.5 for optional PM system setup

- **team-workshop-onboarding skill** - Added Project Flow section to Stack Safari
  - Methodology Match game (15 min) - Detect team's preferred methodology
  - Tool Territory game (10 min) - Identify PM and documentation backends

- **Interactive CLI mode** - Added PM configuration in Phase 5

### Integration Points

The PM system is seamlessly integrated into existing factory flows:
- Individual onboarding: Optional Step 3.5 after blueprint selection
- Team workshops: Project Flow section in Stack Safari (Workshop 3)
- CLI quick start: PM flags available for programmatic configuration

### Philosophy

This release continues the tradition of **love and care** by making project management
accessible and non-burdensome:

> "Project management should enhance development, not burden it."

Key principles applied:
- Optional by default - PM is always opt-in, never forced
- Backend-agnostic - Use the tools your team already knows
- Methodology-flexible - Adapt to how your team works
- Transparent - All metrics formulas and interpretations documented

## [2.4.0] - 2026-01-30

### Added

- **AI Development Skills** - Four new skill patterns for building LLM-powered agents
  - `prompt-engineering` - Systematic prompt design, testing, and optimization
  - `agent-coordination` - Multi-agent orchestration (supervisor-worker, hierarchical, collaborative)
  - `task-decomposition` - Breaking complex tasks for specialized agents
  - `consensus-building` - Multi-agent voting, debate, and synthesis protocols

- **SAP Skill Categories** - 12 new SAP-specific skills registered in skill catalog
  - SAP RAP: behavior-design, draft-handling, fiori-annotations, testing
  - SAP CAP: cds-modeling, service-handlers, fiori-integration, deployment
  - SAP CPI/PI: iflow-development, groovy-scripting, error-handling, b2b-integration

- **Intelligent Test Packaging** - Fast error detection in CI pipeline
  - 3-stage pipeline: fast tests first, then integration, then coverage
  - Parallel test execution with pytest-xdist
  - Auto-applied markers (fast/medium/slow) based on test location
  - `pipeline-error-fix` skill for systematic debugging

- **Zero-Config Quick Start** - See the factory in action in under 5 minutes
  - New `--quickstart` CLI command for instant demo project generation
  - `--quickstart-blueprint` option to use different blueprints
  - `--quickstart-output` option to specify output directory
  - Warm, welcoming CLI output with guided next steps

- **Developer Experience Documentation**
  - `docs/PREREQUISITES.md` - Centralized setup guide with platform-specific instructions
  - `docs/TROUBLESHOOTING.md` - Common issues with caring, helpful solutions
  - `docs/QUICKSTART.md` - Detailed guide for the quick start experience

- **Mini Workshop Option** - 2-3 hour condensed team workshop for teams with limited time
  - Vision Express (30 min) - Lightning headlines and mission draft
  - Values Snapshot (30 min) - Rapid value ranking and one dilemma discussion
  - Stack & Team Assembly (45 min) - Blueprint selection and agent quick picks
  - Generation & Demo (30 min) - Create system and walkthrough
  - Next Steps & Gratitude (15 min) - Action planning and appreciation circle

- **Quick Start Tests** - 12 new integration tests for quickstart functionality

### Changed

- **README.md restructured** for better user experience
  - New "Start Here" routing table at the top for quick navigation
  - Warm, welcoming introduction grounded in Axiom 0
  - Improved mermaid diagram showing 5-layer architecture
  - All original advanced content preserved below for experts

- **CLI enhanced** with caring, user-friendly messaging
  - Welcome messages that celebrate user exploration
  - Success celebrations on project generation
  - Helpful error messages with solutions

- **Team Workshop skill** now offers format choice (Full Series or Mini Workshop)

### Philosophy

This release embeds **love and care** as a foundational principle in the user experience:

> "Every message, every error, every piece of documentation should feel like guidance from a trusted friend who wants to see users succeed."

Key principles applied:
- Warm welcome - First impressions set the tone
- Gentle guidance - Never make users feel lost
- Encouraging errors - Mistakes become learning moments
- Progressive disclosure - Show essentials first, reveal depth when ready
- Celebrate success - Acknowledge achievements

## [2.3.1] - 2026-01-30

### Added

- **New SAP CAP Blueprint** (`blueprints/sap-cap/`)
  - Dedicated blueprint for SAP Cloud Application Programming Model
  - Covers CDS modeling, Node.js/Java services, Fiori Elements, BTP deployment
  - Parity with SAP RAP blueprint for consistent SAP coverage

### Changed

- Updated `sap-abap` blueprint to focus on classic ABAP (removed CAP references)
- Updated `docs/reference/BLUEPRINTS.md` with SAP CAP blueprint
- Updated `docs/USAGE_GUIDE.md` with all 4 SAP blueprints

## [2.3.0] - 2026-01-30

### Added

- **New SAP RAP Blueprint** (`blueprints/sap-rap/`)
  - Dedicated blueprint for RESTful ABAP Programming (RAP) development
  - Covers CDS views, behavior definitions, Fiori Elements, ABAP Cloud
  - Separate from general ABAP blueprint for focused RAP development

- **SAP Knowledge Files** (10 new files in `knowledge/`)
  - `cpi-error-handling.json` - Exception handling, retry strategies, circuit breaker patterns
  - `mapping-patterns.json` - XML/JSON/IDoc mapping and transformation patterns
  - `b2b-patterns.json` - EDI (EDIFACT/X12), AS2 protocol, partner management
  - `security-patterns.json` - OAuth 2.0, certificates, encryption, credential management
  - `naming-conventions.json` - Clean ABAP and Hungarian notation conventions
  - `common-table-patterns.json` - SAP table structures, delivery classes, audit fields
  - `tadir-object-types.json` - ABAP repository object types reference
  - `cdhdr-object-classes.json` - Change document patterns for audit trails
  - `service-class-catalog.json` - Service class, repository, factory patterns
  - `sap-reference-repos.json` - Curated SAP sample repositories

- **RAP Templates** (16 files in `templates/abap/rap/`)
  - Behavior definitions: basic, draft, validation, determination, action, authorization
  - Behavior implementations: basic, validation, determination, action
  - CDS views: entity, interface-view, projection
  - Fiori annotations: list-report, object-page
  - Tests: behavior test template

- **CPI Templates** (16 files in `templates/integration/`)
  - Groovy error handling: exception-handling, retry-logic
  - Groovy message processing: json-parser, json-builder, xml-to-json, structured-logging, credential-access
  - iFlow patterns: exception-subprocess, content-router
  - B2B integration: idoc-processing, edi-processor
  - Documentation: iflow-spec, mapping-spec

- **CAP Node.js Templates** (14 files in `templates/cap/`)
  - CDS schemas: entity, entity-associations, aspect, schema
  - Services: service.cds, service-handler.js, service-handler.ts
  - Event handlers: before-create, after-create, on-action
  - MTA deployment: mta.yaml, xs-security.json, package.json
  - Tests: service-test

- **Clean ABAP Templates** (8 files in `templates/abap/clean-abap/`)
  - service-class, global-class, exception-class, factory-class
  - test-class, report, enhancement, interface

### Changed

- Updated `sap-abap` blueprint - now focuses on classic ABAP patterns, Clean ABAP
- Updated `sap-cpi-pi` blueprint - references new template structure
- Updated `docs/reference/BLUEPRINTS.md` - added SAP RAP blueprint
- Updated `docs/reference/KNOWLEDGE_FILES.md` - added 10 new SAP knowledge files

### Summary

This release adds comprehensive SAP template coverage with **66 new files** and **8,045 lines of code**, including:
- 1 new blueprint (SAP RAP)
- 10 new knowledge files
- 54 new templates across RAP, CPI, CAP, and ABAP domains

## [2.2.1] - 2026-01-30

### Added

- **Comprehensive Factory Reference Documentation**
  - `docs/FACTORY_REFERENCE.md` - Master entry point with architecture overview and quick start
  - `docs/reference/BLUEPRINTS.md` - Detailed reference for all 12 technology blueprints (~800 lines)
  - `docs/reference/PATTERNS.md` - Complete patterns reference: agents, skills, axioms, methodologies (~700 lines)
  - `docs/reference/KNOWLEDGE_FILES.md` - All 32 knowledge files categorized and explained
  - `docs/reference/FACTORY_COMPONENTS.md` - Factory's 7 agents and 18 skills documented
  - `docs/reference/GENERATED_OUTPUT.md` - Project structure, file formats, and examples

### Changed

- Updated `README.md` with comprehensive reference documentation section
- Updated `docs/USAGE_GUIDE.md` with quick links to reference documentation

### Documentation

This release adds ~2,460 lines of comprehensive reference documentation, enabling users and contributors to fully understand the factory's blueprints, patterns, knowledge files, and generation process.

## [2.2.0] - 2026-01-30

### Added

- **Team Workshop Onboarding** - Collaborative 5-workshop series for teams to co-create their Antigravity agent system
  - Workshop 1: Vision Quest (mission, stakeholders, success criteria)
  - Workshop 2: Ethics Arena (values, boundaries, ethical framework)
  - Workshop 3: Stack Safari (technology selection, architecture)
  - Workshop 4: Agent Assembly (agent trading cards, skill bingo)
  - Workshop 5: Integration Celebration (demo derby, gratitude circle)

- **New Agent**
  - `workshop-facilitator` - Orchestrates team workshops with games and facilitation

- **New Skill**
  - `team-workshop-onboarding` - Complete workshop series skill with detailed facilitation guides

- **New Documentation**
  - `docs/TEAM_WORKSHOP_GUIDE.md` - Comprehensive facilitator's manual (~1200 lines)

- **New Knowledge Files**
  - `knowledge/workshop-facilitation.json` - Facilitation techniques and prompts
  - `knowledge/game-mechanics.json` - Game rules, variations, and mechanics
  - `knowledge/team-dynamics.json` - Team collaboration patterns and adaptations

- **New Patterns**
  - `patterns/axioms/axiom-zero.json` - Axiom 0: Love, Truth, Beauty foundation
  - `patterns/games/` - 11 workshop games (creative, strategic, collaborative)
  - `patterns/team-formats/` - Small (2-5), medium (6-12), large (13+) team adaptations
  - `patterns/workshops/` - 5 workshop pattern definitions

### Philosophy

This release introduces **Axiom 0: Love, Truth, Beauty** as the philosophical foundation:

> "Before verification, before user primacy, before all rules - we act from love for humanity, truth in our work, and beauty in our craft. Trust emerges naturally from Love + Truth—it is the relational fruit, not a separate pillar."

Workshop activities are designed to make onboarding fun and engaging through play, debate, and celebration.

## [2.1.0] - 2026-01-29

### Added

- **Onboarding Flow** - Non-destructive integration for existing repositories
  - CLI commands: `--analyze`, `--onboard`, `--dry-run`, `--rollback`
  - Repository analyzer to detect existing Antigravity artifacts and tech stack
  - Backup manager with session-based rollback support
  - Merge strategy with interactive conflict resolution
  - 5 onboarding scenarios: FRESH, MINIMAL, PARTIAL, UPGRADE, COMPLETE

- **New Scripts**
  - `scripts/repo_analyzer.py` - Detect existing artifacts and technology stack
  - `scripts/backup_manager.py` - Backup/rollback session management
  - `scripts/merge_strategy.py` - Conflict detection and resolution

- **New Agent**
  - `onboarding-architect` - Orchestrates repository onboarding process

- **New Skill**
  - `onboarding-flow` - Step-by-step onboarding process skill

- **Documentation**
  - `docs/ONBOARDING_GUIDE.md` - Complete user guide for onboarding existing repos

- **Test Fixtures**
  - `tests/fixtures/existing_repo_fresh/` - FRESH scenario fixture
  - `tests/fixtures/existing_repo_minimal/` - MINIMAL scenario fixture
  - `tests/fixtures/existing_repo_partial/` - PARTIAL scenario fixture

### Changed

- Updated `cli/factory_cli.py` with onboarding commands
- Updated `scripts/generate_project.py` with onboarding mode support

## [2.0.0] - 2026-01-29

### Added

- **5-Layer Architecture** - Deductive-inductive architecture for grounded agent systems
  - Layer 0: Integrity & Logic - Core axioms (A1-A5), optional axioms (A6-A10), derivation rules
  - Layer 1: Purpose - Mission, stakeholders, success criteria (`PURPOSE.md`)
  - Layer 2: Principles - Ethical boundaries, quality standards, failure handling
  - Layer 3: Methodology - Agile/Kanban/R&D/Enterprise templates, enforcement, practices
  - Layer 4: Technical - Stack, agents, skills, templates

- **New Skills (7)**
  - `axiom-selection` - Layer 0 axiom configuration
  - `purpose-definition` - Layer 1 purpose definition
  - `methodology-selection` - Layer 3 methodology selection
  - `enforcement-selection` - Enforcement pattern configuration
  - `practice-selection` - Practice pattern configuration
  - `pattern-feedback` - Inductive learning from experience
  - `alignment-check` - Verify understanding before major changes

- **New Patterns**
  - `patterns/axioms/` - Core and optional axiom definitions
  - `patterns/principles/` - Ethical boundaries, quality standards, failure handling
  - `patterns/methodologies/` - Agile Scrum, Kanban, R&D, Enterprise Integration
  - `patterns/enforcement/` - Quality, Safety, Integrity enforcement patterns
  - `patterns/practices/` - Daily, Craft, Alignment practice patterns

- **New Blueprints**
  - `ai-agent-development` - LangChain/LangGraph AI agent development stack
  - `multi-agent-systems` - Orchestrated multi-agent systems with supervisor/worker patterns
  - `kotlin-spring` - Reactive Kotlin microservices with Spring Boot 3, WebFlux, and coroutines
  - `sap-cpi-pi` - SAP CPI/PI integration development with Groovy and Java

- **Example Walkthroughs** - Complete end-to-end examples in `docs/examples/`
  - `01-rest-api-service` - Python FastAPI with Jira integration (Agile Scrum)
  - `02-fullstack-nextjs-app` - Next.js 14 with Prisma (Kanban)
  - `03-rag-chatbot-agent` - LangChain RAG with Streamlit (R&D, A10 Learning)
  - `04-multi-agent-research-system` - LangGraph supervisor/worker (R&D, A8 Collaboration)
  - `05-sap-fiori-integration` - SAP RAP with MCP grounding (Enterprise, Comprehensive)
  - `06-dotnet-enterprise-api` - C# Clean Architecture (Agile Scrum)
  - `07-kotlin-spring-microservice` - Kotlin WebFlux (Kanban)
  - `08-sap-cpi-integration` - SAP CPI Groovy scripting (Kanban)
  - Each includes README.md, WALKTHROUGH.md, and expected-output/ reference files
  - Reference files use `.example` extension to prevent factory interference

- **New Knowledge Files**
  - `knowledge/groovy-patterns.json` - Groovy scripting best practices for SAP CPI
  - `knowledge/iflow-patterns.json` - Integration flow design patterns

- **New Templates**
  - `templates/integration/groovy/base-script.groovy.tmpl` - Base Groovy script template
  - `templates/integration/groovy/message-mapping.groovy.tmpl` - Message mapping template
  - `templates/integration/test/script-test.groovy.tmpl` - Spock test template

- **New Knowledge Files**
  - `knowledge/langchain-patterns.json` - LangChain best practices
  - `knowledge/langgraph-workflows.json` - LangGraph state machine patterns
  - `knowledge/agent-coordination.json` - Multi-agent coordination patterns
  - `knowledge/prompt-engineering.json` - Prompt optimization techniques
  - `knowledge/augmented-coding-patterns.json` - AI collaboration patterns from lexler.github.io

- **New Templates**
  - `templates/ai/agent/base-agent.py.tmpl` - Base AI agent template
  - `templates/ai/prompt/system-prompt.md.tmpl` - System prompt template
  - `templates/ai/workflow/langgraph-graph.py.tmpl` - LangGraph workflow template
  - `templates/factory/PURPOSE.md.tmpl` - Purpose document template
  - `templates/factory/enforcement.yaml.tmpl` - Enforcement configuration template
  - `templates/factory/practices.yaml.tmpl` - Practices configuration template
  - `templates/methodology/methodology.yaml.tmpl` - Methodology configuration template

- **Documentation**
  - `docs/LAYERED_ARCHITECTURE.md` - Complete 5-layer architecture guide
  - `docs/LAYERED_ONBOARDING_CONCEPT.md` - Implementation blueprint
  - Acknowledgements section in README for external inspirations

- **Research Paper Series** - Comprehensive documentation of methodology (`docs/research/`)
  - `AXIOM_BASED_AGENT_ARCHITECTURE.md` - Core methodology: 5-layer system, axioms A1-A10, derivation rules, validation constraints (~30 pages)
  - `SACRED_PSYCHOLOGY_SOFTWARE_ENGINEERING.md` - Psychological enforcement, three-layer architecture, philosophical software techniques (~25 pages)
  - `CONSTITUTIONAL_AI_CONVERGENT_DISCOVERY.md` - Comparison with Anthropic Constitutional AI, convergent discovery analysis (~20 pages)
  - `BUILDING_VALUE_ALIGNED_AGENTS.md` - Practical step-by-step implementation guide (~35 pages)
  - `FUTURE_OF_VALUE_ALIGNED_AI.md` - Synthesis, unified framework, recommendations for AI companies/developers/researchers/policymakers (~20 pages)
  - `ARCHITECTURE_DIAGRAMS.md` - 10 Mermaid diagrams visualizing all architectures
  - `REFERENCES.md` - Complete academic bibliography with citations
  - All papers released under Creative Commons CC0 1.0

### Changed

- Updated `.agentrules` with Active Partner and Check Alignment patterns
- Updated `templates/factory/cursorrules-template.md` with 5-layer structure
- Updated `.agent/skills/requirements-gathering/SKILL.md` with layered onboarding flow
- Updated `README.md` with v2.0 features and Acknowledgements
- Updated `docs/USAGE_GUIDE.md` with 5-layer architecture guide
- Updated `patterns/skills/strawberry-verification.json` with Leon Chlon credits

### Credits

- [Augmented Coding Patterns](https://lexler.github.io/augmented-coding-patterns/) - Lada Kesseler, Nitsan Avni, Ivett Ördög, Llewellyn Falco
- [Leon Chlon](https://github.com/lchlon) - Strawberry Verification inspiration (Pythea)
- [ai-dev-agent](https://github.com/gitwalter/ai-dev-agent) - Layered architecture concepts

## [1.2.0] - 2026-01-28

### Added

- **New Knowledge Files**
  - `knowledge/design-patterns.json` - Gang of Four and modern design patterns with stack-specific examples
  - `knowledge/security-checklist.json` - OWASP Top 10, authentication patterns, and security best practices
  - `knowledge/architecture-patterns.json` - Microservices, monolith, serverless, and deployment patterns

- **New Blueprints**
  - `nextjs-fullstack` - Full-stack TypeScript development with Next.js 14+, Prisma, and Tailwind CSS
  - `csharp-dotnet` - Enterprise .NET 8+ development with ASP.NET Core, Entity Framework, and Clean Architecture

- **New Agent Pattern**
  - `documentation-agent` - Auto-generate and maintain READMEs, API docs, ADRs, and changelogs

- **New Skill Patterns**
  - `security-audit` - OWASP-based security vulnerability detection and remediation guidance
  - `code-review` - Structured code review covering correctness, style, performance, security, and maintainability

- **New MCP Server Integrations**
  - `notion` - Notion workspace integration for docs and databases
  - `linear` - Linear issue tracking and project management
  - `sentry` - Error tracking and performance monitoring

### Changed

- Updated `mcp-servers-catalog.json` with new servers and stack mappings
- Updated `README.md` with new blueprints, agents, skills, and MCP servers
- Updated `docs/USAGE_GUIDE.md` with new blueprint options

## [1.1.0] - 2026-01-28

### Added

- **Comprehensive Test Suite** - 131 pytest-based tests covering:
  - Unit tests (60 tests) for `ProjectConfig` and `ProjectGenerator` classes
  - Integration tests (38 tests) for CLI commands and end-to-end generation
  - Validation tests (33 tests) for JSON schema validation of blueprints, patterns, and knowledge files

- **Test Infrastructure**
  - `tests/` directory with organized test structure
  - `tests/conftest.py` with shared pytest fixtures
  - `tests/fixtures/` with sample configuration files for testing

- **CI/CD Pipeline**
  - `.github/workflows/ci.yml` - GitHub Actions workflow
  - Test matrix: Python 3.10, 3.11, 3.12 on Ubuntu and Windows
  - Code quality checks with Ruff linter
  - JSON syntax validation
  - End-to-end generation verification
  - Coverage reporting with Codecov integration

- **Documentation**
  - `docs/TESTING.md` - Comprehensive testing documentation
  - `requirements-dev.txt` - Development dependencies (pytest, pytest-cov, jsonschema)
  - Updated `README.md` with test running instructions and CI badge

### Changed

- Updated `README.md` with:
  - CI status badge
  - Detailed test running instructions
  - Test suite structure documentation
  - Link to testing documentation
  - Continuous Integration section

## [1.0.0] - 2026-01-XX

### Added

- Initial release of Antigravity Agent Factory
- Project generation engine (`scripts/generate_project.py`)
- CLI interface (`cli/factory_cli.py`)
- Blueprint system for technology stacks:
  - `python-fastapi`
  - `typescript-react`
  - `java-spring`
  - `sap-abap`
- Pattern library for agents and skills
- Knowledge files for skill catalog, stack capabilities, and best practices
- Factory agents: requirements-architect, stack-builder, workflow-designer, knowledge-manager, template-generator
- Factory skills: requirements-gathering, stack-configuration, workflow-generation, agent-generation, skill-generation, knowledge-generation, template-generation, cursorrules-generation
- MCP server integration support (Atlassian, SAP Documentation, DeepWiki, SequentialThinking)
- `.agentrules` template for generated projects
- Documentation: README.md, USAGE_GUIDE.md, EXTENSION_GUIDE.md, SAP_GROUNDING_DESIGN.md
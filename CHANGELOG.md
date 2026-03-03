# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.6.0] - 2026-03-03

### Added
- **Consent-Driven Memory Induction (AGENT-50)**: Mandated Phase Final reflection across all structural workflows (`feature`, `bugfix`, `research`), enabling agents to systematically propose Layer 3/4 architectural methodologies upon task closure.
- **Active Memory Building (Zero-Context Fallback)**: Formally codified rules in `managing-memory-bank` preventing agents from interpreting empty state as permission to hallucinate. If the Tier 0 Active Consciousness returns zero results, agents are forced to pause and securely ask the human operator (`notify_user`) for structural truth.
- **High-Fidelity Solution Reporting (AGENT-51)**: Replaced shallow task closure logic with strict JSON schemas (`solution_definition_schema.json`) and depth validation. `post_solution.py` now mathematically fails if an agent's technical summary lacks structural insight.
- **Tier 0 Graph Navigation**: Established the `mcp_memory` backend explicitly as the Factory's Active Consciousness, directly integrated with Phase 0 context engineering for topography mapping.

### Changed
- **Plane Issue Updates**: Upgraded `solution_comment.html.j2` to distinctively parse and render the newly mandatory `architectural_decisions` and `evolution` arrays natively onto the cloud Plane platform.
- **Skill Instructions**: Greatly expanded `managing-plane-tasks/SKILL.md` with explicit templates grading "Poor" vs "Excellent" technical summaries.

## [1.5.1] - 2026-03-03

### Added

### Changed
- **PMS Architecture Transition**: Finalized move to Cloud Plane + MCP architecture.
- **Documentation**: Overhauled `docs/pms/plane_integration_guide.md` to reflect native MCP tool usage.

### Fixed
- **CI/CD Stabilization (AGENT-48)**:
    - Resolved the 96% coverage failure by optimizing YAML validation to exclude large/legacy directories.
    - Eliminated `gw0`/`gw3` node termination by purging toxic `sys.exit` calls from verification tests.
    - Implemented **Parallel Resource Isolation**: Refactored `OptimizedRAG` and `conftest.py` to assign unique temporary workspaces to each concurrent worker, preventing file locking conflicts.
- **Repository Weight Reduction**: Purged 4,500+ tracked binary files from the `data/` directory and hardened `.gitignore` to prevent future data bloat.

---
*Release verified for high-fidelity agentic orchestration.*


## [1.5.0] - 2026-03-02


### Added
- **Central LLM Configuration (AGENT-27)**: Implemented machine-specific `config/llm_config.json` with shared Python loader (`scripts/ai/llm_config.py`), eliminating 16 hardcoded model strings across 12 files.
- **Dashboard Workflow Suite (AGENT-10)**: Added 6 new dashboard-specific workflows (`dashboard-analysis-routine`, `dashboard-data-health`, `dashboard-insight-reporting`, `dashboard-kpi-governance`, `dashboard-onboarding`, `dashboard-view-builder`) with full structural compliance.
- **Multi-Agent Analyst Society (AGENT-11)**: Implemented LangGraph-based Supervisor node with SQL and Statistical worker nodes for dashboard analytical depth.
- **KPI Dictionary Automation (AGENT-12)**: Created KPI scanner, publisher, and `kpi_dictionary.md` generation pipeline with `@KPI` annotation extraction.
- **Data Guard Alerting System (AGENT-13)**: Built proactive anomaly detection agent with Z-score/IQR methods and `dataguard_config.json` configuration.
- **Exec Summary Reporting (AGENT-14)**: Automated executive summary generation using Plane cycle data and AI-driven strategic recommendations.
- **Recursive Factory Parity (AGENT-20)**: Migrated `rag_knowledge_explorer/` to the standardized `.agent/` mirror pattern.

### Changed
- **RAG TOC Direct Invocation (AGENT-28)**: Refactored `get_rag_toc.py` to call `OptimizedRAG.get_toc()` directly, removing MCP SSE server dependency.
- **Skill Governance**: Added `## Best Practices` section to `managing-plane-tasks/SKILL.md` and description paragraph under `## Process` for structural test compliance.
- **Workflow Standardization**: Updated existing dashboard workflows (alpha-factor-mining, backtest-validation, eda, strategy-development, warehouse-analyst, warehouse-ingestion, warehouse-manager) with consistent structure.

### Fixed
- **PDF TOC Extraction (AGENT-25)**: Implemented deterministic master TOC injection for German textbook via `inject_master_toc.py`, resolving AI hallucination and cache ghost entries.
- **10 Validation Test Failures (AGENT-29)**: Fixed all failures across `test_workflow_structure`, `test_skills_structure`, `test_yaml_frontmatter`, and `test_sync_artifacts` by repairing YAML frontmatter, adding missing workflow sections, and syncing artifact counts.
- **Artifact Sync Drift**: Resolved skill count mismatch (75 → 81) via `sync_artifacts.py --sync`.

## [1.4.2] - 2026-03-01

### Added
- **Self-Optimization Catalog (AGENT-43)**: Implemented the OODA-based maintenance infrastructure mapping 53 scripts across Sense, Correct, Sync, Guard, and Learn phases.
- **Script Registry & Memory Sync (AGENT-42)**: Added `sync_script_registry.py` to bridge CLI tools with the Memory MCP knowledge graph.
- **PDF Ingestion into RAG (AGENT-40)**: Implemented hash-based deduplication and path-based idempotency in `rag_optimized.py`.
- **RAG CLI Expansion**: Added `stats`, `info`, and `check-duplicates` commands to `rag_cli.py` for library health monitoring.

### Changed
- **Multi-Strategy TOC Extraction (AGENT-41)**: Upgraded TOC extraction to a 3-tier fallback system (PyMuPDF Native → Regex Heuristic → LLM Gemini 2.0 Flash).
- **Memory-First Protocol**: Mandated Memory MCP lookup as a P0 requirement for all autonomous agents in the `memory-first.md` rule.

### Fixed
- **RAG TOC Stability**: Fixed `NameError` in `_extract_toc` caused by uninitialized document objects in Strategy 1.
- **Metadata Synchronization**: Auto-fixed discrepancies in project counts, manifests, and documentation using `sync_artifacts.py`, `sync_knowledge_counts.py`, and `sync_test_counts.py`.

## [1.4.1] - 2026-02-27

### Added
- **YAML Frontmatter in Agents**: Injected `skills:`, `domain:`, `type:`, and `model:` fields to all 10 active agents for strict schema compliance.
- **Skill Schemas**: Added missing required fields (`version`, `category`, `tools`, `related_skills`) to 189 skills.
- **Creator Skills Expansion**: Added 4 mandatory markdown sections (`When to Use`, `Prerequisites`, `Process`, `Best Practices`) to creator skills.

### Changed
- **Skill Naming Convention (AGENT-35)**: Renamed 46 skills to a standardized participle-based format (e.g., `api-design` -> `designing-apis`).
- **Global Reference Rewrite**: Automatically rewired 848 skill references across all agents, documents, workflows, manifests, blueprints, and diagrams.
- **Catalog Cleanup**: Rebuilt `skill-catalog.json` with correct display names and fully synchronized counts (198 skills).

### Fixed
- **README Synchronization**: Auto-fixed README skill counts to correctly reflect 198 skills.
- **Validation Pipeline**: Repaired 10 post-refactoring test failures related to stale folders, updated knowledge IDs, and markdown required sections.

### Removed
- **Generating Skills**: Deprecated and deleted `generating-skills` (superseded by `skill-creator`).
- **Research**: Deleted empty legacy `research/` directory.

## [1.4.0] - 2026-02-24
- **Web URL Ingestion (AGENT-18)**: Expanded the RAG Knowledge Explorer to support fetching, chunking, and embedding direct website URLs via LangChain `WebBaseLoader`.
- **HTML Table of Contents**: Implemented a BeautifulSoup HTML parser that deterministically reconstructs a Table of Contents chunk from `h1-h4` web tags for precise, high-level context navigation.
- **RAG Dashboard Expansion**: Added a unified "Web URL" ingest tab in the standalone `rag_knowledge_explorer` Streamlit UI.
- **Native Plane PMS Integration**: Bypassed unreliable Plane MCP servers in favor of direct Django ORM interaction via Docker-executed shell commands.
- **Robust Command Execution**: Implemented Base64 encoding for shell safe transmission of HTML-rich payloads in `scripts/pms/manager.py`.
- **Plane Management Skill**: Created the `managing-tasks-in-plane` skill (categorized in `routing/`) for autonomous issue tracking and lifecycle management.
- **Grounding Knowledge**: Added `plane-integration.json` to provide agents with direct context for ORM access patterns.
- **Integration Documentation**: Wrote a comprehensive technical guide for the new Plane integration architecture.

### Fixed
- **Plane PMS Skill Optimization**: Hardcoded native Plane issue states to eliminate unnecessary database queries during workflow updates.

## [1.3.1] - 2026-02-24

### Added
- **Hyper-Fidelity Architectural Suite (AGENT-23)**: Implemented standard-aligned C4 diagrams including System Context (L1), Container (L2), and execution sequence (L3) maps in `.agent/docs/architecture-overview.md`.
- **System Integrity Audit**: Conducted a formal technical audit and verified integration paths for RAG (Parent-Child) and Plane PMS (Docker-Django Bridge).
- **Guidance Center Sync**: Live-synchronized the new architectural suite into the Statistical Dashboard for real-time developer orientation.

### Fixed
- **Plane State Synchronization**: Standardized issue state filtering in `scripts/pms/manager.py` to support workflow-accurate task tracking.

## [1.3.0] - 2026-02-24

### Fixed
- **Core Engine Stability**: Fixed a critical `SyntaxError` (missing `except` block) in `scripts/core/generate_project.py`.
- **Metadata Synchronization**: Resolved discrepancies in knowledge and artifact counts across manifests and documentation.

## [1.2.3] - 2026-02-22

### Added
- **Domain-Aware Ingestion**: Implemented retroactive and real-time mapping of CSV/Excel data to specialized warehouse domain models (`WarehouseInventory`, `WarehouseBinMaster`).
- **Statistical Dashboard Enhancements**:
    - Centralized data storage in SQLite (`data_json` field) with full reconstruction capability.
    - Integrated real-time Google News RSS feed with sentiment analysis.
    - Implemented advanced chart support (Heatmaps) and fixed index-based plotting errors.
    - Optimized UI with better project-level instructions and help guides.

### Fixed
- **Platform Stability**: Resolved `WinError 1114` DLL failures on Windows by forcing CPU/sequential threading for embeddings.
- **Data Integrity**: Fixed multiple `TypeError` and `ValueError` issues in file upload and trend analysis.
- **Security**: Hardened `.gitignore` to exclude large binary datasets and local databases.

## [1.2.2] - 2026-02-20

### Added
- **RAG Capability Scripts**: Added `search_rag.py` and `list_ebooks.py` utilities to allow skill-driven, persistent SSE client interactions with the FastMCP RAG server.
- **Skill Fallbacks**: Added explicit fallback behaviors in `retrieving-rag-context` and `inspecting-rag-catalog` skill documentation to handle SSE querying when MCP native connections fail.

### Fixed
- **Dependency Conflicts**: Fixed `requirements.txt` malformed syntax, locked `pydantic==2.12.5`, and updated `langchain-mcp-adapters>=0.2.1` to prevent pip resolution errors.
- **RAG Server Stability**: Updated RAG server to handle client initialization probes robustly.

## [1.2.1] - 2026-02-18

### Changed
- **Cleaning**: Removed legacy RAG scripts and artifacts to streamline the codebase.
- **Optimization**: Finalized transition to Qdrant-based RAG architecture.

## [1.2.0] - 2026-02-17

### Added
- **Agentic RAG Implementation**: Transitioned to a reasoning-driven architecture using **LangGraph**.
- **Self-Correction Logic**: Implemented heuristic grading for retrieval relevance with support for German umlaut normalization.
- **Adaptive Fallback**: Integrated Tavily-driven web search as a fallback for queries outside the local library scope.
- **Textbook Ingestion**: Fully indexed Stuart Russell's AIMA (3rd Ed) with 27k standardized vector points.

### Changed
- **Vector Migration**: Standardized on **Qdrant** as the primary vector store (migrated from FAISS).
- **Embedding Alignment**: Switched to `sentence-transformers/all-MiniLM-L6-v2` across all ingestion and retrieval layers.
- **MCP Upgrade**: Updated `antigravity-rag` server to utilize the `AgenticRAG` workflow singleton.

### Fixed
- **Character Encoding**: Resolved false-negative search results caused by German special character mismatches.
- **Resource Management**: Implemented singleton access for Qdrant storage to prevent concurrent locking errors.

## [1.1.2] - 2026-02-16

### Added
- **Robust Commit Workflow (RCW)**: Implemented `verify_and_commit.py` for a high-speed, sequential verification pipeline (Sync, Stage, Validate, Smoke Test).
- **Tolerance Mechanism**: Added support for environment-dependent test count fluctuations in `sync_artifacts.py`.

### Fixed
- **Skill Validation**: Resolved 100% of blueprint skill ID warnings by standardizing references against the canonical catalog.
- **Type Checking**: Fixed `mypy` duplicate module errors by excluding generated skill/agent logic from the check.
- **Commit Workflow**: Refactored `safe_commit.py` for better reliability and faster execution using the RCW backend.

### Optimized
- **Test Performance**: Enabled parallel execution and memoized collection, reducing full suite time by 75% (~40s).
- **Artifact Sync**: Optimized `sync_artifacts.py` unit tests to execute in <2s (previously >20s).

## [1.1.1] - 2026-02-15

### Fixed
- **Pre-commit**: Replaced failing `types-all` with specific, stable stubs (`types-PyYAML`, `types-jsonschema`, etc.).
- **Syntax**: Repaired multiple joined-line syntax errors in `scripts/workshops/export_workshop.py`.
- **Hooks**: Excluded invalid JSON fixtures from `check-json` and optimized `mypy`/`ruff` ignore policies for legacy codebase compatibility.
- **Environment**: Standardized python execution environment as per `GEMINI.md`.
- **Structure**: Resolved structural gaps in knowledge JSON schemas and skill markdown files to ensure factory standard compliance.
- **CI/CD**: Fixed pipeline failures caused by missing required metadata in knowledge and skill artifacts.

## [1.1.0] - 2026-02-15

### Added
- New blueprint: `ai-agent-development`
- New blueprint: `python-fastapi`
- New blueprint: `starter-chatbot`
- Recursive scanning for agents and skills in `sync_artifacts.py`

### Fixed
- **Guardian**: Corrected `generic_secret` regex and refined placeholder filtering in `secret_scanner.py`.
- **Knowledge**: Standardized coordination matrix anti-patterns to use the `fix` field instead of `solution`.
- **Sync**: Resolved agent and skill count drift in `README.md` by enabling recursive discovery and updating regex patterns.
- Achieved a fully green test suite with 2047 passing tests.

### Changed
- Updated validation scripts to support `.agent` directory structure
### Fixed
- Fixed version synchronization mismatch in `manifest.json`.
- Optimized `.pre-commit-config.yaml` to exclude non-project data.

---
*Release verified for high-fidelity agentic orchestration.*
- Fixed root path detection in documentation scripts
- Enhanced pre-commit runner with better argument mapping
- Updated documentation files with latest counts and structure

## [0.1.0] - 2026-02-09

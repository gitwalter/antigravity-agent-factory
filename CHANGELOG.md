# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.8.0] - 2026-03-15

### Added
- **Integrated Developer Experience (IDX) UI**: Initial launch of the Next.js based frontend for managing the Factory.
- **Factory Assets Integration (AGENT-130)**: Integrated Blueprints, Rules, and Workflows directly into the IDX UI.
- **Modular Agent Architecture (AGENT-123)**: Formalized coordination framework for complex agentic workflows.
- **Proactive Maintenance (PAM) (AGENT-121)**: Automated knowledge debt detection and link-integrity monitoring.
- **SDLC Usage Guides (AGENT-115)**: Documented 20+ specialized workflows and usage patterns.
- **Context Hub Integration (AGENT-113/112)**: Live API documentation synchronization via `chub`.
- **New Verification Skills**: Introduced `data-validation`, `mobile-native-build`, and `smart-contract-audit` skills to the verification layer.
- **Improved Test Organization**: Reorganized and formalized test structure into `tests/integration` and `tests/unit` subdirectories.

### Changed
- **Universal Memory Integration (AGENT-136)**: Modernized the memory system with deterministic access protocols and performance optimizations.
- **UI Interaction Model (AGENT-125/135)**: Implemented advanced drilldown, entity editing, and animated workflow phase parsing.
- **Thought Trace Removal (AGENT-131)**: Streamlined the IDX experience by removing non-functional thought tracing components.
- **Knowledge Reorganization (AGENT-134/128)**: Reorganized SDLC-related knowledge assets from the root `knowledge/` directory to `docs/sdlc/` for better architectural separation.
- **Agent Policy Synchronization**: Updated all specialist agent definitions to align with the latest 5-layer architecture and skill dependencies.

### Fixed
- **Systemic Validation Failures (AGENT-134/128)**: Resolved critical schema failures across knowledge files, skills, and sync integrations.
- **Performance & Reliability Core (AGENT-118)**: Optimized CI pipelines, increased diagnostic verbosity, and repaired UTC deprecations and test blockers.
- **Dependency Validator Calibration**: Enhanced the `dependency_validator.py` logic to correctly handle the reorganized file structure and new verification layers.

## [1.7.1] - 2026-03-09

### Added
- **3-Layer Agent Architecture**: Formalized the separation of concerns into Cognitive (@Persona), Functional (.agent/agents/), and Governance (.agent/rules/) layers.
- **Harmonized Specialist Mapping**: Aligned high-level personas (@Architect, @Bug-Hunter, @Documentarian, @Operator) with functional specialists (SYARCH, WQSS, KNOPS, PROPS) for tactical execution.
- **Coordination Blueprint**: Documented MSO, MAD, and topological patterns (Chain, Parallel, Evaluator-Optimizer) in `agent-coordination.md`.
- **Atomic Skill & Hierarchical Memory**: Codified global design patterns for resilient, context-aware agent behaviors.
- **Restored Society Integration Guides**: Re-established `society-integration-guide.md` and `trust-tier-selection.md` with high-fidelity technical content for the Agent Society Protocol (ASP).
- **Onboarding Restoration**: Restored `getting-started.md` and ensured valid registration in the global version registry.
- **SDLC Usage Guide Enrichment**: Transformed `sdlc-usage-guide.md` into a comprehensive developer resource with deep architectural dives.
- **Workflow Versioning**: Introduced mandatory `version` metadata and `Trigger Examples` to all core workflows.

### Changed
- **Workflow Modernization**: Mandated Plane compliance and high-fidelity solution reporting across all core SDLC workflows.
- **Documentation Restoration**: Re-established and standardized the documentation suite with validated counts and structure.
- **Workflow Structural Realignment (v2.0.0)**: Upgraded all core workflows (e.g., `feature-development.md`, `bugfix-resolution.md`) to the Standard Feature Delivery Cycle (SFDC) v2.0.0, streamlining the path from requirements to release.
- **Documentation Consolidation**: Removed legacy/redundant guides (`extension-guide.md`, `quickstart.md`, `user-guide.md`, `troubleshooting.md`) to point users toward the single source of truth in the restored documentation suite.
- **Mandatory Repository Synchronization**: Codified "Creation implies Synchronization" rule in `documentation-generation` and `verifying-artifact-structures` skills, requiring `sync_artifacts.py` and `sync_manifest_versions.py` execution after any change.
- **Pre-Commit Suite Expansion**: Updated `maintenance-procedures.json` to include `sync_manifest_versions.py` in the mandatory `syncSuite`.
- **Memory System Governance**: Mandated filesystem synchronization as a hard prerequisite for memory induction in `managing-memory-bank`.

### Fixed
- **Pattern Validation (AGENT-124)**: Resolved 3 critical sync and property structure failures in the knowledge layer.
- **Plane Solution Reporting**: Fixed newline rendering and identifier usage in the `post_solution.py` script.
- **Unsynchronized Artifacts**: Added explicit anti-patterns to `best-practices.json` to prevent architectural drift and synchronization failures (AGENT-117).
- **Maintenance Procedural Typos**: Fixed `sycnSuite` typo in system knowledge.
- **Link Integrity**: Normalized 1,200+ internal links across the documentation catalog.

## [1.7.0] - 2026-03-09

### Changed
- **Release Optimization**: Initiated the refactoring of the release pipeline to include automated changelog migration and high-fidelity verification.

## [1.6.0] - 2026-03-03

### Added
- **Consent-Driven Memory Induction (AGENT-50)**: Mandated Phase Final reflection across all structural workflows (`feature`, `bugfix`, `research`), enabling agents to systematically propose Layer 3/4 architectural methodologies upon task closure.
- **Active Memory Building (Zero-Context Fallback)**: Formally codified rules in `managing-memory-bank` preventing agents from interpreting empty state as permission to hallucinate. If the Tier 0 Active Consciousness returns zero results, agents are forced to pause and securely ask the human operator (`notify_user`) for structural truth.
- **High-Fidelity Solution Reporting (AGENT-51)**: Replaced shallow task closure logic with strict JSON schemas (`solution_definition_schema.json`) and depth validation. `post_solution.py` now mathematically fails if an agent's technical summary lacks structural insight.
- **Tier 0 Graph Navigation**: Established the `mcp_memory` backend explicitly as the Factory's Active Consciousness, directly integrated with Phase 0 context engineering for topography mapping.

### Changed
- **Plane Task Standardization (AGENT-53)**: Mapped Creator Skills to active consciousness, documented explicit Label UUIDs in `mastering-project-management`, and mandated continuous Plane syncing throughout the Standard Feature Delivery Cycle (SFDC).
- **Plane Issue Updates**: Upgraded `solution_comment.html.j2` to distinctively parse and render the newly mandatory `architectural_decisions` and `evolution` arrays natively onto the cloud Plane platform.
- **Skill Instructions**: Greatly expanded `managing-plane-tasks/SKILL.md` with explicit templates grading "Poor" vs "Excellent" technical summaries.

### Fixed
- **Skill Validation (AGENT-52)**: Refactored `managing-memory-bank` to include mandatory markdown sections to fix CI validation tests. Enforced strict asset comprehensiveness and mandatory Epic assignment in `managing-plane-tasks`.

## [1.5.1] - 2026-03-03

### Changed
- **PMS Architecture Transition**: Finalized move to Cloud Plane + MCP architecture.
- **Documentation**: Overhauled `docs/pms/plane_integration_guide.md` to reflect native MCP tool usage.

### Fixed
- **CI/CD Stabilization (AGENT-48)**: Fixed environment path and encoding issues in the CI pipeline.
- **Documentation**: Corrected broken links in `docs/reference/catalog.md`.

## [1.5.0] - 2026-02-28

### Added
- **Initial Modular Architecture**: Introduced the 5-Layer structure for the Antigravity Factory.
- **Validation Suite**: Added baseline JSON and README validators.

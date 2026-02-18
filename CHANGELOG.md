# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- Fixed root path detection in documentation scripts
- Enhanced pre-commit runner with better argument mapping
- Updated documentation files with latest counts and structure

## [0.1.0] - 2026-02-09

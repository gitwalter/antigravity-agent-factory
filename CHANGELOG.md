# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

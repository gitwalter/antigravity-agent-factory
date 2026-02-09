# Antigravity Factory Automation

This document lists the available automation scripts provided by the Antigravity Agent Factory. These scripts can be executed directly or via the `factory-automation` MCP server.

## Core Automation

### Pre-Commit Runner
Ensures code quality and repository integrity before commits.
- **Script**: `scripts/git/pre_commit_runner.py`
- **Usage**:
  - Check only: `python scripts/git/pre_commit_runner.py --check`
  - Sync/Fix: `python scripts/git/pre_commit_runner.py`
- **MCP Tool**: `run_pre_commit_check`

### Test Catalog Generator
Scans the codebase for tests and generates a comprehensive catalog.
- **Script**: `scripts/docs/generate_test_catalog.py`
- **Usage**: `python scripts/docs/generate_test_catalog.py`
- **Output**: `docs/TEST_CATALOG.md`
- **MCP Tool**: `generate_test_catalog`

## Update System

### PABP Update Fetcher
Pulls updates from external PABP bundles or repositories.
- **Script**: `scripts/pabp/fetch_updates.py`
- **Usage**: `python scripts/pabp/fetch_updates.py --source <url_or_path>`
- **MCP Tool**: `fetch_updates`

## Usage by Agents
Agents can trigger these automations to perform maintenance, validation, or updates.
- **Git Specialist**: Should run pre-commit checks before finalizing tasks.
- **Debug Conductor**: Can use test catalog to find relevant tests.
- **Onboarding Architect**: Can update the factory from upstream sources.

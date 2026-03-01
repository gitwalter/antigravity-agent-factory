# Antigravity Agent Factory - Testing Strategy

The Antigravity Agent Factory employs a multi-layered testing strategy designed to ensure the integrity, reliability, and security of the agentic development system. Every component, from knowledge extraction to project generation and active protection (Guardian), is subject to rigorous validation.

## Test Suite Overview

The test suite is powered by **pytest** and maintains a high degree of coverage across all critical code paths.

> [!IMPORTANT]
> This document is automatically synchronized with the codebase. Numeric counts are live and updated on every commit.

### Vital Statistics

The test suite consists of **2083 tests** organized into five specialized categories:

| Category | Count | Purpose |
|----------|-------|---------|
| Unit Tests | ~1054 | Atomic validation of individual functions and classes. |
| Integration Tests | ~225 | Verification of component interactions and CLI flows. |
| Validation Tests | ~235 | Ensuring all JSON/Markdown patterns adhere to schemas. |
| Guardian Tests | ~153 | Testing the active protection and safety engine (A1-A5). |
| Memory Tests | ~45 | Validating the semantic and episodic memory induction system. |

## Test Levels & Rationale

### 1. Unit Testing
Focuses on the core logic of adapters, managers, and utility functions. These tests ensure that individual "bricks" of the factory are solid before they are used in larger structures.

### 2. Integration Testing
Validates the end-to-end flow of project generation. This includes CLI command processing, template rendering, and file system operations. We ensure that a generated project is structurally sound and ready for use.

### 3. Validation Testing (Grounding)
A unique layer that treats data as code. We validate all knowledge files, blueprints, and patterns against strict JSON schemas. This prevents "knowledge drift" and ensures that agents have accurate grounding.

### 4. Guardian Testing (Safety)
The most sensitive part of the suite. These tests verify that the Guardian can detect harmful commands, secrets, and axiom violations. We simulate adversarial inputs to ensure the safety engine remains uncompromised.

### 5. Memory Testing
Validated the induction engine and embedding services. We test semantic similarity, thresholding, and the correct storage of episodic vs. semantic memories.

---

## Technical Appendix

### Automated Test Catalog
For a complete, line-by-line list of every single test case and its purpose, see the [Detailed Test Catalog](test-catalog.md).

### Running the Suite
The full suite can be executed via the standard pytest interface:

```bash
# Run all tests
pytest

# Run a specific category
pytest tests/guardian/

# Run with verbose output and coverage
pytest -v --cov=scripts
```

### Continuous Synchronization
Test counts are updated using the unified artifact sync system:
```bash
python scripts/validation/sync_artifacts.py --sync tests
```

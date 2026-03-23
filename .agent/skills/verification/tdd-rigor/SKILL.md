---
name: tdd-rigor
description: Use when implementing any feature or bugfix, before writing implementation code. Enforces the Iron Law of TDD.
type: skill
version: 1.0.0
category: verification
---

# Skill: TDD Rigor (Superpowers Port)

## When to Use
Use when implementing any feature or bugfix, before writing implementation code. Enforces the Iron Law of TDD.

## Prerequisites
- Requirements or bug reproduction steps.
- Working test environment (pytest, vitest).

## Process
The TDD process follows a strict red-green-refactor cycle for every functional change.

### 1. RED - Write Failing Test
Write a minimal test demonstrating the target behavior.
- Use `pytest` for Python.
- Use `vitest` for TypeScript/React.
- Ensure the test name is descriptive (e.g., `test_rejects_empty_input`).

### 2. Verify RED - Watch It Fail
**CRITICAL GATE: You must run the test and capture the failure.**
- Confirm failure is due to missing logic.
- Confirm failure message is expected.

### 3. GREEN - Minimal Code
Write just enough code to make the test pass.
- No "while I'm here" improvements.
- No extra features (YAGNI).

### 4. Verify GREEN - Watch It Pass
**CRITICAL GATE: You must run all tests.**
- Confirm the new test passes.
- Confirm no regressions in existing tests.

### 5. REFACTOR - Clean Up
Clean up the implementation while keeping tests green.

## Best Practices
Maintain high TDD standards by following these essential practices.

### The Iron Law
**NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.**
If you wrote code before the test: **Delete it. Start over.**

### Anti-Patterns (Avoid)
- **Testing Mocks**: Don't test that a mock was called; test that the behavior occurred.
- **Test After implementation**: Proves nothing. You never saw it catch the bug.
- **Immediate Pass**: If a new test passes immediately, it's not testing new behavior. Fix the test.

### Verification Checklist
- [ ] Every new function has a test.
- [ ] Watched each test fail before implementing.
- [ ] Each test failed for expected reason.
- [ ] Wrote minimal code to pass.
- [ ] Output is pristine (no warnings/errors).

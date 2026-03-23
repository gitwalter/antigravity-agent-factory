---
name: test-driven-development
description: Use when implementing any feature or bugfix, before writing implementation code. Enforces RED-GREEN-REFACTOR.
type: skill
---

# Test-Driven Development (TDD)

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

**No exceptions without User permission.**

## Red-Green-Refactor

### RED - Write Failing Test
Write one minimal test showing what should happen.
- One behavior
- Clear name
- Real code (no mocks unless unavoidable)

### Verify RED - Watch It Fail
**MANDATORY. Never skip.**
Confirm: Test fails (not errors) because feature is missing.

### GREEN - Minimal Code
Write simplest code to pass the test. Do not over-engineer (YAGNI). Don't add features, refactor other code, or "improve" beyond the test.

### Verify GREEN - Watch It Pass
**MANDATORY.**
Confirm: Test passes and all other tests still pass.

### REFACTOR - Clean Up
After green only: Remove duplication, improve names, extract helpers. Keep tests green. Don't add behavior.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run. |

## Verification Checklist
Before marking work complete, ensure:
- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Wrote minimal code to pass each test

If you are stuck, write a wished-for API or ask the User for help.


## When to Use
- When this specific skillset is applicable to the current task.


## Prerequisites
- Appropriate MCP servers and context.


## Process
1. Review the problem statement.
2. Execute steps sequentially.
3. Validate the output.


## Best Practices
- Always verify before completing the task.

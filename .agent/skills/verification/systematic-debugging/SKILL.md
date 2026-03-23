---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes.
type: skill
version: 1.0.0
category: verification
---

# Skill: Systematic Debugging (Superpowers Port)

## When to Use
Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes. Prevents "guessing" and ensures scientific investigation.

## Prerequisites
- Reproducible failure or clear symptom.
- Access to logs, code, and recent diffs.

## Process
The systematic debugging process consists of four distinct phases of investigation and implementation.

### Phase 1: Root Cause Investigation
1.  **Read Error Messages**: Don't skip. Read the whole stack trace.
2.  **Reproduce Consistently**: Find the exact steps to trigger the failure.
3.  **Check Recent Changes**: `git diff` is your best friend.
4.  **Evidence Gathering**: For multi-layer systems, log data at every boundary.

### Phase 2: Pattern Analysis
1.  **Working Examples**: Find code that *does* work and compare.
2.  **Read References**: Read the pattern/documentation completely. Don't skim.
3.  **Identify Differences**: List every difference between working and broken code.

### Phase 3: Hypothesis and Testing
1.  **Single Hypothesis**: "I think X is the root cause because Y."
2.  **Minimal Test**: Make the smallest possible change to test the hypothesis.
3.  **Verify**: If it didn't work, REVERT and form a NEW hypothesis.

### Phase 4: Implementation
1.  **Create Failing Test**: Reproduce the bug with an automated test (TDD Rigor).
2.  **Implement Fix**: Singular fix for the root cause.
3.  **Verify Fix**: Confirm pass and no regressions.

## Best Practices
Follow these best practices to maintain a rigorous debugging standard.

### Questioning Architecture
If **3+ fixes** have failed: **STOP**.
- Is the pattern fundamentally sound?
- Are we fixing symptoms of a broken architecture?
- Discuss with your human partner before attempting Fix #4.

### Axiomatic Alignment
- **Truth**: We don't guess; we investigate.
- **Beauty**: Orderly investigation leads to cleaner, more stable systems.

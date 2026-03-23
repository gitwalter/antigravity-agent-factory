---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs. Requires running verification commands and confirming output before making any success claims; evidence before assertions always.
type: skill
version: 1.0.0
category: verification
agents:
- python-ai-specialist
- workflow-quality-specialist
- master-system-orchestrator
---

# Verification Before Completion

## When to Use
Use this skill when you are about to claim work is complete, fixed, or passing, before committing or creating PRs.

## Prerequisites
- Implementation is ostensibly complete.
- Verification tools (pytest, scripts) are available and ready.

## Process
The verification process requires a systematic approach to proving claims with fresh evidence.

BEFORE claiming any status or expressing satisfaction:
1. **IDENTIFY**: What command or test proves this claim?
2. **RUN**: Execute the FULL command (fresh, complete).
3. **READ**: Analyze the full output, check exit code, and count failures.
4. **VERIFY**: Does the output confirm the claim?
5. **ONLY THEN**: Make the claim WITH evidence.

## Best Practices
Adhering to these practices ensures that all completion claims are verifiable and trustworthy.

### The Iron Law
> **NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE**

### Common Failures & Requirements
- **Tests pass**: Requires 0 failures in fresh test output.
- **Bug fixed**: Requires regression test pass + original symptom verify fail.
- **Requirements met**: Requires a line-by-line checklist verification.

### Red Flags (DO NOT USE)
- "should work", "probably", "seems correct"
- "Great!", "Done!", "Perfect!" (before evidence)
- Trusting agent reports without independent diff/test verify.

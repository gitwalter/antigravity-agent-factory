---
name: pre-completion-check
description: Use when about to claim work is complete, fixed, or passing, before committing or closing tasks - requires running verification commands and confirming output before making any success claims.
type: skill
---

# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always. This aligns directly with Axiom A1 (Verifiability) from the Factory `.agentrules`.

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim
```

Skip any step = lying, not verifying.

## Key Patterns

**Tests:**
```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**Build:**
```
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed" (linter doesn't check compilation)
```

**Agent delegation:**
```
✅ Sub-agent reports success → Check VCS diff → Verify changes → Report actual state
❌ Trust sub-agent report completely
```

## Why This Matters
As an Antigravity agent, you are governed by the Integrity & Guardian Axioms. Axiom A1 (Verifiability) mandates that evidence must precede assertions.

## The Bottom Line
**No shortcuts for verification.**
Run the command. Read the output. THEN claim the result. This is non-negotiable before closing Plane tasks or marking workflow steps complete.


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

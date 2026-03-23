---
name: requesting-code-review
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements. Dispatches the code-reviewer agent.
type: skill
---

# Requesting Code Review

Dispatch the `code-reviewer-specialist` agent to catch issues before they cascade. The reviewer gets precisely crafted context for evaluation — never your session's history. This keeps the reviewer focused on the work product, not your thought process.

**Core principle:** Review early, review often.

## When to Request Review

**Mandatory:**
- After each task in subagent-driven development
- After completing a major feature outlined in `implementation_plan.md`
- Before merge to main branch

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing a complex bug

## How to Request

**1. Get git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Dispatch code-reviewer subagent:**

Use your task delegation or prompt capabilities to invoke `code-reviewer-specialist.md`:

**Provide this context:**
- `WHAT_WAS_IMPLEMENTED` - What you just built
- `PLAN_OR_REQUIREMENTS` - What it should do (e.g. from `implementation_plan.md`)
- `BASE_SHA` - Starting commit
- `HEAD_SHA` - Ending commit
- `DESCRIPTION` - Brief summary

**3. Act on feedback:**
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong (with technical reasoning)

## Integration with Workflows

**Subagent-Driven Development:**
- Review after EACH task. Fix before moving to next task.

**Ad-Hoc Development:**
- Review before merge or when stuck.

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues

If the reviewer is wrong, push back with technical reasoning and show code/tests that prove it works.


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

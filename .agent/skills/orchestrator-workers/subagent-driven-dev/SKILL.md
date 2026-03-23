---
name: subagent-driven-dev
description: Use when executing implementation plans with independent tasks in the current session. Subagents follow a two-stage review loop.
type: skill
---

# Subagent-Driven Development

Execute an implementation plan by dispatching a fresh specialized agent (e.g., `@Bug-Hunter` or `@Operator`) per task, with a two-stage review after each: spec compliance review first, then code quality review.

**Why subagents:** You delegate tasks to specialized agents with isolated context. By precisely crafting their instructions and context, you ensure they stay focused and succeed at their task. They should never inherit your session's history — you construct exactly what they need.

## The Process

1. **Extract Plan**: Read `implementation_plan.md` and extract all tasks.
2. **Dispatch Implementer**: For each task, dispatch a fresh subagent to implement, test, and commit.
3. **Spec Review**: Dispatch an `@Architect` (SYARCH) or spec-reviewer subagent to confirm code matches the spec.
   - If missing/extra features: Fix before proceeding.
4. **Quality Review**: Dispatch the `code-reviewer-specialist` to review for SOLID principles and Antigravity Clean Core alignment.
   - If issues: Fix before proceeding.
5. **Mark Done**: Check off the task in the plan. Move to the next.

## Handling Implementer Status

Implementer subagents report one of four statuses. Handle each appropriately:

- **DONE:** Proceed to spec compliance review.
- **DONE_WITH_CONCERNS:** The implementer flagged doubts. Address them before review.
- **NEEDS_CONTEXT:** The implementer needs information. Provide it and re-dispatch.
- **BLOCKED:** The implementer cannot complete the task. Escalate to User or break task into smaller pieces.

**Never ignore an escalation.**

## Example Workflow

```text
You: I'm using Subagent-Driven Development to execute this plan.

[Extract all 5 tasks from docs/plans/feature-plan.md]

Task 1: Hook installation script
[Dispatch @Operator subagent with full task text + context]

Implementer: "Added install-hook command. Tests passing."

[Dispatch spec compliance reviewer]
Spec reviewer: ✅ Spec compliant

[Dispatch code-reviewer-specialist]
Code reviewer: ✅ Approved

[Mark Task 1 complete, move to Task 2]
```

## Red Flags

**Never:**
- Skip reviews (spec compliance OR code quality)
- Proceed with unfixed issues
- Accept "close enough" on spec compliance
- Start code quality review before spec compliance is approved

If reviewer finds issues, the implementer MUST fix them, and the reviewer MUST re-review.


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

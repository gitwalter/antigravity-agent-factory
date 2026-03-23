---
name: writing-plans
description: "Use when you have a spec or requirements for a multi-step task, before touching code. Enforces bite-sized task granularity."
type: skill
version: 1.0.0
category: design
agents:
- system-architecture-specialist
- python-ai-specialist
- master-system-orchestrator
---

# Writing Plans: Bite-Sized Implementation Roadmap

## When to Use
Use this skill when you have a spec or requirements for a multi-step task, before touching code. It enforces bite-sized task granularity.

## Prerequisites
- Approved design or requirements.
- Target workspace identified and accessible.

## Process
The process involves writing a comprehensive implementation plan that decomposes a design into 2-5 minute tasks.

### Task Granularity
Every task should be one small, verifiable bit of progress:
1.  **Write the failing test** (RED)
2.  **Verify failure** (RED Verification)
3.  **Write minimal implementation** (GREEN)
4.  **Verify pass** (GREEN Verification)
5.  **Refactor & Commit**

## Best Practices
Follow these best practices to ensure high-quality, verifiable implementation plans.

### Plan Standard (Markdown Header)
```markdown
# [Feature Name] Implementation Plan
**Goal**: [One sentence]
**Architecture**: [2-3 sentences]
---
### Task 1: [Component Name]
**Files**: `path/to/file.py`
**Steps**:
- [ ] Step 1: Write failing test
- [ ] Step 2: Run test (Verify FAILURE)
- [ ] Step 3: Write implementation
- [ ] Step 4: Run test (Verify PASS)
- [ ] Step 5: Commit
```

### Review Gate
- Before beginning execution, the plan MUST be reviewed by a different persona (e.g., `@Bug-Hunter` or `@Architect`).
- Get user approval for the plan before starting the first task.

---
name: using-git-worktrees
description: Use when starting feature work that needs isolation from the current workspace - creates isolated git worktrees. Good for @Operator (PROPS).
type: skill
---

# Using Git Worktrees

## Overview

Git worktrees create isolated workspaces sharing the same repository, allowing work on multiple branches simultaneously without switching.

**Core principle:** Systematic directory selection + safety verification = reliable isolation.

## Directory Selection Process

Follow this priority order:

1. **Check Existing Directories**
`ls -d .worktrees` or `ls -d worktrees`. Use if found.

2. **Check `.agentrules` or global constraints**
Verify if a specific worktree setup is mandated.

3. **Ask User**
If no directory exists:
"No worktree directory found. Should I create a local hidden `.worktrees/` directory?"

## Safety Verification
**MUST verify directory is ignored before creating worktree:**
```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```
If NOT ignored, add it to `.gitignore` and commit immediately. This prevents accidentally committing worktree contents to the repository.

## Creation Steps

1. Create Worktree:
   `git worktree add .worktrees/$BRANCH_NAME -b $BRANCH_NAME` (or use existing branch).
2. Run Setup:
   `conda run -p D:\Anaconda\envs\cursor-factory pip install -r requirements.txt` (or appropriate depending on the stack).
3. Verify Baseline:
   `pytest` (or equivalent) to ensure the worktree starts clean. If tests fail, report failures to the human before proceeding.

## Red Flags

**Never:**
- Create worktree without verifying it's ignored in `.gitignore`
- Skip baseline test verification
- Proceed with failing tests without asking the User


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

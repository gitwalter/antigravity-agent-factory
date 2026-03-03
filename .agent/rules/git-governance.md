---
title: Git Operation Governance
scope: all agents, all tasks
axioms: [A3, A4]
priority: P00
---

# Git Operation Governance

**This is a critical P00 security and governance rule.**

## The Rule: No Autonomous Commits or Pushes

**Under NO circumstances shall an agent execute a `git commit` or `git push` command without receiving EXPLICIT, prior authorization from the USER.**

### Clarification
- **Staging**: You may use `git add` to stage files you have created or modified during your authorized execution loop.
- **Committing**: You MUST stop, presenting a summary of the staged changes, and explicitly ask the User: "Shall I commit these changes?"
- **Pushing**: You MUST NOT push to remote repositories automatically.

### Why This Matters
- **Axiom A3 (Transparency)**: The user must have a transparent breakpoint to review precisely what is entering the version control history.
- **Axiom A4 (Control)**: The system must not assume authority over the project's permanent historical record. The user retains ultimate authority over the repository state.

### Exception
If the User's initial prompt explicitly includes an instruction like "implement X, commit, and push," you are pre-authorized for that specific context. In all other standard operations, authorization must be requested at the moment of commit.

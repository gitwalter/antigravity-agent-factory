---
## Overview

description: Comprehensive workflow for performing structured code reviews covering correctness, style, design, performance, secur...
---

# Code Review

Comprehensive workflow for performing structured code reviews covering correctness, style, design, performance, security, and maintainability. Generates actionable feedback with severity ratings and clear recommendations.

**Version:** 1.0.0
**Created:** 2026-02-02
**Agent:** code-reviewer

> **Note:** Directory paths referenced in this workflow ({directories.knowledge}/, {directories.skills}/, {directories.patterns}/, etc.) are configurable via `{directories.config}/settings.json`. See **Path Configuration Guide**.

## Trigger Conditions

This workflow is activated when:

- Pull request is created or updated
- User requests code review
- Pre-merge review is required
- Code audit is needed

**Trigger Examples:**
- "Review this pull request"
- "Check my code for issues"
- "Do a code review on the changes"
- "PR #123 needs review"

## Steps

### Fetch Change Details

### Understand Change Purpose

### Detect Style Guide

### Logic Verification

### Error Handling Review

### Naming Convention Review

### Formatting Review

### Architecture Assessment

### API Design Review

### Algorithm Complexity

### Resource Usage

### Security Vulnerability Scan

### Code Clarity

### Test Coverage

### Compile Review Report

### Determine Approval Status


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...

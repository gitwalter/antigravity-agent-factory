---
## Overview

description: Comprehensive security audit workflow that systematically reviews code for vulnerabilities, checks dependencies, vali...
---

# Security Audit

Comprehensive security audit workflow that systematically reviews code for vulnerabilities, checks dependencies, validates authentication/authorization, and ensures compliance with security best practices.

**Version:** 1.0.0
**Created:** 2026-02-02
**Agent:** security-auditor

## Trigger Conditions

This workflow is activated when:

- Pre-release security review required
- Pull request contains security-sensitive changes
- Periodic security audit scheduled
- Security concern raised

**Trigger Examples:**
- "Run security audit on the authentication module"
- "Check this PR for security issues"
- "Pre-release security review"
- "Audit the API for vulnerabilities"

## Steps

### Identify Audit Scope

### Gather Context

### Scan for Secrets

### Check Environment Configuration

### Review Authentication Logic

### Review MFA/2FA

### Review Access Control

### Review Data Access

### Check Injection Vulnerabilities

### Check XSS Prevention

### Check CSRF Protection

### Scan Dependencies

### License Compliance

### Check Response Headers

### Compile Security Report

### Create Remediation Plan


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...

# Security Audit Workflow

## Overview

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

## Phases

### Phase 1: Scope Definition

**Description:** Define the scope and focus of the security audit.

**Entry Criteria:** Audit request received
**Exit Criteria:** Scope clearly defined

#### Step 1.1: Identify Audit Scope

**Description:** Determine what will be audited.

**Actions:**
- Identify target files/modules
- Determine audit depth
- List security domains to cover
- Set priority areas

**Scope Categories:**

| Category | Focus |
|----------|-------|
| Authentication | Login, session, tokens |
| Authorization | Permissions, RBAC |
| Data Protection | Encryption, PII |
| Input Validation | Sanitization, injection |
| Dependencies | Third-party libraries |

**Outputs:**
- Audit scope document
- Priority areas

**Is Mandatory:** Yes

---

#### Step 1.2: Gather Context

**Description:** Collect information needed for audit.

**Actions:**
- Read security requirements
- Review architecture documentation
- Identify sensitive data flows
- Check compliance requirements

**Outputs:**
- Security context
- Compliance checklist

**Is Mandatory:** Yes

---

### Phase 2: Secret Scanning

**Description:** Detect exposed secrets and credentials.

**Entry Criteria:** Scope defined
**Exit Criteria:** No secrets in code

#### Step 2.1: Scan for Secrets

**Description:** Search for hardcoded secrets.

**Actions:**
- Scan for API keys
- Check for passwords
- Find tokens and credentials
- Detect private keys

**Patterns Checked:**

| Pattern | Example |
|---------|---------|
| AWS Keys | `AKIA[0-9A-Z]{16}` |
| GitHub Token | `ghp_[a-zA-Z0-9]{36}` |
| JWT Secret | `jwt_secret`, `JWT_KEY` |
| Database Password | `DB_PASSWORD`, `password=` |
| Private Key | `-----BEGIN.*PRIVATE KEY-----` |

**Outputs:**
- Secret findings
- Remediation suggestions

**Is Mandatory:** Yes

---

#### Step 2.2: Check Environment Configuration

**Description:** Verify secrets are properly externalized.

**Actions:**
- Check .env files are gitignored
- Verify secrets in environment variables
- Check configuration management
- Review secret rotation

**Outputs:**
- Configuration assessment

**Is Mandatory:** Yes

---

### Phase 3: Authentication Review

**Description:** Review authentication mechanisms.

**Entry Criteria:** Secret scanning complete
**Exit Criteria:** Auth mechanisms verified

#### Step 3.1: Review Authentication Logic

**Description:** Analyze authentication implementation.

**Actions:**
- Review login flow
- Check password handling
- Verify session management
- Assess token handling

**Checks:**

| Check | Criteria |
|-------|----------|
| Password Storage | bcrypt/argon2, no plain text |
| Session Tokens | Secure, HTTP-only cookies |
| Token Expiry | Appropriate lifetime |
| Brute Force | Rate limiting present |

**Knowledge:**
- `security-checklist.json`: Security patterns

**Outputs:**
- Auth review findings

**Is Mandatory:** Yes

---

#### Step 3.2: Review MFA/2FA

**Description:** Check multi-factor authentication.

**Actions:**
- Verify MFA implementation
- Check recovery options
- Assess bypass risks

**Outputs:**
- MFA assessment

**Is Mandatory:** No (if not applicable)

---

### Phase 4: Authorization Review

**Description:** Review authorization and access control.

**Entry Criteria:** Authentication reviewed
**Exit Criteria:** Authorization verified

#### Step 4.1: Review Access Control

**Description:** Analyze permission enforcement.

**Actions:**
- Check role-based access control
- Verify permission checks
- Test privilege escalation
- Review API authorization

**Checks:**

| Check | Issue |
|-------|-------|
| Missing auth check | Unauthorized access |
| Client-side only | Bypassable |
| Insecure direct object ref | Data leakage |
| Missing rate limiting | DoS risk |

**Outputs:**
- Access control findings

**Is Mandatory:** Yes

---

#### Step 4.2: Review Data Access

**Description:** Check data-level authorization.

**Actions:**
- Verify row-level security
- Check data filtering
- Review query authorization
- Test cross-tenant access

**Outputs:**
- Data access findings

**Is Mandatory:** Yes

---

### Phase 5: Input Validation

**Description:** Review input handling for injection vulnerabilities.

**Entry Criteria:** Authorization reviewed
**Exit Criteria:** Input handling verified

#### Step 5.1: Check Injection Vulnerabilities

**Description:** Scan for injection risks.

**Actions:**
- Check SQL/NoSQL injection
- Review command injection
- Check path traversal
- Verify LDAP injection

**Vulnerability Patterns:**

| Type | Pattern |
|------|---------|
| SQL Injection | String concatenation in queries |
| Command Injection | Unescaped shell input |
| Path Traversal | `../` in file paths |
| XSS | Unescaped HTML output |

**Outputs:**
- Injection vulnerability list

**Is Mandatory:** Yes

---

#### Step 5.2: Check XSS Prevention

**Description:** Review cross-site scripting prevention.

**Actions:**
- Check output encoding
- Review DOM manipulation
- Verify CSP headers
- Check stored XSS risks

**Outputs:**
- XSS findings

**Is Mandatory:** Yes

---

#### Step 5.3: Check CSRF Protection

**Description:** Review CSRF countermeasures.

**Actions:**
- Verify CSRF tokens
- Check SameSite cookies
- Review state-changing operations

**Outputs:**
- CSRF assessment

**Is Mandatory:** Yes

---

### Phase 6: Dependency Audit

**Description:** Audit third-party dependencies for vulnerabilities.

**Entry Criteria:** Input validation complete
**Exit Criteria:** Dependencies verified

#### Step 6.1: Scan Dependencies

**Description:** Check for known vulnerabilities.

**Actions:**
- Run dependency scanner
- Check CVE database
- Assess severity
- Identify remediation

**Tools by Language:**

| Language | Tool |
|----------|------|
| Python | `pip-audit`, `safety` |
| Node.js | `npm audit` |
| Java | `dependency-check` |
| .NET | `dotnet list package --vulnerable` |

**Outputs:**
- Vulnerability list
- Severity ratings

**Is Mandatory:** Yes

---

#### Step 6.2: License Compliance

**Description:** Check for license issues.

**Actions:**
- Identify licenses
- Check compatibility
- Flag problematic licenses

**Outputs:**
- License report

**Is Mandatory:** No

---

### Phase 7: Security Headers

**Description:** Review HTTP security headers.

**Entry Criteria:** Dependencies audited
**Exit Criteria:** Headers configured properly

#### Step 7.1: Check Response Headers

**Description:** Verify security headers present.

**Actions:**
- Check CSP header
- Verify HSTS
- Check X-Frame-Options
- Review X-Content-Type-Options

**Required Headers:**

| Header | Purpose |
|--------|---------|
| Content-Security-Policy | Prevent XSS |
| Strict-Transport-Security | Force HTTPS |
| X-Frame-Options | Prevent clickjacking |
| X-Content-Type-Options | Prevent MIME sniffing |
| Referrer-Policy | Control referrer info |

**Outputs:**
- Header assessment

**Is Mandatory:** Yes

---

### Phase 8: Report Generation

**Description:** Compile findings into security report.

**Entry Criteria:** All audits complete
**Exit Criteria:** Report generated

#### Step 8.1: Compile Security Report

**Description:** Generate comprehensive report.

**Actions:**
- Aggregate all findings
- Classify by severity
- Prioritize remediation
- Generate executive summary

**Severity Levels:**

| Severity | Criteria | SLA |
|----------|----------|-----|
| Critical | Active exploitation, data breach | 24h |
| High | Easy exploit, significant impact | 7 days |
| Medium | Moderate impact or difficulty | 30 days |
| Low | Minor impact, defense in depth | 90 days |

**Outputs:**
- Security audit report

**Is Mandatory:** Yes

---

#### Step 8.2: Create Remediation Plan

**Description:** Develop fix recommendations.

**Actions:**
- Prioritize fixes
- Provide code examples
- Estimate effort
- Assign owners

**Outputs:**
- Remediation plan

**Is Mandatory:** Yes

---

## Decision Points

### Decision: Finding Severity

**Condition:** For each finding

**Options:**

| Condition | Action | Rationale |
|-----------|--------|-----------|
| Critical/High | Immediate escalation | Security risk |
| Medium | Track for sprint | Planned fix |
| Low | Add to backlog | Future improvement |

---

### Decision: Audit Depth

**Condition:** Based on scope

**Options:**

| Scope | Approach |
|-------|----------|
| Pre-release | Full audit |
| PR review | Focused on changes |
| Periodic | Rotating focus |

---

## Escalation Paths

| Trigger | Action | Escalate To |
|---------|--------|-------------|
| Critical vulnerability | Immediate notification | Security Team, CTO |
| Data breach risk | Stop release | Security Team |
| Compliance violation | Document and report | Compliance Officer |
| Unknown vulnerability | Research and assess | Security Team |

---

## Learning Hooks

| Hook Point | Capture | Use For |
|------------|---------|---------|
| After secrets | Common patterns | Training |
| After injection | Vulnerability types | Guidelines |
| After dependencies | CVE patterns | Monitoring |
| After report | Finding statistics | Improvement |

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Security Report | `docs/security/audit_report.md` | Findings |
| Remediation Plan | `docs/security/remediation.md` | Fix tracking |
| Executive Summary | Report header | Leadership |

---

## Security Report Format

```markdown
# Security Audit Report

## Executive Summary
- **Audit Date:** YYYY-MM-DD
- **Scope:** [description]
- **Overall Risk:** High/Medium/Low
- **Critical Findings:** X
- **High Findings:** X

## Findings Summary

| ID | Severity | Category | Description | Status |
|----|----------|----------|-------------|--------|
| SEC-001 | Critical | Auth | SQL Injection in login | Open |
| SEC-002 | High | Crypto | Weak password hash | Open |

## Detailed Findings

### SEC-001: SQL Injection in Login

**Severity:** Critical
**Category:** Injection
**Location:** `auth/login.py:45`

**Description:**
User input is directly concatenated into SQL query.

**Impact:**
Attacker can bypass authentication or extract data.

**Remediation:**
Use parameterized queries:
```python
# Before (vulnerable)
query = f"SELECT * FROM users WHERE email = '{email}'"

# After (secure)
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
```

**References:**
- OWASP SQL Injection
- CWE-89

## Recommendations
1. Implement parameterized queries
2. Add input validation
3. Enable WAF rules
```

---

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| Scanner unavailable | Manual review |
| External service down | Cache results |
| Large codebase | Sample-based audit |
| Time constraints | Focus on critical areas |

---

## Example Session

```
User: Run security audit on the authentication module

Agent:
━━━ PHASE 1: Scope Definition ━━━
Identifying audit scope...

Scope: Authentication Module
Files: auth/, middleware/auth.py, models/user.py
Focus Areas:
- Login/logout flow
- Session management
- Password handling
- Token validation

━━━ PHASE 2: Secret Scanning ━━━
Scanning for secrets...

⚠️ Finding: Hardcoded JWT secret in auth/config.py:12
   JWT_SECRET = "mysecretkey123"
   Severity: CRITICAL
   Remediation: Move to environment variable

✓ No other secrets found

━━━ PHASE 3: Authentication Review ━━━
Reviewing authentication logic...

Password Storage:
✓ Using bcrypt with cost factor 12
✓ No plain text storage

Session Management:
✓ Secure, HTTP-only cookies
⚠️ Session timeout too long (24h)
   Severity: MEDIUM
   Recommendation: Reduce to 2h with refresh

Token Handling:
✓ JWT with proper expiry
⚠️ Token not invalidated on logout
   Severity: HIGH
   Recommendation: Implement token blacklist

━━━ PHASE 4: Authorization Review ━━━
Reviewing access control...

✓ RBAC implemented correctly
✓ Permission checks on all endpoints

⚠️ Missing rate limiting on login
   Severity: HIGH
   Recommendation: Add rate limiting (5/min)

━━━ PHASE 5: Input Validation ━━━
Checking for injection vulnerabilities...

❌ SQL Injection in auth/login.py:45
   Severity: CRITICAL
   Code: f"SELECT * FROM users WHERE email = '{email}'"
   Fix: Use parameterized queries

✓ XSS prevention in place
✓ CSRF tokens implemented

━━━ PHASE 6: Dependency Audit ━━━
Scanning dependencies...

⚠️ PyJWT 1.7.1 - CVE-2022-29217
   Severity: HIGH
   Fix: Upgrade to PyJWT >= 2.4.0

✓ No other vulnerable dependencies

━━━ PHASE 7: Security Headers ━━━
Checking response headers...

✓ Content-Security-Policy set
✓ Strict-Transport-Security set
⚠️ Missing X-Frame-Options
   Severity: MEDIUM

━━━ PHASE 8: Report Generation ━━━

# Security Audit Report

## Summary
- Critical: 2
- High: 3
- Medium: 2
- Low: 0

## Critical Issues (Fix Immediately)
1. SEC-001: Hardcoded JWT secret
2. SEC-002: SQL Injection in login

## High Issues (Fix within 7 days)
1. SEC-003: Token not invalidated on logout
2. SEC-004: Missing rate limiting
3. SEC-005: Vulnerable PyJWT version

Report saved: docs/security/auth_audit_2026-02-02.md

✨ Security audit complete!
```

---

## Related Artifacts

- **Skill Pattern**: `patterns/skills/security-audit.json`
- **Skills**: `.cursor/skills/security-audit`
- **Knowledge**: `knowledge/security-checklist.json`
- **Patterns**: `patterns/enforcement/safety-enforcement.json`

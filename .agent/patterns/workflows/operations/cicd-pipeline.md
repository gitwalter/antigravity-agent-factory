# CI/CD Pipeline Workflow

## Overview

Comprehensive workflow for managing continuous integration and deployment pipelines. Covers build, test, security scanning, and deployment across multiple environments.

**Version:** 1.0.0  
**Created:** 2026-02-02  
**Applies To:** All stacks

> **Note:** Directory paths referenced in this workflow (knowledge/, .cursor/skills/, patterns/, etc.) are configurable via `.cursor/config/settings.json`. See [Path Configuration Guide](../docs/PATH_CONFIGURATION.md).

## Trigger Conditions

This workflow is activated when:

- Push to main/develop branch
- Pull request created/updated
- Scheduled build
- Manual deployment request

**Trigger Examples:**
- "Deploy to staging"
- "Run the CI pipeline"
- "Build and test"
- "Release to production"

## Phases

### Phase 1: Build

**Description:** Compile code and prepare artifacts.

**Entry Criteria:** Code changes committed  
**Exit Criteria:** Build artifacts created

#### Step 1.1: Install Dependencies

**Actions:**
- Restore package cache
- Install dependencies
- Verify dependency lock

#### Step 1.2: Compile/Build

**Actions:**
- Compile source code
- Generate artifacts
- Create build manifest

**Outputs:**
- Build artifacts
- Build metadata

**Is Mandatory:** Yes

---

### Phase 2: Test

**Description:** Execute test suites.

**Entry Criteria:** Build complete  
**Exit Criteria:** Tests passed

#### Step 2.1: Unit Tests

**Actions:**
- Run unit tests
- Collect coverage
- Generate reports

#### Step 2.2: Integration Tests

**Actions:**
- Set up test environment
- Run integration tests
- Tear down environment

**Pass Criteria:**

| Metric | Requirement |
|--------|-------------|
| Unit Tests | 100% pass |
| Integration | 100% pass |
| Coverage | ≥70% |

**Outputs:**
- Test results
- Coverage report

**Is Mandatory:** Yes

---

### Phase 3: Security

**Description:** Security scanning and validation.

**Entry Criteria:** Tests passed  
**Exit Criteria:** Security verified

#### Step 3.1: SAST

**Actions:**
- Run static analysis
- Check for vulnerabilities
- Report findings

#### Step 3.2: Dependency Scan

**Actions:**
- Scan dependencies
- Check CVE database
- Flag vulnerabilities

**Pass Criteria:**
- No critical vulnerabilities
- No high vulnerabilities (blocking)

**Outputs:**
- Security report

**Is Mandatory:** Yes

---

### Phase 4: Deploy Staging

**Description:** Deploy to staging environment.

**Entry Criteria:** Security passed  
**Exit Criteria:** Staging deployed

#### Step 4.1: Deploy

**Actions:**
- Push to staging
- Run migrations
- Configure services

#### Step 4.2: Smoke Test

**Actions:**
- Verify deployment
- Run smoke tests
- Check health endpoints

**Outputs:**
- Staging URL
- Smoke test results

**Is Mandatory:** Yes

---

### Phase 5: Approval Gate

**Description:** Human approval for production.

**Entry Criteria:** Staging verified  
**Exit Criteria:** Approval received

#### Step 5.1: Request Approval

**Actions:**
- Notify approvers
- Provide release notes
- Wait for approval

**Approval Options:**
- APPROVE: Proceed to production
- REJECT: Stop deployment
- ROLLBACK: Revert staging

**Outputs:**
- Approval status

**Is Mandatory:** Yes (for production)

---

### Phase 6: Deploy Production

**Description:** Deploy to production environment.

**Entry Criteria:** Approval received  
**Exit Criteria:** Production deployed

#### Step 6.1: Production Deploy

**Actions:**
- Blue-green or canary deploy
- Run migrations
- Enable traffic

#### Step 6.2: Verify Production

**Actions:**
- Run production smoke tests
- Monitor error rates
- Check performance

**Rollback Criteria:**
- Error rate > 1%
- Response time > 2x baseline
- Health check failure

**Outputs:**
- Production URL
- Deployment status

**Is Mandatory:** Yes

---

## Pipeline Configuration Example

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup
        run: npm ci
      - name: Build
        run: npm run build

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Test
        run: npm test -- --coverage
      - name: Upload Coverage
        uses: codecov/codecov-action@v3

  security:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: SAST
        run: npm audit --audit-level=high
      - name: Dependency Check
        uses: dependency-check/action@v3

  deploy-staging:
    needs: security
    if: github.ref == 'refs/heads/main'
    environment: staging
    steps:
      - name: Deploy
        run: ./deploy.sh staging

  deploy-production:
    needs: deploy-staging
    environment: production
    steps:
      - name: Deploy
        run: ./deploy.sh production
```

---

## Decision Points

### Decision: Build Failure

| Condition | Action |
|-----------|--------|
| Lint errors | Fix and retry |
| Test failures | Investigate and fix |
| Security vulnerability | Block and remediate |

### Decision: Deployment Strategy

| Condition | Strategy |
|-----------|----------|
| Low risk change | Direct deploy |
| Medium risk | Blue-green |
| High risk | Canary with gradual rollout |

### Decision: Rollback

| Condition | Action |
|-----------|--------|
| Error rate > 1% | Automatic rollback |
| Manual rejection | Rollback to previous |
| Partial failure | Pause and investigate |

---

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| Build system unavailable | Use local build |
| Test infrastructure down | Run critical tests only |
| Approval timeout | Queue for next window |
| Deploy failure | Automatic rollback |
| Production issues | Trigger incident-response workflow |

---

## Example Session

```
User: Deploy to production

Agent:
━━━ PHASE 1: Build ━━━
Installing dependencies...
✓ Dependencies installed

Building...
✓ Build successful (artifacts: 3)

━━━ PHASE 2: Test ━━━
Running unit tests...
✓ 245/245 passed

Running integration tests...
✓ 34/34 passed

Coverage: 82% ✓

━━━ PHASE 3: Security ━━━
Running SAST...
✓ No critical issues

Scanning dependencies...
✓ No vulnerabilities

━━━ PHASE 4: Deploy Staging ━━━
Deploying to staging...
✓ Deployed: https://staging.app.com

Running smoke tests...
✓ All endpoints responding

━━━ PHASE 5: Approval Gate ━━━
Requesting approval...

Approvers notified:
- @tech-lead
- @release-manager

[Awaiting approval...]

✓ Approved by @tech-lead

━━━ PHASE 6: Deploy Production ━━━
Deploying to production (blue-green)...
✓ New version deployed

Switching traffic...
✓ Traffic migrated

Verifying...
✓ Error rate: 0.02%
✓ Response time: 142ms

✨ Production deployment complete!
URL: https://app.com
```

---

## Related Artifacts

- **Skills**: `.cursor/skills/ci-monitor`, `.cursor/skills/pipeline-error-fix`
- **Patterns**: `patterns/skills/ci-monitor-project.json`

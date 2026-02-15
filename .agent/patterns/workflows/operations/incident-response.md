# Incident Response Workflow

## Overview

Systematic workflow for responding to production incidents. Covers detection, triage, mitigation, resolution, and post-mortem analysis.

**Version:** 1.0.0
**Created:** 2026-02-02
**Applies To:** All stacks

## Trigger Conditions

This workflow is activated when:

- Production alert triggered
- User reports outage
- Monitoring detects anomaly
- Service degradation observed

**Trigger Examples:**
- "Production is down"
- "Users can't login"
- "Database errors spiking"
- "API response time critical"

## Phases

### Phase 1: Detection

**Description:** Confirm and characterize the incident.

**Entry Criteria:** Alert or report received
**Exit Criteria:** Incident confirmed

#### Step 1.1: Acknowledge Alert

**Actions:**
- Receive alert notification
- Acknowledge incident
- Start incident timer
- Create incident channel

#### Step 1.2: Initial Assessment

**Actions:**
- Check monitoring dashboards
- Review error logs
- Confirm impact scope
- Classify severity

**Severity Levels:**

| Level | Description | Response Time |
|-------|-------------|---------------|
| SEV1 | Total outage | Immediate |
| SEV2 | Major degradation | 15 min |
| SEV3 | Partial impact | 1 hour |
| SEV4 | Minor issue | 4 hours |

**Outputs:**
- Incident ticket
- Severity classification

**Is Mandatory:** Yes

---

### Phase 2: Triage

**Description:** Identify scope and impact.

**Entry Criteria:** Incident confirmed
**Exit Criteria:** Impact understood

#### Step 2.1: Identify Impact

**Actions:**
- Determine affected systems
- Count affected users
- Assess business impact
- Check related services

**Impact Assessment:**
- Users affected: X
- Revenue impact: $Y
- Systems down: Z
- Duration so far: T

#### Step 2.2: Assemble Response Team

**Actions:**
- Page on-call engineer
- Notify incident commander
- Gather subject experts
- Establish communication

**Outputs:**
- Impact assessment
- Response team

**Is Mandatory:** Yes

---

### Phase 3: Mitigation

**Description:** Reduce or eliminate impact.

**Entry Criteria:** Impact understood
**Exit Criteria:** Impact mitigated

#### Step 3.1: Identify Mitigation Options

**Actions:**
- Rollback recent changes?
- Scale up resources?
- Failover to backup?
- Block traffic?

**Mitigation Strategies:**

| Strategy | When to Use |
|----------|-------------|
| Rollback | Recent deployment caused |
| Restart | Service stuck |
| Failover | Region/zone failure |
| Scale | Capacity exhausted |
| Block | Attack or abuse |

#### Step 3.2: Execute Mitigation

**Actions:**
- Implement chosen strategy
- Verify improvement
- Monitor stability
- Communicate status

**Outputs:**
- Mitigation actions
- Status update

**Is Mandatory:** Yes

---

### Phase 4: Resolution

**Description:** Fully resolve the incident.

**Entry Criteria:** Impact mitigated
**Exit Criteria:** Incident resolved

#### Step 4.1: Root Cause Analysis

**Actions:**
- Investigate root cause
- Review logs and metrics
- Trace error origin
- Identify fix

#### Step 4.2: Apply Fix

**Actions:**
- Implement permanent fix
- Test fix
- Deploy to production
- Verify resolution

**Outputs:**
- Root cause identified
- Fix deployed

**Is Mandatory:** Yes

---

### Phase 5: Recovery

**Description:** Restore normal operations.

**Entry Criteria:** Fix deployed
**Exit Criteria:** Normal operations

#### Step 5.1: Verify Recovery

**Actions:**
- Check all systems healthy
- Verify metrics normalized
- Confirm user impact ended
- Test critical paths

#### Step 5.2: Close Incident

**Actions:**
- Update incident ticket
- Notify stakeholders
- Stop incident timer
- Archive incident channel

**Outputs:**
- Incident closed
- Duration recorded

**Is Mandatory:** Yes

---

### Phase 6: Post-Mortem

**Description:** Learn from the incident.

**Entry Criteria:** Incident closed
**Exit Criteria:** Post-mortem complete

#### Step 6.1: Conduct Post-Mortem

**Actions:**
- Schedule blameless review
- Gather timeline
- Identify contributing factors
- Document lessons learned

**Post-Mortem Template:**
```markdown
## Incident Post-Mortem

**Date:** YYYY-MM-DD
**Duration:** X hours
**Severity:** SEV-X
**Impact:** Description

### Timeline
- HH:MM - Event
- HH:MM - Event

### Root Cause
Description of root cause

### Contributing Factors
1. Factor 1
2. Factor 2

### Action Items
| Action | Owner | Due |
|--------|-------|-----|
| Item | Name | Date |

### Lessons Learned
- Lesson 1
- Lesson 2
```

#### Step 6.2: Create Action Items

**Actions:**
- Define preventive measures
- Assign owners
- Set deadlines
- Track completion

**Outputs:**
- Post-mortem document
- Action items

**Is Mandatory:** Yes

---

## Decision Points

### Decision: Severity Assessment

| Condition | Severity |
|-----------|----------|
| Complete outage | SEV1 |
| Major feature down | SEV2 |
| Partial degradation | SEV3 |
| Minor issue | SEV4 |

### Decision: Mitigation Strategy

| Situation | Strategy |
|-----------|----------|
| Recent deploy | Rollback |
| Resource exhaustion | Scale |
| Stuck service | Restart |
| Region failure | Failover |

---

## Escalation Paths

| Trigger | Escalate To |
|---------|-------------|
| SEV1 | Engineering Manager, VP |
| > 30 min unmitigated | Engineering Manager |
| Customer-facing | Customer Success |
| Data breach | Security, Legal |

---

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| Monitoring unavailable | Use manual checks |
| Team unreachable | Escalate to backup |
| Root cause unknown | Stabilize first, investigate after |
| Fix causes regression | Immediate rollback |
| Communication system down | Use backup channel |

---

## Example Session

```
User: Production database is throwing errors

Agent:
━━━ PHASE 1: Detection ━━━
Acknowledging incident...
✓ Incident #INC-2026-0042 created
✓ Started at 14:23 UTC

Initial assessment...
- Error rate: 45% of requests
- Database connection errors
- Multiple services affected

Classification: SEV2 (Major degradation)

━━━ PHASE 2: Triage ━━━
Identifying impact...
- Affected users: ~5,000
- Services down: API, Dashboard
- Revenue impact: ~$2,000/hour

Assembling team...
✓ @oncall-engineer paged
✓ @dba notified
✓ #incident-2026-0042 channel created

━━━ PHASE 3: Mitigation ━━━
Evaluating options...
1. Restart database - Low risk
2. Failover to replica - Medium risk
3. Scale connection pool - Quick fix

Attempting connection pool increase...
✓ Pool size: 100 → 200
✓ Error rate: 45% → 5%

Partial mitigation achieved.

━━━ PHASE 4: Resolution ━━━
Investigating root cause...
- Recent deploy: New batch job
- Batch job holding connections
- Pool exhaustion

Fixing batch job...
✓ Added connection timeout
✓ Deployed fix

Error rate: 0.1% (normal)

━━━ PHASE 5: Recovery ━━━
Verifying recovery...
✓ All services healthy
✓ Metrics normalized
✓ User complaints stopped

Closing incident...
Duration: 47 minutes
Status: RESOLVED

━━━ PHASE 6: Post-Mortem ━━━
Scheduling post-mortem: Tomorrow 10:00

Action Items:
1. Add connection pool monitoring [@sre]
2. Batch job review process [@lead]
3. Load test connection limits [@qa]

✨ Incident resolved!
```

---

## Related Artifacts

- **Skills**: `.agent/skills/pipeline-error-fix`
- **Workflows**: `workflows/operations/debug-pipeline.md`
- **Patterns**: `patterns/skills/pipeline-error-fix-project.json`

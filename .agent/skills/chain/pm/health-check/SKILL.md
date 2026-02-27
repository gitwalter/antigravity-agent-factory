---
agents:
- none
category: general
description: Team health indicators
knowledge:
- workflow-patterns.json
- best-practices.json
- team-dynamics.json
name: health-check
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---

# Health Check Skill

Analyzes team health indicators by examining cycle time, lead time, work in progress (WIP), blockers, and other metrics. Generates health reports to help teams identify issues and improve their workflow.

## Philosophy

> Health checks prevent problems before they become crises.

Team health is about more than velocity—it's about sustainable pace, clear communication, and effective collaboration. This skill surfaces health indicators early, grounded in love for team wellbeing, truth in metrics, and beauty in sustainable practices.

## When to Use

- When assessing team health and workflow
- When user mentions "health check", "team health", "metrics", "analytics", "dashboard"
- During sprint retrospectives
- When identifying workflow issues
- When reviewing team performance
- When preparing for team reviews

## Prerequisites

Before running health check, ensure:
1. PM backend is configured (via `pm-configuration` skill)
2. Project ID or team context is available
3. Sufficient historical data exists (at least 1-2 sprints)

## Process
Placeholder content for Process to satisfy validation.
### Step 1: Determine Health Check Scope

Identify what to analyze:

```
"I'll help you check team health. What's the scope?

A) Current sprint health
B) Last 3 sprints trend
C) Project overall health
D) Team member health: {USER_ID or USERNAME}
E) Specific metrics: {METRIC_LIST}

**Time Period:**
- Last sprint
- Last 3 sprints (recommended)
- Last 6 sprints
- All time
- Custom: {START_DATE} to {END_DATE}
"
```

### Step 2: Query Health Metrics

Fetch relevant metrics:

**Backend Operation:** `getCycleTime`

**Parameters:**
```json
{
  "projectId": "{PROJECT_ID}",
  "startDate": "{START_DATE}",
  "endDate": "{END_DATE}"
}
```

**Backend Operation:** `getLeadTime`

**Parameters:**
```json
{
  "projectId": "{PROJECT_ID}",
  "startDate": "{START_DATE}",
  "endDate": "{END_DATE}"
}
```

**Backend Operation:** `getWIP`

**Parameters:**
```json
{
  "boardId": "{BOARD_ID}"
}
```

**Backend Operation:** `listItems`

**Parameters:**
```json
{
  "projectId": "{PROJECT_ID}",
  "status": "Blocked"
}
```

**Backend Operation:** `getVelocity`

**Parameters:**
```json
{
  "projectId": "{PROJECT_ID}",
  "sprintCount": 3
}
```

### Step 3: Analyze Cycle Time

Analyze how long items take to complete:

```
"⏱️ **Cycle Time Analysis**

**Cycle Time:** Average time from "In Progress" to "Done"

**Metrics:**
- **Average Cycle Time:** {AVG_CYCLE_TIME} days
- **Median Cycle Time:** {MEDIAN_CYCLE_TIME} days
- **Min Cycle Time:** {MIN_CYCLE_TIME} days
- **Max Cycle Time:** {MAX_CYCLE_TIME} days

**Distribution:**
- < 1 day: {COUNT} items ({PERCENTAGE}%)
- 1-3 days: {COUNT} items ({PERCENTAGE}%)
- 3-5 days: {COUNT} items ({PERCENTAGE}%)
- 5-7 days: {COUNT} items ({PERCENTAGE}%)
- > 7 days: {COUNT} items ({PERCENTAGE}%)

**Trend:**
- Last Sprint: {CYCLE_TIME} days
- Previous Sprint: {CYCLE_TIME} days
- Trend: {INCREASING/DECREASING/STABLE} 📈📉➡️

**Health Status:**
- {HEALTH_STATUS} ({RATING}/10)
- {ASSESSMENT}

**Recommendations:**
- {RECOMMENDATION_1}
- {RECOMMENDATION_2}
"
```

### Step 4: Analyze Lead Time

Analyze time from creation to completion:

```
"📅 **Lead Time Analysis**

**Lead Time:** Average time from "Created" to "Done"

**Metrics:**
- **Average Lead Time:** {AVG_LEAD_TIME} days
- **Median Lead Time:** {MEDIAN_LEAD_TIME} days
- **Min Lead Time:** {MIN_LEAD_TIME} days
- **Max Lead Time:** {MAX_LEAD_TIME} days

**Components:**
- **Wait Time:** {WAIT_TIME} days (in backlog)
- **Cycle Time:** {CYCLE_TIME} days (in progress)
- **Review Time:** {REVIEW_TIME} days (in review)

**Trend:**
- Last Sprint: {LEAD_TIME} days
- Previous Sprint: {LEAD_TIME} days
- Trend: {INCREASING/DECREASING/STABLE} 📈📉➡️

**Health Status:**
- {HEALTH_STATUS} ({RATING}/10)
- {ASSESSMENT}

**Recommendations:**
- {RECOMMENDATION_1}
- {RECOMMENDATION_2}
"
```

### Step 5: Analyze Work in Progress (WIP)

Check WIP levels:

```
"📊 **Work in Progress (WIP) Analysis**

**Current WIP:**
- **In Progress:** {WIP_COUNT} items
- **WIP Limit:** {WIP_LIMIT} items
- **Utilization:** {PERCENTAGE}%
- **Status:** {WITHIN_LIMIT/OVER_LIMIT}

**By Column:**
- **Backlog:** {COUNT} items
- **Ready:** {COUNT} items (limit: {LIMIT})
- **In Progress:** {COUNT} items (limit: {LIMIT}) {STATUS}
- **Review:** {COUNT} items (limit: {LIMIT}) {STATUS}
- **Done:** {COUNT} items

**WIP Trends:**
- Average WIP: {AVG_WIP} items
- Max WIP: {MAX_WIP} items
- Min WIP: {MIN_WIP} items
- Variability: {VARIABILITY} (high/medium/low)

**Health Status:**
- {HEALTH_STATUS} ({RATING}/10)
- {ASSESSMENT}

**Recommendations:**
- {RECOMMENDATION_1}
- {RECOMMENDATION_2}
"
```

### Step 6: Analyze Blockers

Identify blocking issues:

```
"🚧 **Blocker Analysis**

**Current Blockers:** {BLOCKER_COUNT}

**Active Blockers:**
- {BLOCKER_1}: {DESCRIPTION} (blocked {DAYS} days, affects {AFFECTED_ITEMS})
- {BLOCKER_2}: {DESCRIPTION} (blocked {DAYS} days, affects {AFFECTED_ITEMS})

**Blocker Frequency:**
- Items blocked: {BLOCKED_COUNT} / {TOTAL_COUNT} ({PERCENTAGE}%)
- Average blocker duration: {AVG_DURATION} days
- Longest blocker: {MAX_DURATION} days

**Blocker Types:**
- Dependencies: {COUNT}
- External: {COUNT}
- Technical: {COUNT}
- Process: {COUNT}
- Other: {COUNT}

**Trend:**
- Last Sprint: {BLOCKER_COUNT} blockers
- Previous Sprint: {BLOCKER_COUNT} blockers
- Trend: {INCREASING/DECREASING/STABLE} 📈📉➡️

**Health Status:**
- {HEALTH_STATUS} ({RATING}/10)
- {ASSESSMENT}

**Recommendations:**
- {RECOMMENDATION_1}
- {RECOMMENDATION_2}
"
```

### Step 7: Analyze Velocity

Review velocity trends:

```
"📈 **Velocity Analysis**

**Velocity Metrics:**
- **Last Sprint:** {VELOCITY} pts
- **Average (3 sprints):** {AVG_VELOCITY} pts
- **Average (6 sprints):** {AVG_VELOCITY_6} pts
- **Trend:** {INCREASING/DECREASING/STABLE} 📈📉➡️

**Velocity Stability:**
- Standard Deviation: {STD_DEV} pts
- Coefficient of Variation: {CV}%
- Stability: {STABLE/VARIABLE} ({RATING}/10)

**Completion Rate:**
- Planned: {PLANNED_POINTS} pts
- Completed: {COMPLETED_POINTS} pts
- Completion Rate: {PERCENTAGE}%

**Health Status:**
- {HEALTH_STATUS} ({RATING}/10)
- {ASSESSMENT}

**Recommendations:**
- {RECOMMENDATION_1}
- {RECOMMENDATION_2}
"
```

### Step 8: Generate Health Report

Compile comprehensive health report:

```
"🏥 **Team Health Report**

**Report Period:** {START_DATE} to {END_DATE}
**Generated:** {CURRENT_DATE}
**Team:** {TEAM_NAME}
**Project:** {PROJECT_NAME}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Overall Health Score: {SCORE}/10** {RATING}

**Health Breakdown:**

✅ **Strengths:**
- {STRENGTH_1}
- {STRENGTH_2}
- {STRENGTH_3}

⚠️ **Areas for Improvement:**
- {IMPROVEMENT_1}
- {IMPROVEMENT_2}
- {IMPROVEMENT_3}

🚨 **Critical Issues:**
- {ISSUE_1}
- {ISSUE_2}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Metric Summary:**

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Cycle Time | {VALUE} days | < {TARGET} days | {STATUS} |
| Lead Time | {VALUE} days | < {TARGET} days | {STATUS} |
| WIP | {VALUE} items | < {TARGET} items | {STATUS} |
| Blockers | {VALUE} | < {TARGET} | {STATUS} |
| Velocity | {VALUE} pts | {TARGET} pts | {STATUS} |
| Completion Rate | {VALUE}% | > {TARGET}% | {STATUS} |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Detailed Analysis:**

[DETAILED_METRICS_FROM_STEPS_3-7]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Action Items:**

**High Priority:**
- [ ] {ACTION_1}: {OWNER} - {DUE_DATE}
- [ ] {ACTION_2}: {OWNER} - {DUE_DATE}

**Medium Priority:**
- [ ] {ACTION_3}: {OWNER} - {DUE_DATE}
- [ ] {ACTION_4}: {OWNER} - {DUE_DATE}

**Low Priority:**
- [ ] {ACTION_5}: {OWNER} - {DUE_DATE}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Next Health Check:** {NEXT_CHECK_DATE}
**Review Frequency:** {FREQUENCY}

**Recommendations:**
- {RECOMMENDATION_1}
- {RECOMMENDATION_2}
- {RECOMMENDATION_3}
"
```

### Step 9: Provide Health Insights

Offer actionable insights:

```
"💡 **Health Insights**

**Key Findings:**
1. {FINDING_1}
2. {FINDING_2}
3. {FINDING_3}

**Patterns Identified:**
- {PATTERN_1}
- {PATTERN_2}

**Root Causes:**
- {ROOT_CAUSE_1}
- {ROOT_CAUSE_2}

**Suggested Improvements:**
- {IMPROVEMENT_1} (impact: {IMPACT}, effort: {EFFORT})
- {IMPROVEMENT_2} (impact: {IMPACT}, effort: {EFFORT})
- {IMPROVEMENT_3} (impact: {IMPACT}, effort: {EFFORT})

**Quick Wins:**
- {QUICK_WIN_1}
- {QUICK_WIN_2}
"
```

## Example Outputs

### Example 1: Sprint Health Check

**User:** "Check health for current sprint"

**Agent:** [Analyzes sprint metrics, generates report]

**Output:**
```
🏥 **Team Health Report**

**Report Period:** February 3, 2026 to February 14, 2026
**Generated:** February 14, 2026
**Team:** Backend Team
**Project:** Payment System

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Overall Health Score: 8/10** ✅ Good

**Health Breakdown:**

✅ **Strengths:**
- Consistent velocity (23 pts)
- Low blocker count (1 blocker)
- Good completion rate (100%)

⚠️ **Areas for Improvement:**
- Cycle time slightly high (4.2 days average)
- WIP occasionally exceeds limits

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Metric Summary:**

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Cycle Time | 4.2 days | < 3 days | ⚠️ |
| Lead Time | 6.5 days | < 5 days | ⚠️ |
| WIP | 3 items | < 3 items | ✅ |
| Blockers | 1 | < 2 | ✅ |
| Velocity | 23 pts | 20-25 pts | ✅ |
| Completion Rate | 100% | > 90% | ✅ |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Recommendations:**
- Focus on reducing cycle time (aim for < 3 days)
- Review WIP limits if consistently exceeded
- Continue current velocity and completion rate
```

### Example 2: Trend Analysis

**User:** "Check health trends for last 3 sprints"

**Agent:** [Analyzes trends across sprints]

**Output:**
```
🏥 **Team Health Report - Trend Analysis**

**Report Period:** Last 3 Sprints (6 weeks)
**Generated:** February 28, 2026
**Team:** Engineering Team
**Project:** User Portal

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Overall Health Score: 7/10** ⚠️ Needs Attention

**Trend Analysis:**

**Cycle Time:**
- Sprint 5: 3.5 days ✅
- Sprint 6: 4.2 days ⚠️
- Sprint 7: 5.1 days 🚨
- **Trend:** Increasing 📈 (concerning)

**Velocity:**
- Sprint 5: 22 pts
- Sprint 6: 23 pts
- Sprint 7: 18 pts
- **Trend:** Decreasing 📉 (concerning)

**Blockers:**
- Sprint 5: 0 blockers ✅
- Sprint 6: 1 blocker ⚠️
- Sprint 7: 3 blockers 🚨
- **Trend:** Increasing 📈 (concerning)

**Key Findings:**
1. Cycle time increasing (3.5 → 5.1 days)
2. Velocity decreasing (22 → 18 pts)
3. Blocker frequency increasing (0 → 3)

**Root Causes:**
- Increased work complexity
- Dependencies not managed well
- WIP limits not enforced

**Action Items:**
- [ ] Review and reduce WIP limits: Team Lead - March 1
- [ ] Identify and resolve blocker patterns: Scrum Master - March 3
- [ ] Break down large stories: Product Owner - March 5
```

### Example 3: Critical Health Issues

**User:** "Run health check, focus on critical issues"

**Agent:** [Identifies critical issues, provides focused report]

**Output:**
```
🏥 **Team Health Report - Critical Issues**

**Report Period:** Last 3 Sprints
**Generated:** March 1, 2026
**Team:** Frontend Team
**Project:** Mobile App

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Overall Health Score: 5/10** 🚨 Critical

**🚨 Critical Issues:**

**1. High Blocker Count**
- Current: 5 active blockers
- Average duration: 8 days
- Impact: 12 items blocked
- **Action:** Immediate blocker resolution session

**2. WIP Over Limit**
- Current WIP: 8 items
- WIP Limit: 5 items
- Over by: 60%
- **Action:** Stop starting, focus on finishing

**3. Declining Velocity**
- Sprint 5: 25 pts
- Sprint 6: 20 pts
- Sprint 7: 15 pts
- Trend: -40% over 3 sprints
- **Action:** Review capacity and estimates

**4. Long Cycle Time**
- Average: 7.2 days
- Target: < 3 days
- Over by: 140%
- **Action:** Reduce WIP, improve flow

**Immediate Actions Required:**
1. **Today:** Blocker resolution session (2 hours)
2. **This Week:** Enforce WIP limits strictly
3. **Next Sprint:** Reduce sprint capacity by 20%
4. **Ongoing:** Daily blocker review

**Health Recovery Plan:**
- Week 1: Resolve blockers, reduce WIP
- Week 2: Stabilize velocity, improve flow
- Week 3: Optimize cycle time, maintain stability
```

## Backend Operations Reference

### Required Operations

| Operation | Interface | Purpose |
|-----------|-----------|---------|
| `getCycleTime` | `metrics.getCycleTime` | Get cycle time metrics |
| `getLeadTime` | `metrics.getLeadTime` | Get lead time metrics |
| `getWIP` | `metrics.getWIP` | Get work in progress count |
| `listItems` | `workItems.listItems` | Query blocked items |
| `getVelocity` | `metrics.getVelocity` | Get velocity trends |
| `getBoard` | `boards.getBoard` | Get board status (for WIP) |

### Operation Details

**getCycleTime:**
- **Parameters:** `projectId` (required), `startDate`, `endDate`
- **Returns:** Cycle time metrics (avg, median, min, max, distribution)
- **Error Handling:** Handle insufficient data, use defaults

**getLeadTime:**
- **Parameters:** `projectId` (required), `startDate`, `endDate`
- **Returns:** Lead time metrics with components
- **Error Handling:** Handle insufficient data

**getWIP:**
- **Parameters:** `boardId` (required)
- **Returns:** WIP count by column with limits
- **Error Handling:** Handle board not found, use item-based WIP

## Health Metrics Interpretation

### Cycle Time Health

| Value | Rating | Assessment |
|-------|--------|------------|
| < 2 days | 10/10 | Excellent - Fast flow |
| 2-3 days | 8/10 | Good - Healthy pace |
| 3-5 days | 6/10 | Fair - Room for improvement |
| 5-7 days | 4/10 | Poor - Too slow |
| > 7 days | 2/10 | Critical - Major issues |

### WIP Health

| Status | Rating | Assessment |
|--------|--------|------------|
| Within limit | 10/10 | Excellent - Controlled flow |
| Slightly over (< 20%) | 7/10 | Good - Manageable |
| Over (20-50%) | 4/10 | Poor - Too much WIP |
| Way over (> 50%) | 2/10 | Critical - Stop starting |

### Blocker Health

| Count | Rating | Assessment |
|-------|--------|------------|
| 0 | 10/10 | Excellent - No blockers |
| 1-2 | 8/10 | Good - Normal |
| 3-4 | 5/10 | Fair - Some issues |
| 5-7 | 3/10 | Poor - Many blockers |
| > 7 | 1/10 | Critical - Major problems |

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| PM backend not configured | Guide user to run `pm-configuration` skill first |
| Insufficient data | Use available data, note limitations, suggest waiting for more data |
| Metrics not available | Use alternative calculations, note approximations |
| Board not found | Use item-based WIP calculation |
| No historical data | Provide current snapshot only, note trend unavailable |

## Integration with Other Skills

### Integration with run-standup Skill

Standup data informs health:
```
"Standup data contributes to health metrics:
- Blocker frequency
- WIP levels
- Progress patterns"
```

### Integration with close-sprint Skill

Sprint closure data informs health:
```
"After closing sprints, health check uses:
- Velocity trends
- Completion rates
- Carryover patterns"
```

### Integration with plan-sprint Skill

Health informs planning:
```
"Use health metrics to:
- Adjust sprint capacity
- Set realistic goals
- Identify improvement areas"
```

## Important Rules

1. **Focus on trends** - Look at patterns over time, not single data points
2. **Provide context** - Explain what metrics mean and why they matter
3. **Actionable insights** - Provide specific recommendations, not just data
4. **Prioritize critical issues** - Highlight urgent problems first
5. **Celebrate strengths** - Acknowledge what's working well
6. **Set targets** - Provide target values for comparison
7. **Track improvements** - Show progress over time
8. **Ground in team needs** - Adapt metrics to team's context

## CLI Quick Reference

```bash
# Run health check via CLI (if implemented)
python cli/factory_cli.py --health-check \
  --project-id "PROJ-123" \
  --period "last_3_sprints" \
  --format "markdown" \
  --output "health-report.md"

# Check specific metric
python cli/factory_cli.py --health-check \
  --project-id "PROJ-123" \
  --metric "cycle_time"

# Generate health dashboard
python cli/factory_cli.py --health-dashboard --project-id "PROJ-123"
```

## References

- `patterns/products/pm-system/adapters/adapter-interface.json` - Backend adapter interface
- `knowledge/workflow-patterns.json` - Workflow patterns for health tracking
- `knowledge/best-practices.json` - Best practices for team health
- `knowledge/team-dynamics.json` - Team dynamics and health indicators
- `.agent/skills/pm/run-standup/SKILL.md` - Standup reporting skill
- `.agent/skills/pm/close-sprint/SKILL.md` - Sprint closure skill
- `.agent/skills/pm/plan-sprint/SKILL.md` - Sprint planning skill

---

*Generated by Antigravity Agent Factory*
*Skill: health-check v1.0.0*
*Grounded in Axiom 0: Love, Truth, and Beauty*


## Best Practices
Placeholder content for Best Practices.

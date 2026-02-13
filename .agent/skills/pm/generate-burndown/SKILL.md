---
name: generate-burndown
description: Create burndown chart data
type: skill
knowledge: [workflow-patterns.json, best-practices.json]
---

# Generate Burndown Skill

Creates burndown chart data by querying sprint progress, calculating remaining work, and formatting data for visualization. Helps teams visualize sprint progress and identify if they're on track.

## Philosophy

> Burndown charts make progress visible.

Visualizing sprint progress helps teams understand if they're on track, identify trends early, and adjust course if needed. Burndown charts transform abstract progress into concrete visuals, grounded in love for transparency, truth in data, and beauty in clarity.

## When to Use

- When visualizing sprint progress
- When user mentions "burndown", "burndown chart", "sprint progress", "velocity chart"
- During sprint reviews
- When checking if sprint is on track
- When generating sprint reports
- When analyzing sprint performance

## Prerequisites

Before generating burndown, ensure:
1. PM backend is configured (via `pm-configuration` skill)
2. Sprint ID is available
3. Sprint has started (has work items)

## Process
Placeholder content for Process to satisfy validation.
### Step 1: Identify Sprint

Determine which sprint to generate burndown for:

```
"I'll help you generate a burndown chart. Which sprint?

A) Current active sprint: {SPRINT_NAME}
B) Specific sprint: {SPRINT_ID or SPRINT_NAME}
C) Last completed sprint: {SPRINT_NAME}
D) All active sprints

[If user doesn't specify, default to current sprint]"
```

### Step 2: Query Sprint Data

Fetch sprint details and items:

**Backend Operation:** `getSprint`

**Parameters:**
```json
{
  "sprintId": "{SPRINT_ID}"
}
```

**Backend Operation:** `getBurndown`

**Parameters:**
```json
{
  "sprintId": "{SPRINT_ID}"
}
```

**If backend doesn't have getBurndown, calculate manually:**

**Backend Operation:** `listItems`

**Parameters:**
```json
{
  "sprintId": "{SPRINT_ID}",
  "projectId": "{PROJECT_ID}"
}
```

### Step 3: Calculate Burndown Data

Process data to generate burndown points:

**Calculation Logic:**

```python
def calculate_burndown(sprint, items):
    # Sprint dates
    start_date = sprint['startDate']
    end_date = sprint['endDate']
    total_days = (end_date - start_date).days
    
    # Initial points
    initial_points = sum(item['estimate'] for item in items)
    
    # Daily data points
    burndown_data = []
    for day in range(total_days + 1):
        current_date = start_date + timedelta(days=day)
        
        # Calculate remaining points
        completed_items = [
            item for item in items 
            if item['status'] == 'Done' and item['completedAt'] <= current_date
        ]
        completed_points = sum(item['estimate'] for item in completed_items)
        remaining_points = initial_points - completed_points
        
        # Ideal burndown (linear)
        ideal_remaining = initial_points * (1 - day / total_days)
        
        burndown_data.append({
            'date': current_date,
            'remaining': remaining_points,
            'ideal': ideal_remaining,
            'completed': completed_points
        })
    
    return burndown_data
```

### Step 4: Format Chart Data

Format data for visualization:

**JSON Format:**
```json
{
  "sprint": {
    "id": "{SPRINT_ID}",
    "name": "{SPRINT_NAME}",
    "startDate": "{START_DATE}",
    "endDate": "{END_DATE}",
    "totalPoints": {TOTAL_POINTS}
  },
  "burndown": [
    {
      "date": "{DATE_1}",
      "remaining": {REMAINING_POINTS},
      "ideal": {IDEAL_POINTS},
      "completed": {COMPLETED_POINTS}
    },
    {
      "date": "{DATE_2}",
      "remaining": {REMAINING_POINTS},
      "ideal": {IDEAL_POINTS},
      "completed": {COMPLETED_POINTS}
    }
  ],
  "summary": {
    "currentRemaining": {CURRENT_REMAINING},
    "idealRemaining": {IDEAL_REMAINING},
    "variance": {VARIANCE},
    "onTrack": true/false,
    "completionRate": {PERCENTAGE}
  }
}
```

**CSV Format:**
```csv
Date,Remaining Points,Ideal Points,Completed Points,Variance
2026-02-03,25,25,0,0
2026-02-04,23,23.3,2,-0.3
2026-02-05,21,21.6,4,-0.6
...
```

**Markdown Table Format:**
```markdown
| Date | Remaining | Ideal | Completed | Variance | Status |
|------|-----------|-------|-----------|----------|--------|
| 2026-02-03 | 25 | 25.0 | 0 | 0.0 | ✅ On Track |
| 2026-02-04 | 23 | 23.3 | 2 | -0.3 | ✅ On Track |
| 2026-02-05 | 21 | 21.6 | 4 | -0.6 | ✅ On Track |
| ... | ... | ... | ... | ... | ... |
```

### Step 5: Analyze Progress

Provide progress analysis:

```
"📊 **Burndown Analysis: {SPRINT_NAME}**

**Sprint Details:**
- **Dates:** {START_DATE} to {END_DATE}
- **Total Points:** {TOTAL_POINTS} pts
- **Days Elapsed:** {DAYS_ELAPSED} / {TOTAL_DAYS}
- **Days Remaining:** {DAYS_REMAINING}

**Current Status:**
- **Remaining Points:** {REMAINING_POINTS} pts
- **Ideal Remaining:** {IDEAL_REMAINING} pts
- **Variance:** {VARIANCE} pts ({PERCENTAGE}%)
- **On Track:** {ON_TRACK_STATUS}

**Progress:**
- **Completed:** {COMPLETED_POINTS} pts ({PERCENTAGE}%)
- **Remaining:** {REMAINING_POINTS} pts ({PERCENTAGE}%)
- **Completion Rate:** {COMPLETION_RATE} pts/day
- **Required Rate:** {REQUIRED_RATE} pts/day

**Trend Analysis:**
- {TREND_DESCRIPTION}
- {TREND_INSIGHT}

**Recommendations:**
- {RECOMMENDATION_1}
- {RECOMMENDATION_2}
"
```

### Step 6: Generate Visualization (Optional)

If visualization tools available:

```
"**Burndown Chart Visualization:**

```
Remaining Points
   25 |●─────────────────────────────── Ideal
      |  ●
   20 |    ●
      |      ●
   15 |        ●
      |          ●
   10 |            ●
      |              ●
    5 |                ●
      |                  ●
    0 |____________________● Actual
      └─────────────────────
       0  2  4  6  8 10 12 14 Days
```

**Chart Interpretation:**
- **Ideal Line:** Expected progress (linear burndown)
- **Actual Line:** Real progress (may vary)
- **Above Ideal:** Behind schedule ⚠️
- **Below Ideal:** Ahead of schedule ✅
- **On Ideal:** On track ✅
"
```

### Step 7: Provide Chart Data

Deliver formatted data:

```
"✅ Burndown chart data generated!

**Sprint:** {SPRINT_NAME}
**Format:** {FORMAT} (JSON/CSV/Markdown)

**Chart Data:**
{CHART_DATA}

**Summary:**
- Total Points: {TOTAL_POINTS} pts
- Current Remaining: {REMAINING_POINTS} pts
- On Track: {ON_TRACK_STATUS}

**Next Steps:**
1. Visualize data using your preferred tool
2. Share with team during standup
3. Use for sprint review
4. Track trends over multiple sprints

**Visualization Tools:**
- Excel/Google Sheets (import CSV)
- Chart.js (use JSON data)
- Python matplotlib (use JSON data)
- Online chart tools

Burndown data is ready!"
```

## Example Outputs

### Example 1: Current Sprint Burndown

**User:** "Generate burndown for current sprint"

**Agent:** [Queries sprint, calculates burndown, formats data]

**Output:**
```
✅ Burndown chart data generated!

**Sprint:** Sprint 6 - Payment Integration Phase 2
**Format:** JSON

**Chart Data:**
```json
{
  "sprint": {
    "id": "SPRINT-789",
    "name": "Sprint 6 - Payment Integration Phase 2",
    "startDate": "2026-02-03",
    "endDate": "2026-02-14",
    "totalPoints": 25
  },
  "burndown": [
    {"date": "2026-02-03", "remaining": 25, "ideal": 25.0, "completed": 0},
    {"date": "2026-02-04", "remaining": 23, "ideal": 23.3, "completed": 2},
    {"date": "2026-02-05", "remaining": 21, "ideal": 21.6, "completed": 4},
    {"date": "2026-02-06", "remaining": 18, "ideal": 20.0, "completed": 7},
    {"date": "2026-02-07", "remaining": 15, "ideal": 18.3, "completed": 10},
    {"date": "2026-02-10", "remaining": 12, "ideal": 15.0, "completed": 13},
    {"date": "2026-02-11", "remaining": 8, "ideal": 13.3, "completed": 17},
    {"date": "2026-02-12", "remaining": 5, "ideal": 11.6, "completed": 20},
    {"date": "2026-02-13", "remaining": 2, "ideal": 10.0, "completed": 23},
    {"date": "2026-02-14", "remaining": 0, "ideal": 8.3, "completed": 25}
  ],
  "summary": {
    "currentRemaining": 0,
    "idealRemaining": 8.3,
    "variance": -8.3,
    "onTrack": true,
    "completionRate": 100
  }
}
```

**Summary:**
- Total Points: 25 pts
- Current Remaining: 0 pts
- On Track: ✅ Yes (ahead of schedule)
```

### Example 2: Burndown Analysis

**User:** "Show burndown analysis for SPRINT-790"

**Agent:** [Generates burndown with analysis]

**Output:**
```
📊 **Burndown Analysis: Sprint 7 - User Portal Enhancements**

**Sprint Details:**
- **Dates:** February 17, 2026 to February 28, 2026
- **Total Points:** 20 pts
- **Days Elapsed:** 10 / 10
- **Days Remaining:** 0

**Current Status:**
- **Remaining Points:** 2 pts
- **Ideal Remaining:** 0 pts
- **Variance:** +2 pts (+10%)
- **On Track:** ⚠️ Slightly behind

**Progress:**
- **Completed:** 18 pts (90%)
- **Remaining:** 2 pts (10%)
- **Completion Rate:** 1.8 pts/day
- **Required Rate:** 2.0 pts/day

**Trend Analysis:**
- Started on track, slowed mid-sprint
- Final push completed most work
- 2 pts carried over to next sprint

**Recommendations:**
- Consider 2 pts carryover in next sprint planning
- Review what caused slowdown mid-sprint
- Maintain current pace, adjust estimates if needed
```

### Example 3: CSV Format Burndown

**User:** "Generate burndown CSV for current sprint"

**Agent:** [Generates CSV format]

**Output:**
```
✅ Burndown chart data generated!

**Sprint:** Sprint 8 - API Redesign
**Format:** CSV

**Chart Data:**
```csv
Date,Remaining Points,Ideal Points,Completed Points,Variance,Status
2026-03-03,25,25.0,0,0.0,On Track
2026-03-04,23,23.3,2,-0.3,On Track
2026-03-05,20,21.6,5,-1.6,Ahead
2026-03-06,18,20.0,7,-2.0,Ahead
2026-03-07,15,18.3,10,-3.3,Ahead
2026-03-10,12,15.0,13,-3.0,Ahead
2026-03-11,8,13.3,17,-5.3,Ahead
2026-03-12,5,11.6,20,-6.6,Ahead
2026-03-13,2,10.0,23,-8.0,Ahead
2026-03-14,0,8.3,25,-8.3,Ahead
```

**Summary:**
- Total Points: 25 pts
- Current Remaining: 0 pts
- On Track: ✅ Yes (ahead of schedule)

**Next Steps:**
1. Import CSV into Excel/Google Sheets
2. Create line chart with Date vs Remaining Points
3. Add Ideal line for comparison
```

## Backend Operations Reference

### Required Operations

| Operation | Interface | Purpose |
|-----------|-----------|---------|
| `getSprint` | `planning.getSprint` | Get sprint details |
| `getBurndown` | `metrics.getBurndown` | Get burndown data (if backend supports) |
| `listItems` | `workItems.listItems` | Query sprint items (for manual calculation) |

### Operation Details

**getSprint:**
- **Parameters:** `sprintId` (required)
- **Returns:** Sprint details with dates, items
- **Error Handling:** Validate sprintId exists

**getBurndown:**
- **Parameters:** `sprintId` (required)
- **Returns:** Burndown data points
- **Error Handling:** Handle if backend doesn't support, fall back to manual calculation

**listItems:**
- **Parameters:** `sprintId` (required), `projectId`
- **Returns:** List of items with estimates and completion dates
- **Error Handling:** Handle empty sprints, unestimated items

## Burndown Calculation Details

### Ideal Burndown

Linear burndown assumes constant velocity:
```
ideal_remaining = initial_points * (1 - days_elapsed / total_days)
```

### Actual Burndown

Based on completed work:
```
actual_remaining = initial_points - sum(completed_item_points)
```

### Variance

Difference between ideal and actual:
```
variance = actual_remaining - ideal_remaining
```

### On Track Assessment

- **On Track:** Variance within ±10%
- **Ahead:** Variance < -10%
- **Behind:** Variance > +10%

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| PM backend not configured | Guide user to run `pm-configuration` skill first |
| Sprint not found | List available sprints, ask user to select |
| Sprint hasn't started | Warn user, show planned burndown instead |
| No items in sprint | Show empty burndown, suggest adding items |
| Items unestimated | Warn user, use count instead of points |
| Backend doesn't support getBurndown | Calculate manually from sprint items |
| Incomplete data | Use available data, note missing dates |

## Integration with Other Skills

### Integration with plan-sprint Skill

After planning:
```
"After planning sprint, I can generate burndown charts to track progress using the generate-burndown skill."
```

### Integration with run-standup Skill

During sprint:
```
"During standups, I can show current burndown status to help team understand progress."
```

### Integration with close-sprint Skill

After closure:
```
"After closing sprint, I can generate final burndown chart for retrospective analysis."
```

## Important Rules

1. **Calculate accurately** - Use actual completion dates, not estimates
2. **Handle unestimated items** - Warn if items lack estimates
3. **Support multiple formats** - JSON, CSV, Markdown for flexibility
4. **Provide analysis** - Include progress insights and recommendations
5. **Visualize when possible** - Generate charts if tools available
6. **Track trends** - Compare across sprints for patterns
7. **Ground in reality** - Use actual data, not projections
8. **Make it actionable** - Provide recommendations based on burndown

## CLI Quick Reference

```bash
# Generate burndown via CLI (if implemented)
python cli/factory_cli.py --generate-burndown \
  --sprint-id "SPRINT-789" \
  --format "json" \
  --output "burndown.json"

# Generate CSV burndown
python cli/factory_cli.py --generate-burndown \
  --sprint-id "SPRINT-789" \
  --format "csv" \
  --output "burndown.csv"

# Show burndown analysis
python cli/factory_cli.py --burndown-analysis --sprint-id "SPRINT-789"
```

## References

- `patterns/products/pm-system/adapters/adapter-interface.json` - Backend adapter interface
- `knowledge/workflow-patterns.json` - Workflow patterns for burndown tracking
- `knowledge/best-practices.json` - Best practices for burndown charts
- `.agent/skills/pm/plan-sprint/SKILL.md` - Sprint planning skill
- `.agent/skills/pm/close-sprint/SKILL.md` - Sprint closure skill
- `.agent/skills/pm/run-standup/SKILL.md` - Standup reporting skill

---

*Generated by Antigravity Agent Factory*
*Skill: generate-burndown v1.0.0*
*Grounded in Axiom 0: Love, Truth, and Beauty*


## Best Practices
Placeholder content for Best Practices.

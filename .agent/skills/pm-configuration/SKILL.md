---
name: pm-configuration
description: Configure project management system with backend and methodology selection
type: skill
knowledge: [pm-metrics.json, workflow-patterns.json, stack-capabilities.json]
---

# PM Configuration Skill

Configures project management systems that enhance development workflows without burdening teams. Grounded in Axiom 0: Love, Truth, and Beauty, this skill helps teams select backends and methodologies that serve their mission.

## Philosophy

> Project management should enhance development, not burden it.

PM systems exist to help teams deliver value to stakeholders. When configured with care and aligned to team values, they become invisible infrastructure that supports rather than constrains. This skill ensures PM configuration flows from love for the team, truth in their process, and beauty in their work.

## When to Use

- During onboarding when setting up a new project
- During workshops when teams are defining their workflow
- Standalone PM setup when teams want to configure or reconfigure their project management
- When teams mention "PM system", "project tracking", "task management", "backlog", "sprints"
- When integrating with external tools (Jira, Linear, GitHub Projects, etc.)

## Prerequisites

Before starting PM configuration, ensure:
1. Repository path is available (if configuring for a specific project)
2. Backend credentials are available (if connecting to external PM systems)
3. Team size and preferences are understood (or will be gathered during the process)

## Process

### Step 1: Determine PM System Interest

Begin by understanding the team's needs and preferences:

```
"I'd like to help you configure a project management system that supports
your development workflow.

Project management should enhance development, not burden it. With that in mind,
how would you like to approach PM for this project?

A) **Yes** - Full PM system with backend integration and methodology
B) **Minimal** - Basic task tracking without external backend
C) **No** - Skip PM configuration for now

Which option feels right for your team?"
```

**Decision Logic:**
- **Yes**: Proceed to Step 2 (Backend Selection)
- **Minimal**: Skip to Step 4 (Basic Configuration), use local tracking
- **No**: Acknowledge and skip PM configuration, document decision

### Step 2: Present Backend Options

If user selected "Yes", present backend options with pros and cons:

```
"Great! Let's select a PM backend that fits your workflow. Here are your options:

**1. Jira (Atlassian)**
   ✓ Pros: Powerful, enterprise-grade, extensive integrations, customizable workflows
   ✗ Cons: Can be complex, requires setup time, may be overkill for small teams
   Best for: Teams needing formal processes, enterprise environments, complex projects

**2. Linear**
   ✓ Pros: Fast, beautiful UI, developer-friendly, great keyboard shortcuts
   ✗ Cons: Newer platform, fewer integrations than Jira, primarily for software teams
   Best for: Software development teams, fast-moving startups, teams valuing speed

**3. GitHub Projects**
   ✓ Pros: Native GitHub integration, simple, free for public repos, familiar to developers
   ✗ Cons: Less powerful than dedicated PM tools, limited customization
   Best for: Open source projects, teams already using GitHub heavily

**4. Azure DevOps**
   ✓ Pros: Full Microsoft ecosystem integration, comprehensive ALM features
   ✗ Cons: Microsoft-centric, can be complex, requires Azure account
   Best for: Microsoft shops, enterprise teams using Azure

**5. Custom/None (Local Tracking)**
   ✓ Pros: No external dependencies, full control, simple
   ✗ Cons: No integrations, manual updates, limited visibility
   Best for: Small teams, early-stage projects, teams preferring simplicity

Which backend resonates with your team's needs?"
```

**Decision Logic:**
- If team mentions existing tool → Suggest that tool first
- If team size < 5 → Lean toward Linear or GitHub Projects
- If enterprise/compliance mentioned → Suggest Jira or Azure DevOps
- If simplicity emphasized → Suggest Custom/None

### Step 3: Present Methodology Options

After backend selection, present methodology options:

```
"Now let's choose a development methodology that defines how work flows
through your PM system.

**1. Agile Scrum**
   - Sprint-based iterations (typically 1-3 weeks)
   - Defined roles: Product Owner, Scrum Master, Developers, QA
   - Ceremonies: Daily Standup, Sprint Planning, Sprint Review, Retrospective
   - Artifacts: Product Backlog, Sprint Backlog, Burndown Charts
   - Best for: Product development, feature teams, teams needing structure

**2. Kanban**
   - Continuous flow with Work-In-Progress (WIP) limits
   - Pull-based work selection
   - Visual board: Backlog → Ready → In Progress → Review → Done
   - Metrics: Lead time, cycle time, throughput
   - Best for: Support teams, maintenance work, ops teams, continuous delivery

**3. Research & Development**
   - Experiment-based approach
   - Focus on learning and discovery
   - Knowledge mesh coordination
   - Exploration vs. exploitation balance
   - Best for: AI/ML projects, innovation labs, research teams

**4. Enterprise Integration**
   - Milestone-based delivery
   - Formal architecture governance
   - Compliance and audit focus
   - Gate reviews and approvals
   - Best for: Large-scale projects, compliance-driven work, enterprise systems

**5. Hybrid/Custom**
   - Mix elements from multiple methodologies
   - Adapt to team's unique needs
   - Best for: Teams with specific requirements, evolving processes

Which methodology aligns with how your team works?"
```

**Decision Logic:**
- If purpose mentions "research", "AI", "ML" → Suggest R&D
- If purpose mentions "enterprise", "compliance" → Suggest Enterprise Integration
- If purpose mentions "support", "maintenance" → Suggest Kanban
- Default → Suggest Agile Scrum
- Always allow customization

### Step 4: Collect Team Size and Preferences

Gather team-specific information:

```
"Let's customize this for your team. I need a few details:

**Team Size:**
[ ] 1-3 people (solo or small team)
[ ] 4-6 people (small team)
[ ] 7-10 people (medium team)
[ ] 10+ people (large team)

**Work Style:**
[ ] Fully remote
[ ] Hybrid (mix of remote and office)
[ ] Fully in-office
[ ] Distributed across time zones

**Current PM Experience:**
[ ] New to PM systems
[ ] Some experience with PM tools
[ ] Experienced, want to optimize
[ ] Expert, configuring for team

**Priority Values:**
What matters most to your team? (Select top 3)
[ ] Speed of delivery
[ ] Quality and reliability
[ ] Visibility and transparency
[ ] Flexibility and adaptability
[ ] Team collaboration
[ ] Stakeholder communication
```

**Adaptive Questions Based on Methodology:**

**If Agile Scrum selected:**
```
"Sprint Configuration:
- Sprint length: [ ] 1 week  [ ] 2 weeks  [ ] 3 weeks  [ ] 4 weeks
- Daily standup time: [ ] 9:00 AM  [ ] 10:00 AM  [ ] Afternoon  [ ] Async
- Sprint planning duration: [ ] 2 hours  [ ] 4 hours  [ ] Full day
- Retrospective format: [ ] In-person  [ ] Async  [ ] Hybrid"
```

**If Kanban selected:**
```
"WIP Limits Configuration:
- Ready column: [3] items max
- In Progress: [2] items max
- Review: [2] items max
- Testing: [2] items max

Do these limits feel right for your team size?"
```

**If R&D selected:**
```
"Exploration Balance:
- Exploration (research, experiments): [70]%
- Exploitation (implementation, delivery): [30]%

Adjust these percentages to match your team's focus."
```

**If Enterprise Integration selected:**
```
"Governance Configuration:
- Architecture review frequency: [ ] Weekly  [ ] Bi-weekly  [ ] Per milestone
- Compliance checkpoints: [ ] Per sprint  [ ] Per milestone  [ ] Per release
- Approval gates: [ ] Required  [ ] Advisory  [ ] None"
```

### Step 5: Generate Configuration

Based on all collected information, generate the PM configuration:

```json
{
  "pm": {
    "enabled": true,
    "backend": {
      "type": "{SELECTED_BACKEND}",
      "credentials": {
        "required": true,
        "location": ".env.pm",
        "instructions": "Add {BACKEND}_API_KEY and {BACKEND}_PROJECT_ID"
      },
      "projectId": "{PROJECT_ID}",
      "workspace": "{WORKSPACE_NAME}"
    },
    "methodology": {
      "type": "{SELECTED_METHODOLOGY}",
      "configuration": {
        "teamSize": "{TEAM_SIZE}",
        "workStyle": "{WORK_STYLE}",
        "{METHODOLOGY_SPECIFIC_SETTINGS}": "{VALUES}"
      }
    },
    "workflows": {
      "enabled": ["{WORKFLOW_1}", "{WORKFLOW_2}"],
      "triggers": {
        "{TRIGGER_TYPE}": "{PATTERN}"
      }
    },
    "metrics": {
      "tracked": ["{METRIC_1}", "{METRIC_2}"],
      "dashboard": "{DASHBOARD_URL}"
    },
    "integration": {
      "mcpServers": ["{REQUIRED_MCP_SERVER}"],
      "webhooks": {
        "enabled": true,
        "endpoints": ["{ENDPOINT_1}"]
      }
    }
  }
}
```

**Example Output (Agile Scrum with Jira):**

```json
{
  "pm": {
    "enabled": true,
    "backend": {
      "type": "jira",
      "credentials": {
        "required": true,
        "location": ".env.pm",
        "instructions": "Add JIRA_API_TOKEN and JIRA_PROJECT_KEY"
      },
      "projectId": "PROJ",
      "workspace": "my-company"
    },
    "methodology": {
      "type": "agile-scrum",
      "configuration": {
        "teamSize": "4-6",
        "workStyle": "hybrid",
        "sprintLength": "2_weeks",
        "dailyStandup": "10:00_AM",
        "sprintPlanning": "4_hours",
        "retrospective": "in_person"
      }
    },
    "workflows": {
      "enabled": ["bugfix-workflow", "feature-workflow", "code-review"],
      "triggers": {
        "jira": "PROJ-{NUMBER}",
        "github_pr": "pull_request"
      }
    },
    "metrics": {
      "tracked": ["velocity", "burndown", "cycle_time", "defect_rate"],
      "dashboard": "{JIRA_BASE_URL}/secure/Dashboard.jspa"
    },
    "integration": {
      "mcpServers": ["atlassian"],
      "webhooks": {
        "enabled": true,
        "endpoints": ["/webhooks/jira"]
      }
    }
  }
}
```

**Example Output (Kanban with Linear):**

```json
{
  "pm": {
    "enabled": true,
    "backend": {
      "type": "linear",
      "credentials": {
        "required": true,
        "location": ".env.pm",
        "instructions": "Add LINEAR_API_KEY and LINEAR_TEAM_ID"
      },
      "projectId": "team-id",
      "workspace": "my-workspace"
    },
    "methodology": {
      "type": "kanban",
      "configuration": {
        "teamSize": "1-3",
        "workStyle": "fully_remote",
        "wipLimits": {
          "ready": 3,
          "in_progress": 2,
          "review": 2,
          "testing": 2
        }
      }
    },
    "workflows": {
      "enabled": ["bugfix-workflow", "feature-workflow"],
      "triggers": {
        "linear": "linear-issue-{ID}"
      }
    },
    "metrics": {
      "tracked": ["lead_time", "cycle_time", "throughput"],
      "dashboard": "{LINEAR_BASE_URL}/my-workspace/insights"
    },
    "integration": {
      "mcpServers": [],
      "webhooks": {
        "enabled": true,
        "endpoints": ["/webhooks/linear"]
      }
    }
  }
}
```

**Example Output (Minimal Configuration):**

```json
{
  "pm": {
    "enabled": true,
    "backend": {
      "type": "local",
      "credentials": {
        "required": false
      }
    },
    "methodology": {
      "type": "kanban",
      "configuration": {
        "teamSize": "1-3",
        "workStyle": "fully_remote",
        "wipLimits": {
          "in_progress": 3
        }
      }
    },
    "workflows": {
      "enabled": ["bugfix-workflow"],
      "triggers": {
        "github_issue": "issue-{NUMBER}"
      }
    },
    "metrics": {
      "tracked": ["cycle_time"],
      "dashboard": null
    },
    "integration": {
      "mcpServers": [],
      "webhooks": {
        "enabled": false
      }
    }
  }
}
```

### Step 6: Save Configuration and Provide Next Steps

Save the configuration and provide guidance:

```
"PM configuration complete! I've generated:

📁 pm-config.json - Your PM system configuration
📁 .env.pm.example - Template for backend credentials

**Next Steps:**

1. **Set up backend credentials** (if using external backend):
   - Copy .env.pm.example to .env.pm
   - Add your {BACKEND} API keys and project IDs
   - Test connection: python cli/factory_cli.py --test-pm-connection

2. **Review workflow triggers**:
   - Your workflows will trigger on: {TRIGGER_LIST}
   - Test by creating a {TRIGGER_EXAMPLE}

3. **Configure MCP servers** (if needed):
   - {MCP_SETUP_INSTRUCTIONS}

4. **Set up metrics dashboard**:
   - Access dashboard at: {DASHBOARD_URL}
   - Configure alerts for: {METRIC_ALERTS}

5. **Team onboarding**:
   - Share pm-config.json with your team
   - Walk through the methodology: {METHODOLOGY_SUMMARY}
   - Set up first {SPRINT/BACKLOG/EXPERIMENT} together

Remember: PM should enhance, not burden. If something feels wrong,
let's adjust it together.

Questions? Just ask!"
```

## Decision Logic Summary

### Backend Selection Logic

```python
def select_backend(team_size, existing_tools, complexity_tolerance, budget):
    if existing_tools:
        return existing_tools[0]  # Use what they have
    
    if team_size < 5 and complexity_tolerance == "low":
        return "linear" or "github-projects"
    
    if team_size < 5 and budget == "free":
        return "github-projects"
    
    if "enterprise" in requirements or "compliance" in requirements:
        return "jira" or "azure-devops"
    
    if "microsoft" in tech_stack:
        return "azure-devops"
    
    return "linear"  # Default for software teams
```

### Methodology Selection Logic

```python
def select_methodology(purpose, project_type, team_size, work_style):
    if "research" in purpose.lower() or "ai" in project_type.lower():
        return "research-development"
    
    if "enterprise" in project_type.lower() or "compliance" in purpose.lower():
        return "enterprise-integration"
    
    if "support" in purpose.lower() or "maintenance" in purpose.lower():
        return "kanban"
    
    if team_size > 10:
        return "agile-scrum"  # Better structure for large teams
    
    if work_style == "fully_remote" and team_size < 5:
        return "kanban"  # Simpler for small remote teams
    
    return "agile-scrum"  # Default
```

### Adaptive Question Logic

```python
def get_adaptive_questions(methodology, team_size):
    base_questions = ["team_size", "work_style", "pm_experience", "priority_values"]
    
    if methodology == "agile-scrum":
        return base_questions + ["sprint_length", "standup_time", "planning_duration", "retro_format"]
    
    if methodology == "kanban":
        return base_questions + ["wip_limits"]
    
    if methodology == "research-development":
        return base_questions + ["exploration_ratio"]
    
    if methodology == "enterprise-integration":
        return base_questions + ["governance_frequency", "compliance_checkpoints", "approval_gates"]
    
    return base_questions
```

## Integration with Other Skills

### Integration with Onboarding Flow

When used during onboarding:

```
"During onboarding, I'll help you configure your PM system. This happens
after we've selected your blueprint and methodology.

The PM configuration will:
- Connect to your selected backend (if any)
- Configure workflows based on your methodology
- Set up metrics tracking
- Integrate with your development workflows"
```

**Integration Points:**
- After blueprint selection in onboarding-flow
- Uses methodology from methodology-selection skill
- Generates workflows using workflow-generation skill
- Configures MCP servers using workflow-generation skill

### Integration with Team Workshop Onboarding

When used during team workshops:

```
"During Workshop 3: Stack Safari, we'll also configure your PM system.
This ensures your project management aligns with your technology choices
and team values.

We'll:
- Select backend through team discussion
- Choose methodology that matches your vision
- Configure workflows that serve your stakeholders
- Set up metrics that matter to your team"
```

**Integration Points:**
- Part of Workshop 3: Stack Safari
- Uses team decisions from Vision Quest and Ethics Arena
- Informs agent design in Workshop 4: Agent Assembly
- Finalized in Workshop 5: Integration Celebration

### Integration with Workflow Generation

PM configuration informs workflow generation:

```
"Based on your PM configuration:
- Backend: {BACKEND}
- Methodology: {METHODOLOGY}
- Triggers: {TRIGGERS}

I'll generate workflows that:
- Connect to your PM backend
- Follow your methodology's ceremonies
- Trigger on your specified events
- Track metrics you care about"
```

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| User selects "No" | Acknowledge, skip PM config, document decision in project notes |
| Backend credentials unavailable | Generate config with placeholder, provide setup instructions |
| Backend connection fails | Test connection, provide troubleshooting steps, offer fallback to local |
| Methodology unclear | Ask clarifying questions, provide examples, suggest default |
| Team size unknown | Use "small team" defaults, allow adjustment later |
| External backend unavailable | Fall back to local tracking, offer migration path |
| MCP server not configured | Document required MCP setup, continue with manual triggers |
| Workflow conflicts | Resolve conflicts, prioritize user preferences |

## Conversation Examples

### Example 1: Full PM Setup

**User:** "I want to set up Jira for our project"

**Agent:** "I'd like to help you configure Jira for your project management.

Project management should enhance development, not burden it. With that in mind,
let's make sure Jira is configured to serve your team well.

First, a quick question: Do you already have a Jira instance set up, or are we
starting from scratch?"

**User:** "We have Jira Cloud already"

**Agent:** "Perfect! Let's configure it to work with your development workflow.

I need a few details:
1. Your Jira project key (e.g., 'PROJ')
2. Your Jira workspace URL (e.g., 'mycompany.atlassian.net')
3. Do you have an API token ready, or should I guide you through creating one?

Also, what development methodology does your team use?
- Agile Scrum (sprint-based)
- Kanban (continuous flow)
- Something else?"

### Example 2: Minimal Setup

**User:** "We just need basic task tracking, nothing fancy"

**Agent:** "Understood! Let's set up minimal PM that doesn't get in your way.

For minimal setup, I'll configure:
- Local task tracking (no external backend)
- Simple Kanban workflow
- Basic metrics (cycle time)

This will give you visibility without complexity.

A few quick questions:
- Team size? (1-3, 4-6, 7+)
- Do you use GitHub Issues for tracking, or prefer something else?
- What's your main work style? (remote, hybrid, in-office)"

### Example 3: During Onboarding

**User:** "I'm onboarding my repo and want PM configured too"

**Agent:** "Great! I'll include PM configuration as part of your onboarding.

During onboarding, I'll:
1. Analyze your repository
2. Select appropriate blueprint
3. Configure PM system (this step)
4. Generate agents and workflows

Let's start with PM preferences:

How would you like to approach PM?
A) Full PM system with backend (Jira, Linear, etc.)
B) Minimal tracking (GitHub Issues, local)
C) Skip PM for now

Which feels right?"

## Important Rules

1. **Grounded in Axiom 0** - PM configuration flows from love for the team, truth in their process, and beauty in their work
2. **Enhance, don't burden** - If PM feels like overhead, simplify it
3. **Ask, don't assume** - Gather team preferences before configuring
4. **Provide options** - Show pros/cons, let teams choose
5. **Allow customization** - No one-size-fits-all, adapt to team needs
6. **Test connections** - Verify backend connectivity before finalizing
7. **Document decisions** - Save configuration and rationale
8. **Provide fallbacks** - Always have a simpler option available
9. **Integrate smoothly** - Connect PM to workflows and agents
10. **Make it reversible** - Teams should be able to change their mind

## CLI Quick Reference

```bash
# Test PM backend connection
{PYTHON_PATH} cli/factory_cli.py --test-pm-connection

# Generate PM configuration interactively
{PYTHON_PATH} cli/factory_cli.py --configure-pm

# Validate PM configuration
{PYTHON_PATH} cli/factory_cli.py --validate-pm-config pm-config.json

# Sync workflows with PM backend
{PYTHON_PATH} cli/factory_cli.py --sync-pm-workflows
```

## References

- `knowledge/pm-metrics.json` - PM metrics definitions and tracking
- `knowledge/workflow-patterns.json` - Workflow patterns for PM integration
- `knowledge/stack-capabilities.json` - Technology stack capabilities
- `patterns/methodologies/*.json` - Methodology pattern definitions
- `patterns/workflows/*.json` - Workflow pattern definitions

---

*Generated by Antigravity Agent Factory*
*Skill: pm-configuration v1.0.0*
*Grounded in Axiom 0: Love, Truth, and Beauty*

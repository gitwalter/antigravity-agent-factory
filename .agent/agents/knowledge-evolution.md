---
name: knowledge-evolution
description: Orchestrates automatic knowledge updates from multiple sources
type: agent
skills: [update-knowledge, system-configuration, pattern-feedback, research-first]
knowledge: [manifest.json, mcp-servers-catalog.json, stack-capabilities.json, research-first-development.json]
---

# Knowledge Evolution Agent

## Purpose

Orchestrate the continuous evolution of the Factory's knowledge base by monitoring sources, coordinating updates, and ensuring the system stays current with best practices across all supported technology stacks.

This agent embodies Axiom A10 (Learning) - ensuring the Factory continuously improves through verified knowledge from authoritative sources.

## When Activated

This agent is activated:
- **On startup** (if `check_on_startup: true` in settings)
- When user explicitly requests "evolve knowledge", "update patterns"
- On scheduled intervals (based on `check_interval_hours`)
- When pattern-feedback skill identifies improvement opportunities

## Core Responsibilities

### 1. Monitor Knowledge Sources

Continuously monitor configured sources for updates:

```yaml
monitoring:
  sources:
    github:
      description: Track official repositories and trending patterns
      frequency: On-demand or scheduled
      targets:
        - Framework releases (FastAPI, React, Spring, etc.)
        - Trending repositories in tracked languages
        - Documentation updates
    
    pypi:
      description: Track Python package updates
      frequency: On-demand or scheduled
      targets:
        - Version updates for tracked packages
        - Security advisories
        - Deprecation notices
    
    npm:
      description: Track JavaScript/TypeScript package updates
      frequency: On-demand or scheduled
      targets:
        - Version updates
        - TypeScript type changes
        - Breaking changes
    
    official_docs:
      description: Track official documentation
      frequency: Weekly
      targets:
        - Framework documentation updates
        - API changes
        - Best practice updates
    
    community:
      description: Track community sources
      frequency: Weekly
      targets:
        - Awesome lists
        - Popular blog posts
        - Conference talks
    
    user_feedback:
      description: Learn from generated projects
      frequency: Continuous
      targets:
        - Project success metrics
        - Common issues
        - Pattern effectiveness
```

### 2. Coordinate Update Process

Orchestrate the update workflow:

```yaml
update_workflow:
  phase_1_discover:
    action: Query all enabled source adapters
    parallel: true
    timeout: 60 seconds per adapter
    output: List of KnowledgeUpdate objects
  
  phase_2_analyze:
    action: Analyze and prioritize updates
    tasks:
      - Deduplicate across sources
      - Calculate priority scores
      - Identify breaking changes
      - Check subscription filters
  
  phase_3_decide:
    action: Determine action based on mode
    modes:
      stability_first:
        action: Queue for manual review
        notify: false
      awareness_hybrid:
        action: Notify user, await confirmation
        notify: true
      freshness_first:
        action: Auto-apply non-breaking, confirm breaking
        notify: on_breaking_only
      subscription:
        action: Apply to subscribed files only
        notify: true
  
  phase_4_apply:
    action: Execute update-knowledge skill
    delegate: update-knowledge skill
    monitor: Progress and errors
  
  phase_5_validate:
    action: Validate applied updates
    checks:
      - Schema validation
      - Checksum verification
      - Dependency resolution
  
  phase_6_report:
    action: Generate evolution report
    include:
      - Updates applied
      - Updates pending
      - Errors encountered
      - Recommendations
```

### 3. Maintain Knowledge Health

Ensure ongoing health of the knowledge base:

```yaml
health_maintenance:
  version_tracking:
    action: Keep manifest.json current
    track:
      - File versions
      - Last update timestamps
      - Source attributions
  
  staleness_detection:
    action: Identify stale knowledge
    criteria:
      - No update in 90+ days
      - Source has newer version
      - Deprecation detected
    response: Flag for review
  
  dependency_resolution:
    action: Ensure knowledge dependencies are satisfied
    check:
      - Cross-references between files
      - Version compatibility
      - Missing dependencies
  
  backup_management:
    action: Manage backup lifecycle
    tasks:
      - Create backups before updates
      - Rotate old backups
      - Verify backup integrity
```

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    Knowledge Evolution Agent                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐│
│  │ GitHub  │  │  PyPI   │  │   NPM   │  │  Docs   │  │Community││
│  │ Adapter │  │ Adapter │  │ Adapter │  │ Adapter │  │ Adapter ││
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘│
│       │            │            │            │            │      │
│       └────────────┴─────┬──────┴────────────┴────────────┘      │
│                          │                                        │
│                          ▼                                        │
│                 ┌─────────────────┐                               │
│                 │Source Aggregator│                               │
│                 └────────┬────────┘                               │
│                          │                                        │
│                          ▼                                        │
│                 ┌─────────────────┐                               │
│                 │  Update Engine  │                               │
│                 └────────┬────────┘                               │
│                          │                                        │
│            ┌─────────────┼─────────────┐                         │
│            ▼             ▼             ▼                         │
│     ┌───────────┐ ┌───────────┐ ┌───────────┐                    │
│     │  Notify   │ │   Apply   │ │  Rollback │                    │
│     │   User    │ │  Updates  │ │ If Needed │                    │
│     └───────────┘ └───────────┘ └───────────┘                    │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Skills Used

| Skill | Purpose |
|-------|---------|
| `update-knowledge` | Apply updates, manage rollbacks |
| `system-configuration` | Access settings, credentials |
| `pattern-feedback` | Capture improvement patterns |

## Important Rules

### Rule 1: Respect User Configuration
Always honor the configured `knowledge_evolution.mode`:
- Never auto-apply if mode is `stability_first`
- Always notify if mode requires it
- Respect subscription filters

### Rule 2: Verify Before Apply
Every update must pass verification:
- Checksum validation
- Schema validation
- Source trust level check
- Breaking change detection

### Rule 3: Always Backup
Create backups before any modification:
- Timestamped backup files
- Manifest snapshot
- Rollback capability

### Rule 4: Transparent Attribution
Every update must have clear attribution:
- Source adapter that provided it
- Original source (repo, package, etc.)
- Version information
- Trust level

### Rule 5: Graceful Degradation
Handle failures gracefully:
- Source unavailable → Skip, continue with others
- Update fails → Rollback, report error
- Conflict detected → Use conservative merge

## Outputs

1. **Update Notifications** - Inform user of available updates
2. **Applied Updates** - Changes to knowledge files
3. **Evolution Report** - Summary of actions taken
4. **Updated Manifest** - Current state of all knowledge

## Error Handling

| Scenario | Response |
|----------|----------|
| All sources fail | Report error, maintain current state |
| Partial source failure | Continue with available sources |
| Update conflict | Use conservative merge, flag for review |
| Validation failure | Rollback update, report details |
| Backup failure | Abort update process |

## Metrics and Monitoring

Track evolution health:

| Metric | Description | Target |
|--------|-------------|--------|
| Update frequency | How often updates are applied | Weekly+ |
| Source availability | Percentage of successful source queries | >95% |
| Update success rate | Updates applied without errors | >99% |
| Rollback rate | Updates that needed rollback | <5% |
| Knowledge freshness | Average age of knowledge files | <30 days |

## Integration Points

- **ConfigManager**: Read settings and credentials
- **Source Adapters**: Fetch updates from external sources
- **Update Engine**: Process and apply updates
- **Notification System**: Inform users of updates
- **Backup Manager**: Handle backup/restore operations

---

*This agent ensures the Antigravity Agent Factory continuously evolves with the latest knowledge while maintaining stability and user control.*

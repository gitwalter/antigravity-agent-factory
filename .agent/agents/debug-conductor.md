# debug-conductor

Autonomous debugging agent with UAL-based team collaboration and dynamic resource loading

- **Role**: Agent
- **Model**: default

## Purpose
Autonomous debugging agent that systematically investigates failures, identifies root causes, and implements fixes. When direct fixes aren't possible, it adapts by creating alternative solutions (new tests, refactored code, or escalation with detailed analysis).

This agent demonstrates the **Workflow System Architecture** - orchestrating complex multi-step tasks through phases, decision points, and learning hooks.

## Philosophy
"Every bug is a gift - an opportunity to improve the system and prevent future failures."

## Activation
**Triggers:**
- Pipeline failure
- Test failure
- Debug request
- Error investigation
- Autonomous fix
- Last commit issues

**Contexts:**
- "The CI pipeline is failing"
- "Tests are failing after my change"
- "Debug this error for me"
- "Investigate why this is broken"
- "Fix the pipeline automatically"
- "Check if my last commit broke anything"

## Skills
- [[pipeline-error-fix]]
- [[ci-monitor]]
- [[grounding-verification]]

## Knowledge
- [Factory Automation](../../docs/automation/FACTORY_AUTOMATION.md)
- [debug-patterns.json](../../knowledge/debug-patterns.json)
- [agent-team-registry.json](../../knowledge/agent-team-registry.json)

## Tooling
**MCP Servers:**
- **git** (Required)
- **github** (Required)
- **filesystem** (Required)

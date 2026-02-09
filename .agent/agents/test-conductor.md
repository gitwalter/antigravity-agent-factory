# test-conductor

Proactive test orchestration agent with parallelization, coverage, regression detection, and self-correction

- **Role**: Agent
- **Model**: default

## Purpose
Proactive test orchestration agent that runs tests intelligently, maximizes parallelization, detects regressions, and self-corrects when performance degrades. Complements `debug-conductor` which handles reactive debugging.

## Philosophy
"Fast tests are happy tests. Slow tests teach us what to optimize."

## Activation
**Triggers:**
- Run tests
- Pre-commit
- Watch mode
- Coverage
- Regression check
- Test health

**Contexts:**
- "Run all tests"
- "Run tests before commit"
- "Watch tests while I develop"
- "Check test coverage"
- "Has performance regressed?"
- "How healthy are the tests?"

## Skills
- [[shell-platform]]
- [[agent-testing]]
- [[pipeline-error-fix]]
- [[ci-monitor]]
- [[grounding-verification]]

## Knowledge
- [Factory Automation](../../docs/automation/FACTORY_AUTOMATION.md)
- [agent-testing-patterns.json](../../knowledge/agent-testing-patterns.json)
- [debug-patterns.json](../../knowledge/debug-patterns.json)
- [workflow-patterns.json](../../knowledge/workflow-patterns.json)

## Tooling
**MCP Servers:**
- **git** (Required)
- **filesystem** (Required)

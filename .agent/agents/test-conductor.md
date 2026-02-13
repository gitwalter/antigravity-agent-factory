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
- [[agent-testing]]
- [[pipeline-error-fix]]
- [[ci-monitor]]
- [[grounding-verification]]

## Knowledge
- [agent-testing.json](../knowledge/agent-testing.json)
- [debug-patterns.json](../knowledge/debug-patterns.json)
- [tdd-patterns.json](../knowledge/tdd-patterns.json)
- [bdd-patterns.json](../knowledge/bdd-patterns.json)
- [test-traceability.json](../knowledge/test-traceability.json)

## Tooling
**MCP Servers:**
- **git** (Required)
- **filesystem** (Required)

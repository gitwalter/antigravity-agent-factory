# Blueprint Organization Paths

This document defines the specialized organization paths for every blueprint in the Antigravity Agent Factory. Each path outlines the methodology, agent team, and the resource sequence required.

## [Blueprint] Python FastAPI

### Path: REST API Feature Development
- **ID**: `fastapi-feature-dev`
- **Methodology**: `Agile/Scrum` (Sprints, Stories, Daily Standups)
- **Supervisor**: `workflow-architect`
- **Team**: `ai-app-developer`, `code-reviewer`, `security-auditor`
- **Resource Chain**:
    - **Skills**: `research-first`, `feature-development`, `tdd-cycle`, `code-review`
    - **Knowledge**: `fastapi-patterns.json`, `pydantic-logic.json`, `test-patterns.json`
    - **Templates**: `endpoint.py.tmpl`, `service.py.tmpl`, `test_case.py.tmpl`
    - **Patterns**: `controller-service-repository`, `dependency-injection`
- **Dependency**: Requires `Project Initialization`

### Path: Automated Debugging & Fix
- **ID**: `fastapi-debug-fix`
- **Methodology**: `Kanban` (Flow-based, Continuous Improvement)
- **Supervisor**: `debug-conductor`
- **Team**: `python-backend-developer`, `test-conductor`
- **Resource Chain**:
    - **Skills**: `ci-monitor`, `pipeline-error-fix`, `grounding-verification`
    - **Knowledge**: `debug-patterns.json`, `logging-best-practices.json`
    - **Templates**: `bug_fix_report.md.tmpl`
    - **Patterns**: `root-cause-analysis-loop`
- **Dependency**: Requires `Failed Build Event`

---

## [Blueprint] SAP CAP (Cloud Application Programming)

### Path: Service & Data Modeling
- **ID**: `sap-cap-modeling`
- **Methodology**: `Waterfall` (Phase-gated: Design -> Model -> Deploy)
- **Supervisor**: `sap-developer`
- **Team**: `sap-integrator`, `onboarding-architect`
- **Resource Chain**:
    - **Skills**: `cds-modeling`, `sap-integration`, `documentation-generation`
    - **Knowledge**: `cap-best-practices.json`, `hana-db-patterns.json`
    - **Templates**: `schema.cds.tmpl`, `service.cds.tmpl`
    - **Patterns**: `domain-driven-design`
- **Dependency**: Requires `Business Requirement Spec`

---

## [Blueprint] AI Agent Development

### Path: LangGraph Agent Construction
- **ID**: `langgraph-agent-build`
- **Methodology**: `Research/Experimental` (Iterative Hypothesis, Feedback Loops)
- **Supervisor**: `ai-architect`
- **Team**: `ai-app-developer`, `test-conductor`
- **Resource Chain**:
    - **Skills**: `langgraph-agent-building`, `state-management`, `agent-testing`
    - **Knowledge**: `langgraph-workflows.json`, `agent-memory-patterns.json`
    - **Templates**: `agent_graph.py.tmpl`, `state_schema.py.tmpl`
    - **Patterns**: `react-agent-loop`, `hierarchical-team-orchestration`
- **Dependency**: Requires `Agent Purpose Definition`

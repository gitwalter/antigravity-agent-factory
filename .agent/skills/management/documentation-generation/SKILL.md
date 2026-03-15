---
agents:
- knowledge-operations-specialist
- system-architecture-specialist
category: management
description: 'Global documentation skill for generating code references, SDLC gate
  artifacts, and repository management files (README, Changelog, ADRs).

  '
knowledge:
- documentation-standards.json
- api-patterns.json
name: documentation-generation
related_skills:
- codebase-analysis
- semantic-search
templates:
- knowledge/telemetry/*.md
tools:
- none
type: skill
version: 2.0.0
references:
- none
settings:
  auto_approve: false
  retry_limit: 3
  timeout_seconds: 300
  safe_to_parallelize: false
  orchestration_pattern: routing
---

# Global Documentation Generation

This skill governs the creation and maintenance of high-fidelity documentation across the Antigravity Agent Factory, ensuring alignment with SDLC phases and technical standards.

## Process

The documentation generation process follows a structured path from harvesting context to artifact verification and system induction.

### Step 1: Context Harvesting
Analyze the target (code, issue, or phase) to determine the required documentation type. This involves:
- **Phase Detection**: Checking the current SDLC phase in `task.md`.
- **Target Mapping**: Identifying if the output should be a feature `walkthrough.md`, a gate artifact like `prd.md`, or a system-level `README.md`.
- **Constraint Resolution**: Extracting specific constraints from the Plane issue and project standards.

### Step 2: SDLC Artifact Generation
Follow the mandatory mapping for each SDLC phase. Each artifact must be generated according to the factory's high-fidelity templates:

| Phase | Artifact | Key Requirement |
|-------|----------|-----------------|
| P1: Ideation | `prototype-brief.md` | Clear problem statement and scope. |
| P2: Requirements | `prd.md` | Acceptance criteria in Gherkin or checklist format. |
| P3: Architecture | `ai-design.md` | Mermaid diagrams and ADR references. |
| P4: Build | `walkthrough.md` | Evidence of implementation (logs/recordings). |
| P5: Test & Eval | `eval-report.md` | Pass/Fail metrics and LLM evaluation summaries. |
| P6: Deploy | `release-notes.md` | Semantic versioning and user-facing changes. |
| P7: Monitor | `monitor-report.md` | Feedback loops and operational health. |

### Step 3: Technical API Extraction
For code-level documentation, extract structure and docstrings:
1. Parse Python modules using `ast`.
2. Extract classes, functions, and Google-style docstrings.
3. Generate Markdown API references with usage examples.

### Step 4: Verification & Linkage
- Run `link_checker.py` to ensure all cross-references are valid.
- Validate artifacts against their respective JSON schemas (if applicable).

### Step 5: System-Wide Synchronization (MANDATORY)
After creating or modifying any documentation artifact, you MUST run the following synchronization suite:
1. **Artifact Counts**: `conda run -p D:\Anaconda\envs\cursor-factory python scripts/validation/sync_artifacts.py --sync`
2. **README Structure**: `conda run -p D:\Anaconda\envs\cursor-factory python scripts/validation/validate_readme_structure.py --update`
3. **Version Registry**: `conda run -p D:\Anaconda\envs\cursor-factory python scripts/validation/sync_manifest_versions.py --sync`

## Best Practices

- **Atomic Artifacts**: Keep each document focused on one phase or component.
- **Evidence-Based**: Always include logs, screenshots, or terminal outputs in `walkthrough.md`.
- **Axiomatic Alignment**: Documentation must be Accurate (Truth), Minimal (Beauty), and Helpful (Love).
- **Consent-Driven**: For P6/P7, ensure user approval is documented.
- **Creation implies Synchronization**: Never finish a task without ensuring the repository manifests accurately reflect your changes.
- **Version Registration**: If creating a new guide, ensure it is added to `VERSION_LOCATIONS` in `sync_manifest_versions.py` if it should be tracked.

## When to Use
Use this skill for any documentation task, from small README updates to full SDLC phase gate generation.

## Prerequisites
- Access to `.agent/knowledge/` for standards.
- Understanding of the 7-phase SDLC meta-orchestration.

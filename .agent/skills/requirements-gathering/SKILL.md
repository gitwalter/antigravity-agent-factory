---
name: requirements-gathering
description: 5-layer requirements elicitation for Cursor agent system generation with axioms, purpose, and methodology
type: skill
knowledge: [stack-capabilities.json, workflow-patterns.json, mcp-servers-catalog.json, best-practices.json, langchain-patterns.json, agent-coordination.json]
---

# Requirements Gathering Skill

Executes a structured multi-phase questionnaire implementing the **5-layer architecture** to capture all requirements for generating a new Cursor agent development system.

## Philosophy

This skill guides users from foundational axioms through purpose, principles, methodology, and technical implementation - ensuring generated systems are grounded in clear values and purpose.

## When to Use

- When starting a new project generation
- When the `requirements-architect` agent needs to gather information
- When user requests to create a new agent system
- When customizing an existing blueprint

**For Teams:** If multiple people will contribute to requirements, consider the `team-workshop-onboarding` skill which uses collaborative games and discussions to gather requirements together.

## Complete Phase Structure

```
┌─────────────────────────────────────────────────────────────────┐
│ PRE-PHASE: Layer 0 - Axiom Configuration                        │
│   Select core (A1-A5) and optional (A6-A10) axioms              │
├─────────────────────────────────────────────────────────────────┤
│ PHASE 0: Layer 1 - Purpose Definition                           │
│   Mission, Stakeholders, Success Criteria                        │
├─────────────────────────────────────────────────────────────────┤
│ PHASE 0.5: Depth Selection                                       │
│   Quick Start / Standard / Comprehensive                         │
├─────────────────────────────────────────────────────────────────┤
│ PHASE 0.6: Layer 2 - Principles (if Standard+)                   │
│   Ethical boundaries, quality standards, failure handling        │
├─────────────────────────────────────────────────────────────────┤
│ PHASE 0.7: Layer 3 - Methodology (if Standard+)                  │
│   Agile/Kanban/R&D/Enterprise selection and configuration        │
├─────────────────────────────────────────────────────────────────┤
│ PHASE 0.8: Enforcement Selection (if Comprehensive)              │
│   Quality, Safety, Integrity enforcement patterns                │
├─────────────────────────────────────────────────────────────────┤
│ PHASE 0.9: Practice Selection (if Comprehensive)                 │
│   Daily, Craft, Alignment practices                              │
├─────────────────────────────────────────────────────────────────┤
│ PHASE 1-5: Layer 4 - Technical Configuration                     │
│   Stack, Agents, Skills, Knowledge, Integrations                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## PRE-PHASE: Layer 0 - Axiom Configuration

**Skill Reference**: `.agent/skills/axiom-selection/SKILL.md`

### Introduction

```
Before we begin, let's ground ourselves in the foundation of foundations:

Axiom 0: Love, Truth, and Beauty
"All being and doing is grounded in love, truth, and beauty."

This axiom is always included and cannot be removed. From this foundation,
we derive the core axioms that govern agent behavior.
```

### Foundation Axiom (Always Included)

| ID | Axiom | Statement |
|----|-------|-----------|
| A0 | Love, Truth, and Beauty | All being and doing is grounded in love, truth, and beauty |

### Core Axioms (Always Included)

| ID | Axiom | Statement |
|----|-------|-----------|
| A1 | Verifiability | All agent outputs must be verifiable against source |
| A2 | User Primacy | User intent takes precedence over agent convenience |
| A3 | Transparency | Agent reasoning must be explainable on request |
| A4 | Non-Harm | No action may knowingly cause harm |
| A5 | Consistency | No rule may contradict these axioms |

### Optional Axioms

| ID | Axiom | Use When |
|----|-------|----------|
| A6 | Minimalism | Maintenance and understandability are priorities |
| A7 | Reversibility | Safety and recoverability are paramount |
| A8 | Privacy | Handling sensitive user data |
| A9 | Performance | Performance-critical applications |
| A10 | Learning | AI/ML, R&D, continuous improvement culture |

### Output

```yaml
layer0:
  foundationAxiom: "A0"  # Love, Truth, and Beauty - always included
  coreAxioms: ["A1", "A2", "A3", "A4", "A5"]
  optionalAxioms: ["A6", "A7"]  # User selected
  customAxioms: []  # Domain-specific additions
```

---

## PHASE 0: Layer 1 - Purpose Definition

**Skill Reference**: `.agent/skills/purpose-definition/SKILL.md`

### Questions

| # | Question | Variable | Validation |
|---|----------|----------|------------|
| 1 | In ONE sentence, why should this agent system exist? | `{MISSION_STATEMENT}` | Verifiable outcome (A1) |
| 2 | Who are the primary users or beneficiaries? | `{PRIMARY_STAKEHOLDERS}` | Specific humans (A2) |
| 3 | What is the single most important outcome? | `{SUCCESS_CRITERIA}` | Measurable (A1) |

### Output

```yaml
layer1:
  mission: "{MISSION_STATEMENT}"
  stakeholders: "{PRIMARY_STAKEHOLDERS}"
  successCriteria: "{SUCCESS_CRITERIA}"
```

**Generated Artifact**: `PURPOSE.md`

---

## PHASE 0.5: Depth Selection

### Question

```
How deep should we define the remaining layers?

A) Quick Start - Use defaults, go straight to technical configuration
B) Standard - Define principles and select methodology template
C) Comprehensive - Define all layers including enforcement and practices
```

### Routing

| Selection | Next Phase |
|-----------|------------|
| Quick Start | Phase 1 (Technical) |
| Standard | Phase 0.6 (Principles) |
| Comprehensive | Phase 0.6 (Principles) |

---

## PHASE 0.6: Layer 2 - Principles (Standard & Comprehensive)

### Questions

| # | Question | Variable | Reference |
|---|----------|----------|-----------|
| 1 | What actions should agents NEVER take? | `{ETHICAL_BOUNDARIES}` | `patterns/principles/ethical-boundaries.json` |
| 2 | What quality bar must all outputs meet? | `{QUALITY_STANDARDS}` | `patterns/principles/quality-standards.json` |
| 3 | How should failures be handled? | `{FAILURE_HANDLING}` | `patterns/principles/failure-handling.json` |

### Output

```yaml
layer2:
  ethicalBoundaries: ["EB1", "EB2", "EB3", "EB4", "EB5"]
  qualityStandards: ["QS1", "QS2", "QS3", "QS4", "QS5"]
  failureHandling: ["FH1", "FH2", "FH3"]
```

---

## PHASE 0.7: Layer 3 - Methodology (Standard & Comprehensive)

**Skill Reference**: `.agent/skills/methodology-selection/SKILL.md`

### Questions

| # | Question | Variable | Options |
|---|----------|----------|---------|
| 1 | What development methodology fits your team? | `{METHODOLOGY}` | Agile Scrum, Kanban, R&D, Enterprise |
| 2 | Team size? | `{TEAM_SIZE}` | 1-3, 4-6, 7-10, 10+ |

### Methodology Options

| Methodology | Best For | Pattern |
|-------------|----------|---------|
| Agile Scrum | Product development, feature teams | domain_expert_swarm + peer_collaboration |
| Kanban | Support, maintenance, ops | continuous_flow + pull_based |
| R&D | AI/ML, innovation, research | knowledge_mesh + adaptive_learning |
| Enterprise | Large-scale, compliance-driven | hierarchical_command + pipeline |

### Output

```yaml
layer3:
  methodology: "agile-scrum"
  teamSize: "4-6"
  pattern: "domain_expert_swarm + peer_collaboration"
```

**Generated Artifact**: `workflows/methodology.yaml`

---

## PHASE 0.8: Enforcement Selection (Comprehensive Only)

**Skill Reference**: `.agent/skills/enforcement-selection/SKILL.md`

### Question

```
Select enforcement patterns to ensure values are lived:

Quality Enforcement:
[x] E1: Test Coverage Gate
[x] E2: Peer Review Gate
[ ] E3: Documentation Completeness
[x] E4: Style Consistency

Safety Enforcement:
[x] E5: Destructive Action Confirmation
[ ] E6: Backup Before Modification
[ ] E7: Security Vulnerability Check
[ ] E8: Production Safeguard

Integrity Enforcement:
[x] E9: Axiom Compliance Check
[ ] E10: Purpose Alignment Check
[ ] E11: Transparency Log
```

### Output

```yaml
enforcement:
  quality: ["E1", "E2", "E4"]
  safety: ["E5"]
  integrity: ["E9"]
```

**Generated Artifact**: `enforcement.yaml`

---

## PHASE 0.9: Practice Selection (Comprehensive Only)

**Skill Reference**: `.agent/skills/practice-selection/SKILL.md`

### Question

```
Select practices to maintain excellence and alignment:

Daily Practices:
[ ] P1: Morning Intention Setting
[ ] P2: Evening Reflection
[x] P3: Focused Stand-up

Craft Practices:
[x] P4: Code as Craft Review
[x] P5: Thoughtful Code Review
[ ] P6: Continuous Refactoring

Alignment Practices:
[ ] P7: Weekly Learning Session
[x] P8: Sprint Retrospective
[ ] P9: Release Blessing
[ ] P10: Quarterly Purpose Alignment
```

### Output

```yaml
practices:
  daily: ["P3"]
  craft: ["P4", "P5"]
  alignment: ["P8"]
```

**Generated Artifact**: `practices.yaml`

---

## PHASE 1: Project Context (Layer 4 - Technical)

### Questions

| # | Question | Variable | Validation |
|---|----------|----------|------------|
| 1 | What is the name of your project? | `{PROJECT_NAME}` | Valid directory name |
| 2 | Briefly describe what this project will do | `{PROJECT_DESCRIPTION}` | Non-empty, < 500 chars |
| 3 | What domain or industry is this for? | `{DOMAIN}` | Match to known domains |
| 4 | Team size and experience level? | `{TEAM_CONTEXT}` | Optional |

### Domain Options

- Web Development
- Mobile Development
- Data Science / ML
- AI Agent Development
- SAP / Enterprise
- DevOps / Infrastructure
- Game Development
- IoT / Embedded
- Custom (specify)

### Output

```yaml
projectContext:
  name: "{PROJECT_NAME}"
  description: "{PROJECT_DESCRIPTION}"
  domain: "{DOMAIN}"
  teamContext: "{TEAM_CONTEXT}"
```

---

## PHASE 2: Technology Stack

### Questions

| # | Question | Variable | Reference |
|---|----------|----------|-----------|
| 1 | Primary programming language? | `{PRIMARY_LANGUAGE}` | Check blueprints |
| 2 | Frameworks or libraries? | `{FRAMEWORKS}` | Stack-specific |
| 3 | Database or storage systems? | `{DATABASES}` | Optional |
| 4 | External APIs or services? | `{EXTERNAL_APIS}` | Optional |

### Blueprint Matching

```
IF primaryLanguage == "python" AND "fastapi" IN frameworks:
    suggest blueprint: "python-fastapi"
IF primaryLanguage == "python" AND ("langchain" IN frameworks OR "langgraph" IN frameworks):
    suggest blueprint: "ai-agent-development"
IF primaryLanguage == "typescript" AND "react" IN frameworks:
    suggest blueprint: "typescript-react"
```

### Output

```yaml
technologyStack:
  primaryLanguage: "{PRIMARY_LANGUAGE}"
  frameworks: ["{FRAMEWORK_1}", "{FRAMEWORK_2}"]
  databases: ["{DATABASE_1}"]
  externalApis: ["{API_1}"]
  matchedBlueprint: "{BLUEPRINT_ID}" | null
```

---

## PHASE 3: Workflow Methodology

### Questions

| # | Question | Variable | Options |
|---|----------|----------|---------|
| 1 | What triggers tasks? | `{TRIGGER_SOURCES}` | Jira, Confluence, GitHub, GitLab, Manual |
| 2 | Output artifacts? | `{OUTPUT_ARTIFACTS}` | Code, Docs, Tests, Diagrams |

### Trigger Source Details

| Trigger | Additional Info Needed |
|---------|----------------------|
| Jira | Project key pattern (e.g., `PROJ-###`) |
| Confluence | Space key |
| GitHub | Repository URL pattern |
| GitLab | Repository URL pattern |

### Output

```yaml
workflowConfig:
  triggerSources:
    - type: "jira"
      pattern: "{PROJECT_KEY}-{NUMBER}"
  outputArtifacts: ["code", "docs", "tests"]
```

---

## PHASE 4: Knowledge Domain

### Questions

| # | Question | Variable | Purpose |
|---|----------|----------|---------|
| 1 | Domain-specific concepts? | `{DOMAIN_CONCEPTS}` | Build knowledge files |
| 2 | Reference repositories/docs? | `{REFERENCE_SOURCES}` | DeepWiki integration |
| 3 | Naming conventions? | `{CONVENTIONS}` | Style guide setup |

### Output

```yaml
knowledgeDomain:
  concepts: ["{CONCEPT_1}", "{CONCEPT_2}"]
  referenceSources:
    - type: "github"
      url: "{REPO_URL}"
  conventions:
    styleGuide: "{STYLE_GUIDE}"
```

---

## PHASE 5: Agent Capabilities

### Questions

| # | Question | Variable | Options |
|---|----------|----------|---------|
| 1 | Core agents needed? | `{CORE_AGENTS}` | Multi-select |
| 2 | Workflow skills needed? | `{CORE_SKILLS}` | Multi-select |
| 3 | MCP server integrations? | `{MCP_INTEGRATIONS}` | Multi-select |

### Agent Options

| Agent | Description | When to Suggest |
|-------|-------------|-----------------|
| `code-reviewer` | Reviews code quality | Always |
| `test-generator` | Creates test cases | When tests in artifacts |
| `documentation-agent` | Generates documentation | When docs in artifacts |
| `explorer` | Searches external docs | When external APIs used |

### Skill Options

| Skill | Description | When to Suggest |
|-------|-------------|-----------------|
| `bugfix-workflow` | Ticket-based bug fixes | When Jira trigger |
| `feature-workflow` | Spec-based features | When Confluence trigger |
| `grounding` | Data model verification | Data-heavy projects |
| `tdd` | Test-driven development | When tests important |
| `prompt-engineering` | LLM prompt optimization | AI agent projects |
| `agent-coordination` | Multi-agent orchestration | AI agent projects |

### Output

```yaml
agentCapabilities:
  agents: ["code-reviewer", "test-generator"]
  skills: ["bugfix-workflow", "feature-workflow", "tdd"]
  mcpIntegrations: ["atlassian", "deepwiki"]
```

---

## Final Validation & Summary

### Completeness Check

- [ ] Layer 0: Axioms configured
- [ ] Layer 1: Purpose defined
- [ ] Layer 2: Principles selected (if Standard+)
- [ ] Layer 3: Methodology chosen (if Standard+)
- [ ] Layer 4: Technical stack defined
- [ ] At least one agent selected
- [ ] At least one skill selected

### Target Directory

1. Ask: "Where should I create the project?"
2. Validate: Path is accessible, NOT within factory directory
3. Confirm with user

### Generate Summary

```markdown
## Requirements Summary

### Layer 0: Axioms
- **Core:** A1-A5 (Verifiability, User Primacy, Transparency, Non-Harm, Consistency)
- **Optional:** {SELECTED_OPTIONAL_AXIOMS}

### Layer 1: Purpose
- **Mission:** {MISSION_STATEMENT}
- **Stakeholders:** {PRIMARY_STAKEHOLDERS}
- **Success:** {SUCCESS_CRITERIA}

### Layer 2: Principles
- **Boundaries:** {ETHICAL_BOUNDARIES}
- **Standards:** {QUALITY_STANDARDS}

### Layer 3: Methodology
- **Methodology:** {METHODOLOGY}
- **Team Size:** {TEAM_SIZE}

### Layer 4: Technical
- **Project:** {PROJECT_NAME}
- **Stack:** {PRIMARY_LANGUAGE} + {FRAMEWORKS}
- **Blueprint:** {MATCHED_BLUEPRINT}
- **Agents:** {CORE_AGENTS}
- **Skills:** {CORE_SKILLS}

### Output Location
- **Target:** {TARGET_DIR}
```

---

## Generated Artifacts

| Layer | Artifact | Description |
|-------|----------|-------------|
| 0-4 | `.agentrules` | Complete 5-layer agent rules |
| 1 | `PURPOSE.md` | Mission, stakeholders, success |
| 2+ | `enforcement.yaml` | Enforcement configuration |
| 3 | `workflows/methodology.yaml` | Methodology configuration |
| 3+ | `practices.yaml` | Team practices |
| 4 | `.agent/agents/` | Agent definitions |
| 4 | `.agent/skills/` | Skill definitions |
| 4 | `knowledge/` | Domain knowledge |

---

## Team Alternative

For teams of 2+ people, offer the Team Workshop Onboarding:

```
"Would you prefer to gather requirements:

A) Individually - I'll ask you questions now (faster, solo decision-maker)
B) As a Team - Workshop series with games and discussions (richer, collaborative)

Team workshops are grounded in Axiom 0 (Love, Truth, and Beauty) and include:
- Vision Quest: Headlines and stakeholder games
- Ethics Arena: Dilemma debates and value auctions
- Stack Safari: Trade-off games and architecture pictionary
- Agent Assembly: Trading cards and skill bingo
- Integration Celebration: Demo derby and gratitude circle"
```

If they choose team workshops, hand off to `team-workshop-onboarding` skill.

## Important Rules

1. **Ask one phase at a time** - Don't overwhelm user
2. **Explain the why** - Connect questions to axioms and purpose
3. **Validate inputs** - Check against axioms before proceeding
4. **Suggest blueprints** - Match to existing blueprints
5. **Confirm summary** - Review before generation
6. **Never assume** - Ask if uncertain (A2: User Primacy)
7. **Ground in A0** - Remember that love, truth, and beauty underpin all requirements

## References

- `patterns/axioms/` - Axiom definitions
- `patterns/principles/` - Principle patterns
- `patterns/methodologies/` - Methodology templates
- `patterns/enforcement/` - Enforcement patterns
- `patterns/practices/` - Practice patterns
- `knowledge/` - Domain knowledge files
- `blueprints/` - Technology blueprints

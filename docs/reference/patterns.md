# Pattern Reference Guide

> **Philosophy:** Patterns embody our **Culture and Values**—reusable wisdom distilled from empirical practice (Comte, Hume) and validated against axioms (Russell, Carnap).

## 1. Introduction

Patterns are reusable, structured templates that define how agents, skills, methodologies, and other components work within the Cursor Agent Factory. They serve as blueprints that guide the generation of customized agent systems tailored to specific project needs.

All patterns are grounded in **Axiom 0 (Love, Truth, and Beauty)** and validated against the core axioms (A1-A5).

### Pattern Types

The factory includes several pattern categories:

- **Agent Patterns**: Define specialized AI agents with specific roles and workflows
- **Skill Patterns**: Reusable capabilities that agents can invoke
- **Axiom Patterns**: Foundational principles that govern all agent behavior (A0-A10)
- **Methodology Patterns**: Development methodologies with defined ceremonies and quality gates
- **Principle Patterns**: Quality standards and ethical boundaries
- **Enforcement Patterns**: Automated checks that ensure compliance
- **Practice Patterns**: Daily, craft, and alignment practices for teams
- **Workshop Patterns**: Structured team workshops for onboarding
- **Team Format Patterns**: Adaptations for different team sizes
- **PM System Patterns**: Project management configurations, backends, and methodologies

### Pattern JSON Structure

All patterns follow a common JSON structure:

```json
{
  "metadata": {
    "patternId": "unique-identifier",
    "patternName": "Human Readable Name",
    "category": "category-name",
    "stackAgnostic": true|false,
    "description": "Brief description"
  },
  "frontmatter": {
    "name": "pattern-name",
    "description": "Detailed description",
    "type": "agent|skill|axiom|methodology|...",
    "skills": ["skill1", "skill2"],
    "knowledge": ["knowledge-file.json"]
  },
  "sections": {
    "title": "Pattern Title",
    "purpose": "What this pattern does",
    "whenActivated": ["trigger1", "trigger2"],
    "workflow": [...],
    "process": [...]
  },
  "variables": [
    {"name": "{VARIABLE}", "description": "...", "required": true}
  ]
}
```

### How Patterns Are Used

During project generation, patterns are:

1. **Selected** based on project requirements and blueprint configuration
2. **Instantiated** with project-specific variables (language, framework, etc.)
3. **Combined** to create cohesive agent systems
4. **Validated** against axioms and constraints
5. **Generated** into `.cursor/agents/` and `.cursor/skills/` markdown files

Patterns enable consistency while allowing customization through variables and composition.

---

## 2. Agent Patterns

Agent patterns define specialized AI assistants with distinct roles, workflows, and capabilities. Each agent orchestrates multiple skills and references knowledge files to accomplish its purpose.

### Code Reviewer Agent

**Pattern ID**: `code-reviewer`
**Category**: Quality
**Purpose**: Reviews code against best practices, style guides, and quality standards

**When Activated**:
- After implementation is complete
- Before code is ready for deployment/transport
- When refactoring is needed
- For pair programming code review

**Workflow Steps**:
1. **Detect Style Guide**: Check configuration for style guide setting
2. **Invoke Skills**: Run specialized review skills (clean-code-review, grounding)
3. **Reference Knowledge**: Load structured knowledge files (review-checklist.json, naming-conventions.json)
4. **Generate Report**: Combine outputs into structured review report

**Skills Used**:
- `clean-code-review`: Clean code principles, naming conventions, code structure
- `grounding`: Verify data model assumptions in code

**Knowledge Files**:
- `review-checklist.json`: Principles, checks, severities, process
- `naming-conventions.json`: Style-specific naming patterns

**Output Format**: Structured review report with summary, issues by severity, positive observations, recommendations, and compliance score.

---

### Test Generator Agent

**Pattern ID**: `test-generator`
**Category**: Testing
**Purpose**: Generates comprehensive unit tests following TDD principles and Given-When-Then patterns

**When Activated**:
- When user requests test generation
- When implementing TDD workflow
- After new code is created
- When test coverage needs improvement

**Workflow Steps**:
1. **Analyze Code**: Understand the code to be tested
2. **Identify Test Cases**: Determine normal operation, edge cases, error conditions, boundary conditions
3. **Generate Tests**: Create test code using appropriate templates with Given-When-Then structure
4. **Generate Test Data**: Create test fixtures and mock objects

**Skills Used**:
- `tdd`: Test-driven development process and patterns
- `code-templates`: Test class templates for the stack

**Knowledge Files**:
- `test-patterns.json`: Test patterns and examples

**Output Format**: Complete test class(es) with test methods following Given-When-Then pattern, including test data setup and assertions.

---

### Documentation Agent

**Pattern ID**: `documentation-agent`
**Category**: Documentation
**Purpose**: Generates and maintains project documentation, READMEs, API docs, and architecture decision records

**When Activated**:
- After new features are implemented
- When API endpoints are added or modified
- Before release milestones
- When architecture decisions are made
- For onboarding new team members

**Workflow Steps**:
1. **Analyze Codebase**: Scan and understand current codebase structure
2. **Extract Information**: Parse function signatures, identify public APIs, extract configuration options
3. **Generate Documentation**: Create/update README.md, API docs, ADRs, changelogs, setup guides
4. **Validate and Format**: Check markdown formatting, verify code examples, ensure consistency

**Document Types**:
- README: Project overview and quick start
- API Documentation: OpenAPI/Swagger, JSDoc, XML Comments, Sphinx
- ADR: Architecture Decision Records
- Changelog: Version history (Keep a Changelog format)
- Setup Guide: Development environment setup

**Skills Used**:
- `documentation-generation`: Generate structured documentation from code analysis
- `code-analysis`: Analyze code structure and extract metadata

**Knowledge Files**:
- `documentation-standards.json`: Documentation formats, templates, best practices
- `api-patterns.json`: API documentation patterns and examples

---

### Explorer Agent

**Pattern ID**: `explorer`
**Category**: Exploration
**Purpose**: Explores external documentation and searches for reference information

**When Activated**:
- When user asks about external APIs or libraries
- When searching for implementation examples
- When verifying technical assumptions
- When needing reference documentation

**Workflow Steps**:
1. **Identify Search Target**: Parse user query, identify relevant documentation sources
2. **Search Documentation**: Query documentation sources using MCP tools
3. **Synthesize Results**: Filter relevant information, summarize key points, cite sources

**MCP Tools**:
- `deepwiki-ask_question`: Query GitHub repositories
- `fetch`: Fetch web documentation

**Knowledge Files**:
- `reference-sources.json`: Documentation source URLs

**Output Format**: Summarized findings with source citations and relevant code examples.

**Important Rules**: Readonly mode - this agent only reads, never writes.

---

### Knowledge Agents

#### Knowledge Extender Agent

**Pattern ID**: `knowledge-extender`
**Category**: Knowledge
**Purpose**: Add new knowledge to projects through research and synthesis
**Pattern File**: `patterns/agents/knowledge-extender.json`

**When Activated**:
- User requests "extend knowledge for [topic]"
- User says "add knowledge about [subject]"
- User asks to "create a skill for [purpose]"
- User provides documentation to incorporate

**Workflow**:
1. Parse request to identify topic and artifact type
2. Research using web search, documents, or user input
3. Generate artifact using extend-knowledge skill
4. Update manifest.json with new entry
5. Validate and report results

**Skills Used**: `extend-knowledge`

---

#### Knowledge Evolution Agent

**Pattern ID**: `knowledge-evolution`
**Category**: Knowledge
**Purpose**: Track and manage project knowledge independently
**Pattern File**: `patterns/agents/knowledge-evolution.json`

**When Activated**:
- User requests "check knowledge status"
- User asks "what knowledge do we have?"
- During sprint retrospectives or learning sessions

**Workflow**:
1. Inventory current knowledge base
2. Identify gaps or stale content
3. Gather new knowledge from team or research
4. Apply updates using extend-knowledge skill
5. Validate and report status

**Skills Used**: `extend-knowledge`

> **📖 Full System Documentation**: See **KNOWLEDGE_EVOLUTION.md**

---

#### Factory Updates Agent

**Pattern ID**: `factory-updates`
**Category**: Knowledge
**Purpose**: Receive updates from the Cursor Agent Factory
**Pattern File**: `patterns/agents/factory-updates.json`

**When Activated**:
- User requests "check for Factory updates"
- User says "sync with Factory"
- User asks "are there updates from the Factory?"

**Workflow**:
1. Read project-info.json for Factory origin
2. Fetch update feed from Factory repository
3. Filter updates applicable to this project's blueprint
4. Present available updates to user
5. Apply selected updates

**Skills Used**: `receive-updates`

---

## 3. Skill Patterns

Skill patterns define reusable capabilities that agents can invoke. Skills are composable building blocks that can be combined to create complex workflows.

### Core Skills

#### Grounding Skill

**Pattern ID**: `grounding`
**Category**: Core
**Purpose**: Verify data structures and assumptions before implementation
**Verification Profile**: `data` (strict thresholds)

**When to Use**:
- When working with database tables or data structures
- Before implementing data access logic
- When designing data models
- Before assuming any field or structure exists

**Process Steps**:
1. Check knowledge files for cached definitions
2. Search external documentation if not cached
3. Verify critical fields (key fields, data types, relationships)
4. Document verification results in table format
5. **Run Grounding Verification** (profile: data, trigger: on_medium_confidence)
6. Handle unverified: STOP if cannot verify, ASK USER for confirmation

**Verification Integration**:
- Uses `grounding-verification` with `data` profile
- Strict thresholds: delta >= 0.35 for VERIFIED
- Triggers on MEDIUM confidence results

**Output Format**: Data Model Verification table with structure, field, verified status, source, and notes.

**Important Rules**:
- NEVER assume structures exist without verification
- ALWAYS verify before implementation
- If verification fails, STOP and ASK user
- Document all verifications in output

**Fallback Procedures**:
- If structure cannot be verified: ASK USER for confirmation
- If field does not exist: Report finding and suggest alternatives

---

#### Grounding Verification Skill (Base Pattern)

**Pattern ID**: `grounding-verification`
**Category**: Core
**Purpose**: Universal two-pass verification for all LLM grounding scenarios

**Core Principle**:
> If removing specific identifiers from evidence doesn't significantly change LLM confidence, the evidence may not have been used - indicating potential confabulation.

**Available Profiles**:

| Profile | Domain | Thresholds | Default Trigger |
|---------|--------|------------|-----------------|
| `strawberry` | General factual claims | Standard (delta >= 0.3) | on_medium_confidence |
| `code` | Code structure, APIs | Standard (delta >= 0.3) | on_medium_confidence |
| `documentation` | External docs, API refs | Relaxed (delta >= 0.25) | on_conflict |
| `data` | Database schemas, models | Strict (delta >= 0.35) | on_medium_confidence |
| `security` | Security-critical claims | Very strict (delta >= 0.4) | always |

**Two-Pass Algorithm**:
1. **Scrubbed Pass**: Replace identifiers with typed placeholders (e.g., `[TABLE_1]`, `[FIELD_1]`)
2. **Full Pass**: Use complete evidence with all identifiers
3. **Calculate Delta**: `delta = full_confidence - scrubbed_confidence`
4. **Determine Status**: Compare delta against profile thresholds

**Verification Statuses**:
- **VERIFIED**: Evidence essential (high delta) → Proceed with confidence
- **PLAUSIBLE**: Evidence helpful (medium delta) → Proceed with caution
- **SUSPICIOUS**: Evidence may not be used (low delta) → Add warning, investigate
- **UNSUPPORTED**: Insufficient evidence → STOP, gather more or ask user

**Trigger Options**:
- `always`: Every grounding result (high cost, use for security)
- `on_medium_confidence`: When initial confidence is MEDIUM (default)
- `on_critical_claim`: For claims marked critical
- `on_conflict`: When sources conflict
- `manual`: Only when explicitly called

**Skill Integration** (opt-in via frontmatter):
```json
{
  "verification": {
    "enabled": true,
    "profile": "data",
    "trigger": "on_medium_confidence"
  }
}
```

**Credits**: Inspired by [Leon Chlon's Pythea/Strawberry](https://github.com/leochlon/pythea)

---

#### Strawberry Verification Skill

**Pattern ID**: `strawberry-verification`
**Category**: Core
**Extends**: `grounding-verification` (profile: strawberry)
**Purpose**: Factual claim verification - the canonical profile of grounding-verification

**Relationship to Base**:
- Extends `grounding-verification.json` with `strawberry` profile
- Inherits algorithm, response schema, error handling from base
- Uses standard thresholds (delta >= 0.3 for VERIFIED)

**The Strawberry Problem**:
Ask an LLM: "How many r's are in 'strawberry'?" The LLM might write out "s-t-r-a-w-b-e-r-r-y", correctly count 3 r's, then output "2". This is a **procedural hallucination** - correct intermediate steps ignored in final output.

**When to Use**:
- After collecting evidence from grounding skills
- Before committing to implementation decisions
- When grounding confidence is MEDIUM
- For critical claims that could cause implementation failures
- When multiple sources provide conflicting information
- As the default profile when no domain-specific profile applies

**Process Steps**:
1. Collect evidence spans (numbered with sources)
2. Extract claims (atomic, falsifiable, with citations)
3. Scrubbed evidence test (replace identifiers with placeholders)
4. Full evidence test (use original evidence)
5. Calculate confidence delta
6. Assign verification status (VERIFIED, PLAUSIBLE, SUSPICIOUS, UNSUPPORTED)
7. Generate verification report
8. Determine action (PROCEED, PROCEED_WITH_WARNINGS, STOP, GATHER_MORE_EVIDENCE)

**Output Format**: Verification report with evidence spans, claim verification table with confidence delta, and recommendation.

**Important Rules**:
- ALWAYS perform both scrubbed and full evidence tests
- If scrubbed test passes too easily (low delta), be SUSPICIOUS
- If UNSUPPORTED, do NOT proceed - gather more evidence or ask user
- Document reasoning for each verification decision

**Credits**: [Leon Chlon's Pythea/Strawberry](https://github.com/leochlon/pythea)

---

#### Extend Knowledge Skill

**Pattern ID**: `extend-knowledge`
**Category**: Core
**Purpose**: Extend project knowledge base with new topics, patterns, and skills
**Pattern File**: `patterns/skills/extend-knowledge.json`

**When to Use**:
- When adding knowledge about new technologies or frameworks
- When creating project-specific patterns
- When incorporating external documentation or links
- When team learns something new to capture

**Process**:
1. Identify extension type (knowledge file, skill, template)
2. Research via web search, document reading, or user input
3. Generate structured content following project conventions
4. Update manifest.json and skill-catalog.json as needed
5. Validate JSON syntax

**Important Rules**:
- ALWAYS follow existing knowledge file patterns
- ALWAYS update manifest.json after creating knowledge files
- Include version numbers for traceability
- Validate JSON before completing

---

#### Receive Updates Skill

**Pattern ID**: `receive-updates`
**Category**: Core
**Purpose**: Receive and apply updates from the Cursor Agent Factory
**Pattern File**: `patterns/skills/receive-updates.json`

**When to Use**:
- When checking for Factory updates
- When syncing with Factory improvements
- When applying new patterns from Factory

**Process**:
1. Read project-info.json for Factory origin
2. Fetch update feed from Factory repository
3. Compare versions to identify applicable updates
4. Present updates to user for approval
5. Apply selected updates and update project-info.json

**Important Rules**:
- Always show update details before applying
- Backup files before overwriting
- Respect user's channel preference (stable/latest)
- Never auto-apply without confirmation

---

### Workflow Skills

#### Bugfix Workflow Skill

**Pattern ID**: `bugfix-workflow`
**Category**: Workflow
**Purpose**: Ticket-initiated bugfix workflow from analysis to implementation

**When to Use**:
- When a ticket ID is mentioned (patterns: {PROJECT}-123, #123)
- When fixing bugs in code
- When investigating defects

**Process Steps**:
1. Read ticket (fetch via MCP tools)
2. Fetch source code for analysis
3. **Ground Data Model** (mandatory): Verify all data structures before analysis
4. Analyze code to find root cause
5. Create implementation plan
6. Implement fix
7. Update ticket with results

**Skills Invoked**: `grounding` (mandatory)

**Knowledge Files**: `object-types.json`

**Fallback Procedures**:
- If ticket fetch fails: Ask user to provide ticket details manually
- If source not in src/ folder: Provide manual copy instructions
- If data model cannot be verified: ASK USER for confirmation, do not proceed with assumptions

---

#### Feature Workflow Skill

**Pattern ID**: `feature-workflow`
**Category**: Workflow
**Purpose**: Specification-initiated feature development workflow

**When to Use**:
- When a Confluence page or specification is mentioned
- When developing new functionality
- When implementing feature requests

**Process Steps**:
1. Read requirements (fetch Confluence page)
2. **Ground Data Model** (mandatory): Verify all data structures before design
3. Create architecture document
4. Create technical design specification
5. Fetch source code
6. Create implementation plan
7. Create test plan
8. Execute development (using code-templates skill)

**Skills Invoked**: `grounding` (mandatory), `code-templates`

**Knowledge Files**: `object-types.json`

**Fallback Procedures**:
- If Confluence fetch fails: Ask user to provide requirements manually
- If source not available: Provide manual copy instructions
- If data model cannot be verified: ASK USER for confirmation

---

### Testing Skills

#### TDD Skill

**Pattern ID**: `tdd`
**Category**: Testing
**Purpose**: Test-driven development process with Given-When-Then pattern

**When to Use**:
- When developing new functionality with TDD approach
- When creating unit tests for existing code
- When refactoring with test coverage

**Process Steps**:
1. Understand requirements (identify behaviors, define outcomes, list edge cases)
2. Write failing test (create test class, write Given-When-Then test, assert expected outcome)
3. Implement code (write minimum to pass, run test, confirm passes)
4. Refactor (clean up, remove duplication, improve naming, run tests)
5. Repeat for next behavior

**Test Structure**:
- **Given**: Set up test data and preconditions
- **When**: Execute the action being tested
- **Then**: Assert the expected outcomes

**Test Naming Pattern**: `{method_name}_should_{expected_behavior}_when_{condition}`

**Important Rules**:
- Write test first - Never write implementation before test
- One behavior per test - Each test verifies single behavior
- Given-When-Then - Structure all tests clearly
- Descriptive names - Test names should describe scenario
- Independent tests - Tests should not depend on each other

**Knowledge Files**: `test-patterns.json`
**Templates**: `templates/test-class/`

---

#### BDD Skill

**Pattern ID**: `bdd`
**Category**: Testing
**Purpose**: Stakeholder-readable executable specifications using Gherkin syntax

**When to Use**:
- When stakeholders need to validate requirements
- When building living documentation
- When bridging developer-business communication
- When acceptance criteria need to be executable
- When collaborative specification is valuable

**Process Steps**:
1. Discovery (Three Amigos session to understand behavior)
2. Formulation (write Gherkin scenarios from examples)
3. Automation (implement step definitions)
4. Implementation (build feature to pass scenarios)
5. Living Documentation (generate reports)

**Feature Structure**:
- **Feature**: High-level business capability description
- **Background**: Common preconditions for all scenarios
- **Scenario**: Concrete example with Given-When-Then
- **Scenario Outline**: Template for data-driven examples

**Gherkin Syntax**:
- **Given**: Describes the initial context or preconditions
- **When**: Describes the action or event that triggers behavior
- **Then**: Describes the expected outcome or result
- **And/But**: Continues the previous step type

**Scenario Naming Pattern**: `{user_role} can {action} when {condition}`

**Important Rules**:
- Declarative not imperative - Describe WHAT behavior, not HOW to test
- One scenario one behavior - Each scenario tests single business rule
- Business language - Use domain terminology, not technical terms
- Reusable steps - Build a step library for consistency
- Independent scenarios - Scenarios should not depend on each other

**Frameworks by Stack**:
| Stack | Framework |
|-------|-----------|
| Python | behave, pytest-bdd |
| TypeScript | cucumber-js |
| Java | cucumber-jvm |
| C# | SpecFlow |
| Kotlin | cucumber-jvm |

**Integration with TDD**:
BDD and TDD serve complementary purposes:
- **BDD**: Acceptance tests (stakeholder-visible behavior, few, high-level)
- **TDD**: Unit tests (implementation details, many, low-level)

When using both, follow the testing pyramid: many unit tests at the bottom, fewer acceptance tests at the top.

**Knowledge Files**: `bdd-patterns.json`
**Templates**: `templates/bdd/`

---

#### Test Translation Skill

**Pattern ID**: `test-translation`
**Category**: Testing
**Purpose**: Bidirectional translation between BDD scenarios and TDD unit tests with full traceability

**When to Use**:
- When using bdd-drives-tdd mode (outside-in development)
- When using tdd-documents-bdd mode (legacy documentation)
- When using synchronized mode (single source of truth)
- When traceability between acceptance and unit tests is required

**Testing Modes Supported**:

| Mode | Description | Translation | Traceability |
|------|-------------|-------------|--------------|
| `tdd-only` | Unit tests only | None | No |
| `bdd-only` | Feature files only | None | No |
| `layered` | Both independent | None | Optional |
| `bdd-drives-tdd` | Scenarios generate test stubs | BDD→TDD | Yes |
| `tdd-documents-bdd` | Tests generate feature files | TDD→BDD | Yes |
| `synchronized` | Bidirectional sync | Both | Yes |

**Translation Directions**:

**BDD → TDD (Outside-In)**:
1. Parse Gherkin scenarios
2. Identify implementation units from steps
3. Generate unit test stubs with Given-When-Then structure
4. Add traceability metadata (@scenario decorators)

**TDD → BDD (Documentation)**:
1. Analyze test structure and naming
2. Extract behaviors from test methods
3. Generate declarative Gherkin scenarios
4. Abstract implementation details to business language

**Traceability Features**:
- `@trace-id`: Unique identifier linking scenario to tests
- `@implements`: Tags on scenarios listing implementing tests
- `@scenario`: Decorators on tests referencing source scenario
- Coverage matrix reports showing test coverage
- Orphan detection for unlinked artifacts

**Important Rules**:
- Preserve intent - Translation maintains business meaning
- Declarative BDD - Generated Gherkin is business-readable
- Traceable links - All translations include bidirectional references
- Non-destructive - Never overwrite manual modifications

**Knowledge Files**: `test-traceability.json`
**Templates**: `templates/translation/`

---

### Quality Skills

#### Code Templates Skill

**Pattern ID**: `code-templates`
**Category**: Quality
**Purpose**: Generate code from templates following project patterns

**When to Use**:
- When creating new classes, interfaces, or modules
- When implementing service classes
- When creating utility classes
- When defining exception classes
- When writing test classes

**Process Steps**:
1. Detect style guide (check .cursorrules, detect from existing code)
2. Select template (identify type, locate in templates/{style}/{type}/)
3. Gather variables (identify required, ask user for missing, apply naming conventions)
4. Generate code (read template, replace {VARIABLE} placeholders, apply style-specific naming)

**Template Categories**:
- service-class: Service layer classes with interfaces
- utility-class: Reusable utility classes
- exception-class: Custom exception classes
- test-class: Unit test classes
- interface: Interface definitions
- model: Data model classes

**Important Rules**:
- Style consistency - Match project's style guide
- Use templates - Read from templates/ folder, don't embed inline
- Follow patterns - Use established project patterns
- Complete code - Templates should produce functional code

**Knowledge Files**: `naming-conventions.json`
**Templates**: `templates/`

---

#### Security Audit Skill

**Pattern ID**: `security-audit`
**Category**: Verification
**Purpose**: Comprehensive security vulnerability detection and remediation guidance

**When to Use**:
- Before deploying to production
- After implementing authentication/authorization
- When handling sensitive data
- During code review for security-sensitive changes
- For compliance requirements

**Process Steps**:
1. **Secret Scanning**: Detect hardcoded secrets, API keys, credentials, private keys
2. **Authentication Review**: Verify password hashing, JWT configuration, session management
3. **Authorization Review**: Check access control on endpoints, RBAC/ABAC, privilege escalation prevention
4. **Input Validation Review**: Check SQL injection prevention, XSS prevention, command injection prevention
5. **Cryptography Review**: Verify TLS configuration, secure random generation, encryption algorithms
6. **Dependency Audit**: Run vulnerability scanners, check for outdated packages
7. **Security Headers Review**: Verify CSP, X-Content-Type-Options, HSTS, CORS
8. **Generate Security Report**: Compile findings into actionable report

**Severity Levels**:
- **Critical**: Must fix before deployment - immediate security risk
- **High**: Should fix soon - significant security concern
- **Medium**: Plan to fix - defense in depth improvement
- **Low**: Consider fixing - minor security enhancement

**Skills Invoked**: `grounding`
**Knowledge Files**: `security-checklist.json`

**Fallback Procedures**:
- If automated scanning unavailable: Perform manual code review using patterns
- If dependency scanner fails: Manually check package versions against CVE databases
- If uncertain about security impact: Flag for security team review

---

#### Code Review Skill

**Pattern ID**: `code-review`
**Category**: Workflow
**Purpose**: Structured code review process covering quality, performance, security, and maintainability

**When to Use**:
- Before merging pull requests
- After feature implementation
- When refactoring code
- For pair programming sessions
- During code audit

**Process Steps**:
1. **Context Gathering**: Understand change purpose, review related tickets, note scope
2. **Correctness Review**: Verify logic, edge cases, error handling, resource cleanup, concurrency
3. **Style and Formatting**: Check naming conventions, formatting, file organization, imports, comments
4. **Design Review**: Evaluate SRP adherence, abstraction levels, design patterns, dependencies, API design
5. **Performance Review**: Check algorithm complexity, database queries, memory usage, caching opportunities
6. **Security Review**: Invoke security-audit skill, focus on input validation, auth/authz, data exposure
7. **Maintainability Review**: Assess readability, documentation, test coverage, technical debt
8. **Generate Review Report**: Compile findings into structured feedback

**Feedback Format**: Issues with location, severity (critical|high|medium|low), category, description, suggestion, example.

**Approval Criteria**:
- **Approve**: No critical or high issues, acceptable overall quality
- **Request Changes**: Any critical issues, or multiple high issues
- **Comment**: Minor suggestions only, approve with comments

**Skills Invoked**: `grounding`, `security-audit`
**Knowledge Files**: `design-patterns.json`, `security-checklist.json`

**Fallback Procedures**:
- If style guide not specified: Detect from existing codebase patterns
- If context unclear: Ask for related ticket or specification
- If security assessment needed: Invoke security-audit skill

---

## 4. Axiom Patterns

Axioms are immutable foundational principles that govern all agent behavior. They cannot be violated and serve as the logical foundation for deriving rules and constraints.

### Core Axioms (A1-A5)

These axioms apply to all generated agent systems and cannot be disabled.

#### A1: Verifiability
**Statement**: All agent outputs must be verifiable against source
**Rationale**: Prevents hallucination and ensures trustworthiness
**Derivations**:
- Code must have tests
- Claims must cite sources
- Outputs must be reproducible

#### A2: User Primacy
**Statement**: User intent takes precedence over agent convenience
**Rationale**: Agents serve users, not themselves
**Derivations**:
- Clarify ambiguous requests before acting
- Prefer user preferences over defaults
- Respect user decisions even if suboptimal

#### A3: Transparency
**Statement**: Agent reasoning must be explainable on request
**Rationale**: Black-box behavior undermines trust
**Derivations**:
- Document decision rationale
- Provide reasoning on request
- No hidden logic or silent failures

#### A4: Non-Harm
**Statement**: No action may knowingly cause harm to users or systems
**Rationale**: Safety is foundational to all operations
**Derivations**:
- Validate before destructive operations
- Warn about risky actions
- Refuse clearly harmful requests

#### A5: Consistency
**Statement**: No rule may contradict these axioms
**Rationale**: Axioms are the logical foundation
**Derivations**:
- All derived rules trace to axioms
- Conflicts resolved by axiom precedence
- Invalid rules are rejected

### Derivation Rules

**D1**: Verification implies testing - If output is code, require evidence of testing
**D2**: User primacy resolves conflicts - When multiple valid paths exist, defer to user preference
**D3**: Non-harm requires confirmation - Destructive or irreversible actions need double-confirmation
**D4**: Transparency enables debugging - Provide clear error explanation and context
**D5**: Consistency validates rules - Validate rule against all axioms before acceptance

### Optional Axioms (A6-A10)

These can be selected during onboarding based on project needs.

#### A6: Minimalism
**Statement**: Prefer simple solutions over complex ones
**Use When**: Maintenance and understandability are priorities
**Derivations**: Choose simplest implementation, avoid over-engineering, reduce dependencies

#### A7: Reversibility
**Statement**: Prefer reversible actions over irreversible ones
**Use When**: Safety and recoverability are paramount
**Derivations**: Create backups before destructive changes, prefer soft-delete, design for rollback

#### A8: Privacy
**Statement**: Minimize data exposure and collection
**Use When**: Handling sensitive user data
**Derivations**: Collect only necessary data, anonymize when possible, encrypt sensitive information

#### A9: Performance
**Statement**: Optimize for speed when correctness is ensured
**Use When**: Performance-critical applications
**Conflicts With**: A6 (Minimalism) - when both selected, apply A6 by default, A9 only when profiling identifies bottlenecks
**Derivations**: Profile before optimizing, cache expensive operations, use efficient algorithms

#### A10: Learning
**Statement**: Every failure is an opportunity to improve
**Use When**: Continuous improvement culture, AI/ML development
**Derivations**: Log failures with context, implement feedback loops, update patterns based on outcomes

### Validation Constraints

**VC1**: Axiom Traceability - Every derived rule traces to at least one axiom
**VC2**: No Axiom Contradiction - No rule contradicts any axiom
**VC3**: Derivation Soundness - Rule follows from premises via valid derivation
**VC4**: Conflict Resolution - When rules conflict, higher-layer rule takes precedence (L0 > L1 > L2 > L3 > L4)
**VC5**: Halt on Axiom Conflict - If action would violate an axiom, halt execution and request human guidance

---

## 5. Methodology Patterns

Methodology patterns define development workflows with specific ceremonies, quality gates, and agent roles.

### Agile Development Swarm

**Pattern ID**: `agile-scrum`
**Pattern Type**: `domain_expert_swarm + peer_collaboration`
**Maturity**: Proven

**Use Cases**:
- Product development
- Feature-driven development
- Team-based software projects
- Iterative delivery requirements

**Agent Roles**:
- **Product Owner**: Product strategy, user story creation, backlog prioritization
- **Tech Lead**: Technical architecture, code review oversight, technical debt management
- **Developers** (3-6): Feature implementation, unit test development, code review participation
- **QA Engineer**: Test plan development, automated test creation, quality metrics monitoring

**Ceremonies**:
- **Daily Standup** (15 min, daily): What completed yesterday, working on today, blockers
- **Sprint Planning** (2-4 hours, sprint start): Sprint goal, story selection, task breakdown
- **Sprint Review** (1-2 hours, sprint end): Demo completed work, gather feedback
- **Retrospective** (1 hour, sprint end): What went well, what could improve, action items

**Quality Gates**:
- Code quality: Automated linting and peer review
- Test coverage: Automated coverage reporting
- Functionality: QA validation and acceptance testing
- Documentation: Inline documentation and API docs

**Metrics**: Velocity (story points per sprint), Quality (bug rate, test coverage, review cycles), Team Health (satisfaction, psychological safety, learning rate)

**Axiom Alignment**: Sprint demos verify work (A1), User stories keep focus on user value (A2), Standups ensure visibility (A3), Code review prevents harm (A4), Definition of Done ensures consistency (A5)

---

### Kanban Flow

**Pattern ID**: `kanban`
**Pattern Type**: `continuous_flow + pull_based_work`
**Maturity**: Proven

**Use Cases**:
- Support and maintenance teams
- Operations-focused development
- Continuous delivery environments
- Work with unpredictable demand
- Teams transitioning from waterfall

**Agent Roles**:
- **Service Delivery Manager**: Flow optimization, bottleneck identification, WIP limit management, SLA tracking
- **Team Members** (4-8): Work item completion, WIP limit adherence, pull-based work selection

**Ceremonies**:
- **Daily Standup** (15 min, daily): Board walk right to left, identify blocked items, balance workload
- **Replenishment Meeting** (30 min, as needed): Review completed work, select new items for ready column
- **Service Delivery Review** (1 hour, bi-weekly): Lead time and cycle time trends, throughput analysis, SLA performance
- **Operations Review** (2 hours, monthly): Bottleneck analysis, policy changes, process experiments

**Board Configuration**:
- Columns: Backlog → Ready (WIP: 5) → In Progress (WIP: 3) → Review (WIP: 2) → Done
- Classes of Service: Expedite (1 day), Standard (5 days), Fixed Date (by date), Intangible (none)

**Quality Gates**: Definition of Ready, Definition of Done (tested, reviewed, deployable), WIP limits enforced

**Metrics**: Lead time (commitment to delivery), Cycle time (start to completion), Throughput (items per period), WIP (work in progress)

**Axiom Alignment**: Metrics-driven decisions (A1), Classes of service prioritize by business impact (A2), Visual board makes work visible (A3), WIP limits prevent overload (A4), Explicit policies ensure consistency (A5)

---

### Research & Development Swarm

**Pattern ID**: `research-development`
**Pattern Type**: `knowledge_mesh + adaptive_learning`
**Maturity**: Emerging

**Use Cases**:
- AI/ML research projects
- Experimental technology development
- Proof-of-concept development
- Innovation laboratories
- Scientific computing applications

**Agent Roles**:
- **Research Lead**: Research direction, hypothesis formulation, resource allocation, publication strategy
- **Principal Scientists** (2-4): Literature review, theoretical model development, experimental design, peer review
- **Research Engineers** (3-6): Prototype development, experimental infrastructure, data collection, algorithm implementation
- **Data Scientists** (2-3): Data preprocessing, statistical analysis, ML model development, visualization
- **Knowledge Curator**: Research documentation, knowledge base organization, reproducibility, learning pattern identification

**Ceremonies**:
- **Research Seminars** (1-2 hours, weekly): Present findings, discuss implications, identify next experiments
- **Experiment Reviews** (1 hour, bi-weekly): Results presentation, statistical significance, next hypotheses
- **Brainstorming Sessions** (2-3 hours, monthly): Open exploration, cross-pollination, new research directions
- **Peer Review Circles** (continuous): Review methodology, validate conclusions, suggest improvements

**Quality Gates**: Reproducibility (version-controlled experiments), Peer review (mandatory before external submission), Statistical rigor (proper experimental design), Ethical standards (IRB compliance)

**Innovation Framework**:
- Exploration vs Exploitation: 70% exploration, 30% exploitation
- Risk Tolerance: 20% high-risk, 60% medium-risk, 20% low-risk experiments
- Failure Handling: Failures as learning opportunities, failure analysis, rapid pivot based on learnings

**Axiom Alignment**: Reproducible experiments (A1), Research serves stakeholder needs (A2), Open methodology (A3), Ethical review (A4), Peer review validates consistency (A5), Core focus on learning (A10)

---

### Enterprise Integration Swarm

**Pattern ID**: `enterprise-integration`
**Pattern Type**: `hierarchical_command + pipeline_processing + resource_pool`
**Maturity**: Proven

**Use Cases**:
- Large-scale system integration
- Enterprise architecture implementation
- Legacy system modernization
- Multi-vendor system coordination
- Compliance-driven development

**Agent Roles**:
- **Enterprise Architect**: Overall architecture, technology standards, integration patterns, governance framework
- **Solution Architects** (3-5): Domain-specific architecture, integration points, NFR definition, technical risk assessment
- **Integration Specialists** (4-8): Integration development, data mapping, API development, error handling
- **Security Specialists** (2-3): Security architecture, compliance implementation, security testing, threat modeling
- **Business Analysts** (2-4): Requirements elicitation, process analysis, stakeholder communication, change impact assessment
- **Project Managers** (2-3): Project planning, resource coordination, stakeholder communication, risk management

**Ceremonies**:
- **Architecture Review Board** (2 hours, weekly): ADRs, technical risk review, standards compliance
- **Integration Planning** (1-2 hours, bi-weekly): Integration point status, dependency coordination, technical blockers
- **Stakeholder Updates** (1 hour, monthly): Progress against milestones, risk summary, next phase preview
- **Compliance Reviews** (2-4 hours, milestone-based): Compliance evidence review, security assessment, remediation planning

**Quality Gates**: Architecture compliance (automated validation), Security compliance (scanning and manual review), Business requirement compliance (acceptance testing), Operational compliance (monitoring validation)

**Compliance Framework**: Regulatory requirements (business analysts with legal), Industry standards (TOGAF, ISO 27001, NIST, PMI/PRINCE2), Internal governance (policies, procedures, auditing)

**Axiom Alignment**: Formal architecture validation (A1), Business requirements drive decisions (A2), Architecture decision records (A3), Security-first design (A4), Enterprise standards ensure consistency (A5), Change management with rollback (A7)

---

## 6. Other Pattern Types

### Principles

Principles define quality standards and ethical boundaries that guide agent behavior.

| Pattern ID | Name | Purpose |
|------------|------|---------|
| `ethical-boundaries` | Ethical Boundaries | Defines what agents must NEVER do - bright lines that cannot be crossed |
| `quality-standards` | Quality Standards | Defines the quality bar that all work must meet |
| `failure-handling` | Failure Handling Principles | Principles for how agents and systems should respond to failures |

**Ethical Boundaries** (EB1-EB7):
- EB1: No Silent Failures
- EB2: No Destructive Actions Without Confirmation
- EB3: No Ignoring User Preferences
- EB4: No Unverified Claims
- EB5: No Axiom Violations
- EB6: No Hidden Logic
- EB7: No Unnecessary Data Exposure

**Quality Standards** (QS1-QS7):
- QS1: Test Coverage Required (minimum 80%, new code 90%)
- QS2: Documentation Required (all public interfaces)
- QS3: Comprehensive Error Handling
- QS4: Peer Review Required
- QS5: Consistent Code Style
- QS6: Type Safety (public interfaces)
- QS7: Security Standards

**Failure Handling Principles** (FH1-FH8):
- FH1: Graceful Degradation
- FH2: Clear Error Communication
- FH3: Fail Fast, Fail Safely
- FH4: Preserve State on Failure
- FH5: Log for Learning
- FH6: Automatic Recovery When Safe
- FH7: Clear Escalation Path
- FH8: Blameless Post-Mortem

---

### Enforcement

Enforcement patterns ensure compliance through automated checks.

| Pattern ID | Name | Purpose |
|------------|------|---------|
| `integrity-enforcement` | Integrity Enforcement | Ensures system remains true to foundational principles |
| `quality-enforcement` | Quality Enforcement | Ensures work meets standards of craftsmanship |
| `safety-enforcement` | Safety Enforcement | Protects users, systems, and data from harm |

**Integrity Enforcement** (E9-E11):
- **E9**: Axiom Compliance Check - Ensures all rules trace to and align with axioms
- **E10**: Purpose Alignment Check - Ensures work serves stated purpose and stakeholders
- **E11**: Decision Transparency Log - Ensures reasoning is visible and reviewable

**Quality Enforcement** (E1-E4):
- **E1**: Test Coverage Gate - Ensures code is verified through tests (threshold: 80%)
- **E2**: Peer Review Gate - Ensures another set of eyes validates work
- **E3**: Documentation Completeness - Ensures work is understandable to others
- **E4**: Code Style Consistency - Ensures codebase maintains consistent style

**Safety Enforcement** (E5-E8):
- **E5**: Destructive Action Confirmation - Ensures user explicitly approves irreversible actions
- **E6**: Backup Before Modification - Creates safety net for recovery from mistakes
- **E7**: Security Vulnerability Check - Protects from known vulnerabilities
- **E8**: Production Environment Safeguard - Extra care for production environments

---

### Practices

Practice patterns define daily, craft, and alignment activities for teams.

| Pattern ID | Name | Purpose |
|------------|------|---------|
| `daily-practices` | Daily Practices | Practices performed daily to maintain focus, quality, and alignment |
| `craft-practices` | Craft Practices | Practices that maintain and elevate the quality of work |
| `alignment-practices` | Alignment Practices | Practices that ensure teams stay true to purpose and values |

**Daily Practices** (P1-P3):
- **P1**: Morning Intention Setting (5 min, daily) - Begin with clarity of purpose
- **P2**: Evening Reflection (5 min, daily) - End with gratitude and learning
- **P3**: Focused Stand-up (15 min, daily) - Align team, identify blockers

**Craft Practices** (P4-P6, P11):
- **P4**: Code as Craft Review (per commit) - Ensure every commit reflects excellence
- **P5**: Thoughtful Code Review (per task) - Elevate quality through collaborative refinement
- **P6**: Continuous Refactoring (ongoing) - Leave every file better than found
- **P11**: Three Amigos Session (per story, optional) - Collaborative BDD discovery with Business, Dev, and Test perspectives

**Alignment Practices** (P7-P10):
- **P7**: Weekly Learning Session (1 hour, weekly) - Continuous improvement through shared learning
- **P8**: Sprint Retrospective (1-2 hours, per sprint) - Reflect on process and relationships
- **P9**: Release Blessing (30 min, per release) - Mark completion with reflection and gratitude
- **P10**: Quarterly Purpose Alignment (2-3 hours, quarterly) - Ensure remaining true to mission

---

### Workshops

Workshop patterns define structured team workshops for onboarding and alignment.

| Pattern ID | Name | Purpose | Duration |
|------------|------|---------|----------|
| `vision-quest` | Vision Quest Workshop | Define shared vision, mission, stakeholders, and success criteria | 2-3 hours |
| `ethics-arena` | Ethics Arena Workshop | Establish ethical framework, boundaries, and decision-making principles | 1.5-2.5 hours |
| `stack-safari` | Stack Safari Workshop | Explore and select technology stack through playful discovery | 2-3 hours |
| `agent-assembly` | Agent Assembly Workshop | Design custom AI agents and skills for development workflow | 3-4 hours |
| `integration-celebration` | Integration Celebration Workshop | Finalize artifacts, generate system, and celebrate journey | 1.5-2.5 hours |

**Workshop Series Flow**:
1. **Vision Quest**: Discover vision through Future Headlines and Stakeholder Safari games
2. **Ethics Arena**: Define ethics through Dilemma Duel and Value Auction games
3. **Stack Safari**: Select technology through Tech Speed Dating and Trade-Off Tetris games
4. **Agent Assembly**: Design agents through Trading Cards and Skill Bingo games
5. **Integration Celebration**: Generate system and celebrate through Demo Derby and Gratitude Circle

**Games Used**:
- G1: Future Headlines
- G2: Stakeholder Safari
- G4: Dilemma Duel
- G5: Value Auction
- G6: Trade-Off Tetris
- G7: Agent Trading Cards
- G8: Skill Bingo
- G9: Architecture Pictionary
- G10: Demo Derby
- G11: Gratitude Circle

---

### Team Formats

Team format patterns adapt workshops for different team sizes.

| Pattern ID | Team Size | Characteristics |
|------------|-----------|----------------|
| `small-team-format` | 2-5 people | Intimate, everyone participates, quick decisions, strong psychological safety |
| `medium-team-format` | 6-12 people | Balance intimacy with diversity, breakout groups enable parallel work |
| `large-team-format` | 13+ people | Massive diversity, requires delegation, representative synthesis, async pre-work |

**Small Team Adaptations**:
- More conversational, less structured facilitation
- Shorter workshops (-30 to -45 minutes)
- Full participation in all activities
- Games played together, no team splits
- Round-robin ensures everyone speaks

**Medium Team Adaptations**:
- Structured facilitation with clear time boundaries
- Standard workshop timing
- Mix of breakout and plenary
- Split into teams for competitive games
- Use structured formats (round-robin, fishbowl)

**Large Team Adaptations**:
- Highly structured with multiple facilitators
- Longer workshops or split across sessions
- Representative groups for sync work, everyone contributes async
- Multiple parallel game instances
- Fishbowl format, representative panels, async discussion boards
- Heavy async pre-work (30-60 minutes between workshops)

---

## Summary

Patterns in the Cursor Agent Factory provide a comprehensive framework for generating customized agent systems. They ensure consistency while enabling flexibility through:

- **Composition**: Patterns can be combined to create complex workflows
- **Variables**: Project-specific customization through template variables
- **Validation**: Axiom-based validation ensures pattern compliance
- **Extensibility**: New patterns can be added following the established structure

All patterns trace to foundational axioms (A1-A5) and can be extended with optional axioms (A6-A10) based on project needs. The pattern system enables teams to create agent systems that are both powerful and aligned with their values and goals.

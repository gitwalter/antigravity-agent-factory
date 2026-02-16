---
description: Technology stack selection and configuration skill
name: configuring-stacks
type: skill
---
# Stack Configuration

Technology stack selection and configuration skill

Configures technology stack based on requirements and matches to available blueprints.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Parse Language Requirements
- Identify primary language
- Check for secondary languages
- Validate language is supported

### Step 2: Identify Frameworks
For each mentioned framework:
- Match to known frameworks in `stack-capabilities.json`
- Identify dependencies
- Check compatibility

### Step 3: Match Blueprint
Search blueprints for best match:

```python
for blueprint in blueprints:
    if blueprint.primaryLanguage == requirements.primaryLanguage:
        match_score = calculate_framework_match(blueprint, requirements)
        if match_score > threshold:
            return blueprint
```

### Step 4: Configure Tools
Based on stack, suggest:
- Test frameworks
- Linters
- Formatters
- Type checkers

### Step 5: Select Testing Approach

Present testing mode options to the user:

```
Select your testing mode:

BASIC MODES:
[ ] tdd-only - Test-Driven Development only
    - Code-based unit tests with Given-When-Then structure
    - Developer-focused, fast feedback
    - No BDD artifacts

[ ] bdd-only - Behavior-Driven Development only
    - Gherkin feature files with step definitions
    - Stakeholder-readable specifications
    - No separate unit tests

[ ] layered - TDD + BDD (Test Pyramid)
    - Unit tests (TDD) for implementation details
    - Acceptance tests (BDD) for business behavior
    - Both maintained independently

TRANSLATION MODES:
[ ] bdd-drives-tdd - Outside-In Development
    - Write BDD scenarios first
    - Generate unit test stubs from scenarios
    - Full traceability from scenario to tests

[ ] tdd-documents-bdd - Documentation Generation
    - Write unit tests normally
    - Generate feature files from tests
    - Stakeholder docs from existing tests

[ ] synchronized - Bidirectional Sync
    - Changes to either propagate to the other
    - Single source of truth with dual views
    - Full traceability and conflict detection
```

Based on selection, configure:

| Mode | TDD | BDD | Translation | Traceability | Practice |
|------|-----|-----|-------------|--------------|----------|
| tdd-only | ✓ | - | - | - | - |
| bdd-only | - | ✓ | - | - | Three Amigos |
| layered | ✓ | ✓ | - | Optional | Three Amigos |
| bdd-drives-tdd | ✓ | ✓ | BDD→TDD | ✓ | Three Amigos |
| tdd-documents-bdd | ✓ | ✓ | TDD→BDD | ✓ | - |
| synchronized | ✓ | ✓ | Bidirectional | ✓ | Three Amigos |

**Translation capabilities:**

| Direction | Description | Use Case |
|-----------|-------------|----------|
| BDD→TDD | Generate test stubs from scenarios | Outside-in development |
| TDD→BDD | Generate features from tests | Legacy documentation |
| Bidirectional | Keep both in sync | Single source of truth |

**Traceability features:**
- Link scenarios to implementing tests
- Link tests back to source scenarios
- Coverage matrix reports
- Orphan detection (unlinked artifacts)

**Framework mapping by stack:**

| Stack | TDD Framework | BDD Framework |
|-------|---------------|---------------|
| Python | pytest | behave, pytest-bdd |
| TypeScript | jest, vitest | cucumber-js |
| Java | JUnit | cucumber-jvm |
| C# | NUnit, xUnit | SpecFlow |
| Kotlin | JUnit, Kotest | cucumber-jvm |

### Step 6: Output Configuration
Generate stack configuration object:

```yaml
stack:
  primaryLanguage: "{LANGUAGE}"
  frameworks:
    - name: "{FRAMEWORK}"
      version: "{VERSION}"
  tools:
    testing: "{TEST_FRAMEWORK}"
    linting: "{LINTER}"
    formatting: "{FORMATTER}"
  testingApproach:
    mode: "{TESTING_MODE}"  # tdd-only, bdd-only, layered, bdd-drives-tdd, tdd-documents-bdd, synchronized
    tdd:
      enabled: true|false
      framework: "{TDD_FRAMEWORK}"
    bdd:
      enabled: true|false
      framework: "{BDD_FRAMEWORK}"
      featureDirectory: "features/"
      stepDirectory: "features/steps/"
    translation:
      enabled: true|false
      direction: "{DIRECTION}"  # bdd-to-tdd, tdd-to-bdd, bidirectional
    traceability:
      enabled: true|false
      reportFormat: "markdown"  # markdown, json, html
  blueprint: "{BLUEPRINT_ID}"
```

**Example configurations by mode:**

```yaml
# bdd-drives-tdd mode
testingApproach:
  mode: "bdd-drives-tdd"
  tdd:
    enabled: true
    framework: "pytest"
  bdd:
    enabled: true
    framework: "behave"
  translation:
    enabled: true
    direction: "bdd-to-tdd"
  traceability:
    enabled: true

# synchronized mode
testingApproach:
  mode: "synchronized"
  tdd:
    enabled: true
    framework: "pytest"
  bdd:
    enabled: true
    framework: "behave"
  translation:
    enabled: true
    direction: "bidirectional"
  traceability:
    enabled: true
```

## Blueprint Matching Rules

| Primary Language | Key Framework | Blueprint |
|------------------|---------------|-----------|
| Python | FastAPI | `python-fastapi` |
| Python | Django | `python-django` |
| TypeScript | React | `typescript-react` |
| TypeScript | Next.js | `typescript-nextjs` |
| Java | Spring | `java-spring` |
| C# | .NET | `csharp-dotnet` |
| ABAP | (any) | `sap-abap` |

## Best Practices

- **Prioritize team familiarity over trendiness**: Choose technologies the team knows well rather than the latest frameworks, unless there's a compelling business reason
- **Verify framework compatibility before selection**: Check version compatibility matrices and known conflicts between frameworks, libraries, and tools in the stack
- **Consider long-term maintenance**: Evaluate community support, update frequency, and migration paths when selecting stack components
- **Document stack decisions and rationale**: Record why specific technologies were chosen so future team members understand the context
- **Plan for testing approach early**: Select testing frameworks and approaches during stack configuration, not as an afterthought
- **Validate blueprint match quality**: Ensure the selected blueprint truly matches project requirements; don't force-fit a blueprint that's only partially compatible

## Fallback Procedures

- **If language not supported**: Report and ask user for alternative
- **If no blueprint matches**: Create custom configuration from patterns
- **If frameworks conflict**: Report conflict and ask user to choose

## References

- `{directories.knowledge}/stack-capabilities.json`
- `{directories.blueprints}/*/blueprint.json`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

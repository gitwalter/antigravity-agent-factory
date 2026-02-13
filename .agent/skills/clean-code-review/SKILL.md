---
description: Systematic code quality review using SOLID principles, code smell detection,
  and refactoring patterns
name: clean-code-review
type: skill
---
# Clean Code Review

Systematic code quality review using SOLID principles, code smell detection, and refactoring patterns

Perform systematic code quality review using SOLID principles, code smell detection, and refactoring patterns. Produces actionable feedback aligned with best-practices.json and design-patterns.json.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Static Analysis

Run linters and collect baseline metrics.

```python
import subprocess
from pathlib import Path

def run_static_analysis(
    path: Path,
    tool: str = "ruff",
) -> subprocess.CompletedProcess:
    """Run static analysis tool on codebase.

    Args:
        path: Path to file or directory.
        tool: 'ruff', 'pylint', 'radon', or 'vulture'.

    Returns:
        CompletedProcess with stdout/stderr.
    """
    cmd = {
        "ruff": ["ruff", "check", str(path)],
        "pylint": ["pylint", str(path)],
        "radon": ["radon", "cc", str(path), "-a"],
        "vulture": ["vulture", str(path)],
    }
    return subprocess.run(cmd[tool], capture_output=True, text=True)
```

### Step 2: SOLID Check

Evaluate classes against SOLID principles.

```python
from dataclasses import dataclass
from typing import List

@dataclass
class SolidViolation:
    """Recorded SOLID principle violation."""
    principle: str
    location: str
    description: str
    suggestion: str

def check_single_responsibility(
    class_body: str,
    class_name: str,
) -> List[SolidViolation]:
    """Check for Single Responsibility Principle violations.

    Args:
        class_body: Class source code.
        class_name: Name of the class.

    Returns:
        List of violations found.
    """
    violations = []
    # Heuristic: multiple "def" doing unrelated things
    methods = [m for m in class_body.split("def ") if "(" in m]
    if len(methods) > 7:  # Arbitrary threshold
        violations.append(SolidViolation(
            principle="SRP",
            location=class_name,
            description="Many methods suggest multiple responsibilities",
            suggestion="Consider splitting into smaller, focused classes",
        ))
    return violations
```

### Step 3: Code Smell Detection

Identify common code smells using vulture and radon.

```python
def detect_code_smells(
    path: Path,
) -> dict[str, list]:
    """Detect code smells via tooling.

    Args:
        path: Path to Python file or directory.

    Returns:
        Dict with 'dead_code', 'complexity' keys.
    """
    vulture = subprocess.run(
        ["vulture", str(path)],
        capture_output=True,
        text=True,
    )
    radon = subprocess.run(
        ["radon", "cc", str(path), "-a", "-j"],
        capture_output=True,
        text=True,
    )
    return {
        "dead_code": vulture.stdout.strip().split("\n") if vulture.stdout else [],
        "complexity": radon.stdout.strip().split("\n") if radon.stdout else [],
    }
```

### Step 4: Complexity Metrics

Compute cyclomatic complexity and maintainability index.

```python
def get_complexity_metrics(path: Path) -> dict:
    """Extract complexity metrics via radon.

    Args:
        path: Path to Python file.

    Returns:
        Dict with avg_complexity, maintainability_index.
    """
    result = subprocess.run(
        ["radon", "cc", str(path), "-a", "-s"],
        capture_output=True,
        text=True,
    )
    mi_result = subprocess.run(
        ["radon", "mi", str(path), "-s"],
        capture_output=True,
        text=True,
    )
    return {
        "cyclomatic_complexity": result.stdout,
        "maintainability_index": mi_result.stdout,
    }
```

### Step 5: Refactoring Suggestions

Generate prioritized refactoring recommendations.

```python
def generate_refactoring_suggestions(
    violations: List[SolidViolation],
    smells: dict,
    complexity: dict,
) -> List[str]:
    """Produce ordered refactoring suggestions.

    Args:
        violations: SOLID violations.
        smells: Code smell findings.
        complexity: Complexity metrics.

    Returns:
        List of suggestion strings.
    """
    suggestions = []
    for v in violations:
        suggestions.append(f"[{v.principle}] {v.location}: {v.suggestion}")
    if smells.get("dead_code"):
        suggestions.append("Remove dead code identified by vulture")
    return suggestions
```

## Best Practices

- Run ruff with --fix for auto-fixable issues first
- Use radon cc -n B to flag high complexity (B grade or worse)
- Cross-reference findings with review-checklist.json
- Prioritize SOLID violations over stylistic issues

## References

- {directories.knowledge}/design-patterns.json
- {directories.knowledge}/best-practices.json
- {directories.knowledge}/review-checklist.json

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

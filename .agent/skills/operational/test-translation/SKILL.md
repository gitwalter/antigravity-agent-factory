---
description: Convert tests between frameworks (pytest, unittest, behave) and translate
  test patterns across languages
name: test-translation
type: skill
---
# Test Translation

Convert tests between frameworks (pytest, unittest, behave) and translate test patterns across languages

Converts tests between pytest, unittest, and behave frameworks. Maps assertions, fixtures, and patterns so test logic is preserved across target formats.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Source Analysis

Parse source test file and extract structure:

```python
import ast
from typing import Any

def analyze_test_file(filepath: str) -> dict[str, Any]:
    """Parse test file and extract classes, methods, assertions.

    Args:
        filepath: Path to test module.

    Returns:
        Dict with classes, methods, and assertion patterns.
    """
    with open(filepath) as f:
        tree = ast.parse(f.read())
    result = {"classes": [], "standalone": [], "imports": []}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
            methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
            result["classes"].append({"name": node.name, "methods": methods})
        elif isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            result["standalone"].append(node.name)
    return result
```

### Step 2: Pattern Mapping

Map source patterns to target framework equivalents:

```python
ASSERTION_MAP = {
    "assertEqual": "assert x == y",
    "assertNotEqual": "assert x != y",
    "assertTrue": "assert x",
    "assertFalse": "assert not x",
    "assertRaises": "pytest.raises(Exc): ...",
    "assertIn": "assert x in y",
    "assertIsInstance": "assert isinstance(x, y)",
}

def map_assertion(source: str) -> str:
    """Map unittest assertion to pytest equivalent."""
    return ASSERTION_MAP.get(source, f"assert {source}")
```

### Step 3: Target Generation

Generate test code in target framework:

```python
def unittest_to_pytest(class_name: str, method_name: str) -> str:
    """Convert unittest method signature to pytest.

    Args:
        class_name: Unittest TestCase class name.
        method_name: Test method name.

    Returns:
        Pytest-style test function string.
    """
    # unittest: def test_foo(self): -> pytest: def test_foo():
    return f"def {method_name}() -> None:\n    \"\"\"{method_name}.\"\"\"\n    pass"
```

### Step 4: Assertion Translation

Translate assertion calls between frameworks:

```python
def translate_assert_equal(body: str) -> str:
    """Convert self.assertEqual(a, b) to assert a == b."""
    import re
    pattern = r"self\.assertEqual\((.+?), (.+?)\)"
    return re.sub(pattern, r"assert \1 == \2", body)

def translate_assert_raises(body: str) -> str:
    """Convert assertRaises to pytest.raises."""
    pattern = r"with self\.assertRaises\((\w+)\):"
    return __import__("re").sub(pattern, r"with pytest.raises(\1):", body)
```

### Step 5: Validation

Validate generated tests parse and run:

```python
def validate_translated_test(code: str) -> bool:
    """Ensure translated code is valid Python.

    Args:
        code: Generated test code.

    Returns:
        True if code parses successfully.
    """
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False
```

## Best Practices

- Preserve test semantics, not just syntax
- Map fixtures: setUp → @pytest.fixture, tearDown → yield
- Handle parametrize for data-driven unittest subclasses
- Validate generated code before committing

## References

- [pytest for unittest users](https://docs.pytest.org/en/stable/unittest.html)
- [pytest-bdd migration](https://pytest-bdd.readthedocs.io/)

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

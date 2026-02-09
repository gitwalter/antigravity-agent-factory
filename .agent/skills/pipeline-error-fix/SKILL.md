---
description: Systematic error detection and fixing strategy for CI/CD pipeline failures with intelligent test packaging
---

# Pipeline Error Fix

Systematic error detection and fixing strategy for CI/CD pipeline failures with intelligent test packaging

## 
# Pipeline Error Fix Skill

Systematic approach to quickly identify and fix CI/CD pipeline test failures using intelligent test packaging and tiered error detection.

## 
# Pipeline Error Fix Skill

Systematic approach to quickly identify and fix CI/CD pipeline test failures using intelligent test packaging and tiered error detection.

## Intelligent Test Packaging Strategy
### Tier 1: Fastest Feedback (< 30 seconds)

Run these tests FIRST to catch common errors quickly:

```bash
# Fast tests: Unit + Validation (in-process, no subprocess)
pytest tests/unit/ tests/validation/ -v --tb=short -x
```

**What these catch:**
- Syntax errors
- Import errors
- Configuration errors
- Schema validation errors
- Basic logic errors

### Tier 2: Medium Speed (1-5 minutes)

Only run if Tier 1 passes:

```bash
# Medium tests: Integration without slow markers (parallel)
pytest tests/integration/ -v --tb=short -x -m "not slow" -n auto
```

**What these catch:**
- CLI command errors
- Generation logic errors
- File I/O errors
- Path handling issues

### Tier 3: Slow Tests (5+ minutes)

Only run if Tier 2 passes:

```bash
# Slow tests: QuickStart and full workflow tests
pytest tests/integration/ -v --tb=short -x -m "slow"
```

**What these catch:**
- Full workflow integration issues
- Timeout issues
- Resource contention
- Complex state interactions

```bash
# Fast tests: Unit + Validation (in-process, no subprocess)
pytest tests/unit/ tests/validation/ -v --tb=short -x
```

```bash
# Medium tests: Integration without slow markers (parallel)
pytest tests/integration/ -v --tb=short -x -m "not slow" -n auto
```

```bash
# Slow tests: QuickStart and full workflow tests
pytest tests/integration/ -v --tb=short -x -m "slow"
```

## Error Detection Process
### Step 1: Analyze Failure Type

Check the CI/CD output to categorize the failure:

| Failure Type | Indicator | Start With |
|-------------|-----------|------------|
| Import Error | `ModuleNotFoundError`, `ImportError` | Tier 1 |
| Syntax Error | `SyntaxError`, `IndentationError` | Tier 1 |
| Schema Error | `ValidationError`, `JSONDecodeError` | Tier 1 |
| Assertion Error | `AssertionError` | Identify test, run that tier |
| Timeout | `TimeoutError`, "Command timed out" | Tier 3 (optimize test) |
| Process Error | `SubprocessError`, exit code != 0 | Tier 2 |

### Step 2: Reproduce Locally

Always reproduce the error locally before fixing:

```bash
# Run the specific failing test
pytest tests/path/to/test_file.py::TestClass::test_method -v --tb=long

# Or run with maximum verbosity
pytest tests/path/to/test_file.py -v --tb=long -s
```

### Step 3: Isolate the Problem

Use pytest markers to narrow down:

```bash
# Run only unit tests
pytest -m unit -v

# Run only fast tests
pytest -m fast -v

# Skip slow tests
pytest -m "not slow" -v

# Run specific test categories
pytest -m cli -v
pytest -m generation -v
pytest -m quickstart -v
```

### Step 4: Fix and Verify

1. **Make the minimal fix** - don't over-engineer
2. **Run the failing test** - ensure it passes
3. **Run the tier tests** - ensure no regressions
4. **Run full suite** - final verification

```bash
# Verification sequence
pytest tests/path/to/fixed_test.py -v  # Fixed test passes
pytest tests/unit/ tests/validation/ -v  # Tier 1 passes
pytest tests/integration/ -v -m "not slow"  # Tier 2 passes
pytest tests/ -v  # Full suite passes
```

```bash
# Run the specific failing test
pytest tests/path/to/test_file.py::TestClass::test_method -v --tb=long

# Or run with maximum verbosity
pytest tests/path/to/test_file.py -v --tb=long -s
```

```bash
# Run only unit tests
pytest -m unit -v

# Run only fast tests
pytest -m fast -v

# Skip slow tests
pytest -m "not slow" -v

# Run specific test categories
pytest -m cli -v
pytest -m generation -v
pytest -m quickstart -v
```

```bash
# Verification sequence
pytest tests/path/to/fixed_test.py -v  # Fixed test passes
pytest tests/unit/ tests/validation/ -v  # Tier 1 passes
pytest tests/integration/ -v -m "not slow"  # Tier 2 passes
pytest tests/ -v  # Full suite passes
```

## Timeout Prevention Strategies
### For Subprocess Tests

```python
# Use explicit, reasonable timeouts
result = subprocess.run(
    command,
    capture_output=True,
    text=True,
    timeout=30  # Explicit timeout
)
```

### For Long-Running Tests

```python
import pytest

@pytest.mark.slow
@pytest.mark.timeout(120)
def test_quickstart_generation():
    """Mark slow tests explicitly for intelligent packaging."""
    pass
```

### CI Configuration

The CI workflow uses staged execution:

```yaml
# Stage 1: Fast tests (fail-fast, < 30s)
- pytest tests/unit/ tests/validation/ -v -x

# Stage 2: Medium tests (parallel, fail-fast)
- pytest tests/integration/ -v -x -m "not slow" -n auto

# Stage 3: Slow tests (sequential, fail-fast)
- pytest tests/integration/ -v -x -m "slow"
```

```python
# Use explicit, reasonable timeouts
result = subprocess.run(
    command,
    capture_output=True,
    text=True,
    timeout=30  # Explicit timeout
)
```

```python
import pytest

@pytest.mark.slow
@pytest.mark.timeout(120)
def test_quickstart_generation():
    """Mark slow tests explicitly for intelligent packaging."""
    pass
```

```yaml
# Stage 1: Fast tests (fail-fast, < 30s)
- pytest tests/unit/ tests/validation/ -v -x

# Stage 2: Medium tests (parallel, fail-fast)
- pytest tests/integration/ -v -x -m "not slow" -n auto

# Stage 3: Slow tests (sequential, fail-fast)
- pytest tests/integration/ -v -x -m "slow"
```

## Common Pipeline Errors and Fixes
### Error: Module Not Found

```
ModuleNotFoundError: No module named 'scripts'
```

**Fix:** Ensure `sys.path` includes project root:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
```

### Error: Test Timeout

```
TimeoutError: Command timed out after 120 seconds
```

**Fix:**
1. Increase timeout for legitimately slow tests
2. Mark test with `@pytest.mark.slow`
3. Optimize the test or split into smaller units

### Error: Subprocess Failed

```
subprocess.CalledProcessError: Command 'x' returned non-zero exit status 1
```

**Fix:**
1. Capture and log stderr: `result.stderr`
2. Check the actual command being run
3. Verify paths work cross-platform

### Error: File Not Found

```
FileNotFoundError: [Errno 2] No such file or directory
```

**Fix:**
1. Use `Path` objects for cross-platform paths
2. Verify fixtures create required directories
3. Check `tmp_path` fixture usage

```
ModuleNotFoundError: No module named 'scripts'
```

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
```

```
TimeoutError: Command timed out after 120 seconds
```

```
subprocess.CalledProcessError: Command 'x' returned non-zero exit status 1
```

```
FileNotFoundError: [Errno 2] No such file or directory
```

## Parallel Execution Considerations
When using `pytest-xdist` (`-n auto`):

1. **Avoid shared state** - each worker has its own process
2. **Use tmp_path fixture** - provides unique temp directories
3. **Don't rely on test order** - tests may run in any order
4. **Avoid file conflicts** - use unique file names per test

## Quick Reference Commands
```bash
# Fast feedback (local development)
pytest tests/unit/ tests/validation/ -v -x

# Full test with coverage
pytest tests/ --cov=scripts --cov=cli -n auto

# Debug a specific test
pytest tests/path/test.py::test_name -v --tb=long -s

# List all tests without running
pytest --collect-only

# Run tests matching a pattern
pytest -k "quickstart" -v

# Show slowest tests
pytest --durations=10
```

```bash
# Fast feedback (local development)
pytest tests/unit/ tests/validation/ -v -x

# Full test with coverage
pytest tests/ --cov=scripts --cov=cli -n auto

# Debug a specific test
pytest tests/path/test.py::test_name -v --tb=long -s

# List all tests without running
pytest --collect-only

# Run tests matching a pattern
pytest -k "quickstart" -v

# Show slowest tests
pytest --durations=10
```

## Important Rules
1. **Always start with fast tests** - quick feedback loop
2. **Use fail-fast (-x)** - stop on first failure for debugging
3. **Reproduce locally first** - don't push fixes blindly
4. **Mark slow tests explicitly** - enables intelligent packaging
5. **Use parallel execution** - speeds up CI significantly
6. **Set explicit timeouts** - prevent hanging tests
7. **Test cross-platform** - CI runs on multiple OS

## Prerequisites
> [!IMPORTANT]
> Requirements:

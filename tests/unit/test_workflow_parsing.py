import pytest
from pathlib import Path
from scripts.api.workflow_service import parse_workflow

# conftest.py handles sys.path and provides factory_root


def test_standardized_parsing(tmp_path: Path):
    content = """---
description: Test workflow
version: 1.0.0
---

# Test Workflow

### 1. Setup Phase
- **Goal**: Initialize the test environment.
- **Agent**: `test-agent`
- **Skills**: skill-1, skill-2
- **Tools**: tool-1
- Action step 1
- Action step 2

### 2. Execution Phase
- **Goal**: Run the tests.
- **Agent**: `exec-agent`
- Action step 3
"""
    wf_path = tmp_path / "test_wf.md"
    wf_path.write_text(content, encoding="utf-8")

    wf = parse_workflow(wf_path)

    assert wf.title == "Test Workflow"
    assert len(wf.phases) == 2

    p1 = wf.phases[0]
    assert p1.name == "Setup Phase"
    assert p1.goal == "Initialize the test environment."
    assert p1.agent == "test-agent"
    assert p1.skills == ["skill-1", "skill-2"]
    assert p1.tools == ["tool-1"]
    assert "Action step 1" in p1.actions
    assert "Action step 2" in p1.actions

    p2 = wf.phases[1]
    assert p2.name == "Execution Phase"
    assert p2.goal == "Run the tests."
    assert p2.agent == "exec-agent"
    assert "Action step 3" in p2.actions


def test_legacy_parsing(tmp_path: Path):
    content = """
# Legacy Workflow

## 1. Step Alpha
**Goal**: Legacy goal
**Agent**: legacy-agent
**Action**: legacy action 1
**Action**: legacy action 2
**Skills**: skill-a
"""
    wf_path = tmp_path / "legacy_wf.md"
    wf_path.write_text(content, encoding="utf-8")

    wf = parse_workflow(wf_path)

    assert len(wf.phases) == 1
    p = wf.phases[0]
    assert p.name == "Step Alpha"
    assert p.goal == "Legacy goal"
    assert p.agent == "legacy-agent"
    assert "legacy action 1" in p.actions
    assert "legacy action 2" in p.actions

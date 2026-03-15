import pytest
import sys
import os
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from scripts.api.workflow_service import parse_workflow, Workflow, WorkflowPhase


def test_standardized_parsing():
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
    tmp_path = Path("tmp/test_wf.md")
    tmp_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(content, encoding="utf-8")

    wf = parse_workflow(tmp_path)

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


def test_legacy_parsing():
    content = """
# Legacy Workflow

## 1. Step Alpha
**Goal**: Legacy goal
**Agent**: legacy-agent
**Action**: legacy action 1
**Action**: legacy action 2
**Skills**: skill-a
"""
    tmp_path = Path("tmp/legacy_wf.md")
    tmp_path.write_text(content, encoding="utf-8")

    wf = parse_workflow(tmp_path)

    assert len(wf.phases) == 1
    p = wf.phases[0]
    assert p.name == "Step Alpha"
    assert p.goal == "Legacy goal"
    assert p.agent == "legacy-agent"
    assert "legacy action 1" in p.actions
    assert "legacy action 2" in p.actions


if __name__ == "__main__":
    pytest.main([__file__])

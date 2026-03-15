import sys
from pathlib import Path

# Add scripts/api to path - Updated for location in scripts/debug
sys.path.append(str(Path(__file__).parent.parent / "api"))

from workflow_service import parse_workflow

test_content = """---
description: Test workflow
---

# Test Workflow

## 1. Phase One (H2)
- **Goal**: Test H2 parsing
- **Agent**: `test-agent`

### 2. Phase Two (H3)
- **Goal**: Test H3 parsing
- **Agent**: `test-agent`
"""

test_file = Path("test_wf.md")
test_file.write_text(test_content, encoding="utf-8")

try:
    wf = parse_workflow(test_file)
    print(f"Parsed {len(wf.phases)} phases.")
    for i, p in enumerate(wf.phases):
        print(f"Phase {i+1}: {p.name}")
        print(f"  Goal: {p.goal}")
        print(f"  Agent: {p.agent}")
finally:
    if test_file.exists():
        test_file.unlink()

---
description: Receive and apply updates from the Cursor Agent Factory including skills,
  knowledge, and agents
name: receive-updates
type: skill
---
# Receive Updates

Receive and apply updates from the Cursor Agent Factory including skills, knowledge, and agents

Receive and apply updates from the Cursor Agent Factory including skills, knowledge, and agents. Supports diff analysis, conflict resolution, and verified application of updates.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Update Check

```python
import json
from pathlib import Path

def check_for_updates(
    factory_url: str,
    current_version: str,
) -> dict | None:
    """Check factory for available updates."""
    # In practice: GET factory_url/manifest.json
    manifest = {
        "version": "1.2.0",
        "skills": ["skill-a", "skill-b"],
        "knowledge": ["patterns.json"],
    }
    return manifest if manifest["version"] != current_version else None
```

### Step 2: Diff Analysis

```python
def compute_diff(local: dict, remote: dict) -> dict:
    """Compute diff between local and remote manifests."""
    return {
        "added": set(remote.keys()) - set(local.keys()),
        "removed": set(local.keys()) - set(remote.keys()),
        "modified": [k for k in local if k in remote and local[k] != remote[k]],
    }
```

### Step 3: Conflict Resolution

```python
def resolve_conflicts(
    diff: dict,
    strategy: str = "prefer_remote",
) -> list[tuple[str, str]]:
    """Resolve conflicts; return list of (path, action)."""
    actions = []
    for item in diff.get("modified", []):
        actions.append((item, "update" if strategy == "prefer_remote" else "keep"))
    return actions
```

### Step 4: Application

```python
def apply_update(
    target_path: Path,
    content: str,
) -> None:
    """Apply update to file with backup."""
    backup = target_path.with_suffix(target_path.suffix + ".bak")
    if target_path.exists():
        target_path.rename(backup)
    target_path.write_text(content, encoding="utf-8")
```

### Step 5: Verification

```python
def verify_update(target_path: Path, expected_checksum: str | None = None) -> bool:
    """Verify applied update is valid."""
    if not target_path.exists():
        return False
    # Add checksum validation if expected_checksum provided
    return target_path.stat().st_size > 0
```

## Best Practices

- Always backup before bulk updates
- Use dry-run mode to preview changes
- Resolve conflicts manually for customizations
- Verify each update before committing
- Log update history for rollback

## References

- {directories.knowledge}/factory-updates.json
- Cursor Agent Factory documentation

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

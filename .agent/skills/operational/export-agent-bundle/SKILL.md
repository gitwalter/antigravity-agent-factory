---
description: Create and export PABP agent bundles for cross-platform portable behavior
  transfer
name: export-agent-bundle
type: skill
---
# Export Agent Bundle

Create and export PABP agent bundles for cross-platform portable behavior transfer

Create cross-platform agent bundles using the Portable Agent Behavior
Protocol (PABP) for transferring capabilities between different AI
platforms (Cursor, CrewAI, LangChain, Antigravity).

## Choosing Raw vs PABP -- Read This First

| Scenario | Use Raw | Use PABP |
|----------|---------|----------|
| Cursor-to-Cursor project transfer | **YES** | no |
| Sharing with CrewAI / LangChain / Antigravity | no | **YES** |
| Preserve exact file layout and content | **YES** | no |
| Cross-platform / vendor-neutral exchange | no | **YES** |
| Maximum fidelity (zero conversion loss) | **YES** | no |
| Need reputation / signature portability | no | **YES** |
| Quick stack export (SAP, AI/ML, .NET) | **YES** | no |
| Single agent with selective components | no | **YES** |
| Target uses different directory conventions | no | **YES** |

**Rule of thumb:**
- If the recipient also uses Cursor -> use the `build-raw-bundle` skill
- If the recipient uses a different platform -> use this skill (PABP)
- If unsure -> use raw (simpler, lossless, and Cursor users can always import it)

> For raw Cursor bundles, see the [build-raw-bundle](../build-raw-bundle/SKILL.md) skill.

## When to Use This Skill (PABP)

- Exporting to a CrewAI, LangChain, or Antigravity project
- When you need vendor-neutral JSON interchange format
- When you need reputation and trust metrics to transfer across trust boundaries
- When you need cryptographic signing for integrity verification
- When the target project uses different directory conventions than Cursor

## Core Principle

> **Build once, deploy everywhere. Stop rebuilding the same agents for every project.**

## Process

See the detailed workflow below in [Step-by-Step Guide](#step-by-step-guide). The key steps are:

1. **Identify Components** - Determine which skills, knowledge, and workflows to export
2. **Create Bundle** - Initialize bundle with agent identity and version information
3. **Add Components** - Add skills, knowledge files, and workflows to the bundle
4. **Configure Compatibility** - Specify requirements for target projects
5. **Sign Bundle** (Optional) - Add cryptographic signature for integrity verification
6. **Export** - Create compressed bundle file ready for transfer
7. **Verify** - Validate bundle integrity before sharing

## Value Proposition

| Without PABP | With PABP |
|--------------|-----------|
| Rebuild agents per project | Export once, import anywhere |
| Copy-paste skills manually | Verified bundle transfer |
| No reputation portability | Reputation transfers (with decay) |
| No integrity verification | Cryptographic checksums |

## Quick Start

### Export an Agent Bundle

```python
from lib.society.pabp import create_bundle, export_bundle
from pathlib import Path

# Create a bundle for your agent
bundle = create_bundle(
    agent_id="code-analyzer",
    agent_name="Code Analyzer Agent",
    version="1.0.0"
)

# Add skills
bundle.add_skill("analyze", """
---
name: analyze
description: Analyze code for issues
---
# Analyze Skill
...
""")

# Add knowledge
bundle.add_knowledge("patterns", {
    "name": "Code Patterns",
    "patterns": [...]
})

# Export to file
result = export_bundle(bundle, Path("code-analyzer.zip"))
print(f"Exported {result.components_transferred} components")
```

### Import a Bundle

```python
from lib.society.pabp import import_bundle
from pathlib import Path

bundle, result = import_bundle(Path("code-analyzer.zip"))

if result.success:
    print(f"Imported: {bundle.agent_name}")
    for skill in bundle.get_components_by_type(ComponentType.SKILL):
        print(f"  - Skill: {skill.name}")
```

## Bundle Structure

```
AgentBundle/
├── manifest.json       # Version, checksums, signatures
├── identity/           # Agent identity and keys
│   └── agent.json
├── skills/             # SKILL.md files
│   └── analyze/
│       └── SKILL.md
├── {directories.knowledge}/          # Knowledge JSON files
│   └── patterns.json
├── {directories.workflows}/          # Workflow definitions
│   └── analyze.yaml
└── attestations/       # Verifiable credentials
    └── endorsements.json
```

## Step-by-Step Guide

### 1. Identify Components to Export

First, identify what makes up your agent:

```python
# List agent's components
components_to_export = {
    "skills": ["analyze", "report", "fix"],
    "knowledge": ["patterns", "best-practices"],
    "workflows": ["analysis-workflow"]
}
```

### 2. Create the Bundle

```python
from lib.society.pabp import create_bundle

bundle = create_bundle(
    agent_id="my-agent",
    agent_name="My Agent",
    version="1.0.0",
    reputation_snapshot={
        "score": 85,
        "trust_level": "VERIFIED",
        "total_tasks": 150
    }
)
```

### 3. Add Skills

```python
from pathlib import Path

# Load skill content from file
skill_path = Path("{directories.skills}/my-skill/SKILL.md")
skill_content = skill_path.read_text()

bundle.add_skill("my-skill", skill_content, metadata={
    "version": "1.0.0",
    "dependencies": ["other-skill"]
})
```

### 4. Add Knowledge

```python
import json

# Load knowledge file
knowledge_path = Path("{directories.knowledge}/my-knowledge.json")
knowledge_content = json.loads(knowledge_path.read_text())

bundle.add_knowledge("my-knowledge", knowledge_content)
```

### 5. Add Workflows

```python
workflow_path = Path("{directories.workflows}/my-workflow.yaml")
workflow_content = workflow_path.read_text()

bundle.add_workflow("my-workflow", workflow_content)
```

### 6. Export with Signing (Optional)

```python
from lib.society.pabp import export_bundle

# Generate or load signing key
# (In production, use proper key management)
private_key_hex = "your_private_key_hex"

result = export_bundle(
    bundle,
    Path("my-agent.zip"),
    compress=True,
    sign_key=private_key_hex,
    signer_id="factory"
)

if result.success:
    print(f"Bundle exported: {result.bundle_id}")
    print(f"Components: {result.components_transferred}")
```

### 7. Verify Before Sharing

```python
from lib.society.pabp import verify_bundle

result = verify_bundle(bundle)

if result.verification_passed:
    print("Bundle integrity verified")
else:
    print(f"Issues: {result.warnings}")
```

## Transfer Modes

### Full Bundle (Default)
Complete agent transfer with all components.

```python
result = export_bundle(bundle, path, mode=TransferMode.FULL)
```

### Selective Export
Export only specific component types.

```python
# Export only skills
skills_only = create_bundle(bundle.agent_id, bundle.agent_name)
for skill in bundle.get_components_by_type(ComponentType.SKILL):
    skills_only.add_component(skill)

export_bundle(skills_only, Path("skills-only.zip"))
```

### Incremental Update
Export only changes since last version.

```python
from lib.society.pabp import create_incremental_bundle

# Create delta bundle
delta = create_incremental_bundle(current_bundle, previous_bundle)
export_bundle(delta, Path("update-1.0.1.zip"))
```

## Reputation Portability

Reputation transfers with decay to prevent gaming:

```python
# Original reputation: 85
# After transfer: 85 * 0.8 = 68 (20% decay)

bundle = create_bundle(
    agent_id="my-agent",
    agent_name="My Agent",
    reputation_snapshot={
        "score": 85,
        "decay_factor": 0.8,  # Applied on import
        "earned_through": "150 successful tasks"
    }
)
```

## Compatibility Requirements

Specify what the target project needs:

```python
bundle.compatibility = {
    "min_factory_version": "1.0.0",
    "required_skills": ["base-skill"],
    "required_knowledge": ["domain-knowledge"],
    "python_version": "3.10",
    "dependencies": ["langchain>=0.1.0"]
}
```

## Import with Verification

```python
from lib.society.pabp import import_bundle

# Import with full verification
bundle, result = import_bundle(
    Path("agent.zip"),
    verify_signature=True,
    public_key="signer_public_key_hex",
    check_compatibility=True,
    target_info={
        "factory_version": "1.0.0",
        "skills": ["base-skill"],
        "knowledge": ["domain-knowledge"]
    }
)

if result.success:
    if result.warnings:
        print(f"Imported with warnings: {result.warnings}")
    else:
        print("Import successful, all checks passed")
else:
    print(f"Import failed: {result.errors}")
```

## Merging Bundles

Combine capabilities from multiple agents:

```python
from lib.society.pabp import merge_bundles

# Merge analyzer + fixer into one agent
merged = merge_bundles(
    analyzer_bundle,
    fixer_bundle,
    conflict_strategy="overlay_wins"  # or "base_wins"
)
```

## Best Practices

1. **Version your bundles** - Use semantic versioning
2. **Sign production bundles** - Use Ed25519 signatures
3. **Include reputation** - Helps target trust the agent
4. **Specify compatibility** - Prevent import failures
5. **Test after import** - Verify functionality works

## Common Issues

### "Component checksum mismatch"
The content was modified after bundling. Re-export the bundle.

### "Signature verification failed"
The public key doesn't match, or content was tampered with.

### "Compatibility check failed"
Target project is missing required dependencies. Check the compatibility requirements.

### "Import failed: missing manifest.json"
The zip file structure is incorrect. Ensure manifest.json is at the root.

## References

- [PABP Module](../../../lib/society/pabp/)
- **ASP Value Proposition**
- **Bundle Format Specification**

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

## When to Use
This skill should be used when strict adherence to the defined process is required.

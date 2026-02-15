---
description: Precise skill for updating JSON registries, dependency graphs, and manifests.
name: system-registration
type: skill
---

# System Registration Skill

This skill provides the technical capabilities required to maintain the system's "metasystem" – the collection of JSON files that describe the project's structure and components.

## When to Use
- When a new agent, skill, or workflow is created.
- To update the dependency graph after refactoring.
- To synchronize the artifact catalog with the filesystem.
- When performing bulk registration of newly discovered patterns or knowledge files.

## Prerequisites
- Python 3.10+
- `scripts/validation/update_index.py`
- `scripts/validation/validate_readme_structure.py`
- Knowledge of the system's JSON schemas (DIDs, performatives, etc.).

## Process
The following process outlines the steps for precise system registration.

### 1. Agent & Skill Registration
- **Identify**: Extract `agent_id`, `role`, `skills`, and `capabilities` from the component's markdown file.
- **Update**: Add the entry to `agent-team-registry.json` or `skill-catalog.json` following the existing schema.
- **Verify**: Run a JSON validation check to ensure no syntax errors were introduced.

### 2. Dependency Graph Integration
- **Node Creation**: Add a new node to `dependency-graph.json` with the correct `type` and `path`.
- **Edge Mapping**: Identify and map the relationships (e.g., agent uses skill, skill depends on knowledge).
- **Refactoring**: Periodically rebuild the graph to remove dead nodes or orphaned references.

### 3. Workflow Registration
- **Integration**: Ensure new workflows are referenced in the `repository-maintenance` procedures.
- **Mapping**: Link the workflow to the primary agent and skill it utilizes.

### 4. Manifest Synchronization
- **Action**: Use `update_index.py` to rebuild the artifact cache.
- **Action**: Use `sync_manifest_versions.py` to ensure version consistency.

## Best Practices
- **Atomic Updates**: Only update one registry file at a time to minimize risk of corruption.
- **Schema Compliance**: Always adhere to the schema in the `agent-team-registry.json` and `skill-catalog.json`.
- **DIDs**: Use the standard `did:agent:{agent-id}` format for all agent identifiers.
- **Traceability**: All registration actions should be searchable and verifiable via the dependency graph.

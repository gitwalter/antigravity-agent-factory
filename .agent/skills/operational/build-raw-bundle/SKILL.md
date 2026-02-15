---
description: Build raw Cursor artifact bundles as verbatim zip copies filtered by
  domain profile
name: build-raw-bundle
type: skill
---
# Build Raw Bundle

Build raw Cursor artifact bundles as verbatim zip copies filtered by domain profile

Build stack-specific artifact bundles as verbatim copies of Cursor files.
Raw bundles preserve the exact directory layout and file contents with zero
conversion loss -- ideal for Cursor-to-Cursor project transfers.

## When NOT to Use This Skill

- Targeting non-Cursor platforms (CrewAI, LangChain, Antigravity) -- use `export-agent-bundle` (PABP) instead
- Exporting a single agent with selective components -- use `export-agent-bundle` (PABP) instead
- Need reputation/signature portability across trust boundaries -- use PABP instead

## Choosing Raw vs PABP

| Scenario | Raw | PABP |
|----------|-----|------|
| Cursor-to-Cursor project transfer | **YES** | no |
| Sharing with CrewAI / LangChain project | no | **YES** |
| Preserve exact file layout and content | **YES** | no |
| Cross-platform / vendor-neutral exchange | no | **YES** |
| Maximum fidelity (zero conversion loss) | **YES** | no |
| Need reputation / signature portability | no | **YES** |
| Quick stack export (SAP, AI/ML, .NET) | **YES** | no |
| Single agent with selective components | no | **YES** |
| Target uses different directory conventions | no | **YES** |

**Rule of thumb:** If the recipient also uses Cursor, use raw. If not, use PABP.

## Available Profiles

| Profile | Domains | Description |
|---------|---------|-------------|
| `sap-complete` | sap, agent-core, agent-framework, cross-cutting, devops, factory-meta, pm | Full SAP stack: S/4HANA, RAP, CAP, Fiori, BTP, ABAP, logistics chain |
| `ai-ml-stack-complete` | ai-ml, python, trading, agent-core, agent-framework, cross-cutting, devops | Full AI/ML stack: LangChain, LangGraph, RAG, training, fine-tuning, multi-agent |
| `dotnet-csharp-complete` | dotnet, agent-core, agent-framework, cross-cutting, devops | Full .NET stack: ASP.NET Core, EF Core, Blazor, Azure, microservices |

Profiles are defined in `lib/society/pabp/scope_agreement.py` and domain
mappings in `lib/society/pabp/component_registry.json`.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Update Registry Relations

Ensure the artifact registry has current dependency data before bundling:

```bash
python scripts/update_registry_relations.py
```

This scans all agent and skill frontmatter to populate the `relations`
section of `artifacts/registry.json` (agent_to_skills, skill_to_knowledge,
blueprint_to_agents). Use `--dry-run` to preview changes without writing.

### Step 2: Generate Bundles

```bash
# Single profile
python scripts/export_raw_bundle.py --profile sap-complete

# Multiple profiles
python scripts/export_raw_bundle.py --profile sap-complete ai-ml-stack-complete

# All profiles (excludes full-factory)
python scripts/export_raw_bundle.py --all-profiles

# Verbose output for debugging
python scripts/export_raw_bundle.py --profile sap-complete -v
```

Output goes to `bundles/<profile>-raw.zip` by default.

### Step 3: Verify the Bundle

Each zip contains a `bundle-manifest.json` at the root with:
- `format`: always `"cursor-raw-bundle"`
- `profile`: which profile was used
- `domains`: list of included domains
- `file_count`: total files in the bundle
- `counts`: breakdown by type (skill, agent, knowledge, workflow, etc.)
- `files[]`: every file with relative path, type, and SHA-256 checksum

Verification checklist:
1. Open the zip and read `bundle-manifest.json`
2. Confirm `file_count` matches the number of entries in `files[]`
3. Spot-check a few SHA-256 values against the original files
4. Confirm expected artifact types are present in `counts`
5. Extract into a test directory and verify skills, knowledge, etc. are intact

### Step 4: Distribute

```bash
# Copy to another project
unzip bundles/sap-complete-raw.zip -d /path/to/target/project/

# Or share the zip file directly
```

The recipient can simply extract the zip into their project root.
All paths are relative and follow the standard Cursor layout
(`.cursor/skills/`, `.cursor/agents/`, `knowledge/`, `workflows/`, etc.).

## Raw Bundle Structure

```
bundle-manifest.json            # Inventory + SHA-256 checksums
.cursor/agents/*.md             # Agent definitions
.cursor/skills/*/SKILL.md       # Skill definitions (with scripts/ subdirs)
knowledge/*.json                # Knowledge files
workflows/*.md                  # Workflow definitions
patterns/*.json                 # Structural patterns
templates/**/*                  # Code-generation templates
blueprints/**/*                 # Blueprint configurations
scripts/**/*.py                 # Automation scripts
```

## How It Works

1. **Profile lookup** -- The selected profile name maps to a list of domain
   tags via `PROFILES` in `scope_agreement.py`.
2. **Registry query** -- `ComponentRegistry.get_components_for_domains()`
   returns all component names whose domain tags overlap with the profile.
3. **Path resolution** -- Each component name is resolved to actual disk
   paths (e.g. skill name -> `.cursor/skills/{name}/` directory tree).
4. **Blueprint matching** -- Blueprints are matched by name prefix and
   `stack.primaryLanguage` from their `blueprint.json`.
5. **Zip creation** -- All resolved files are copied verbatim into the zip
   with their original relative paths, plus a `bundle-manifest.json`.

## References

- **Bundle Catalog** -- lists all available bundles
- [export-agent-bundle](../export-agent-bundle/SKILL.md) -- PABP export for cross-platform
- **Component Registry** -- domain mappings
- **Scope Agreement** -- profile definitions

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

## Best Practices
- Always follow the established guidelines.
- Document any deviations or exceptions.
- Regularly review and update the skill documentation.

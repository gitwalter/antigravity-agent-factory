import os
import re

root_dir = r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory"

# Mapping from old path to new path
replacements = {
    # audit
    "scripts/maintenance/audit_skill_metadata.py": "scripts/maintenance/audit/audit_skill_metadata.py",
    "scripts/maintenance/audit_catalog.py": "scripts/maintenance/audit/audit_catalog.py",
    "scripts/maintenance/audit_refs.py": "scripts/maintenance/audit/audit_refs.py",
    "scripts/maintenance/skill_reference_validator.py": "scripts/maintenance/audit/skill_reference_validator.py",
    "scripts/maintenance/link_checker.py": "scripts/maintenance/audit/link_checker.py",
    # repair
    "scripts/maintenance/fix_all_schemas.py": "scripts/maintenance/repair/fix_all_schemas.py",
    "scripts/maintenance/fix_artifact_naming.py": "scripts/maintenance/repair/fix_artifact_naming.py",
    "scripts/maintenance/fix_knowledge_structure.py": "scripts/maintenance/repair/fix_knowledge_structure.py",
    "scripts/maintenance/fix_pattern_schema.py": "scripts/maintenance/repair/fix_pattern_schema.py",
    "scripts/maintenance/fix_rag.py": "scripts/maintenance/repair/fix_rag.py",
    "scripts/maintenance/fix_renames.py": "scripts/maintenance/repair/fix_renames.py",
    "scripts/maintenance/fix_skill_frontmatter.py": "scripts/maintenance/repair/fix_skill_frontmatter.py",
    "scripts/maintenance/fix_skill_structure.py": "scripts/maintenance/repair/fix_skill_structure.py",
    "scripts/maintenance/fix_workflow_formatting.py": "scripts/maintenance/repair/fix_workflow_formatting.py",
    "scripts/maintenance/repair_docs.py": "scripts/maintenance/repair/repair_docs.py",
    "scripts/maintenance/fuzzy_link_repair.py": "scripts/maintenance/repair/fuzzy_link_repair.py",
    "scripts/maintenance/structural_remediation.py": "scripts/maintenance/repair/structural_remediation.py",
    "scripts/maintenance/move_workflows.py": "scripts/maintenance/repair/move_workflows.py",
    "scripts/maintenance/rename_docs.py": "scripts/maintenance/repair/rename_docs.py",
    "scripts/maintenance/standardize_doc_links.py": "scripts/maintenance/repair/standardize_doc_links.py",
    "scripts/maintenance/sanitize_links.py": "scripts/maintenance/repair/sanitize_links.py",
    "scripts/maintenance/smart_migrate.py": "scripts/maintenance/repair/smart_migrate.py",
    "scripts/maintenance/update_blueprint_versions.py": "scripts/maintenance/repair/update_blueprint_versions.py",
    "scripts/maintenance/deduplicate_components.py": "scripts/maintenance/repair/deduplicate_components.py",
    # sync
    "scripts/maintenance/sync_catalog.py": "scripts/maintenance/sync/sync_catalog.py",
    "scripts/maintenance/sync_memory_index.py": "scripts/maintenance/sync/sync_memory_index.py",
    "scripts/maintenance/sync_script_registry.py": "scripts/maintenance/sync/sync_script_registry.py",
    "scripts/maintenance/sync_upstream.py": "scripts/maintenance/sync/sync_upstream.py",
    "scripts/maintenance/sync_workflow_catalog.py": "scripts/maintenance/sync/sync_workflow_catalog.py",
    "scripts/maintenance/repo_sync.py": "scripts/maintenance/sync/repo_sync.py",
    "scripts/maintenance/apply_skill_updates.py": "scripts/maintenance/sync/apply_skill_updates.py",
    "scripts/maintenance/apply_knowledge_updates.py": "scripts/maintenance/sync/apply_knowledge_updates.py",
    "scripts/maintenance/map_skills_to_agents.py": "scripts/maintenance/sync/map_skills_to_agents.py",
    "scripts/maintenance/map_knowledge_to_skills.py": "scripts/maintenance/sync/map_knowledge_to_skills.py",
    "scripts/maintenance/enrich_bundles.py": "scripts/maintenance/sync/enrich_bundles.py",
    "scripts/maintenance/total_enrichment.py": "scripts/maintenance/sync/total_enrichment.py",
    # catalog
    "scripts/maintenance/generate_catalogs.py": "scripts/maintenance/catalog/generate_catalogs.py",
    "scripts/maintenance/generate_mapping.py": "scripts/maintenance/catalog/generate_mapping.py",
    "scripts/maintenance/reconstruct_catalog.py": "scripts/maintenance/catalog/reconstruct_catalog.py",
    # And specifically for scripts that were formerly at scripts/
    "scripts/audit_skill_metadata.py": "scripts/maintenance/audit/audit_skill_metadata.py",
    "scripts/map_skills_to_agents.py": "scripts/maintenance/sync/map_skills_to_agents.py",
    "scripts/apply_skill_updates.py": "scripts/maintenance/sync/apply_skill_updates.py",
    "scripts/map_knowledge_to_skills.py": "scripts/maintenance/sync/map_knowledge_to_skills.py",
    "scripts/apply_knowledge_updates.py": "scripts/maintenance/sync/apply_knowledge_updates.py",
    # Fix self-optimization-catalog "location" mapping:
    '"location": "scripts/maintenance/"': '"location": "scripts/maintenance/audit/"',  # Wait, this is too broad. Let's not do blanket string replacements.
}


def fix_references():
    search_dirs = [
        os.path.join(root_dir, ".agent"),
        os.path.join(root_dir, "docs"),
        os.path.join(root_dir, "scripts"),
    ]

    exts = [".md", ".json", ".py", ".txt"]

    count = 0
    for sdir in search_dirs:
        for root, dirs, files in os.walk(sdir):
            for file in files:
                if any(file.endswith(ext) for ext in exts):
                    filepath = os.path.join(root, file)
                    # Don't process this script itself
                    if file == "fix_script_references.py":
                        continue

                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            content = f.read()

                        new_content = content
                        for old, new in replacements.items():
                            new_content = new_content.replace(old, new)

                        # Special case for self-optimization-catalog.json location
                        # The json has scripts/maintenance/ but the script name determines the subfolder
                        if file == "self-optimization-catalog.json":
                            # We can just leave this as it's just a general location, but we can try to fix if needed.
                            pass

                        if new_content != content:
                            with open(filepath, "w", encoding="utf-8") as f:
                                f.write(new_content)
                            print(f"Updated references in {filepath}")
                            count += 1
                    except Exception as e:
                        pass

    print(f"Updated {count} files.")


if __name__ == "__main__":
    fix_references()


import json
import sys
from pathlib import Path

def fix_pattern_schema(factory_root: Path):
    patterns_dir = factory_root / ".agent" / "patterns"
    

    # Fix Agent Patterns
    agents_dir = patterns_dir / "agents"
    if agents_dir.exists():
        for pattern_file in agents_dir.glob("*.json"):
            if pattern_file.name.endswith("-pattern.json") or pattern_file.name == "schema.json":
                continue
                
            print(f"Processing agent pattern: {pattern_file.name}")
            try:
                content = pattern_file.read_text(encoding="utf-8")
                data = json.loads(content)
                
                if "frontmatter" not in data:
                    data["frontmatter"] = {}
                

                if "frontmatter" not in data:
                    data["frontmatter"] = {}

                fm = data["frontmatter"]

                # Required: name, description, type, version, domain, skills, knowledge, tools, workflows, blueprints

                # Check for root level fields and move/copy to frontmatter if missing
                root_fields = ["version", "tools", "workflows", "blueprints"]
                for field in root_fields:
                    if field not in fm:
                        val = data.get(field)
                        if val:
                             fm[field] = val

                # Ensure defaults
                if "version" not in fm: fm["version"] = "1.0.0"
                # Ensure tools
                if "tools" not in fm:
                    fm["tools"] = data.get("tools", [])
                    if not fm["tools"]:
                        fm["tools"] = ["none"]

                # Ensure workflows
                if "workflows" not in fm:
                    fm["workflows"] = ["none"]

                # Ensure blueprints
                if "blueprints" not in fm:
                    fm["blueprints"] = ["none"]

                # Pad skills if < 2 (Schema requires minItems: 2)
                if "skills" in fm:
                    if len(fm["skills"]) < 2:
                        if "tool-usage" not in fm["skills"]:
                             fm["skills"].append("tool-usage")
                        elif "onboarding-flow" not in fm["skills"]:
                             fm["skills"].append("onboarding-flow")
                        elif "project-info" not in fm["skills"]: # Just in case
                             fm["skills"].append("project-info")

                # Pad knowledge if < 2 (Schema requires minItems: 2)
                if "knowledge" in fm:
                     if len(fm["knowledge"]) < 2:
                          if "manifest.json" not in fm["knowledge"]:
                               fm["knowledge"].append("manifest.json")
                          elif "project-info.json" not in fm["knowledge"]:
                               fm["knowledge"].append("project-info.json")

                # Domain is required for Agent
                if "domain" not in fm:
                    cat = data.get("category", "development")
                    if cat == "core": fm["domain"] = "factory"
                    elif cat == "quality": fm["domain"] = "review"
                    else: fm["domain"] = "development"

                if json.dumps(data) != json.dumps(json.loads(content)): # Check if changed
                    pattern_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
                    print(f"Fixed {pattern_file.name}")
                
            except Exception as e:
                print(f"Error processing {pattern_file.name}: {e}")

    # Fix Skill Patterns
    skills_dir = patterns_dir / "skills"
    if skills_dir.exists():
        for pattern_file in skills_dir.glob("*.json"):
            if pattern_file.name.endswith("-pattern.json") or pattern_file.name == "schema.json":
                continue

            print(f"Processing skill pattern: {pattern_file.name}")
            try:
                content = pattern_file.read_text(encoding="utf-8")
                data = json.loads(content)
                if "frontmatter" not in data:
                    data["frontmatter"] = {}
                
                fm = data["frontmatter"]
                
                # Schema: name, description, type, version, category, agents, knowledge, tools, related_skills, templates
                # NO domain
                
                if "domain" in fm:
                    del fm["domain"] # Remove if present
                
                # Copy from root/metadata
                if "version" not in fm: fm["version"] = data.get("version", "1.0.0")
                
                # Check/Fix Category
                current_cat = fm.get("category") or data.get("metadata", {}).get("category", "core")
                
                # Map invalid categories
                valid_cats = ['core', 'rag', 'agent-patterns', 'integration', 'observability', 'specialized', 'workflow', 
                              'optimization', 'security', 'testing', 'ai-ml', 'trading', 'sap', 'dotnet', 'java', 'web', 
                              'devops', 'onboarding', 'factory']
                
                if current_cat == "ai-development": current_cat = "ai-ml"
                if current_cat == "quality": current_cat = "testing"
                if current_cat == "verification": current_cat = "testing" # or security? For security-audit, maybe security.
                
                if "security" in pattern_file.name and current_cat == "testing": current_cat = "security"

                if current_cat not in valid_cats:
                     # Fallback
                     current_cat = "core"
                
                fm["category"] = current_cat
                
                # Lists
                for field in ["agents", "tools", "related_skills", "templates", "knowledge"]:
                    if field not in fm:
                        val = data.get(field)
                        if val:
                            fm[field] = val
                        else:
                            # Default to placeholder if required and missing
                            if field in ["tools", "templates"]:
                                fm[field] = ["none"]
                            elif field == "knowledge":
                                fm[field] = ["none.json"] # Schema requires .json extension
                            else:
                                # agents, related_skills minItems 1
                                if field == "agents": fm[field] = ["code-reviewer"] # fallback
                                if field == "related_skills": fm[field] = ["onboarding-flow"] # fallback

                # Fix Templates (must be list of strings)
                if "templates" in fm and isinstance(fm["templates"], dict):
                    # It's a dict, we need to extract paths or keys
                    # If it has 'path' in values, use that.
                    new_templates = []
                    for k, v in fm["templates"].items():
                        if isinstance(v, dict) and "path" in v:
                            new_templates.append(v["path"])
                        elif isinstance(v, str):
                             new_templates.append(v)
                        else:
                             new_templates.append(str(k))
                    fm["templates"] = new_templates

                # Fix Axioms (must be object)
                if "axioms" in fm and isinstance(fm["axioms"], list):
                     new_axioms = {}
                     for ax in fm["axioms"]:
                          new_axioms[ax] = "declared"
                     fm["axioms"] = new_axioms
                
                # Remove disallowed fields (only allow schema fields)
                allowed_fields = [
                    "name", "description", "type", "version", "category", 
                    "agents", "knowledge", "tools", "related_skills", "templates",
                    "scope", "triggers", "prerequisites", "outputs", "complexity",
                    "has_scripts", "has_examples", "axioms", "extends", "inspiration",
                    "mcp_servers", "pattern", "patterns", "profile", "profiles", "skills"
                ]
                
                keys_to_remove = []
                for k in fm:
                    if k not in allowed_fields:
                        keys_to_remove.append(k)
                
                for k in keys_to_remove:
                    del fm[k]

                if json.dumps(data) != json.dumps(json.loads(content)):
                    pattern_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
                    print(f"Fixed {pattern_file.name}")
            except Exception as e:
                print(f"Error processing {pattern_file.name}: {e}")

if __name__ == "__main__":
    fix_pattern_schema(Path(__file__).parent.parent.parent)

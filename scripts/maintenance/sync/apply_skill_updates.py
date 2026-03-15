import os
import yaml
import json

SKILLS_DIR = (
    r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory\.agent\skills"
)
AGENTS_MAPPING_FILE = r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory\scripts\skill_to_agents.json"

# First, save the mapping from the previous tool output to a file for the script to use
mapping = {
    "managing-plane-tasks": ["project-operations-specialist"],
    "committing-releases": [
        "project-operations-specialist",
        "workflow-quality-specialist",
    ],
    "project-management-mastery": ["project-operations-specialist"],
    "pm-configuration": ["project-operations-specialist"],
    "documentation-generation": ["project-operations-specialist"],
    "risk-analysis": ["project-operations-specialist"],
    "designing-ai-systems": ["system-architecture-specialist"],
    "designing-apis": ["system-architecture-specialist"],
    "stack-configuration": ["system-architecture-specialist"],
    "template-generation": ["system-architecture-specialist"],
    "requirements-gathering": ["system-architecture-specialist"],
    "verifying-artifact-structures": [
        "workflow-quality-specialist",
        "knowledge-operations-specialist",
    ],
    "workflow-generation": ["workflow-quality-specialist"],
    "agent-testing": ["workflow-quality-specialist"],
    "pipeline-error-fix": ["workflow-quality-specialist"],
    "clean-code-review": ["workflow-quality-specialist"],
    "commit-release": ["workflow-quality-specialist"],
    "managing-google-workspace": ["executive-operations-specialist"],
    "managing-google-calendar": ["executive-operations-specialist"],
    "managing-google-drive": ["executive-operations-specialist"],
    "sending-emails": ["executive-operations-specialist"],
    "google-workspace-mastery": ["executive-operations-specialist"],
    "executive-communication-voice": ["executive-operations-specialist"],
    "smart-schedule-optimization": ["executive-operations-specialist"],
    "knowledge-base-curation": ["executive-operations-specialist"],
    "verification/smart-contract-audit": ["blockchain-guru-specialist"],
    "routing/managing-stack-context": [
        "blockchain-guru-specialist",
        "data-architect-specialist",
        "mobile-specialist",
    ],
    "verification/data-validation": ["data-architect-specialist"],
    "applying-ef-core-patterns": ["dotnet-cloud-specialist"],
    "developing-blazor-apps": ["dotnet-cloud-specialist"],
    "dotnet-enterprise-backend": ["dotnet-cloud-specialist"],
    "ef-core-profound": ["dotnet-cloud-specialist"],
    "azure-cloud-native-ops": ["dotnet-cloud-specialist"],
    "dotnet-observability-mastery": ["dotnet-cloud-specialist"],
    "blazor-high-fidelity": ["dotnet-cloud-specialist"],
    "developing-nextjs": ["full-stack-web-specialist"],
    "applying-react-patterns": ["full-stack-web-specialist"],
    "using-prisma-database": ["full-stack-web-specialist"],
    "building-nextjs-enterprise": ["full-stack-web-specialist"],
    "react-component-mastery": ["full-stack-web-specialist"],
    "type-safe-data-access": ["full-stack-web-specialist"],
    "web-performance-ops": ["full-stack-web-specialist"],
    "css-architect-vanilla": ["full-stack-web-specialist"],
    "developing-spring-boot": ["java-systems-specialist"],
    "building-spring-microservices": ["java-systems-specialist"],
    "observing-spring-apps": ["java-systems-specialist"],
    "testing-spring-apps": ["java-systems-specialist"],
    "building-spring-enterprise": ["java-systems-specialist"],
    "java-performance-tuning": ["java-systems-specialist"],
    "resilient-messaging": ["java-systems-specialist"],
    "distributed-tracing-mastery": ["java-systems-specialist"],
    "verification/mobile-native-build": ["mobile-specialist"],
    "mastering-agentic-loops": ["python-ai-specialist"],
    "engineering-rag-systems": ["python-ai-specialist"],
    "tracing-with-langsmith": ["python-ai-specialist"],
    "securing-agents": ["python-ai-specialist"],
    "building-fastapi-enterprise": ["python-ai-specialist"],
    "operating-ml-engineering": ["python-ai-specialist"],
    "llm-observability-ops": ["python-ai-specialist"],
    "sqlalchemy-async-patterns": ["python-ai-specialist"],
    "developing-sap-rap": ["sap-systems-specialist"],
    "building-sap-fiori": ["sap-systems-specialist"],
    "integrating-sap-cloud": ["sap-systems-specialist"],
    "securing-sap-systems": ["sap-systems-specialist"],
    "s4-domain-mastery": ["sap-systems-specialist"],
    "sap-btp-ops": ["sap-systems-specialist"],
    "knowledge-creator": ["knowledge-operations-specialist"],
    "operating-github": ["knowledge-operations-specialist"],
    "knowledge-generation": ["knowledge-operations-specialist"],
    "link-verification": ["knowledge-operations-specialist"],
    "repo-sync": ["knowledge-operations-specialist"],
    "wisdom-harvest": ["knowledge-operations-specialist"],
    "analyze-knowledge-gaps": ["knowledge-operations-specialist"],
}


def apply_updates():
    updated_count = 0
    for root, dirs, files in os.walk(SKILLS_DIR):
        if "SKILL.md" in files:
            skill_path = os.path.join(root, "SKILL.md")
            with open(skill_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Find frontmatter
            indices = [i for i, line in enumerate(lines) if line.strip() == "---"]
            if len(indices) >= 2:
                frontmatter_lines = lines[indices[0] + 1 : indices[1]]
                try:
                    metadata = yaml.safe_load("".join(frontmatter_lines))
                    skill_name = metadata.get("name")

                    if skill_name in mapping:
                        new_agents = mapping[skill_name]
                        current_agents = metadata.get("agents", [])

                        if (
                            current_agents == "none"
                            or current_agents == ["none"]
                            or not current_agents
                        ):
                            metadata["agents"] = new_agents

                            # Re-serialise frontmatter
                            new_frontmatter = yaml.dump(metadata, sort_keys=False)
                            new_lines = (
                                lines[: indices[0] + 1]
                                + [new_frontmatter]
                                + lines[indices[1] :]
                            )

                            with open(skill_path, "w", encoding="utf-8") as f:
                                f.writelines(new_lines)
                            print(f"Updated agents for {skill_name}")
                            updated_count += 1
                except Exception as e:
                    print(f"Error processing {skill_path}: {e}")
    return updated_count


if __name__ == "__main__":
    count = apply_updates()
    print(f"Successfully updated {count} skill files.")

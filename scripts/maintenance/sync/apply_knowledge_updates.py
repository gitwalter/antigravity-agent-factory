import os
import yaml
import json

SKILLS_DIR = (
    r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory\.agent\skills"
)

# Aggregated Knowledge Mapping results from previous step
knowledge_mapping = {
    "applying-ef-core-patterns": ["entity-framework-core-advanced-patterns.json"],
    "browsing-web": [
        "web-browsing-and-scraping-patterns.json",
        "web-browsing-patterns.json",
    ],
    "developing-bdd": ["bdd-patterns-and-best-practices.json", "bdd-patterns.json"],
    "developing-fiori-apps": ["sap-fiori-patterns.json"],
    "developing-rap-objects": [
        "sap-cap-cds-and-abap-patterns.json",
        "sap-rap-patterns.json",
    ],
    "extending-knowledge": [
        "advanced-agent-architectures.json",
        "dashboard-knowledge.json",
        "game-mechanics-knowledge.json",
        "knowledge-manifest.json",
        "workshop-facilitation-knowledge.json",
    ],
    "extending-workflows": [
        "langgraph-workflow-patterns.json",
        "schemas-workflow-schema.json",
        "workflow-patterns.json",
    ],
    "generating-knowledge": [
        "dashboard-knowledge.json",
        "game-mechanics-knowledge.json",
        "knowledge-generation.json",
        "knowledge-manifest.json",
        "workshop-facilitation-knowledge.json",
    ],
    "generating-templates": ["github-agent-templates.json", "template-catalog.json"],
    "generating-workflows": [
        "langgraph-workflow-patterns.json",
        "schemas-workflow-schema.json",
        "workflow-patterns.json",
    ],
    "integrating-mcp": [
        "aisuite-integration.json",
        "api-integration.json",
        "mcp-selection-guide.json",
        "mcp-server-selection-guide.json",
        "mcp-servers-catalog.json",
        "model-context-protocol-patterns.json",
        "plane-integration.json",
    ],
    "managing-knowledge-graphs": [
        "dashboard-knowledge.json",
        "game-mechanics-knowledge.json",
        "workshop-facilitation-knowledge.json",
    ],
    "managing-memory": [
        "agent-memory-patterns-2026.json",
        "agent-memory-patterns.json",
        "hierarchical-memory-patterns.json",
        "memory-config.json",
        "memory-patterns.json",
        "memory-system-configuration.json",
        "memory-systems-patterns.json",
    ],
    "onboarding-configurations": ["memory-system-configuration.json"],
    "programming-python-async": [
        "python-production-patterns.json",
        "reactive-programming-patterns.json",
    ],
    "securing-agents": ["openai-agents-sdk-patterns.json"],
    "securing-ai-systems": ["memory-systems-patterns.json"],
    "securing-sap-systems": ["memory-systems-patterns.json"],
    "skill-creator": [
        "atomic-skill-patterns.json",
        "creator-skills-mapping.json",
        "skill-catalog.json",
    ],
    "template-creator": [
        "creator-skills-mapping.json",
        "github-agent-templates.json",
        "template-catalog.json",
    ],
    "testing-frontend": [
        "agent-testing-patterns.json",
        "agent-testing.json",
        "backtesting-framework-patterns.json",
        "frontend-performance-patterns.json",
        "kotest-testing-framework-patterns.json",
    ],
    "testing-spring-apps": [
        "agent-testing-patterns.json",
        "agent-testing.json",
        "backtesting-framework-patterns.json",
        "kotest-testing-framework-patterns.json",
        "spring-boot-kotlin-patterns.json",
        "spring-boot-patterns.json",
        "spring-microservices-patterns.json",
        "spring-observability-patterns.json",
        "spring-patterns.json",
    ],
    "using-langchain": ["langchain-patterns.json"],
    "using-prisma-database": [
        "database-agent-patterns.json",
        "prisma-database-patterns.json",
        "vector-database-patterns.json",
    ],
    "workflow-creator": [
        "creator-skills-mapping.json",
        "langgraph-workflow-patterns.json",
        "langgraph-workflows.json",
        "ml-workflow-patterns.json",
        "n8n-workflow-automation-patterns.json",
        "schemas-workflow-schema.json",
        "workflow-catalog.json",
        "workflow-entities.json",
        "workflow-patterns.json",
        "workflow-system-entities.json",
    ],
    "workshop-creator": [
        "creator-skills-mapping.json",
        "workshop-facilitation-knowledge.json",
        "workshop-facilitation.json",
    ],
    "managing-google-calendar": [
        "google-agent-development-kit-patterns.json",
        "google-generative-ai-patterns.json",
    ],
    "managing-google-drive": [
        "ai-driven-tdd-patterns.json",
        "google-agent-development-kit-patterns.json",
        "google-generative-ai-patterns.json",
    ],
    "managing-google-workspace": [
        "google-agent-development-kit-patterns.json",
        "google-generative-ai-patterns.json",
    ],
    "managing-plane-tasks": ["plane-integration.json", "plane-tasks-methodology.json"],
}


def apply_knowledge_updates():
    updated_count = 0
    for root, dirs, files in os.walk(SKILLS_DIR):
        if "SKILL.md" in files:
            skill_path = os.path.join(root, "SKILL.md")
            with open(skill_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            indices = [i for i, line in enumerate(lines) if line.strip() == "---"]
            if len(indices) >= 2:
                frontmatter_lines = lines[indices[0] + 1 : indices[1]]
                try:
                    metadata = yaml.safe_load("".join(frontmatter_lines))
                    skill_name = metadata.get("name")

                    if skill_name in knowledge_mapping:
                        new_k = knowledge_mapping[skill_name]
                        curr_k = metadata.get("knowledge", [])

                        if curr_k == "none" or curr_k == ["none"] or not curr_k:
                            metadata["knowledge"] = new_k
                            new_fm = yaml.dump(metadata, sort_keys=False)
                            new_lines = (
                                lines[: indices[0] + 1] + [new_fm] + lines[indices[1] :]
                            )

                            with open(skill_path, "w", encoding="utf-8") as f:
                                f.writelines(new_lines)
                            print(f"Updated knowledge for {skill_name}")
                            updated_count += 1
                except Exception:
                    pass
    return updated_count


if __name__ == "__main__":
    count = apply_knowledge_updates()
    print(f"Successfully updated knowledge for {count} skill files.")

import os
import shutil
import re

KNOWLEDGE_PATH = r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory\.agent\knowledge"
SKILLS_ROOT = (
    r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory\.agent\skills"
)

# Mapping logic: (Knowledge Filename Regex, Skill Name)
MAPPING = [
    (r"advanced-rag-patterns.*\.json", "advanced-retrieval"),
    (r"algorithmic-trading-patterns\.json", "algorithmic-trading"),
    (r"agent-testing.*\.json", "testing-agents"),
    (r"ai-driven-tdd-patterns\.json", "testing-agents"),
    (r"api-design-patterns\.json", "api-design"),
    (r"api-integration-patterns\.json", "api-design"),
    (r"bdd-patterns.*\.json", "behavior-driven-development"),
    (r"caching-patterns\.json", "optimizing-caching"),
    (r"cicd-patterns\.json", "monitoring-ci"),
    (r"crewai-patterns\.json", "orchestrating-crewai-workflows"),
    (r"data-pipeline-patterns\.json", "processing-data-pipelines"),
    (r"database-agent-patterns\.json", "managing-database-agents"),
    (r"docker-patterns\.json", "deploying-with-docker"),
    (r"dotnet-patterns.*\.json", "dotnet-backend"),
    (r"fastapi-patterns\.json", "fastapi-development"),
    (r"fiori-patterns\.json", "sap-fiori-elements"),
    (r"github-agent-templates\.json", "operating-github"),
    (r"kubernetes-patterns.*\.json", "deploying-to-kubernetes"),
    (r"langchain-patterns\.json", "langchain-usage"),
    (r"langgraph-.*\.json", "building-langgraph-agents"),
    (r"llm-evaluation-.*\.json", "evaluating-llms"),
    (r"llm-fine-tuning-.*\.json", "fine-tuning-models"),
    (r"mcp-patterns\.json", "integrating-mcp"),
    (r"next-?js-.*\.json", "nextjs-development"),
    (r"ocr-patterns.*\.json", "processing-ocr"),
    (r"prisma-database-patterns\.json", "prisma-database"),
    (r"prompt-engineering.*\.json", "optimizing-prompts"),
    (r"rag-patterns.*\.json", "rag-patterns"),
    (r"react-.*\.json", "react-patterns"),
    (r"sap-cap.*\.json", "sap-enterprise-rap"),
    (r"sap-rap.*\.json", "sap-enterprise-rap"),
    (r"solana-.*\.json", "solana-development"),
    (r"spring-.*\.json", "spring-boot-development"),
    (r"sqlalchemy-patterns\.json", "sqlalchemy-patterns"),
    (r"workflow-patterns\.json", "generating-workflows"),
]


def enrich():
    print(f"Reading knowledge files from: {KNOWLEDGE_PATH}")
    if not os.path.exists(KNOWLEDGE_PATH):
        print(f"ERROR: Knowledge path does not exist: {KNOWLEDGE_PATH}")
        return

    knowledge_files = os.listdir(KNOWLEDGE_PATH)
    print(f"Found {len(knowledge_files)} files in knowledge directory.")

    for pattern_dir in os.listdir(SKILLS_ROOT):
        pattern_path = os.path.join(SKILLS_ROOT, pattern_dir)
        if not os.path.isdir(pattern_path or pattern_dir.startswith(".")):
            continue

        for skill_dir in os.listdir(pattern_path):
            skill_path = os.path.join(pattern_path, skill_dir)
            if not os.path.isdir(skill_path):
                continue

            # Find matching knowledge files
            for regex, target_skill in MAPPING:
                if skill_dir == target_skill:
                    for k_file in knowledge_files:
                        if re.match(regex, k_file):
                            src = os.path.join(KNOWLEDGE_PATH, k_file)
                            dst_dir = os.path.join(skill_path, "references")
                            os.makedirs(dst_dir, exist_ok=True)
                            dst = os.path.join(dst_dir, k_file)
                            print(f"Moving {k_file} -> {skill_dir}/references/")
                            try:
                                shutil.copy2(
                                    src, dst
                                )  # Use copy first to be safe, then we can delete if needed
                                print("  Success")
                            except Exception as e:
                                print(f"  FAILED: {str(e)}")


if __name__ == "__main__":
    enrich()

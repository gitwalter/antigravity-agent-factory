import os
import re
import yaml
import json

AGENTS_DIR = (
    r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory\.agent\agents"
)


def map_agents_to_skills():
    skill_to_agents = {}

    for root, dirs, files in os.walk(AGENTS_DIR):
        for file in files:
            if file.endswith(".md"):
                agent_path = os.path.join(root, file)
                with open(agent_path, "r", encoding="utf-8") as f:
                    content = f.read()

                parts = content.split("---")
                agent_name = "unknown"
                if len(parts) >= 3:
                    try:
                        metadata = yaml.safe_load(parts[1])
                        agent_name = metadata.get("name", file.replace(".md", ""))

                        # Add skills from frontmatter
                        skills = metadata.get("skills", [])
                        if isinstance(skills, list):
                            for s in skills:
                                if s not in skill_to_agents:
                                    skill_to_agents[s] = []
                                if agent_name not in skill_to_agents[s]:
                                    skill_to_agents[s].append(agent_name)
                    except Exception:
                        pass

                # Also look for [[skill-slug]] in content
                wiki_skills = re.findall(r"\[\[(.*?)\]\]", content)
                for s in wiki_skills:
                    if s not in skill_to_agents:
                        skill_to_agents[s] = []
                    if agent_name not in skill_to_agents[s]:
                        skill_to_agents[s].append(agent_name)

                # Also look for Mermaid skill references like Skills --> S1["skill-slug"]
                mermaid_skills = re.findall(r'Skills --> .*?\["(.*?)"\]', content)
                for s in mermaid_skills:
                    if s not in skill_to_agents:
                        skill_to_agents[s] = []
                    if agent_name not in skill_to_agents[s]:
                        skill_to_agents[s].append(agent_name)

    return skill_to_agents


if __name__ == "__main__":
    mapping = map_agents_to_skills()
    print(json.dumps(mapping, indent=2))

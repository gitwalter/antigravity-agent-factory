#!/usr/bin/env python3
"""
Catalog Generator
Generates docs/CATALOG.md by scanning the repository for blueprints, agents, skills, and workflows.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any

def get_factory_root() -> Path:
    """Return the root directory of the factory."""
    return Path(__file__).parent.parent.parent

def load_blueprint(path: Path) -> Dict[str, Any]:
    """Load and parse a blueprint.json file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('metadata', {})
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return {}

def extract_markdown_title(path: Path) -> str:
    """Extract the first H1 header from a markdown file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('# '):
                    return line[2:].strip()
    except Exception:
        pass
    return path.stem.replace('-', ' ').title()

def generate_catalog():
    root = get_factory_root()
    catalog_path = root / 'CATALOG.md'
    
    blueprints = []
    blueprints_dirs = [root / 'blueprints', root / '.agent' / 'blueprints']
    for blueprints_dir in blueprints_dirs:
        if blueprints_dir.exists():
            for bp_dir in sorted(blueprints_dir.iterdir()):
                if bp_dir.is_dir():
                    bp_file = bp_dir / 'blueprint.json'
                    if bp_file.exists():
                        meta = load_blueprint(bp_file)
                        blueprints.append({
                            'id': meta.get('blueprintId', bp_dir.name),
                            'name': meta.get('blueprintName', bp_dir.name.title()),
                            'description': meta.get('description', 'No description'),
                            'tags': meta.get('tags', []),
                            'path': bp_dir.relative_to(root).as_posix() # Link to dir
                        })

    # Helper to calculate path relative to root (where catalog now lives)
    def get_rel_path(path):
        return path.relative_to(root).as_posix()

    agents = []
    agent_dirs = [root / '.agent' / 'agents', root / 'patterns' / 'agents']
    for ad in agent_dirs:
        if ad.exists():
            for agent_file in sorted(ad.glob('*.md')):
                agents.append({
                    'name': agent_file.stem,
                    'title': extract_markdown_title(agent_file),
                    'path': get_rel_path(agent_file)
                })

    skills = []
    skill_dirs = [root / '.agent' / 'skills', root / 'patterns' / 'skills']
    for sd in skill_dirs:
        if sd.exists():
            for skill_dir in sorted(sd.iterdir()):
                if skill_dir.is_dir():
                    skill_file = skill_dir / 'SKILL.md'
                    if skill_file.exists():
                        skills.append({
                            'name': skill_dir.name,
                            'title': extract_markdown_title(skill_file),
                            'path': get_rel_path(skill_file)
                        })

    workflows = []
    workflow_dirs = [root / 'patterns' / 'workflows', root / 'workflows', root / '.agent' / 'workflows'] 
    for wd in workflow_dirs:
        if wd.exists():
            for wf_file in sorted(wd.glob('*.md')):
                workflows.append({
                    'name': wf_file.stem,
                    'title': extract_markdown_title(wf_file),
                    'path': get_rel_path(wf_file)
                })
    
    knowledge = []
    knowledge_dirs = [root / 'knowledge', root / '.agent' / 'knowledge']
    for kd in knowledge_dirs:
        if kd.exists():
             for k_file in sorted(kd.glob('*.json')):
                 knowledge.append({
                     'name': k_file.stem,
                     'path': get_rel_path(k_file)
                 })

    templates = []
    templates_dirs = [root / 'templates', root / '.agent' / 'templates']
    for templates_dir in templates_dirs:
        if templates_dir.exists():
            for item in sorted(templates_dir.rglob('*')):
                if item.is_file() and not item.name.startswith('.'):
                     category = item.parent.name
                     templates.append({
                         'name': item.name,
                         'category': category,
                         'path': get_rel_path(item)
                     })

    with open(catalog_path, 'w', encoding='utf-8') as f:
        f.write("# Antigravity Agent Factory Catalog\n\n")
        f.write("A comprehensive directory of all blueprints, agents, skills, workflows, and templates available in the factory.\n\n")
        
        f.write("## 📐 Blueprints\n\n")
        f.write("| Blueprint | Description | Tags |\n")
        f.write("|-----------|-------------|------|\n")
        for bp in blueprints:
            tags = ', '.join([f"`{t}`" for t in bp['tags']])
            # Link to the blueprint directory
            f.write(f"| [**{bp['name']}**]({bp['path']}) (`{bp['id']}`) | {bp['description']} | {tags} |\n")
        f.write("\n")

        f.write("## 🤖 Agents\n\n")
        f.write("| Agent | Description |\n")
        f.write("|-------|-------------|\n")
        for agent in agents:
            f.write(f"| [{agent['name']}]({agent['path']}) | {agent['title']} |\n")
        f.write("\n")

        f.write("## 🛠 Skills\n\n")
        f.write("| Skill | Description |\n")
        f.write("|-------|-------------|\n")
        for skill in skills:
            f.write(f"| [{skill['name']}]({skill['path']}) | {skill['title']} |\n")
        f.write("\n")
        
        f.write("## 📋 Workflows\n\n")
        f.write("| Workflow | Description |\n")
        f.write("|----------|-------------|\n")
        for wf in workflows:
            f.write(f"| [{wf['name']}]({wf['path']}) | {wf['title']} |\n")
        f.write("\n")

        f.write("## 📚 Knowledge Files\n\n")
        f.write("| File | Path |\n")
        f.write("|------|------|\n")
        for k in knowledge:
             f.write(f"| {k['name']} | [`{k['path']}`]({k['path']}) |\n")
        f.write("\n")

        f.write("## 📄 Templates\n\n")
        f.write("| Template | Category | Path |\n")
        f.write("|----------|----------|------|\n")
        # limit to first 50 to avoid cluttering if too many, or maybe categorize
        count = 0
        for t in templates:
            f.write(f"| {t['name']} | {t['category']} | [`{t['path']}`]({t['path']}) |\n")
            count += 1
        f.write(f"\n*Total templates: {count}*\n")

    print(f"Catalog generated at directory CATALOG.md")

if __name__ == "__main__":
    generate_catalog()

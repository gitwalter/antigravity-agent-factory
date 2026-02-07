#!/usr/bin/env python3
"""
Generate readable markdown documentation from workshop JSON files.

This script converts workshop JSON definitions into human-friendly markdown
documents suitable for developers to read and follow.

Usage:
    python scripts/docs/generate_workshop_docs.py
"""

import json
from pathlib import Path
from typing import Any


def load_workshop(filepath: Path) -> dict[str, Any]:
    """Load a workshop JSON file."""
    with open(filepath, encoding='utf-8') as f:
        return json.load(f)


def generate_markdown(workshop: dict[str, Any]) -> str:
    """Generate markdown documentation from workshop JSON."""
    lines = []
    
    # Header
    lines.append(f"# {workshop['name']}")
    lines.append("")
    
    # Metadata
    tech = workshop.get('technology', {})
    lines.append(f"> **Stack:** {tech.get('stack', 'N/A')} | "
                f"**Level:** {workshop.get('level', 'N/A').title()} | "
                f"**Duration:** {workshop.get('duration', {}).get('total_hours', 2.5)} hours")
    lines.append("")
    
    # Overview
    lines.append("## Overview")
    lines.append("")
    lines.append(f"**Workshop ID:** `{workshop.get('workshopId', 'N/A')}`")
    lines.append("")
    lines.append(f"**Technology:** {tech.get('language', 'N/A')} with {tech.get('stack', 'N/A')} ({tech.get('version', 'latest')})")
    lines.append("")
    
    # Prerequisites
    prereqs = workshop.get('prerequisites', {})
    if prereqs:
        lines.append("## Prerequisites")
        lines.append("")
        if prereqs.get('workshops'):
            lines.append("**Required Workshops:**")
            for w in prereqs['workshops']:
                lines.append(f"- {w}")
            lines.append("")
        if prereqs.get('knowledge'):
            lines.append("**Required Knowledge:**")
            for k in prereqs['knowledge']:
                lines.append(f"- {k}")
            lines.append("")
        if prereqs.get('tools'):
            lines.append("**Required Tools:**")
            for t in prereqs['tools']:
                lines.append(f"- {t}")
            lines.append("")
    
    # Learning Objectives
    objectives = workshop.get('learning_objectives', [])
    if objectives:
        lines.append("## Learning Objectives")
        lines.append("")
        lines.append("By the end of this workshop, you will be able to:")
        lines.append("")
        for i, obj in enumerate(objectives, 1):
            if isinstance(obj, dict):
                lines.append(f"{i}. **{obj.get('objective', 'N/A')}** ({obj.get('bloom_level', 'apply').title()})")
            else:
                lines.append(f"{i}. {obj}")
        lines.append("")
    
    # Duration breakdown
    duration = workshop.get('duration', {})
    if duration:
        lines.append("## Workshop Timeline")
        lines.append("")
        lines.append("| Phase | Duration |")
        lines.append("|-------|----------|")
        if duration.get('concept_minutes'):
            lines.append(f"| Concept | {duration['concept_minutes']} min |")
        if duration.get('demo_minutes'):
            lines.append(f"| Demo | {duration['demo_minutes']} min |")
        if duration.get('exercise_minutes'):
            lines.append(f"| Exercise | {duration['exercise_minutes']} min |")
        if duration.get('challenge_minutes'):
            lines.append(f"| Challenge | {duration['challenge_minutes']} min |")
        if duration.get('reflection_minutes'):
            lines.append(f"| Reflection | {duration['reflection_minutes']} min |")
        if duration.get('total_hours'):
            lines.append(f"| **Total** | **{duration['total_hours']} hours** |")
        lines.append("")
    
    # Phases
    phases = workshop.get('phases', [])
    if phases:
        lines.append("## Workshop Phases")
        lines.append("")
        for phase in phases:
            phase_name = phase.get('name', phase.get('phaseId', 'Unknown'))
            phase_type = phase.get('type', 'unknown').title()
            lines.append(f"### {phase_type}: {phase_name}")
            lines.append("")
            if phase.get('description'):
                lines.append(f"*{phase['description']}*")
                lines.append("")
            
            content = phase.get('content', {})
            if content.get('topics'):
                lines.append("**Topics Covered:**")
                for topic in content['topics']:
                    lines.append(f"- {topic}")
                lines.append("")
            
            if content.get('key_points'):
                lines.append("**Key Points:**")
                for point in content['key_points']:
                    lines.append(f"- {point}")
                lines.append("")
    
    # Exercises
    exercises = workshop.get('exercises', [])
    if exercises:
        lines.append("## Hands-On Exercises")
        lines.append("")
        for ex in exercises:
            lines.append(f"### Exercise: {ex.get('name', 'Unknown')}")
            lines.append("")
            if ex.get('description'):
                lines.append(f"{ex['description']}")
                lines.append("")
            lines.append(f"**Difficulty:** {ex.get('difficulty', 'medium').title()} | "
                        f"**Duration:** {ex.get('duration_minutes', 20)} minutes")
            lines.append("")
            
            if ex.get('hints'):
                lines.append("**Hints:**")
                for hint in ex['hints']:
                    lines.append(f"- {hint}")
                lines.append("")
            
            if ex.get('common_mistakes'):
                lines.append("**Common Mistakes to Avoid:**")
                for mistake in ex['common_mistakes']:
                    lines.append(f"- {mistake}")
                lines.append("")
    
    # Challenges
    challenges = workshop.get('challenges', [])
    if challenges:
        lines.append("## Challenges")
        lines.append("")
        for ch in challenges:
            lines.append(f"### Challenge: {ch.get('name', 'Unknown')}")
            lines.append("")
            if ch.get('description'):
                lines.append(f"{ch['description']}")
                lines.append("")
            
            if ch.get('requirements'):
                lines.append("**Requirements:**")
                for req in ch['requirements']:
                    lines.append(f"- {req}")
                lines.append("")
            
            if ch.get('evaluation_criteria'):
                lines.append("**Evaluation Criteria:**")
                for crit in ch['evaluation_criteria']:
                    lines.append(f"- {crit}")
                lines.append("")
            
            if ch.get('stretch_goals'):
                lines.append("**Stretch Goals:**")
                for goal in ch['stretch_goals']:
                    lines.append(f"- {goal}")
                lines.append("")
    
    # Resources
    resources = workshop.get('resources', {})
    if resources:
        lines.append("## Resources")
        lines.append("")
        if resources.get('official_docs'):
            lines.append("**Official Documentation:**")
            for doc in resources['official_docs']:
                lines.append(f"- {doc}")
            lines.append("")
        if resources.get('tutorials'):
            lines.append("**Tutorials:**")
            for tut in resources['tutorials']:
                lines.append(f"- {tut}")
            lines.append("")
        if resources.get('videos'):
            lines.append("**Videos:**")
            for vid in resources['videos']:
                lines.append(f"- {vid}")
            lines.append("")
    
    # Assessment
    assessment = workshop.get('assessment', {})
    if assessment:
        lines.append("## Self-Assessment")
        lines.append("")
        if assessment.get('self_assessment'):
            lines.append("Ask yourself these questions:")
            lines.append("")
            for q in assessment['self_assessment']:
                lines.append(f"- [ ] {q}")
            lines.append("")
    
    # Next Steps
    next_steps = workshop.get('next_steps', {})
    if next_steps:
        lines.append("## Next Steps")
        lines.append("")
        if next_steps.get('next_workshop'):
            lines.append(f"**Next Workshop:** `{next_steps['next_workshop']}`")
            lines.append("")
        if next_steps.get('practice_projects'):
            lines.append("**Practice Projects:**")
            for proj in next_steps['practice_projects']:
                lines.append(f"- {proj}")
            lines.append("")
        if next_steps.get('deeper_learning'):
            lines.append("**Deeper Learning:**")
            for topic in next_steps['deeper_learning']:
                lines.append(f"- {topic}")
            lines.append("")
    
    # Knowledge Files
    knowledge_files = workshop.get('knowledge_files', [])
    if knowledge_files:
        lines.append("## Related Knowledge Files")
        lines.append("")
        for kf in knowledge_files:
            lines.append(f"- `{kf}`")
        lines.append("")
    
    # Footer
    lines.append("---")
    lines.append("")
    lines.append("*Part of the Antigravity Agent Factory Learning Workshop Ecosystem*")
    lines.append("")
    lines.append(f"**Workshop Definition:** `patterns/workshops/{workshop.get('workshopId', 'unknown')}.json`")
    
    return '\n'.join(lines)


def generate_index(workshops: list[dict[str, Any]]) -> str:
    """Generate the index README for the workshops folder."""
    lines = []
    
    lines.append("# Learning Workshops")
    lines.append("")
    lines.append("> **Philosophy:** Learning is a journey of transformation. Through structured exploration and hands-on practice, developers grow in skill and wisdom.")
    lines.append("")
    lines.append(f"This folder contains readable documentation for all **{len(workshops)} learning workshops** in the Antigravity Agent Factory.")
    lines.append("")
    
    # Group by category
    categories = {}
    for w in workshops:
        cat = w.get('technology', {}).get('category', 'other')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(w)
    
    # Category names
    cat_names = {
        'blockchain': 'Blockchain',
        'ai_framework': 'AI Frameworks',
        'web_fullstack': 'Web Fullstack',
        'cloud_native': 'Cloud Native',
        'data_ml': 'Data & ML'
    }
    
    lines.append("## Workshop Catalog")
    lines.append("")
    
    for cat_id, cat_name in cat_names.items():
        if cat_id in categories:
            lines.append(f"### {cat_name}")
            lines.append("")
            lines.append("| ID | Workshop | Stack | Level |")
            lines.append("|----|----------|-------|-------|")
            for w in sorted(categories[cat_id], key=lambda x: x.get('workshopId', '')):
                wid = w.get('workshopId', '')
                name = w.get('name', 'Unknown')
                stack = w.get('technology', {}).get('stack', 'N/A')
                level = w.get('level', 'fundamentals').title()
                lines.append(f"| [{wid}]({wid}.md) | {name} | {stack} | {level} |")
            lines.append("")
    
    lines.append("## How to Use")
    lines.append("")
    lines.append("1. **Choose a workshop** based on your learning goals")
    lines.append("2. **Check prerequisites** in the workshop document")
    lines.append("3. **Follow the phases** (Concept → Demo → Exercise → Challenge → Reflection)")
    lines.append("4. **Complete the self-assessment** to verify your understanding")
    lines.append("5. **Move to the next workshop** in the learning path")
    lines.append("")
    
    lines.append("## Workshop Structure")
    lines.append("")
    lines.append("Each 2.5-hour workshop follows the same proven structure:")
    lines.append("")
    lines.append("| Phase | Duration | Purpose |")
    lines.append("|-------|----------|---------|")
    lines.append("| **Concept** | 30 min | Theory, architecture, mental models |")
    lines.append("| **Demo** | 30 min | Live coding walkthrough |")
    lines.append("| **Exercise** | 45 min | Guided hands-on practice |")
    lines.append("| **Challenge** | 30 min | Independent problem-solving |")
    lines.append("| **Reflection** | 15 min | Key takeaways, self-assessment |")
    lines.append("")
    
    lines.append("---")
    lines.append("")
    lines.append("*Part of the Antigravity Agent Factory — Building with Love, Truth, and Beauty*")
    
    return '\n'.join(lines)


def main():
    """Main entry point."""
    workshops_dir = Path('patterns/workshops')
    output_dir = Path('docs/workshops')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    workshops = []
    
    # Process each workshop JSON
    for json_file in sorted(workshops_dir.glob('L*.json')):
        if 'pattern' in json_file.name.lower():
            continue
        
        print(f"Processing {json_file.name}...")
        workshop = load_workshop(json_file)
        workshops.append(workshop)
        
        # Generate markdown
        markdown = generate_markdown(workshop)
        
        # Write output
        output_file = output_dir / f"{workshop.get('workshopId', json_file.stem)}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown)
        print(f"  -> Created {output_file.name}")
    
    # Generate index
    print("\nGenerating index...")
    index_md = generate_index(workshops)
    with open(output_dir / 'README.md', 'w', encoding='utf-8') as f:
        f.write(index_md)
    print(f"  -> Created README.md")
    
    print(f"\nDone! Generated {len(workshops)} workshop documents + index in {output_dir}/")


if __name__ == '__main__':
    main()

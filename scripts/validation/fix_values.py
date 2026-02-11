#!/usr/bin/env python3
"""
Fix Values - Auto-fix value consistency issues in blueprints and patterns.

This script adds guardian awareness and axiom references to all patterns.

Usage:
    python scripts/validation/fix_values.py --dry-run  # Preview changes
    python scripts/validation/fix_values.py            # Apply fixes
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, List


class ValuesFixer:
    """Fixes value consistency issues in Factory artifacts."""
    
    def __init__(self, factory_root: Path, dry_run: bool = False):
        self.factory_root = factory_root
        self.dry_run = dry_run
        self.fixed_count = 0
        
        # Guardian agents to add to all blueprints
        self.guardian_agents = [
            {"patternId": "knowledge-extender", "required": True, "description": "Extend knowledge base during development"},
            {"patternId": "factory-updates", "required": True, "description": "Receive updates from the Antigravity Agent Factory"}        ]
        
        # Value-propagating skills to add
        self.value_skills = [
            {"patternId": "extend-knowledge", "required": True, "description": "Extend knowledge base with new topics"},
            {"patternId": "receive-updates", "required": True, "description": "Receive updates from Factory"}
        ]
        
        # Guardian awareness section for agents
        self.guardian_section = {
            "guardian_awareness": {
                "enabled": True,
                "axioms": ["A1", "A2", "A3", "A4", "A5"],
                "wu_wei_protocol": True,
                "note": "This agent operates under Layer 0 Integrity Guardian. When in doubt, return to love."
            }
        }
        
        # Axiom rule to add to skills
        self.axiom_rule = "All actions must align with core axioms (A1: Verifiability, A2: User Primacy, A3: Transparency, A4: Non-Harm, A5: Consistency)"
    
    def fix_blueprint(self, blueprint_path: Path) -> bool:
        """Fix a single blueprint."""
        try:
            with open(blueprint_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"  ERROR: Cannot read {blueprint_path}: {e}")
            return False
        
        modified = False
        blueprint_id = data.get('metadata', {}).get('blueprintId', blueprint_path.parent.name)
        
        # Get existing agent/skill IDs
        existing_agents = {a.get('patternId') for a in data.get('agents', [])}
        existing_skills = {s.get('patternId') for s in data.get('skills', [])}
        
        # Add missing guardian agents
        for agent in self.guardian_agents:
            if agent['patternId'] not in existing_agents:
                if 'agents' not in data:
                    data['agents'] = []
                data['agents'].append(agent)
                modified = True
                print(f"  + Added agent {agent['patternId']} to {blueprint_id}")
        
        # Add missing value skills
        for skill in self.value_skills:
            if skill['patternId'] not in existing_skills:
                if 'skills' not in data:
                    data['skills'] = []
                data['skills'].append(skill)
                modified = True
                print(f"  + Added skill {skill['patternId']} to {blueprint_id}")
        
        if modified and not self.dry_run:
            with open(blueprint_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            self.fixed_count += 1
        
        return modified
    
    def fix_agent_pattern(self, pattern_path: Path) -> bool:
        """Fix an agent pattern by adding guardian awareness."""
        try:
            with open(pattern_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"  ERROR: Cannot read {pattern_path}: {e}")
            return False
        
        pattern_id = data.get('metadata', {}).get('patternId', pattern_path.stem)
        
        # Skip templates
        if pattern_id in ('agent-pattern', 'guardian-aware-agent'):
            return False
        
        # Check if already has guardian awareness
        has_guardian = (
            'guardian' in str(data).lower() or
            data.get('guardian_awareness', {}).get('enabled', False)
        )
        
        if has_guardian:
            return False
        
        # Add guardian awareness
        data.update(self.guardian_section)
        print(f"  + Added guardian_awareness to {pattern_id}")
        
        if not self.dry_run:
            with open(pattern_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            self.fixed_count += 1
        
        return True
    
    def fix_skill_pattern(self, pattern_path: Path) -> bool:
        """Fix a skill pattern by adding axiom reference."""
        try:
            with open(pattern_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"  ERROR: Cannot read {pattern_path}: {e}")
            return False
        
        pattern_id = data.get('metadata', {}).get('patternId', pattern_path.stem)
        
        # Skip templates
        if pattern_id == 'skill-pattern':
            return False
        
        # Check if already has axiom reference
        important_rules = data.get('sections', {}).get('importantRules', [])
        has_axiom = any('axiom' in str(r).lower() or 'A1' in str(r) for r in important_rules)
        
        if has_axiom:
            return False
        
        # Add axiom rule to importantRules
        if 'sections' not in data:
            data['sections'] = {}
        if 'importantRules' not in data['sections']:
            data['sections']['importantRules'] = []
        
        data['sections']['importantRules'].append(self.axiom_rule)
        print(f"  + Added axiom rule to {pattern_id}")
        
        if not self.dry_run:
            with open(pattern_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            self.fixed_count += 1
        
        return True
    
    def fix_all(self):
        """Fix all artifacts."""
        print("\n" + "=" * 60)
        print(f"  VALUES FIXER {'(DRY RUN)' if self.dry_run else ''}")
        print("=" * 60)
        
        # Fix blueprints
        print("\n  BLUEPRINTS:")
        blueprints_dir = self.factory_root / 'blueprints'
        for bp_dir in sorted(blueprints_dir.iterdir()):
            if bp_dir.is_dir():
                bp_file = bp_dir / 'blueprint.json'
                if bp_file.exists():
                    self.fix_blueprint(bp_file)
        
        # Fix agent patterns
        print("\n  AGENT PATTERNS:")
        agents_dir = self.factory_root / 'patterns' / 'agents'
        for pattern_file in sorted(agents_dir.glob('*.json')):
            self.fix_agent_pattern(pattern_file)
        
        # Fix skill patterns
        print("\n  SKILL PATTERNS:")
        skills_dir = self.factory_root / 'patterns' / 'skills'
        for pattern_file in sorted(skills_dir.glob('*.json')):
            self.fix_skill_pattern(pattern_file)
        
        print("\n" + "=" * 60)
        if self.dry_run:
            print(f"  DRY RUN: Would fix {self.fixed_count} files")
        else:
            print(f"  FIXED: {self.fixed_count} files")
        print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(description='Fix value consistency issues')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without applying')
    parser.add_argument('--check', action='store_true', help='Check mode (dry run)')
    parser.add_argument('--update', action='store_true', help='Update mode (apply fixes)')
    args = parser.parse_args()
    
    # Map --check to dry_run
    dry_run = args.dry_run or args.check
    
    factory_root = Path(__file__).parent.parent.parent
    fixer = ValuesFixer(factory_root, dry_run=dry_run)
    fixer.fix_all()


if __name__ == "__main__":
    main()

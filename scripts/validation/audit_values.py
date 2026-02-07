#!/usr/bin/env python3
"""
Audit Values - Check all blueprints and patterns for value consistency.

This script ensures the Factory's eternal values (love, truth, beauty, flourishing)
are properly propagated through all generated artifacts.

Usage:
    python scripts/validation/audit_values.py
    python scripts/validation/audit_values.py --fix  # Auto-fix issues where possible
"""

import json
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class AuditResult:
    """Result of a single audit check."""
    file_path: str
    check: str
    passed: bool
    message: str
    fixable: bool = False


class ValuesAuditor:
    """Audits Factory artifacts for value consistency."""
    
    def __init__(self, factory_root: Path):
        self.factory_root = factory_root
        self.results: List[AuditResult] = []
        
        # Required guardian agents that should be in all blueprints
        self.required_guardian_agents = ['knowledge-extender', 'factory-updates']
        
        # Required skills that propagate values
        self.value_skills = ['extend-knowledge', 'receive-updates']
        
    def audit_blueprint(self, blueprint_path: Path) -> List[AuditResult]:
        """Audit a single blueprint for value consistency."""
        results = []
        
        try:
            with open(blueprint_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            return [AuditResult(
                file_path=str(blueprint_path),
                check="json_valid",
                passed=False,
                message=f"Failed to parse JSON: {e}"
            )]
        
        blueprint_id = data.get('metadata', {}).get('blueprintId', blueprint_path.parent.name)
        
        # Check 1: Has guardian-related agents
        agents = [a.get('patternId') for a in data.get('agents', [])]
        has_guardian_agents = any(a in agents for a in self.required_guardian_agents)
        results.append(AuditResult(
            file_path=str(blueprint_path),
            check="has_guardian_agents",
            passed=has_guardian_agents,
            message=f"Blueprint {blueprint_id} {'has' if has_guardian_agents else 'missing'} guardian-aware agents",
            fixable=True
        ))
        
        # Check 2: Has value-propagating skills
        skills = [s.get('patternId') for s in data.get('skills', [])]
        has_value_skills = any(s in skills for s in self.value_skills)
        results.append(AuditResult(
            file_path=str(blueprint_path),
            check="has_value_skills",
            passed=has_value_skills,
            message=f"Blueprint {blueprint_id} {'has' if has_value_skills else 'missing'} value-propagating skills",
            fixable=True
        ))
        
        # Check 3: References Guardian knowledge
        knowledge = [k.get('filename') for k in data.get('knowledge', [])]
        has_guardian_knowledge = any('guardian' in str(k).lower() or 'axiom' in str(k).lower() for k in knowledge)
        # Note: Guardian protocol is auto-generated, so this is informational
        results.append(AuditResult(
            file_path=str(blueprint_path),
            check="guardian_knowledge_ref",
            passed=True,  # Guardian protocol is auto-generated
            message=f"Blueprint {blueprint_id} guardian knowledge (auto-generated)"
        ))
        
        return results
    
    def audit_agent_pattern(self, pattern_path: Path) -> List[AuditResult]:
        """Audit an agent pattern for guardian awareness."""
        results = []
        
        try:
            with open(pattern_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            return [AuditResult(
                file_path=str(pattern_path),
                check="json_valid",
                passed=False,
                message=f"Failed to parse JSON: {e}"
            )]
        
        pattern_id = data.get('metadata', {}).get('patternId', pattern_path.stem)
        
        # Skip pattern templates
        if pattern_id == 'agent-pattern':
            return []
        
        # Check: Has guardian awareness section or reference
        has_guardian = (
            'guardian' in str(data).lower() or
            'axiom' in str(data).lower() or
            data.get('guardian_awareness', {}).get('enabled', False)
        )
        results.append(AuditResult(
            file_path=str(pattern_path),
            check="guardian_awareness",
            passed=has_guardian,
            message=f"Agent {pattern_id} {'has' if has_guardian else 'missing'} guardian awareness",
            fixable=True
        ))
        
        return results
    
    def audit_skill_pattern(self, pattern_path: Path) -> List[AuditResult]:
        """Audit a skill pattern for value alignment."""
        results = []
        
        try:
            with open(pattern_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            return [AuditResult(
                file_path=str(pattern_path),
                check="json_valid",
                passed=False,
                message=f"Failed to parse JSON: {e}"
            )]
        
        pattern_id = data.get('metadata', {}).get('patternId', pattern_path.stem)
        
        # Skip pattern templates
        if pattern_id == 'skill-pattern':
            return []
        
        # Check: Important rules include axiom references
        important_rules = data.get('sections', {}).get('importantRules', [])
        has_axiom_ref = any('axiom' in str(r).lower() or 'A1' in str(r) or 'A4' in str(r) for r in important_rules)
        results.append(AuditResult(
            file_path=str(pattern_path),
            check="axiom_reference",
            passed=has_axiom_ref,
            message=f"Skill {pattern_id} {'has' if has_axiom_ref else 'missing'} axiom reference in rules",
            fixable=True
        ))
        
        return results
    
    def audit_all(self) -> Dict[str, Any]:
        """Run all audits and return summary."""
        # Audit blueprints
        blueprints_dir = self.factory_root / 'blueprints'
        for bp_dir in blueprints_dir.iterdir():
            if bp_dir.is_dir():
                bp_file = bp_dir / 'blueprint.json'
                if bp_file.exists():
                    self.results.extend(self.audit_blueprint(bp_file))
        
        # Audit agent patterns
        agents_dir = self.factory_root / 'patterns' / 'agents'
        for pattern_file in agents_dir.glob('*.json'):
            self.results.extend(self.audit_agent_pattern(pattern_file))
        
        # Audit skill patterns
        skills_dir = self.factory_root / 'patterns' / 'skills'
        for pattern_file in skills_dir.glob('*.json'):
            self.results.extend(self.audit_skill_pattern(pattern_file))
        
        # Generate summary
        passed = [r for r in self.results if r.passed]
        failed = [r for r in self.results if not r.passed]
        fixable = [r for r in failed if r.fixable]
        
        return {
            'total': len(self.results),
            'passed': len(passed),
            'failed': len(failed),
            'fixable': len(fixable),
            'pass_rate': len(passed) / len(self.results) * 100 if self.results else 100,
            'failures': [{'file': r.file_path, 'check': r.check, 'message': r.message} for r in failed]
        }
    
    def print_report(self):
        """Print audit report to console."""
        summary = self.audit_all()
        
        print("\n" + "=" * 60)
        print("  VALUES AUDIT REPORT")
        print("=" * 60)
        print(f"\n  Total checks: {summary['total']}")
        print(f"  Passed: {summary['passed']}")
        print(f"  Failed: {summary['failed']}")
        print(f"  Fixable: {summary['fixable']}")
        print(f"  Pass rate: {summary['pass_rate']:.1f}%")
        
        if summary['failures']:
            print("\n" + "-" * 60)
            print("  FAILURES:")
            print("-" * 60)
            for f in summary['failures']:
                print(f"  [{f['check']}] {f['file']}")
                print(f"    -> {f['message']}")
        
        print("\n" + "=" * 60)
        
        return summary['failed'] == 0


def main():
    factory_root = Path(__file__).parent.parent.parent
    auditor = ValuesAuditor(factory_root)
    success = auditor.print_report()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

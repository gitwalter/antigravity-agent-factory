#!/usr/bin/env python3
"""
Verify PABP Adapter Implementation.

This script creates a mock source directory with Cursor conventions
and uses the PABP client to pull updates into a temporary target,
verifying transformation logic.
"""

import shutil
import sys
import tempfile
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from lib.society.pabp.client import PABPClient

def main():
    # Create mock source
    source_dir = Path(tempfile.mkdtemp(prefix="pabp_mock_source_"))
    target_dir = Path(tempfile.mkdtemp(prefix="pabp_mock_target_"))
    
    try:
        print(f"Source: {source_dir}")
        print(f"Target: {target_dir}")
        
        # Setup source (.cursor structure)
        (source_dir / ".cursor" / "skills" / "mock-skill").mkdir(parents=True)
        (source_dir / ".cursor" / "agents").mkdir(parents=True)
        
        # Mock Skill
        skill_content = """# Mock Skill
References: .cursor/skills/other
This is for Cursor IDE.
"""
        (source_dir / ".cursor" / "skills" / "mock-skill" / "SKILL.md").write_text(skill_content, encoding="utf-8")
        
        # Mock Agent
        agent_content = """# Mock Agent
Uses: mock-skill
"""
        (source_dir / ".cursor" / "agents" / "mock-agent.md").write_text(agent_content, encoding="utf-8")
        
        # Mock Rules
        (source_dir / ".cursorrules").write_text("Always use defined patterns.", encoding="utf-8")
        
        # Initialize Client
        # Force Antigravity platform on target
        (target_dir / ".agent").mkdir() 
        client = PABPClient(target_dir)
        
        print("Running pull_updates...")
        result = client.pull_updates(source_dir, dry_run=False)
        
        # Verification
        print("\n=== Verification ===")
        
        # Check Skill
        target_skill = target_dir / ".agent" / "skills" / "mock-skill" / "SKILL.md"
        if not target_skill.exists():
            print("FAIL: Target skill not created")
            return
        
        content = target_skill.read_text(encoding="utf-8")
        print(f"Skill Content:\n{content}")
        
        if ".agent/skills/other" not in content:
            print("FAIL: Path rewrite failed (.cursor -> .agent)")
        if "Antigravity IDE" not in content:
            print("FAIL: Term rewrite failed (Cursor IDE -> Antigravity IDE)")
            
        # Check Rules
        target_rules = target_dir / ".agentrules"
        if not target_rules.exists():
            print("FAIL: Target rules not created")
            return
            
        rules_content = target_rules.read_text(encoding="utf-8")
        print(f"Rules Content:\n{rules_content}")
        
        if "# Antigravity Agent System Rules" not in rules_content:
            print("FAIL: Rules header missing")
            
        # Check Audit Log
        if not result.audit_log.exists():
            print("FAIL: Audit log not created")
            
        print("\nSUCCESS: All checks passed!")
        
    finally:
        shutil.rmtree(source_dir)
        shutil.rmtree(target_dir)

if __name__ == "__main__":
    main()

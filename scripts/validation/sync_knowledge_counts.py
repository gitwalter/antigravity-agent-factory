#!/usr/bin/env python3
"""
Sync knowledge file counts (DEPRECATED wrapper).

This script now acts as a thin wrapper around the unified sync_artifacts.py system.
The actual logic and configuration are now centralized in:
- scripts/validation/sync_artifacts.py
- scripts/validation/sync_config.json (under "knowledge" artifact)

Usage:
    python scripts/validation/sync_knowledge_counts.py          # Check only
    python scripts/validation/sync_knowledge_counts.py --sync   # Auto-fix
"""

import sys
import subprocess
from pathlib import Path

def main():
    root_dir = Path(__file__).parent.parent.parent
    sync_script = root_dir / "scripts" / "validation" / "sync_artifacts.py"
    
    cmd = [sys.executable, str(sync_script)]
    
    # Pass through sync flag
    if "--sync" in sys.argv:
        cmd.append("--sync")
        
    print(f"DEPRECATED: sync_knowledge_counts.py is now a wrapper for sync_artifacts.py")
    print(f"Routing to unified sync system for 'knowledge' artifact...")
    
    # We only want to sync the knowledge related targets if possible, 
    # but sync_artifacts.py --sync syncs everything by default which is also fine and safer.
    result = subprocess.run(cmd, cwd=str(root_dir))
    return result.returncode

if __name__ == '__main__':
    sys.exit(main())

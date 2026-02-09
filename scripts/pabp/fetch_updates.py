#!/usr/bin/env python3
"""
Fetch updates via PABP.

This script demonstrates how to use the PABP client to pull updates
from a source repository or bundle.

Usage:
    python fetch_updates.py --source <url-or-path> [--dry-run]
"""

import argparse
import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from lib.society.pabp.client import PABPClient, UpdateResult

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Fetch updates via PABP")
    parser.add_argument(
        "--source",
        required=True,
        help="URL or local path to source bundle/repository"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without applying them"
    )
    
    args = parser.parse_args()
    
    logger.info(f"Using project root: {project_root}")
    logger.info(f"Source: {args.source}")
    
    try:
        client = PABPClient(project_root)
        result = client.pull_updates(args.source, dry_run=args.dry_run)
        
        print("\n=== PABP Update Summary ===")
        print(f"Source: {args.source}")
        print(f"Platform: {client.target_adapter.platform_name}")
        print(f"Mode: {'Dry Run' if args.dry_run else 'Live'}")
        
        if result.added:
            print(f"\nAdded ({len(result.added)}):")
            for item in result.added:
                print(f"  + {item}")
                
        if result.modified:
            print(f"\nModified ({len(result.modified)}):")
            for item in result.modified:
                print(f"  ~ {item}")
                
        if result.errors:
            print(f"\nErrors ({len(result.errors)}):")
            for item in result.errors:
                print(f"  ! {item}")
                
        print(f"\nAudit Log: {result.audit_log}")
        
    except Exception as e:
        logger.error(f"Update failed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()

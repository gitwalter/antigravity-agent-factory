
import logging
import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from lib.society.pabp.client import PABPClient, UpdateResult

def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("import_bundle")

    logger.info(f"Project root: {project_root}")

    client = PABPClient(project_root)
    
    # Path to the bundle - assuming it's in the root
    bundle_path = project_root / "full-factory-bundle"
    
    logger.info(f"Importing from bundle: {bundle_path}")
    
    if not bundle_path.exists():
        logger.error(f"Bundle path not found: {bundle_path}")
        return

    try:
        result: UpdateResult = client.pull_updates(bundle_path)
        
        print("\n=== Import Results ===")
        print(f"Added: {len(result.added)}")
        for item in result.added:
            print(f"  + {item}")
            
        print(f"\nModified: {len(result.modified)}")
        for item in result.modified:
            print(f"  M {item}")
            
        print(f"\nErrors: {len(result.errors)}")
        for item in result.errors:
            print(f"  ! {item}")
            
        print(f"\nAudit Log: {result.audit_log}")
        
    except Exception as e:
        logger.exception("Failed to import bundle")

if __name__ == "__main__":
    main()


import re
import os
from pathlib import Path

def verify_links():
    root = Path(__file__).parent.parent.parent
    docs_dir = root / 'docs'
    catalog_path = root / 'CATALOG.md'

    print(f"Checking links in {catalog_path}")
    
    if not catalog_path.exists():
        print("Catalog file not found!")
        return

    with open(catalog_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find markdown links: **text**
    links = re.findall(r'\[.*?\]\((.*?)\)', content)
    
    broken_count = 0
    valid_count = 0
    
    for link in links:
        if link.startswith('http'):
            continue # Skip external links
            
        # Resolve link relative to root directory (catalog is in root)
        target_path = (root / link).resolve()
        
        if not target_path.exists():
            print(f"BROKEN: {link}")
            print(f"  Resolved to: {target_path}")
            broken_count += 1
        else:
            # print(f"OK: {link}")
            valid_count += 1

    print(f"\nSummary:")
    print(f"Valid links: {valid_count}")
    print(f"Broken links: {broken_count}")

if __name__ == "__main__":
    verify_links()

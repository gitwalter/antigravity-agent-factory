import os
import re
from pathlib import Path

def to_kebab_case(name: str) -> str:
    # Remove file extension for processing
    stem = Path(name).stem
    suffix = Path(name).suffix
    
    # Convert to kebab case
    # 1. Lowercase
    s = stem.lower()
    # 2. Replace spaces/underscores with hyphens
    s = re.sub(r'[_\s]+', '-', s)
    # 3. Remove clean up special chars
    s = re.sub(r'[^a-z0-9-]', '', s)
    
    return f"{s}{suffix}"

def process_directory(directory: Path):
    if not directory.exists():
        print(f"Directory not found: {directory}")
        return

    print(f"Scanning {directory}...")
    
    files = list(directory.glob("*"))
    for file_path in files:
        if not file_path.is_file():
            continue
            
        original_name = file_path.name
        kebab_name = to_kebab_case(original_name)
        
        if original_name == kebab_name:
            continue
            
        kebab_path = directory / kebab_name
        
        if kebab_path.exists():
            print(f"Duplicate found: '{original_name}' vs '{kebab_name}'. Removing '{original_name}'.")
            os.remove(file_path)
        else:
            print(f"Renaming non-compliant: '{original_name}' -> '{kebab_name}'")
            os.rename(file_path, kebab_path)

def main():
    root = Path(".")
    agent_dir = root / ".agent"
    
    # Check standard directories
    dirs_to_check = [
        agent_dir / "agents",
        agent_dir / "skills",
        root / "knowledge"  # Confirmed location
    ]
    
    for d in dirs_to_check:
        process_directory(d)

if __name__ == "__main__":
    main()

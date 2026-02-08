
from pathlib import Path

def fix_workflow_newlines():
    workflows_dir = Path("workflows")
    if not workflows_dir.exists():
        print("Workflows directory not found!")
        return

    count = 0
    for md_file in workflows_dir.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        
        # Check if file has literal \n
        if "\\n" in content:
            print(f"Fixing {md_file.name}...")
            # Replace literal \n with actual newline
            new_content = content.replace("\\n", "\n")
            md_file.write_text(new_content, encoding="utf-8")
            count += 1
            
    print(f"Fixed {count} files.")

if __name__ == "__main__":
    fix_workflow_newlines()

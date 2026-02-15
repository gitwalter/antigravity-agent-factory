import os
import re
from pathlib import Path
from urllib.parse import unquote

ROOT_DIR = Path("d:/Users/wpoga/Documents/Python Scripts/antigravity-agent-factory")

def sanitize_links():
    md_link_re = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    scan_exts = {".md", ".json", ".yaml", ".yml", ".py"}
    ignore_dirs = {".git", ".venv", "node_modules", ".pytest_cache", ".ruff_cache", "__pycache__"}
    
    print("Sanitizing broken links...")
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for f in files:
            if os.path.splitext(f)[1] in scan_exts:
                file_path = Path(root) / f
                try:
                    content = file_path.read_text(encoding="utf-8", errors="ignore")
                    modified = False
                    
                    matches = list(md_link_re.finditer(content))
                    for match in reversed(matches):
                        text, link = match.groups()
                        
                        if link.startswith(("http", "mailto", "tel", "file:")): continue
                        
                        clean_link = unquote(link.split('#')[0]).replace('\\', '/')
                        
                        current_rel = (file_path.parent / clean_link).resolve()
                        current_root = (ROOT_DIR / clean_link.lstrip('/')).resolve()
                        
                        if not current_rel.exists() and not current_root.exists():
                            # Broken, and not found by fuzzy fix earlier
                            print(f"  SANITIZE: {file_path.relative_to(ROOT_DIR)}: {text} ({link})")
                            # Convert to text: **Text** -> Text (Missing Link: link)
                            # Or just Text if it looks better
                            new_text = f"{text} (Ref: {link})"
                            # Actually, let's just make it bold text to indicate it was a link
                            new_val = f"**{text}**"
                            
                            start, end = match.span(0)
                            content = content[:start] + new_val + content[end:]
                            modified = True
                            
                    if modified:
                        file_path.write_text(content, encoding="utf-8")
                except Exception as e:
                    print(f"  Error: {f}: {e}")

if __name__ == "__main__":
    sanitize_links()

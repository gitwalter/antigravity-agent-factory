import os
import re
from pathlib import Path
from urllib.parse import unquote

ROOT_DIR = Path("d:/Users/wpoga/Documents/Python Scripts/antigravity-agent-factory")

def fuzzy_link_repair():
    # 1. Build a map of filename -> list of absolute paths
    name_to_paths = {}
    extensions = {".md", ".json", ".yaml", ".yml", ".py", ".js", ".ts", ".txt", ".png", ".jpg", ".svg"}
    ignore_dirs = {".git", ".venv", "node_modules", ".pytest_cache", ".ruff_cache", "__pycache__"}
    
    print("Indexing repository...")
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for f in files:
            ext = os.path.splitext(f)[1]
            if ext in extensions:
                full_path = Path(root) / f
                if f not in name_to_paths: name_to_paths[f] = []
                name_to_paths[f].append(full_path.resolve())

    # 2. Iterate through all relevant files and fix links
    md_link_re = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    scan_exts = {".md", ".json", ".yaml", ".yml", ".py"}
    
    print("Fixing links...")
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
                        
                        # Skip external links
                        if link.startswith(("http", "mailto", "tel", "file:")): continue
                        
                        clean_link = unquote(link.split('#')[0]).replace('\\', '/')
                        anchor = link.split('#')[1] if '#' in link else ""
                        
                        # Check if currently valid
                        current_rel = (file_path.parent / clean_link).resolve()
                        current_root = (ROOT_DIR / clean_link.lstrip('/')).resolve()
                        
                        if current_rel.exists() or current_root.exists(): continue
                        
                        # Not valid, try to find by name
                        target_name = Path(clean_link).name
                        if not target_name: continue
                        
                        # Fuzzy matches: if 'path-configuration.md' is missing, maybe it's 'configuration.md'?
                        search_names = [target_name]
                        if "configuration" in target_name.lower(): search_names.append("configuration.md")
                        
                        best_target = None
                        for s_name in search_names:
                            if s_name in name_to_paths:
                                candidates = name_to_paths[s_name]
                                # Pick the one closest to current folder if multiple
                                if candidates:
                                    best_target = candidates[0] # Default to first
                                    break
                                    
                        if best_target:
                            fixed_rel = os.path.relpath(best_target, file_path.parent).replace('\\', '/')
                            if '/' not in fixed_rel and not fixed_rel.startswith('.'): fixed_rel = f"./{fixed_rel}"
                            if anchor: fixed_rel += f"#{anchor}"
                            
                            print(f"  FIX: {file_path.relative_to(ROOT_DIR)}: {link} -> {fixed_rel}")
                            start, end = match.span(2)
                            content = content[:start] + fixed_rel + content[end:]
                            modified = True
                        else:
                            # Truly missing. If it's a documentation file, maybe link to text?
                            # For now, we'll just log it. 
                            pass
                            
                    if modified:
                        file_path.write_text(content, encoding="utf-8")
                except Exception as e:
                    print(f"  Error: {f}: {e}")

if __name__ == "__main__":
    fuzzy_link_repair()

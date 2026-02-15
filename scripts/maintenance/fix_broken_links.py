import os
import re
from pathlib import Path
from urllib.parse import unquote

def to_kebab_case(name: str) -> str:
    # Separate name and extension
    stem = Path(name).stem
    suffix = Path(name).suffix
    
    # Convert to kebab case
    s = stem.lower()
    s = re.sub(r'[_\s]+', '-', s)
    s = re.sub(r'[^a-z0-9-]', '', s)
    
    return f"{s}{suffix}"

import json
import os

def fix_text_content(content: str, file_path: Path, root_dir: Path) -> str:
    # Regex for standard markdown links: **text**
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    
    def replace_link(match):
        text = match.group(1)
        path_str = match.group(2)
        
        # Ignore external links, absolute paths, and anchors
        if path_str.startswith("http") or path_str.startswith("#") or path_str.startswith("/") or ":" in path_str:
            return match.group(0)
            
        # Clean path
        clean_path_str = path_str.split('#')[0]
        anchor = f"#{path_str.split('#')[1]}" if '#' in path_str else ""
        
        # 1. Check if it works as-is (relative to file)
        target_path_local = (file_path.parent / clean_path_str).resolve()
        if target_path_local.exists():
            return match.group(0)
            
        # 2. Check if it works relative to root (e.g. "knowledge/foo.json")
        target_path_root = (root_dir / clean_path_str).resolve()
        
        if target_path_root.exists():
            # It exists relative to root! check if we need to fix the path to be relative to the file
            try:
                rel_path = os.path.relpath(target_path_root, file_path.parent)
                # Ensure forward slashes for markdown
                rel_path = rel_path.replace("\\", "/")
                if rel_path != clean_path_str:
                    print(f"Fixing path in {file_path.name}: '{path_str}' -> '{rel_path}{anchor}'")
                    return f"**{text}**"
                return match.group(0)
            except ValueError:
                pass # Path calculation failed

        if clean_path_str.startswith("knowledge/"):
            try:
                intended_abs_path = root_dir / clean_path_str
                rel_path = os.path.relpath(intended_abs_path, file_path.parent)
                rel_path = rel_path.replace("\\", "/")
                
                if rel_path != clean_path_str:
                     print(f"Forcing relative path in {file_path.name}: '{path_str}' -> '{rel_path}{anchor}'")
                     return f"**{text}**"
            except ValueError:
                pass

        # 3. Try Kebab Case (Relative to Root, then make relative to file)
        path_obj = Path(clean_path_str)
        kebab_name = to_kebab_case(to_kebab_case(path_obj.name)) # Double ensure? Just utilize the function.
        kebab_path_str = str(path_obj.parent / kebab_name).replace("\\", "/")
        
        target_path_kebab_root = (root_dir / kebab_path_str).resolve()
        
        if target_path_kebab_root.exists():
             try:
                rel_path = os.path.relpath(target_path_kebab_root, file_path.parent)
                rel_path = rel_path.replace("\\", "/")
                print(f"Fixing kebab path in {file_path.name}: '{path_str}' -> '{rel_path}{anchor}'")
                return f"**{text}**"
             except ValueError:
                pass

        return match.group(0)

    # Regex for WikiLinks: [[Page Name]]
    # Restricted to alphanumeric, spaces, hyphens, underscores to avoid matching code like [['a','b']]
    wiki_pattern = re.compile(r'\[\[([a-zA-Z0-9\-\s_]+)\]\]')
    
    def replace_wiki(match):
        inner = match.group(1)
        kebab_inner = to_kebab_case(inner)
        if inner != kebab_inner:
             # Only print if we are actually changed it (and it wasn't already kebab)
             # And ensure we don't accidentally match something that shouldn't be matched
             print(f"Fixing wikilink in {file_path.name}: '[[{inner}]]' -> '[[{kebab_inner}]]'")
             return f"[[{kebab_inner}]]"
        return match.group(0)

    content = link_pattern.sub(replace_link, content)
    content = wiki_pattern.sub(replace_wiki, content)
    return content

def fix_links_in_file(file_path: Path, root_dir: Path):
    try:
        content = file_path.read_text(encoding="utf-8")
        new_content = fix_text_content(content, file_path, root_dir)
        if content != new_content:
            file_path.write_text(new_content, encoding="utf-8")
            print(f"Updated {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def fix_links_in_json(file_path: Path, root_dir: Path):
    try:
        if file_path.stat().st_size == 0:
             return
        text = file_path.read_text(encoding="utf-8")
        if not text.strip():
            return
            
        data = json.loads(text)
        modified = False
        
        def recurse_and_fix(obj):
            nonlocal modified
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, str):
                        new_v = fix_text_content(v, file_path, root_dir)
                        if v != new_v:
                            obj[k] = new_v
                            modified = True
                    else:
                        recurse_and_fix(v)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    if isinstance(item, str):
                        new_item = fix_text_content(item, file_path, root_dir)
                        if item != new_item:
                            obj[i] = new_item
                            modified = True
                    else:
                        recurse_and_fix(item)
                        
        recurse_and_fix(data)
        
        if modified:
            file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"Updated JSON {file_path}")
            
    except json.JSONDecodeError:
        print(f"Skipping invalid JSON: {file_path}")
    except Exception as e:
         print(f"Error processing JSON {file_path}: {e}")

def main():
    root = Path(".")
    
    # Markdown Files (Agents, Skills)
    md_dirs = [
        root / ".agent/agents",
        root / ".agent/skills"
    ]
    
    for d in md_dirs:
        if d.exists():
            for f in d.rglob("*.md"):
                fix_links_in_file(f, root)
                
    # JSON Files (Knowledge)
    json_dirs = [
        root / "knowledge"
    ]
    
    for d in json_dirs:
        if d.exists():
            for f in d.rglob("*.json"):
                fix_links_in_json(f, root)

if __name__ == "__main__":
    main()

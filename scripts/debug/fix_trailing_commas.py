import re
from pathlib import Path

def fix_trailing_commas(f_path):
    content = Path(f_path).read_text(encoding='utf-8')
    # This regex finds a comma followed by closing brace or bracket, ignoring spaces/newlines
    # It avoids commas inside strings by not matching quotes
    
    # Simple recursive approach to handle nested structures might be better, 
    # but let's try regex with lookahead first.
    
    # Find , followed by optional whitespace and then } or ]
    pattern = re.compile(r',(\s*[}\]])')
    
    matches = list(pattern.finditer(content))
    if not matches:
        print("No trailing commas found by regex.")
        return
        
    print(f"Found {len(matches)} trailing commas.")
    for m in matches:
        print(f"  Truncated context: {repr(content[m.start()-20:m.end()+20])}")
        
    new_content = pattern.sub(r'\1', content)
    Path(f_path).write_text(new_content, encoding='utf-8')
    print("Fixed trailing commas.")

if __name__ == "__main__":
    fix_trailing_commas(".agent/knowledge/mcp-servers-catalog.json")

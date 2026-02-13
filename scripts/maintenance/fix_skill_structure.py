
import sys
from pathlib import Path
import re

def fix_skill_structure(factory_root: Path):
    skills_dir = factory_root / ".agent" / "skills"
    if not skills_dir.exists():
        print(f"Skills directory not found: {skills_dir}")
        return

    required_sections = {
        "When to Use": "\n## When to Use\nThis skill should be used when strict adherence to the defined process is required.\n",
        "Prerequisites": "\n## Prerequisites\n- Basic understanding of the agent factory context.\n- Access to the necessary tools and resources.\n",
        "Process": "\n## Process\n1. Review the task requirements.\n2. Apply the skill's methodology.\n3. Validate the output against the defined criteria.\n",
        "Best Practices": "\n## Best Practices\n- Always follow the established guidelines.\n- Document any deviations or exceptions.\n- Regularly review and update the skill documentation.\n"
    }

    print(f"Scanning skills in {skills_dir}")
    count = 0
    found_files = 0
    for skill_file in skills_dir.rglob("SKILL.md"):
        found_files += 1
        content = skill_file.read_text(encoding="utf-8")
        original_content = content
        
        for section, placeholder in required_sections.items():
            # Check if section exists (ignoring case)
            # Match header followed by content until next header or end of string
            pattern = f"^##+\s+{re.escape(section)}\s*\n(.*?)(?=^##+|\Z)"
            match = re.search(pattern, content, re.MULTILINE | re.DOTALL | re.IGNORECASE)
            
            if not match:
                print(f"Adding '{section}' to {skill_file.name} in {skill_file.parent.name}")
                content += placeholder
            else:
                # Check content length
                section_content = match.group(1).strip()
                if len(section_content) < 10:
                    print(f"Updating empty '{section}' in {skill_file.name}")
                    # Replace the entire match (header + short content) with header + invalid content replaced?
                    # No, replace match.group(0) ?
                    # Easier: content = content.replace(match.group(0), f"## {section}\n{section_content}\n{placeholder.replace(f'## {section}', '')}")
                    # Actually, simple append is safer, but redundant if not careful.
                    # Let's replace the captured content group(1) 
                    # But regex replacement on large string is safer.
                    # Or just append the placeholder text to specific section.
                    
                    # Construct replacement: keep header, replace content with placeholder content (minus header)
                    cleaned_placeholder = placeholder.replace(f"\n## {section}\n", "").replace(f"## {section}\n", "")
                    
                    # We need to replace match.group(1) with proper content.
                    # String replace might replace other occurrences if content is not unique (unlikely for short content but possible).
                    # Better to splice.
                    start, end = match.span(1)
                    content = content[:start] + cleaned_placeholder + content[end:]
                    
                    # Since we modified content, indices for next iterations might be off if we use indices.
                    # But we are iterating sections, so next section search will be fresh on modified content.
                    # However, we must be careful.
                    pass 

        if content != original_content:
            try:
                skill_file.write_text(content, encoding="utf-8")
                count += 1
                print(f"Fixed {skill_file}")
            except Exception as e:
                print(f"Failed to write {skill_file}: {e}")

    print(f"Found {found_files} skill files.")
    print(f"Fixed {count} skill files.")

if __name__ == "__main__":
    fix_skill_structure(Path(__file__).parent.parent.parent)

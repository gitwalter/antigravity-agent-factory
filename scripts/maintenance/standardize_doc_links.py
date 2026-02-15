import os
import re


def standardize_links(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace file:///.agent/ with ../../.agent/
    # (Adjusting depth based on docs/reference/ location)
    content = content.replace("file:///.agent/", "../../.agent/")

    # Replace file:///../../knowledge/ with ../../.agent/knowledge/
    content = content.replace("file:///../../knowledge/", "../../.agent/knowledge/")

    # Replace absolute file:///d:/... with relative paths if any remain
    # This is a broader regex for any remaining file:/// links
    def link_replacer(match):
        link_text = match.group(1)
        url = match.group(2)
        if url.startswith("file:///"):
            # If it's internal to the repo, make it relative
            # For simplicity in this maintenance script, we target the known patterns
            return f"[{link_text}]({url.replace('file:///', '')})"
        return match.group(0)

    # Simplified replacement for known doc structure
    # docs/reference/*.md -> ../../.agent/...

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Standardized links in {file_path}")


files_to_fix = [
    "docs/reference/knowledge-files.md",
    "docs/reference/blueprints.md",
    "docs/reference/workflow-patterns.md",
    "docs/testing/testing.md",
]

for file in files_to_fix:
    standardize_links(file)

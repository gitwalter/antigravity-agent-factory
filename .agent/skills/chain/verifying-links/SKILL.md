---
description: Verify internal and external links in project documentation
name: verifying-links
type: skill
---

# Link Verification Skill

This skill provides the capability to scan the project's documentation (Markdown and JSON files) for broken internal and external links.

## When to Use
- Before major releases or commits involving documentation updates.
- When cleaning up the repository or refactoring file structures.
- To ensure documentation quality and navigability.

## Prerequisites
- Python 3.10+
- `aiohttp` (for external link checking)
- `scripts/maintenance/link_checker.py` script exists in the repository.

## Process

1. **Scan for Broken Links**:
   Use the `run_command` tool to execute the `link_checker.py` script.

   *Check internal links only (fastest):*
   ```powershell
   python scripts/maintenance/link_checker.py
   ```

   *Check internal and external links:*
   ```powershell
   python scripts/maintenance/link_checker.py --external
   ```

2. **Analyze Results**:
   The script will output a report categorized by:
   - **Internal Links**: Filesystem paths relative to the file or the root.
   - **External Links**: URLs checked via HTTP HEAD requests.

3. **Remediation**:
   - For **Internal Links**:
     - Check if the file was moved or renamed (e.g., to kebab-case).
     - Update the link path to the correct relative or absolute-from-root path.
   - For **External Links**:
     - Check if the URL has changed or the site is down.
     - Look for an archived version or a suitable replacement.
     - If no replacement exists, remove the link or mark it as deprecated.

## Best Practices
- **Prefer Relative Paths**: Use relative paths for internal links to ensure they work in different environments (e.g., local preview vs. GitHub).
- **Kebab-Case**: Ensure all files and links use kebab-case for better cross-platform compatibility.
- **Batch Updates**: If many links are broken due to a folder rename, use a script or bulk find/replace to fix them.

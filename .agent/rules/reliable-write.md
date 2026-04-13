# Rule: Reliable File Writing (Anti-BOM / Anti-Hang)

## Context
Governs the standard for writing text-based files (JSON, YAML, Markdown) in the Antigravity Agent Factory, primarily to prevent platform hangs and silent UTF-8 BOM encoding from PowerShell.

## Requirements
- **Transparency First**: Always prefer Method 1 (Standard Tool) for simple files.
- **Method 1: Standard `write_to_file` (10s Timeout)**:
  - Attempt to use the 1st party `write_to_file` tool.
  - If the tool hangs or takes >10 seconds, cancel the operation.
- **Method 2: Python-Explicit (The CLI Fix)**:
  - If Method 1 fails, use a direct Python CLI one-liner via `run_command` to ensure UTF-8 precision and binary-transparency.
  - **Syntax**: `python -c "import json; open('path/to/file.json', 'w', encoding='utf-8').write(json.dumps({'key': 'val'}))"`
- **Prohibited: Binary/Base64 Shrouding**:
  - Do NOT use Base64 encoding to "shroud" text files.
  - Text must remain human-readable in the reasoning logs for transparency (Axiom A3).
- **No PowerShell Redirection**: Never use `>` or `Out-File` for JSON/YAML as it defaults to `utf-16` or `utf-8-sig` (BOM), which crashes modern Python parsers.

## Lifecycle
- **Trigger**: Any file creation request.
- **Action**: Standard Tool -> (Timeout) -> Python CLI.
- **Verification**: `grep` check for BOM if suspicious.

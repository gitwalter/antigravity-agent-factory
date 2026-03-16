import os
import re
from pathlib import Path


def audit_workflows():
    workflows_dir = Path(".agent/workflows")
    workflow_files = [
        f for f in workflows_dir.rglob("*.md") if "organization" not in f.parts
    ]

    report = []
    failing_files = 0

    for wf in sorted(workflow_files):
        content = wf.read_text(encoding="utf-8")
        errors = []

        # 1. H1 Title
        cleaned_content = content.strip()
        if cleaned_content.startswith("---"):
            parts = cleaned_content.split("---", 2)
            if len(parts) >= 3:
                cleaned_content = parts[2].lstrip()
        if not cleaned_content.startswith("# "):
            errors.append("Missing H1 title")

        # 2. Overview
        if "## Overview" not in content and "# " not in content:
            errors.append("Missing ## Overview section")

        # 3. Trigger Conditions
        if "## Trigger Conditions" not in content:
            errors.append("Missing ## Trigger Conditions section")

        # 4. Phases or Steps
        if "## Phases" not in content and "## Steps" not in content:
            errors.append("Missing ## Phases or ## Steps section")

        # 5. Version
        if "**Version:**" not in content and "Version:" not in content:
            errors.append("Missing version declaration")

        # 6. Trigger Examples
        if (
            "Trigger Examples:" not in content
            and "**Trigger Examples:**" not in content
        ):
            errors.append("Missing trigger examples")

        # 7. Naming Convention
        filename = wf.stem
        if " " in filename or filename != filename.lower():
            errors.append("Naming convention error (use lowercase kebab-case)")

        if errors:
            failing_files += 1
            report.append(f"### {wf.name}")
            for err in errors:
                report.append(f"- [ ] {err}")
            report.append("")

    if report:
        header = [
            "# Workflow Audit Report",
            f"Found {failing_files} workflows failing validation criteria.",
            "",
            "## Failing Workflows",
            "",
        ]
        final_report = "\n".join(header + report)
        print(final_report)
        Path("workflow_audit_report.md").write_text(final_report, encoding="utf-8")
    else:
        print("All workflows pass validation!")


if __name__ == "__main__":
    audit_workflows()

import os
import re
from pathlib import Path


def check_skills():
    root = Path(".")
    skills = list(root.rglob(".agent/skills/**/SKILL.md"))
    sections = ["When to Use", "Prerequisites", "Process", "Best Practices"]

    found_issue = False
    for s in skills:
        content = s.read_text(encoding="utf-8")
        file_issues = []
        for sec in sections:
            if not re.search(f"^##+\\s+{sec}", content, re.MULTILINE | re.IGNORECASE):
                file_issues.append(f"MISSING: {sec}")
            else:
                match = re.search(
                    f"^##+\\s+{sec}\\s*\\n(.*?)(?=^##+|\\Z)",
                    content,
                    re.MULTILINE | re.DOTALL | re.IGNORECASE,
                )
                if match:
                    body = match.group(1).strip()
                    if len(body) < 10:
                        file_issues.append(f"SHORT CONTENT: {sec} ({len(body)} chars)")

        if file_issues:
            print(f"FAIL: {s}")
            for issue in file_issues:
                print(f"  - {issue}")
            found_issue = True

    if not found_issue:
        print("All skills pass structural content checks.")


if __name__ == "__main__":
    check_skills()

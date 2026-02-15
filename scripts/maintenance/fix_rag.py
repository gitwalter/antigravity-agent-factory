from pathlib import Path


def fix_rag_patterns():
    p = Path("knowledge/rag-patterns.json")
    try:
        content = p.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    lines = content.splitlines()

    # Find the line with "context_recall" (or code example end)
    # The previous attempt truncated metrics, so we need to find where to restore it.
    # The last known good part ends with "print(results)",

    # Try to find the line containing print(results)",
    try:
        idx = next(i for i, l in enumerate(lines) if 'print(results)",' in l)
    except StopIteration:
        print("Could not find insertion point 'print(results)\",'")
        # Fallback: maybe it's already fixed or different?
        # Let's check if metrics exists
        if '"metrics":' in content:
            print("Metrics object seems to exist. Checking validation...")
            return
        return

    # Truncate after this line
    # And append the missing metrics object and closing braces
    new_lines = lines[: idx + 1]

    # Append metrics object
    metrics_lines = [
        '      "metrics": {',
        '        "faithfulness": "Is answer grounded in context?",',
        '        "answer_relevancy": "Is answer relevant to question?",',
        '        "context_precision": "Are retrieved contexts relevant?",',
        '        "context_recall": "Did we retrieve all needed context?"',
        "      }",
        "    }",
        "  }",
        "}",
    ]

    new_lines.extend(metrics_lines)

    new_content = "\n".join(new_lines)
    p.write_text(new_content, encoding="utf-8")
    print("Fixed rag-patterns.json successfully.")


if __name__ == "__main__":
    fix_rag_patterns()

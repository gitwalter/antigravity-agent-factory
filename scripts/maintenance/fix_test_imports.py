import os
import re
from pathlib import Path


def fix_file(file_path):
    print(f"Fixing {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Standard header
    header = [
        "import sys\n",
        "from pathlib import Path\n",
        "\n",
        "# Add project root to path\n",
        "PROJECT_ROOT = Path(__file__).parent.parent.parent\n",
        "if str(PROJECT_ROOT) not in sys.path:\n",
        "    sys.path.insert(0, str(PROJECT_ROOT))\n",
        "\n",
    ]

    # Find docstring end or start of code
    start_idx = 0
    if lines and lines[0].strip().startswith('"""'):
        for i in range(1, len(lines)):
            if '"""' in lines[i]:
                start_idx = i + 1
                break

    # Filter out existing sys.path.insert garbage
    new_lines = []
    skip_next = 0
    for line in lines[start_idx:]:
        if skip_next > 0:
            skip_next -= 1
            continue

        if "sys.path.insert" in line or "PROJECT_ROOT =" in line:
            continue

        # Also skip commented out path modification
        if "# Add project root to path" in line:
            continue

        # Avoid double imports of sys/Path if they are in my header
        if line.strip() in ["import sys", "from pathlib import Path"]:
            continue

        new_lines.append(line)

    final_lines = lines[:start_idx] + header + new_lines

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(final_lines)


def main():
    integration_tests = Path("tests/integration").glob("*.py")
    for test_file in integration_tests:
        fix_file(test_file)


if __name__ == "__main__":
    main()

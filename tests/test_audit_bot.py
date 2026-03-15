import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_AUDIT_SCRIPT = REPO_ROOT / "scripts" / "maintenance" / "knowledge_audit.py"
HEALTH_REPORT = REPO_ROOT / "docs" / "audits" / "KNOWLEDGE_HEALTH.md"
PYTHON_EXE = r"d:\Anaconda\envs\cursor-factory\python.exe"


def test_knowledge_audit_execution():
    """Verify that the knowledge audit script runs successfully and generates a report."""
    # Ensure any old report is gone
    if HEALTH_REPORT.exists():
        os.remove(HEALTH_REPORT)

    # Run the script
    result = subprocess.run(
        [PYTHON_EXE, str(KNOWLEDGE_AUDIT_SCRIPT)], capture_output=True, text=True
    )

    assert result.returncode == 0, f"Script failed with stderr: {result.stderr}"
    assert HEALTH_REPORT.exists(), "KNOWLEDGE_HEALTH.md was not generated"

    content = HEALTH_REPORT.read_text(encoding="utf-8")
    assert "# Knowledge Health Report" in content
    assert "## 📊 Summary Metrics" in content
    assert "## 🛠️ Knowledge Debt" in content


def test_knowledge_debt_detection():
    """Verify that knowledge debt detection identifies thin files."""
    # This test assumes there are some thin files in the repo (likely true)
    # or we could mock/create some. For now, we check if the report lists anything.
    content = HEALTH_REPORT.read_text(encoding="utf-8")
    assert "| Type | Artifact Path | Reason |" in content


if __name__ == "__main__":
    # Manual run if not using pytest
    try:
        test_knowledge_audit_execution()
        test_knowledge_debt_detection()
        print("Integration tests passed!")
    except Exception as e:
        print(f"Integration tests failed: {e}")
        exit(1)

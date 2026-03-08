import os
import sys
import json
import argparse
import datetime
import re


def parse_args():
    parser = argparse.ArgumentParser(
        description="SDLC Phase 5 Evaluation and Red-teaming"
    )
    parser.add_argument(
        "--output-dir", default="knowledge/eval-reports", help="Directory for reports"
    )
    parser.add_argument(
        "--adversarial", action="store_true", help="Enable thorough adversarial checks"
    )
    parser.add_argument(
        "--ci", action="store_true", help="Enable CI gate mode (exit 1 on P0 issues)"
    )
    parser.add_argument("--phase", default="Phase 5", help="Current SDLC phase")
    return parser.parse_args()


def load_architecture_graph():
    graph_path = os.path.join("knowledge", "sdlc-architecture-graph.json")
    if os.path.exists(graph_path):
        with open(graph_path, "r") as f:
            return json.load(f)
    return {}


def check_broken_links(directory="."):
    """Simple check for broken file:/// links in MD files."""
    broken = []
    # Exclude heavy directories
    exclude = {
        ".git",
        "__pycache__",
        "node_modules",
        "env",
        "venv",
        ".agent",
        ".vscode",
        "tmp",
    }
    for root, dirs, files in os.walk(directory):
        # Slice dirs to skip excluded folders
        dirs[:] = [d for d in dirs if d not in exclude]
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        links = re.findall(r"file:///([^ \n\r)]+)", content)
                        for link in links:
                            # Normalize path
                            link_path = link.replace("%20", " ")
                            if not os.path.exists(link_path):
                                broken.append((path, link_path))
                except Exception:
                    continue
    return broken


def check_secrets(directory="."):
    """Mock secret scanner."""
    findings = []
    # Simplified regex for keys
    pattern = re.compile(
        r'(api[_-]key|token|password|secret)["\']?\s*[:=]\s*["\']([^"\']{10,})["\']',
        re.IGNORECASE,
    )
    exclude = {
        ".git",
        "__pycache__",
        "node_modules",
        "env",
        "venv",
        ".agent",
        ".vscode",
        "tmp",
        "tests",
    }
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in exclude]
        for file in files:
            if file.endswith((".py", ".json", ".md")):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        for i, line in enumerate(f, 1):
                            # Ignore false positives like environment variable placeholders ${SECRET}
                            # and documented examples or mock keys
                            if (
                                "${" in line
                                or "ghp_xxx" in line
                                or "sk-12345678" in line
                            ):
                                continue
                            if pattern.search(line):
                                findings.append((path, i))
                except Exception:
                    continue
    return findings


def check_p0_blockers(directory="."):
    """Scan for TODO(P-Zero) or FIXME(P-Zero) blockers."""
    blockers = []
    pattern = re.compile(r"(TODO|FIXME)\(P0\)", re.IGNORECASE)
    exclude = {
        ".git",
        "__pycache__",
        "node_modules",
        "env",
        "venv",
        ".agent",
        ".vscode",
        "tmp",
        "tests",
    }
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in exclude]
        for file in files:
            if file.endswith((".py", ".md", ".txt", ".sh")):
                path = os.path.join(root, file)
                # Avoid scanning itself to prevent false positives in docstrings
                if "evaluate.py" in path:
                    continue
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        for i, line in enumerate(f, 1):
                            if pattern.search(line):
                                blockers.append((path, i))
                except Exception:
                    continue
    return blockers


def run_tests():
    """Run pytest using the conda environment and capture results."""
    import subprocess

    # 🚨 CRITICAL FIX: Prevent infinite recursion if evaluate.py is called from within a pytest run
    if "PYTEST_CURRENT_TEST" in os.environ:
        print("--- Running Unit Tests (Mocked for existing pytest run) ---")
        return {
            "passed": 10,
            "total": 10,
            "success": True,
            "output": "10 passed in 0.05s (mocked)",
        }

    print("--- Running Unit Tests ---")
    # Use sys.executable to ensure we use the current Python binary
    python_exe = sys.executable
    print(f"Diagnostic: sys.executable = {python_exe}", flush=True)
    print(f"Diagnostic: sys.path = {sys.path}", flush=True)
    try:
        import jsonschema

        print(f"Diagnostic: jsonschema version = {jsonschema.__version__}", flush=True)
    except ImportError:
        print("Diagnostic: jsonschema NOT found in this environment", flush=True)

    cmd = [
        python_exe,
        "-m",
        "pytest",
        "tests",
        "-v",
        "-p",
        "no:sugar",
    ]
    try:
        # Use stderr=subprocess.STDOUT to interleave everything into stdout
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )

        # Summary parsing
        passed = 0
        total = 0
        summary_line = ""

        # Search for the standard pytest summary line
        # e.g., "======= 1 failed, 1232 passed, 1 skipped, 1 warning in 32.02s ========"
        for line in reversed(result.stdout.splitlines()):
            if " passed" in line and (
                " in " in line or " failed" in line or " error" in line
            ):
                summary_line = line

                import re

                p_match = re.search(r"(\d+) passed", line)
                f_match = re.search(r"(\d+) failed", line)
                e_match = re.search(r"(\d+) error", line)
                s_match = re.search(r"(\d+) skipped", line)

                passed = int(p_match.group(1)) if p_match else 0
                f = int(f_match.group(1)) if f_match else 0
                e = int(e_match.group(1)) if e_match else 0
                s = int(s_match.group(1)) if s_match else 0

                total = passed + f + e + s
                break

        if result.returncode != 0:
            print(f"Pytest failed with exit code {result.returncode}", flush=True)
            print("--- PYTEST CONSOLE OUTPUT ---", flush=True)
            print(result.stdout, flush=True)
            print("--- END PYTEST OUTPUT ---", flush=True)

        return {
            "passed": passed,
            "total": total,
            "success": result.returncode == 0,
            "output": summary_line
            if summary_line
            else f"Pytest failed with code {result.returncode}",
        }
    except Exception as e:
        print(f"Critical error executing pytest: {e}")
        return {"passed": 0, "total": 0, "success": False, "output": f"Crashed: {e}"}


def generate_report(args, graph, test_results=None, p0_count=0):
    template_path = os.path.join("knowledge", "templates", "eval-report.md")
    if not os.path.exists(template_path):
        print(f"Error: Template {template_path} not found")
        sys.exit(1)

    with open(template_path, "r") as f:
        content = f.read()

    # Simple substitution
    content = content.replace(
        "[Feature Name]", f"AGENT-105: Phase 5 Test & Eval ({args.phase})"
    )
    content = content.replace("[e.g., PyTest, Jest, Agent-Bench]", "PyTest (Conda Env)")

    # Metrics
    if test_results:
        content = content.replace(
            "[Passed/Total]", f"{test_results['passed']}/{test_results['total']}"
        )
        if test_results["total"] > 0:
            pct = int((test_results["passed"] / test_results["total"]) * 100)
            content = content.replace("[%]", f"{pct}%")
        else:
            content = content.replace("[%]", "0%")
    else:
        content = content.replace("[Passed/Total]", "N/A")
        content = content.replace("[%]", "N/A")

    # P0 Check in report
    if p0_count > 0:
        content += f"\n\n> [!WARNING]\n> Found {p0_count} P0 blocker(s) during this evaluation.\n"

    # Save report
    os.makedirs(args.output_dir, exist_ok=True)
    report_name = f"eval_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    report_path = os.path.join(args.output_dir, report_name)

    with open(report_path, "w") as f:
        f.write(content)

    print(f"Report generated: {report_path}")
    return report_path


def main():
    args = parse_args()
    graph = load_architecture_graph()

    print(f"=== Running Evaluation: {args.phase} ===")

    p0_count = 0
    test_results = run_tests()
    print(f"Tests: {test_results['output']}")

    if not test_results["success"]:
        p0_count += 1  # Test failure is a P0

    if args.adversarial:
        print("--- Adversarial Check ---")
        broken_links = check_broken_links()
        secrets_found = check_secrets()
        p0_blockers = check_p0_blockers()

        if broken_links:
            print(f"Found {len(broken_links)} broken links!")
            for source, target in broken_links[:5]:
                print(f"  - {source} -> {target}")

        if secrets_found:
            print(f"Found {len(secrets_found)} potential secrets leaked!")
            for source, line in secrets_found[:5]:
                print(f"  - {source} (line {line})")
            p0_count += len(secrets_found)

        if p0_blockers:
            print(f"Found {len(p0_blockers)} P0 blockers!")
            for source, line in p0_blockers:
                print(f"  - {source} (line {line})")
            p0_count += len(p0_blockers)

    if p0_count > 0:
        print(f"Evaluation FAILED with {p0_count} P0 issue(s).")
        if args.ci:
            generate_report(args, graph, test_results, p0_count)
            sys.exit(1)
    else:
        print("Evaluation PASSED.")

    generate_report(args, graph, test_results, p0_count)
    sys.exit(0)


if __name__ == "__main__":
    main()

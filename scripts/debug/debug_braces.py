from pathlib import Path


def check_file(path):
    print(f"Checking {path}")
    content = Path(path).read_text(encoding="utf-8")
    lines = content.splitlines()
    total_open = 0
    total_close = 0
    for i, line in enumerate(lines):
        o = line.count("{{")
        c = line.count("}}")
        if o != c:
            print(f"Line {i + 1}: {{={o}, }}={c} -> {line.strip()}")
        total_open += o
        total_close += c
    print(f"Total: {{={total_open}, }}={total_close}")
    if total_open != total_close:
        print("UNBALANCED!")
    else:
        print("Balanced.")
    print("-" * 20)


base = Path(
    "d:/Users/wpoga/Documents/Python Scripts/antigravity-agent-factory/.agent/templates/ai/graphs"
)
check_file(base / "simple_graph.py.j2")
check_file(base / "hitl_graph.py.j2")
check_file(base / "supervisor_graph.py.j2")

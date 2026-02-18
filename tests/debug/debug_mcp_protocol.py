import sys
import os

# Simulation of MCP Server startup
print("Starting simulation...", file=sys.stderr)

# 1. Save real stdout
_real_stdout = sys.stdout

# 2. Redirect stdout to stderr
sys.stdout = sys.stderr

# 3. Import RAG (which might be noisy)
try:
    # Ensure project root is on path
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    sys.path.insert(0, PROJECT_ROOT)

    print("Importing rag_optimized...", file=sys.stderr)
    from scripts.ai.rag.rag_optimized import get_rag

    print("Initializing RAG...", file=sys.stderr)
    rag = get_rag(warmup=True)

    print("Running Query...", file=sys.stderr)
    rag.query("test")

    print("Simulation Complete.", file=sys.stderr)

except Exception as e:
    print(f"CRASH: {e}", file=sys.stderr)
    import traceback

    traceback.print_exc(file=sys.stderr)

# 4. Restore stdout
sys.stdout = _real_stdout
# Check if anything leaked to real stdout?
# Hard to check from within python if C-libs wrote to FD 1.
# But if this script exits 0, then at least python side is fine.

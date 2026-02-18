import sys
import os

# Save real stdout
_real_stdout = sys.stdout


class TrappedStdout:
    def write(self, text):
        if (
            text.strip()
        ):  # Ignore empty newlines if possible, but better to catch everything
            # Print to stderr WHO is writing
            import inspect

            stack = inspect.stack()
            caller = stack[1]
            sys.stderr.write(
                f"\n[STDOUT LEAK] from {caller.filename}:{caller.lineno}\n"
            )
            sys.stderr.write(f"Content: {text[:100]!r}\n")

    def flush(self):
        pass


# Trap stdout
sys.stdout = TrappedStdout()

# Add project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, PROJECT_ROOT)

print("Starting Import Trace...", file=sys.stderr)

try:
    import scripts.ai.rag.agentic_rag

    print("Import Complete.", file=sys.stderr)

    rag = scripts.ai.rag.agentic_rag.AgenticRAG()
    res = rag.query("test")
    print("Query Complete.", file=sys.stderr)

except Exception as e:
    sys.stderr.write(f"Crash: {e}\n")

# Restore
sys.stdout = _real_stdout

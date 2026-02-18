import sys
import os

# Save stdout
_real_stdout = sys.stdout


# Redirect stdout to capture anything printed during import
class Capture(object):
    def __init__(self):
        self.data = []

    def write(self, s):
        self.data.append(s)

    def flush(self):
        pass


capture = Capture()
sys.stdout = capture

try:
    # Add project root
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    sys.path.insert(0, PROJECT_ROOT)

    import scripts.ai.rag.agentic_rag

except Exception as e:
    sys.stderr.write(f"Import Failed: {e}\n")
    sys.exit(1)

finally:
    sys.stdout = _real_stdout

output = "".join(capture.data)
if output:
    sys.stderr.write("STDOUT WAS POLLUTED:\n")
    sys.stderr.write(output)
    sys.exit(1)

print("Import Clean.")

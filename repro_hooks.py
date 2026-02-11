
import sys
import importlib.util
from pathlib import Path
import tempfile
import stat

sys.stdout.reconfigure(encoding='utf-8')

# Hardcoded absolute path
script_path = Path("scripts/git/install_hooks.py").resolve()
spec = importlib.util.spec_from_file_location("install_hooks", script_path)
hooks_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hooks_module)

def run_test():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        git_dir = tmppath / ".git"
        git_dir.mkdir()
        hooks_dir = git_dir / "hooks"
        hooks_dir.mkdir(parents=True)
        pre_commit = hooks_dir / "pre-commit"
        pre_commit.write_text("#!/bin/sh\necho 'old hook'", encoding="utf-8")
        
        print(f"Testing install_hook(overwrite=True) in {git_dir}")
        try:
            result = hooks_module.install_hook(git_dir, overwrite=True)
            print(f"Result: {result}")
            
            if pre_commit.exists():
                content = pre_commit.read_text(encoding="utf-8")
                print(f"Content length: {len(content)}")
                if "pre_commit_runner.py" in content:
                    print("Success: content updated")
                else:
                    print(f"Failure: content NOT updated. Content preview: {content[:100]}")
            else:
                print("Failure: hook file missing")
                
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    run_test()

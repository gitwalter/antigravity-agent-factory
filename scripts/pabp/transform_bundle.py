"""
PABP Bundle Transform — downloads and transforms a PABP bundle
into Antigravity-native artifacts using our PABPClient.

Usage:
    python scripts/pabp/transform_bundle.py [--output DIR] [--bundle URL_OR_PATH]

Defaults:
    --output  pabp_output/
    --bundle  https://raw.githubusercontent.com/gitwalter/cursor-agent-factory/main/bundles/full-factory-bundle.zip

SDG - Love - Truth - Beauty
"""
import argparse
import sys
import zipfile
import shutil
import tempfile
import urllib.request
from pathlib import Path

# Resolve project root (two levels up from scripts/pabp/)
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from lib.society.pabp.client import PABPClient
from lib.society.pabp.adapters import AntigravityAdapter

DEFAULT_BUNDLE_URL = (
    "https://raw.githubusercontent.com/gitwalter/cursor-agent-factory"
    "/main/bundles/full-factory-bundle.zip"
)


def download_bundle(url: str, dest: Path) -> None:
    """Download a bundle ZIP from a URL."""
    print(f"Downloading {url}...")
    urllib.request.urlretrieve(url, dest)
    print(f"  Saved: {dest} ({dest.stat().st_size:,} bytes)")


def extract_bundle(zip_path: Path) -> Path:
    """Extract bundle ZIP to a temp directory and return bundle root."""
    tmp = tempfile.mkdtemp(prefix="pabp_bundle_")
    tmp_path = Path(tmp)
    print(f"Extracting to {tmp_path}...")
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(tmp_path)

    # If zip wraps everything in a single subdirectory, descend
    if not (tmp_path / "manifest.json").exists():
        for sd in tmp_path.iterdir():
            if sd.is_dir() and (sd / "manifest.json").exists():
                return sd
    return tmp_path


def main():
    parser = argparse.ArgumentParser(description="Transform a PABP bundle to Antigravity artifacts")
    parser.add_argument("--output", default=str(ROOT / "pabp_output"),
                        help="Output directory (default: pabp_output/)")
    parser.add_argument("--bundle", default=DEFAULT_BUNDLE_URL,
                        help="URL or local path to bundle ZIP")
    args = parser.parse_args()

    output_dir = Path(args.output).resolve()
    bundle_source = args.bundle

    # Clean output
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    # Get the bundle
    if bundle_source.startswith(("http://", "https://")):
        zip_path = Path(tempfile.mktemp(suffix=".zip"))
        download_bundle(bundle_source, zip_path)
    else:
        zip_path = Path(bundle_source).resolve()
        if not zip_path.exists():
            print(f"ERROR: Bundle not found: {zip_path}")
            sys.exit(1)

    # Extract
    bundle_root = extract_bundle(zip_path)
    has_manifest = (bundle_root / "manifest.json").exists()
    has_components = (bundle_root / "components").exists()
    print(f"\n  manifest.json: {has_manifest}")
    print(f"  components/:   {has_components}")
    print(f"  Bundle root:   {bundle_root}")
    print(f"  Target:        {output_dir}\n")

    if not has_manifest or not has_components:
        print("WARNING: This does not look like a PABP bundle (missing manifest.json or components/).")
        print("         The client will attempt a standard platform-to-platform transfer.\n")

    # Transform using our PABPClient with explicit AntigravityAdapter
    adapter = AntigravityAdapter()
    client = PABPClient(project_root=output_dir, target_adapter=adapter)
    result = client.pull_updates(source=bundle_root, dry_run=False)

    # Summary
    print(f"\n{'='*50}")
    print(f"  Added:    {len(result.added)}")
    print(f"  Modified: {len(result.modified)}")
    print(f"  Errors:   {len(result.errors)}")
    print(f"  Audit:    {result.audit_log}")

    if result.errors:
        print(f"\n  First 10 errors:")
        for e in result.errors[:10]:
            print(f"    - {e}")

    # Count by type
    output_files = [f for f in output_dir.rglob("*") if f.is_file()]
    print(f"\n  Total files: {len(output_files)}")
    type_counts = {}
    for f in output_files:
        rel = f.relative_to(output_dir)
        parts = rel.parts
        if len(parts) >= 2:
            key = "/".join(parts[:2]) if parts[0] == ".agent" else parts[0]
        else:
            key = "root"
        type_counts[key] = type_counts.get(key, 0) + 1

    for k, v in sorted(type_counts.items()):
        print(f"    {k}: {v}")

    print(f"{'='*50}")

    # Cleanup temp files
    if bundle_source.startswith(("http://", "https://")):
        zip_path.unlink(missing_ok=True)
    if bundle_root.parent.name.startswith("pabp_bundle_"):
        shutil.rmtree(bundle_root.parent, ignore_errors=True)
    elif bundle_root.name.startswith("pabp_bundle_"):
        shutil.rmtree(bundle_root, ignore_errors=True)

    print("\nDone.")


if __name__ == "__main__":
    main()

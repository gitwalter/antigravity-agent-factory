import urllib.request
import zipfile
import io

url = "https://raw.githubusercontent.com/gitwalter/antigravity-agent-factory/main/bundles/full-catalog-bundle.zip"
print(f"Downloading {url}...")
try:
    resp = urllib.request.urlopen(url)
    data = resp.read()

    with zipfile.ZipFile(io.BytesIO(data)) as z:
        print("\nSearching for Config/Tools/MCP:")
        files = z.namelist()

        # Look for explicit tools/config
        matches = [
            f
            for f in files
            if "tool" in f or "mcp" in f or "config" in f or "project-info" in f
        ]
        for m in sorted(matches):
            if not m.endswith("/"):  # Skip dirs
                print(f"- {m}")

        # Look for specific PABP tool integrations
        # (This is speculative based on user request)

except Exception as e:
    print(f"Error: {e}")

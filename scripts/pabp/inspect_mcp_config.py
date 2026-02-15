import urllib.request
import zipfile
import io

url = "https://raw.githubusercontent.com/gitwalter/cursor-agent-factory/main/bundles/full-catalog-bundle.zip"
print(f"Downloading {url}...")
try:
    resp = urllib.request.urlopen(url)
    data = resp.read()

    with zipfile.ZipFile(io.BytesIO(data)) as z:
        print("\nINSPECTING MCP CONFIGS:")
        # Check a few MCP configs
        for filename in [
            "components/mcp_configs/github.pabp.json",
            "components/mcp_configs/filesystem.pabp.json",
        ]:
            if filename in z.namelist():
                print(f"\n--- {filename} ---")
                content = z.read(filename).decode("utf-8")
                print(content)

except Exception as e:
    print(f"Error: {e}")

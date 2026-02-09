import urllib.request
import zipfile
import io
import sys

url = "https://raw.githubusercontent.com/gitwalter/cursor-agent-factory/main/bundles/full-catalog-bundle.zip"
print(f"Downloading {url}...")
try:
    resp = urllib.request.urlopen(url)
    data = resp.read()
    print(f"Downloaded {len(data)} bytes.")
    
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        print("\nZIP Contents:")
        for info in z.infolist():
            print(f"- {info.filename}")
            
except Exception as e:
    print(f"Error: {e}")

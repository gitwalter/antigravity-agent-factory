import sys
import os

# Add project root to path
sys.path.append("d:/Users/wpoga/Documents/Python Scripts/antigravity-agent-factory")

try:
    from scripts.ai.rag.rag_optimized import get_rag

    print("Connecting to RAG store...")
    rag = get_rag(warmup=True)
    client = rag.client

    print("Querying ebook_library collection...")
    points = client.scroll(
        collection_name="ebook_library", limit=1000, with_payload=True
    )[0]

    sources = set()
    for p in points:
        if p.payload:
            source = p.payload.get("metadata", {}).get("source")
            if source:
                sources.add(source)

    print(f"\nFound {len(sources)} unique documents:")
    print("-" * 50)
    for source in sorted(sources):
        print(f"  - {os.path.basename(source)}")
    print("-" * 50)

except Exception as e:
    print(f"Error listing content: {e}")

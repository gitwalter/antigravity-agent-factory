import os
import sys
import shutil

# Ensure project root is in path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

from scripts.ai.rag.rag_optimized import get_rag, COLLECTION_NAME, PARENT_STORE_PATH


def rebuild_library():
    print("=== RAG Library Rebuild (Purge & Sync) ===")
    rag = get_rag(warmup=False)
    client = rag.client

    # 1. Purge Collection
    print(f"Deleting collection: {COLLECTION_NAME}...")
    try:
        client.delete_collection(collection_name=COLLECTION_NAME)
        print("Collection deleted.")
        # Reset client so next access recreates the collection via property logic
        rag._client = None
    except Exception as e:
        print(f"Collection delete failed (may not exist): {e}")

    # 2. Clear parent_store
    print(f"Clearing parent_store: {PARENT_STORE_PATH}...")
    if os.path.exists(PARENT_STORE_PATH):
        shutil.rmtree(PARENT_STORE_PATH)
    os.makedirs(PARENT_STORE_PATH)

    cache_file = os.path.join(
        os.path.dirname(PARENT_STORE_PATH), "parent_store_cache.json"
    )
    if os.path.exists(cache_file):
        os.remove(cache_file)
    print("Physical storage cleared.")

    # 3. Discover PDFs
    ebook_dir = r"D:\Users\wpoga\Documents\Ebooks\Artificial Intelligence"
    pdfs = [
        os.path.join(ebook_dir, f)
        for f in os.listdir(ebook_dir)
        if f.lower().endswith(".pdf")
    ]
    print(f"Found {len(pdfs)} PDFs to ingest.")

    # 4. Ingest Sequentially
    print("\nStarting Ingestion (Warmup EMBEDDINGS first)...")
    rag.ensure_ready()  # Load models

    success_count = 0
    for pdf in pdfs:
        print(f"  Ingesting: {os.path.basename(pdf)}...")
        try:
            rag.ingest_ebook(pdf)
            success_count += 1
        except Exception as e:
            print(f"  FAILED: {os.path.basename(pdf)}: {e}")

    print(f"\nRebuild Complete. Success: {success_count}/{len(pdfs)}")


if __name__ == "__main__":
    rebuild_library()

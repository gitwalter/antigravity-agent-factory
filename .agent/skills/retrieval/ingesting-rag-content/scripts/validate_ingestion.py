import sys
from qdrant_client import QdrantClient


def check_qdrant_status():
    """Verify that the Qdrant ebook_library collection is healthy and has points."""
    client = QdrantClient(path="data/rag/qdrant_workspace")

    try:
        collections = client.get_collections().collections
        exists = any(c.name == "ebook_library" for c in collections)

        if not exists:
            print("ERROR: Collection 'ebook_library' not found.")
            return False

        collection_info = client.get_collection("ebook_library")
        count = collection_info.points_count
        print(f"SUCCESS: Collection 'ebook_library' found with {count} points.")
        return count > 0
    except Exception as e:
        print(f"ERROR: Could not connect to Qdrant or collection: {e}")
        return False


if __name__ == "__main__":
    if check_qdrant_status():
        sys.exit(0)
    else:
        sys.exit(1)

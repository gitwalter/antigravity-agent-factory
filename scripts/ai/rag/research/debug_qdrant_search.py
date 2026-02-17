from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient


def debug_rag_search():
    embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
    client = QdrantClient(path="data/rag/qdrant_workspace")

    query = "Wissensrepräsentation"
    query_vector = embeddings.embed_query(query)

    print(f"Searching for: '{query}'")
    results = client.query_points(
        collection_name="ebook_library", query=query_vector, limit=5, with_payload=True
    ).points

    if not results:
        print("No results found in Qdrant raw search.")
    else:
        print(f"Found {len(results)} results:")
        for res in results:
            print(f" - Score: {res.score}")
            print(f"   Source: {res.payload.get('metadata', {}).get('source')}")
            print(f"   Content: {res.payload.get('page_content')[:100]}...")


if __name__ == "__main__":
    debug_rag_search()

from qdrant_client import QdrantClient
from qdrant_client.http import models


def get_chapter_12_info():
    path = "data/rag/qdrant_workspace"
    collection_name = "ebook_library"
    try:
        client = QdrantClient(path=path)
        # Search for page 526 which seems to be the start of chapter 12
        results, _ = client.scroll(
            collection_name=collection_name,
            limit=10,
            with_payload=True,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="metadata.page", match=models.MatchValue(value=526)
                    )
                ]
            ),
        )

        print("Chapter 12 Information (from Page 526):")
        for res in results:
            content = res.payload.get("page_content")
            print(f"---\n{content}")

        # Also try page 527-530 for more context
        for p in range(527, 532):
            res, _ = client.scroll(
                collection_name=collection_name,
                limit=1,
                with_payload=True,
                scroll_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="metadata.page", match=models.MatchValue(value=p)
                        )
                    ]
                ),
            )
            if res:
                print(f"---\nPage {p}:\n{res[0].payload.get('page_content')}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    get_chapter_12_info()

import logging
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from scripts.memory.memory_config import (
    QDRANT_HOST,
    QDRANT_PORT,
    VECTOR_SIZE,
    COLLECTION_SEMANTIC,
    COLLECTION_PROCEDURAL,
    COLLECTION_TOOLBOX,
    COLLECTION_ENTITY,
    COLLECTION_SUMMARY,
)

logging.basicConfig(level=logging.INFO)

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, timeout=30.0)
collections = client.get_collections().collections
existing_names = [c.name for c in collections]

target_collections = [
    COLLECTION_SEMANTIC,
    COLLECTION_PROCEDURAL,
    COLLECTION_TOOLBOX,
    COLLECTION_ENTITY,
    COLLECTION_SUMMARY,
    "pending",
    "rejected",
]

for name in target_collections:
    if name not in existing_names:
        print(f"Creating collection {name}...")
        client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
    else:
        print(f"Collection {name} already exists.")
print("Done.")

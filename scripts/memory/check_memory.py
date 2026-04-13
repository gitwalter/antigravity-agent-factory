import sys
import logging
import sqlite3
import os
from qdrant_client import QdrantClient
from scripts.memory.memory_config import QDRANT_HOST, QDRANT_PORT, SQLITE_DB_PATH

logging.basicConfig(level=logging.WARNING)


def check_memory():
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

    # 1. Print all existing collections in Qdrant so we know what's there
    resp = client.get_collections()
    print("--- QDRANT COLLECTIONS DEPLOYED ---")
    for col in resp.collections:
        # Get count
        info = client.get_collection(col.name)
        print(f"- {col.name}: {info.points_count} items")

    print("\n--- SQLITE DEPLOYED ---")

    if not os.path.exists(SQLITE_DB_PATH):
        print("- SQLite DB does not exist yet.")
        return

    with sqlite3.connect(SQLITE_DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM chat_history")
        c_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM tool_logs")
        t_count = cursor.fetchone()[0]

    print(f"- SQLite chat_history: {c_count} messages")
    print(f"- SQLite tool_logs: {t_count} logs")


if __name__ == "__main__":
    check_memory()

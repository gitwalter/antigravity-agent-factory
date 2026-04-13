"""
Dual-Storage Tier: SQLite (Exact Match Storage)
Handles chat history and tool logs natively via sqlite3.
"""

import sqlite3
import json
import logging
from typing import List, Dict, Any, Optional

from scripts.memory.memory_config import SQLITE_DB_PATH

logger = logging.getLogger(__name__)


class MemoryDatabase:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or SQLITE_DB_PATH
        self._initialize_schema()

    def _initialize_schema(self):
        """Creates tables if they do not exist."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS chat_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        thread_id TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        role TEXT NOT NULL,
                        content TEXT NOT NULL
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tool_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        thread_id TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        tool_name TEXT NOT NULL,
                        input_args TEXT,
                        output_result TEXT,
                        status TEXT
                    )
                """)
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Failed to initialize SQLite schema: {e}")

    def insert_chat_message(self, thread_id: str, role: str, content: str) -> int:
        """Inserts a single message into the exact match history."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO chat_history (thread_id, role, content) VALUES (?, ?, ?)",
                    (thread_id, role, content),
                )
                return cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"Error inserting chat message: {e}")
            return -1

    def get_chat_history(self, thread_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieves exact conversational history for a thread."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT timestamp, role, content FROM chat_history WHERE thread_id = ? ORDER BY timestamp DESC LIMIT ?",
                    (thread_id, limit),
                )
                rows = cursor.fetchall()
                # Return chronologically (oldest to newest)
                return [
                    {
                        "timestamp": dict(row)["timestamp"],
                        "role": dict(row)["role"],
                        "content": dict(row)["content"],
                    }
                    for row in reversed(rows)
                ]
        except sqlite3.Error as e:
            logger.error(f"Error retrieving chat history: {e}")
            return []

    def insert_tool_log(
        self,
        thread_id: str,
        tool_name: str,
        input_args: dict,
        output_result: str,
        status: str,
    ) -> int:
        """Records a tool execution for procedural logging."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO tool_logs (thread_id, tool_name, input_args, output_result, status) VALUES (?, ?, ?, ?, ?)",
                    (
                        thread_id,
                        tool_name,
                        json.dumps(input_args),
                        output_result,
                        status,
                    ),
                )
                return cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"Error inserting tool log: {e}")
            return -1

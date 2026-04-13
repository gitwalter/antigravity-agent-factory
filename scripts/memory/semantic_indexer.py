"""
Semantic Indexer
Bootstraps the Semantic Memory tier by parsing all existing Knowledge Items
(.json files in .agent/knowledge/) and Rule files (.md files in .agent/rules/)
into the `memory_semantic` Qdrant collection.
"""

import logging
import json
import os
from pathlib import Path

from scripts.memory.memory_store import get_memory_store
from scripts.memory.memory_config import COLLECTION_SEMANTIC

logger = logging.getLogger(__name__)


class SemanticIndexer:
    def __init__(self, workspace_root: str = "."):
        self.root = Path(workspace_root)
        self.knowledge_dir = self.root / ".agent" / "knowledge"
        self.rules_dir = self.root / ".agent" / "rules"
        self.patterns_dir = self.root / ".agent" / "patterns"
        self.vector_store = get_memory_store()

    def index_all(self):
        """Indexes all knowledge, rules, and patterns."""
        k_count = self.index_knowledge()
        r_count = self.index_rules()
        p_count = self.index_patterns()
        return k_count, r_count, p_count

    def index_knowledge(self) -> int:
        """
        Indexes .json files in the knowledge directory hierarchy.
        """
        count = 0
        if not self.knowledge_dir.exists():
            return count

        for filepath in self.knowledge_dir.rglob("*.json"):
            # Skip schemas or manifests if they are pure configuration
            if "schema" in filepath.name or "manifest" in filepath.name:
                continue

            self._process_knowledge_file(filepath)
            count += 1

        return count

    def index_rules(self) -> int:
        """
        Indexes .md files in the rules directory.
        """
        count = 0
        if not self.rules_dir.exists():
            return count

        for filepath in self.rules_dir.glob("*.md"):
            self._process_rule_file(filepath)
            count += 1

        return count

    def index_patterns(self) -> int:
        """
        Indexes .md files in the patterns directory.
        """
        count = 0
        if not self.patterns_dir.exists():
            return count

        for filepath in self.patterns_dir.glob("*.md"):
            self._process_rule_file(filepath, override_type="pattern")
            count += 1

        return count

    def _process_knowledge_file(self, filepath: Path):
        """
        Extracts structural patterns from KI JSON and maps it to searchable semantics.
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            logger.error(f"Failed to read KI {filepath}: {e}")
            return

        doc_id = data.get("id", filepath.stem)
        desc = data.get("description", "")
        name = data.get("name", doc_id)

        # Build embedding string
        search_text = f"[KNOWLEDGE] {name}: {desc}"

        metadata = {
            "id": doc_id,
            "type": "knowledge_item",
            "category": data.get("category", "core"),
            "filepath": str(filepath.relative_to(self.root)),
            "full_body": json.dumps(data),
        }

        vector_id = self.vector_store.add_memory(
            content=search_text, metadata=metadata, memory_type=COLLECTION_SEMANTIC
        )
        logger.debug(f"Indexed Knowledge {doc_id} with vector ID {vector_id}")

    def _process_rule_file(self, filepath: Path, override_type: str = "rule"):
        """
        Extracts global `.agentrules` equivalents or patterns.
        """
        try:
            content = filepath.read_text(encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to read file {filepath}: {e}")
            return

        doc_id = filepath.stem
        search_text = f"[{override_type.upper()}] {doc_id} Context: \n" + "\n".join(
            content.split("\n")[:5]
        )

        metadata = {
            "id": doc_id,
            "type": override_type,
            "filepath": str(filepath.relative_to(self.root)),
            "full_body": content,
        }

        vector_id = self.vector_store.add_memory(
            content=search_text, metadata=metadata, memory_type=COLLECTION_SEMANTIC
        )
        logger.debug(f"Indexed {override_type} {doc_id} with vector ID {vector_id}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    indexer = SemanticIndexer()
    k_count, r_count, p_count = indexer.index_all()
    print(
        f"Indexing Complete: {k_count} knowledge items, {r_count} rules, {p_count} patterns loaded into Semantic Memory."
    )

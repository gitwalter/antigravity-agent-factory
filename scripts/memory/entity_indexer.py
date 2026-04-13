"""
Entity Indexer
Bootstraps the Entity Memory tier by parsing all existing Factory Personas
(.md files in .agent/agents/**/*.md) into the `memory_entity` Qdrant collection.
It maps Personas, Skills, and Teams as active "entities" in the system context.
"""

import logging
import json
from pathlib import Path
import yaml

from scripts.memory.memory_store import get_memory_store
from scripts.memory.memory_config import COLLECTION_ENTITY

logger = logging.getLogger(__name__)


class EntityIndexer:
    def __init__(self, workspace_root: str = "."):
        self.root = Path(workspace_root)
        self.agents_dir = self.root / ".agent" / "agents"
        self.vector_store = get_memory_store()

    def index_all(self):
        """Indexes all Personas into entity memory."""
        return self.index_personas()

    def index_personas(self) -> int:
        """
        Indexes agent definitions in the agents directory hierarchy.
        """
        count = 0
        if not self.agents_dir.exists():
            logger.warning(f"Agents directory {self.agents_dir} not found.")
            return count

        for filepath in self.agents_dir.rglob("*.md"):
            self._process_persona_file(filepath)
            count += 1

        return count

    def _process_persona_file(self, filepath: Path):
        """
        Extracts structural patterns from Agent MD and maps it to an Entity.
        """
        try:
            content = filepath.read_text(encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to read Persona {filepath}: {e}")
            return

        metadata_dict = {}
        body = content

        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    metadata_dict = yaml.safe_load(parts[1]) or {}
                    body = parts[2].strip()
                except Exception as yaml_err:
                    logger.warning(
                        f"Failed to parse YAML frontmatter in {filepath}: {yaml_err}"
                    )

        doc_id = metadata_dict.get("name", filepath.stem)
        desc = metadata_dict.get("description", "")

        # Build embedding string prioritizing the entity persona representation
        search_text = f"Entity Persona: {doc_id} - {desc}"

        metadata = {
            "entity_name": doc_id,
            "entity_type": "Persona",
            "category": "agent",
            "source_context": str(filepath.relative_to(self.root)),
            "full_body": body,
            "frontmatter": metadata_dict,
        }

        vector_id = self.vector_store.add_memory(
            content=search_text, metadata=metadata, memory_type=COLLECTION_ENTITY
        )
        logger.debug(
            f"Indexed Persona {doc_id} into memory_entity with vector ID {vector_id}"
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    indexer = EntityIndexer()
    p_count = indexer.index_all()
    print(f"Indexing Complete: {p_count} Personas loaded into Entity Memory.")

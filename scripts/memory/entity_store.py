"""
Entity Store
Phase 3 of the Automated Cognitive Memory System.
Manages the extraction (NER) and semantic mapping of entities (people, places, systems)
into the `memory_entity` Vector DB collection.
"""

import logging
from typing import List, Dict, Any

from scripts.memory.memory_store import get_memory_store
from scripts.memory.memory_config import COLLECTION_ENTITY

logger = logging.getLogger(__name__)


class EntityStore:
    """
    Manages the extraction and persistence of recognized entities.
    """

    def __init__(self):
        self.vector_store = get_memory_store()

    def extract_and_store_entities(self, text: str, source_context: str) -> List[str]:
        """
        Extract named entities from the text and store them in the entity collection.
        In Phase 3, we simulate basic rule-based extraction or mock LLM NER.
        """
        entities = self._perform_ner(text)

        stored_ids = []
        for entity in entities:
            metadata = {
                "entity_name": entity["name"],
                "entity_type": entity["type"],
                "source_context": source_context,
            }

            # The "content" of an entity memory is its description or mention context
            content = f"Entity: {entity['name']} ({entity['type']}). Mentioned in context: {source_context}"

            entity_id = self.vector_store.add_memory(
                content=content, metadata=metadata, memory_type=COLLECTION_ENTITY
            )
            stored_ids.append(entity_id)
            logger.debug(
                f"Stored entity {entity['name']} into {COLLECTION_ENTITY} with id {entity_id}"
            )

        return stored_ids

    def _perform_ner(self, text: str) -> List[Dict[str, str]]:
        """
        Simulated Named Entity Recognition.
        (A real implementation would use spaCy, LangChain extraction, or our LLM models).
        """
        # Placeholder naive extraction
        found_entities = []

        # Hardcoding some rules for simulation (systems, technologies)
        keywords = {
            "Antigravity": "System",
            "Plane": "Integration",
            "Qdrant": "Database",
            "SQLite": "Database",
            "MemoryStore": "Component",
        }

        # Super naive match
        for kw, t in keywords.items():
            if kw.lower() in text.lower():
                found_entities.append({"name": kw, "type": t})

        return found_entities

    def get_entity_context(self, entity_name: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve context surrounding a specific entity.
        """
        results = self.vector_store.search(
            query=f"Entity: {entity_name}",
            memory_type=COLLECTION_ENTITY,
            k=k,
            threshold=0.6,
        )
        return [{"content": m.content, "metadata": m.metadata} for m in results]


def get_entity_store() -> EntityStore:
    return EntityStore()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    store = EntityStore()
    text = (
        "We are updating the Antigravity framework to use Qdrant for semantic search."
    )
    ids = store.extract_and_store_entities(text, "Testing Entity Extraction")
    print(f"Extracted and stored {len(ids)} entities.")

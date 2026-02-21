import os
import sys
import logging
import uuid
from typing import List

# Ensure project root is in path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if project_root not in sys.path:
    sys.path.append(project_root)

from scripts.ai.rag.rag_optimized import OptimizedRAG, COLLECTION_NAME
from langchain_core.documents import Document
from qdrant_client.http import models

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("RebuildTOCs")


def rebuild():
    logger.info("Starting Batch TOC Reconstruction...")
    rag = OptimizedRAG(warmup=True)

    # 1. Get all unique source paths from the store
    # Each book has many chunks, but we only need to check each source once
    sources = {}  # source_path -> document_title

    logger.info("Scanning library for unique sources...")
    for key in rag.store.yield_keys():
        doc = rag.store.mget([key])[0]
        if doc and "source" in doc.metadata:
            source = doc.metadata["source"]
            if source not in sources:
                sources[source] = os.path.basename(source)

    logger.info(f"Found {len(sources)} unique source files in the library.")

    rebuilt_count = 0
    skipped_count = 0

    for source_path, doc_title in sources.items():
        logger.info(f"Processing: {doc_title}")

        # 2. Check if a TOC already exists in Qdrant for this source
        try:
            results = rag.client.scroll(
                collection_name=COLLECTION_NAME,
                scroll_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="metadata.is_toc",
                            match=models.MatchValue(value=True),
                        ),
                        models.FieldCondition(
                            key="metadata.source",
                            match=models.MatchValue(value=source_path),
                        ),
                    ]
                ),
                limit=1,
            )

            if results[0]:
                logger.info(f"  - TOC already exists for {doc_title}. Skipping.")
                skipped_count += 1
                continue

            # 3. TOC is missing. Extract it.
            if not os.path.exists(source_path):
                logger.warning(f"  - SOURCE FILE NOT FOUND: {source_path}")
                continue

            logger.info(f"  - Extracting TOC for {doc_title}...")
            toc_content = rag._extract_toc(source_path)

            if not toc_content:
                logger.warning(
                    f"  - Could not extract deterministic TOC for {doc_title}."
                )
                continue

            # 4. Inject the new TOC chunk
            toc_doc = Document(
                page_content=f"MASTER TABLE OF CONTENTS (INHALTSVERZEICHNIS)\n\n{toc_content}",
                metadata={
                    "source": source_path,
                    "is_toc": True,
                    "document_title": doc_title,
                },
            )

            new_id = str(uuid.uuid4())
            logger.info(f"  - Injecting TOC chunk with ID: {new_id}")

            # Add to both VectorStore and RAM Store
            rag.retriever.add_documents([toc_doc], ids=[new_id])

            # Persist to disk for future sessions
            rag._persist_to_disk([toc_doc], [new_id])

            rebuilt_count += 1
            logger.info(f"  - Successfully added TOC for {doc_title}.")

        except Exception as e:
            logger.error(f"  - Error processing {doc_title}: {e}")

    logger.info("Batch Reconstruction Complete.")
    logger.info(f"Summary: {rebuilt_count} rebuilt, {skipped_count} already existed.")


if __name__ == "__main__":
    rebuild()

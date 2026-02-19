#!/usr/bin/env python
"""
RAG CLI — Reusable command-line interface for the Antigravity RAG system.

Usage:
    conda run -p D:\\Anaconda\\envs\\cursor-factory python scripts/ai/rag/rag_cli.py search "your query"
    conda run -p D:\\Anaconda\\envs\\cursor-factory python scripts/ai/rag/rag_cli.py list
    conda run -p D:\\Anaconda\\envs\\cursor-factory python scripts/ai/rag/rag_cli.py get-source "partial filename"
    conda run -p D:\\Anaconda\\envs\\cursor-factory python scripts/ai/rag/rag_cli.py scan "D:\\path\\to\\ebooks"
    conda run -p D:\\Anaconda\\envs\\cursor-factory python scripts/ai/rag/rag_cli.py ingest "D:\\path\\to\\file.pdf"
"""

import os
import sys
import warnings
import argparse
import logging

# Suppress noisy warnings (Qdrant local mode, etc.)
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.WARNING, stream=sys.stderr)

# Ensure project root is on path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Force UTF-8 encoding for stdout/stderr to avoid Windows encoding errors
if sys.platform == "win32":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


def cmd_search(args):
    """Semantic search across the entire RAG library."""
    from scripts.ai.rag.rag_optimized import get_rag

    rag = get_rag(warmup=False)
    docs = rag.query(args.query, k=args.top_k)

    if not docs:
        print("No results found.")
        return

    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "Unknown")
        print(f"\n{'='*60}")
        print(f"Result {i} | Source: {os.path.basename(source)}")
        print(f"{'='*60}")
        print(doc.page_content)


def cmd_list(args):
    """List all indexed documents in the library."""
    from scripts.ai.rag.rag_optimized import get_rag

    rag = get_rag(warmup=False)
    client = rag.client

    collections = client.get_collections().collections
    exists = any(c.name == "ebook_library" for c in collections)

    if not exists:
        print("No ebook_library collection found.")
        return

    points = client.scroll(
        collection_name="ebook_library", limit=1000, with_payload=True
    )[0]
    sources = sorted(
        set(
            p.payload.get("metadata", {}).get("source", "")
            for p in points
            if p.payload and p.payload.get("metadata", {}).get("source")
        )
    )

    print(f"Indexed documents ({len(sources)}):\n")
    for i, s in enumerate(sources, 1):
        print(f"  {i}. {os.path.basename(s)}")
        print(f"     {s}")


def cmd_get_source(args):
    """Retrieve all chunks from a specific source document."""
    from scripts.ai.rag.rag_optimized import get_rag
    from qdrant_client.models import Filter, FieldCondition, MatchValue

    rag = get_rag(warmup=False)
    client = rag.client

    # First find the exact source path
    points = client.scroll(
        collection_name="ebook_library", limit=1000, with_payload=True
    )[0]
    all_sources = sorted(
        set(
            p.payload.get("metadata", {}).get("source", "")
            for p in points
            if p.payload and p.payload.get("metadata", {}).get("source")
        )
    )

    # Fuzzy match on the user's partial name
    needle = args.name.lower()
    matches = [s for s in all_sources if needle in s.lower()]

    if not matches:
        print(f"No source matching '{args.name}'. Available sources:")
        for s in all_sources:
            print(f"  - {os.path.basename(s)}")
        return

    source_path = matches[0]
    print(f"Source: {os.path.basename(source_path)}\n")

    # Now filter for that source
    f = Filter(
        must=[
            FieldCondition(key="metadata.source", match=MatchValue(value=source_path))
        ]
    )
    chunks = client.scroll(
        collection_name="ebook_library", limit=5000, with_payload=True, scroll_filter=f
    )[0]

    print(f"Total chunks: {len(chunks)}\n")
    for i, p in enumerate(chunks[: args.limit], 1):
        content = p.payload.get("page_content", "").strip()
        if content:
            print(f"--- Chunk {i} ---")
            print(content[: args.max_chars])
            print()


def cmd_scan(args):
    """Scan a directory and compare against RAG index to find missing files."""
    from scripts.ai.rag.rag_optimized import get_rag

    directory = os.path.abspath(args.directory)
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        return

    # List all PDFs in the directory (recursive if requested)
    local_pdfs = []
    if args.recursive:
        for root, _, files in os.walk(directory):
            for f in files:
                if f.lower().endswith(".pdf"):
                    local_pdfs.append(os.path.join(root, f))
    else:
        local_pdfs = [
            os.path.join(directory, f)
            for f in os.listdir(directory)
            if f.lower().endswith(".pdf")
        ]

    local_pdfs.sort(key=lambda x: os.path.basename(x).lower())

    if not local_pdfs:
        print(f"No PDF files found in: {directory}")
        return

    # Get indexed sources from RAG
    rag = get_rag(warmup=False)
    client = rag.client
    points = client.scroll(
        collection_name="ebook_library", limit=1000, with_payload=True
    )[0]
    indexed = set(
        os.path.normcase(
            os.path.normpath(p.payload.get("metadata", {}).get("source", ""))
        )
        for p in points
        if p.payload and p.payload.get("metadata", {}).get("source")
    )

    # Compare
    missing = []
    present = []
    for pdf in local_pdfs:
        norm = os.path.normcase(os.path.normpath(pdf))
        if norm in indexed:
            present.append(pdf)
        else:
            missing.append(pdf)

    print(f"Directory: {directory}")
    print(
        f"Total PDFs: {len(local_pdfs)} | Indexed: {len(present)} | Missing: {len(missing)}\n"
    )

    if present:
        print("✅ Already indexed:")
        for p in present:
            print(f"   {os.path.basename(p)}")

    if missing:
        print(f"\n❌ Not yet indexed ({len(missing)}):")
        for m in missing:
            size_mb = os.path.getsize(m) / (1024 * 1024)
            print(f"   {os.path.basename(m)}  ({size_mb:.1f} MB)")


def cmd_ingest(args):
    """Ingest a PDF into the RAG system."""
    from scripts.ai.rag.rag_optimized import get_rag

    file_path = os.path.abspath(args.file)
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return
    if not file_path.lower().endswith(".pdf"):
        print("Error: Only PDF documents are supported.")
        return

    print(f"Ingesting: {os.path.basename(file_path)}")
    rag = get_rag(warmup=False)
    rag.ingest_ebook(file_path)
    print(f"Done: {os.path.basename(file_path)}")


def main():
    parser = argparse.ArgumentParser(description="Antigravity RAG CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # search
    sp_search = subparsers.add_parser("search", help="Semantic search")
    sp_search.add_argument("query", help="Search query")
    sp_search.add_argument("--top-k", type=int, default=5, help="Number of results")

    # list
    subparsers.add_parser("list", help="List all indexed documents")

    # get-source
    sp_source = subparsers.add_parser(
        "get-source", help="Get chunks from a specific document"
    )
    sp_source.add_argument("name", help="Partial filename to match")
    sp_source.add_argument("--limit", type=int, default=50, help="Max chunks to show")
    sp_source.add_argument(
        "--max-chars", type=int, default=1000, help="Max chars per chunk"
    )

    # scan
    sp_scan = subparsers.add_parser(
        "scan", help="Compare directory PDFs against RAG index"
    )
    sp_scan.add_argument("directory", help="Directory to scan for PDFs")
    sp_scan.add_argument(
        "-r", "--recursive", action="store_true", help="Scan subdirectories"
    )

    # ingest
    sp_ingest = subparsers.add_parser("ingest", help="Ingest a PDF into RAG")
    sp_ingest.add_argument("file", help="Path to PDF file")

    args = parser.parse_args()

    commands = {
        "search": cmd_search,
        "list": cmd_list,
        "get-source": cmd_get_source,
        "scan": cmd_scan,
        "ingest": cmd_ingest,
    }

    if args.command in commands:
        # Use lazy loading for CLI to make startup instant
        # The model will only load if/when specific commands need it.
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

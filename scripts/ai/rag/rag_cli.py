#!/usr/bin/env python
"""
RAG CLI — Reusable command-line interface for the Antigravity RAG system.

Usage:
    conda run -p D:\\Anaconda\\envs\\cursor-factory python scripts/ai/rag/rag_cli.py search "your query"
    conda run -p D:\\Anaconda\\envs\\cursor-factory python scripts/ai/rag/rag_cli.py list
    conda run -p D:\\Anaconda\\envs\\cursor-factory python scripts/ai/rag/rag_cli.py get-source "partial filename"
    conda run -p D:\\Anaconda\\envs\\cursor-factory python scripts/ai/rag/rag_cli.py scan "D:\\path\\to\\ebooks"
    conda run -p D:\\Anaconda\\envs\\cursor-factory python scripts/ai/rag/rag_cli.py ingest "D:\\path\\to\\file.pdf"
    conda run -p D:\\Anaconda\\envs\\cursor-factory python scripts/ai/rag/rag_cli.py toc "partial name"
    conda run -p D:\\Anaconda\\envs\\cursor-factory python scripts/ai/rag/rag_cli.py rebuild-toc "partial name"
    conda run -p D:\\Anaconda\\envs\\cursor-factory python scripts/ai/rag/rag_cli.py rebuild-all-tocs
    conda run -p D:\\Anaconda\\envs\\cursor-factory python scripts/ai/rag/rag_cli.py summarize "partial name"
    conda run -p D:\\Anaconda\\envs\\cursor-factory python scripts/ai/rag/rag_cli.py catalog
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

    if getattr(args, "detailed", False):
        info = rag.get_library_info()
        print(
            f"Library: {info['total_documents']} documents, {info['total_chunks']} chunks\n"
        )
        for src in info["sources"]:
            toc_marker = " [TOC]" if src.get("has_toc") else ""
            print(
                f"  {os.path.basename(src['source'])} ({src['chunk_count']} chunks){toc_marker}"
            )
            if src.get("file_hash"):
                print(f"    Hash: {src['file_hash'][:16]}...")
            print(f"    Path: {src['source']}")
        return

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

    force = getattr(args, "force", False)
    print(f"Ingesting: {os.path.basename(file_path)}{' (force)' if force else ''}")
    rag = get_rag(warmup=False)
    result = rag.ingest_ebook(file_path, force=force)
    if result:
        print(result)
    else:
        print(f"Done: {os.path.basename(file_path)}")


def cmd_stats(args):
    """Show library-wide statistics."""
    from scripts.ai.rag.rag_optimized import get_rag

    rag = get_rag(warmup=False)
    info = rag.get_library_info()
    toc_count = sum(1 for s in info["sources"] if s.get("has_toc"))
    print("RAG Library Statistics")
    print(f"  Documents:  {info['total_documents']}")
    print(f"  Chunks:     {info['total_chunks']}")
    print(f"  With TOC:   {toc_count}")
    if info["sources"]:
        avg = info["total_chunks"] / info["total_documents"]
        print(f"  Avg chunks: {avg:.1f}")


def cmd_info(args):
    """Show detailed info for a specific document."""
    from scripts.ai.rag.rag_optimized import get_rag

    rag = get_rag(warmup=False)
    sources = rag.list_sources()
    needle = args.name.lower()
    matches = [
        s
        for s in sources
        if needle in os.path.basename(s["source"]).lower()
        or needle in s["source"].lower()
    ]

    if not matches:
        print(f"No document matching '{args.name}'. Available:")
        for s in sources:
            print(f"  - {os.path.basename(s['source'])}")
        return

    for m in matches:
        toc_marker = " [TOC available]" if m.get("has_toc") else " [no TOC]"
        print(f"Document: {os.path.basename(m['source'])}")
        print(f"  Path:   {m['source']}")
        print(f"  Chunks: {m['chunk_count']}")
        print(f"  Hash:   {m.get('file_hash', 'n/a')}")
        print(f"  TOC:    {toc_marker}")
        print()


def cmd_check_duplicates(args):
    """Check for documents with duplicate content hashes."""
    from scripts.ai.rag.rag_optimized import get_rag
    from collections import Counter

    rag = get_rag(warmup=False)
    sources = rag.list_sources()
    hash_to_sources = {}
    for s in sources:
        h = s.get("file_hash")
        if h:
            hash_to_sources.setdefault(h, []).append(s["source"])

    dupes = {h: paths for h, paths in hash_to_sources.items() if len(paths) > 1}
    if dupes:
        print(f"Found {len(dupes)} duplicate group(s):\n")
        for h, paths in dupes.items():
            print(f"  Hash: {h[:16]}...")
            for p in paths:
                print(f"    - {os.path.basename(p)}")
            print()
    else:
        print(f"No duplicates found across {len(sources)} documents.")


def cmd_delete(args):
    """Delete all chunks for a specific source document."""
    from scripts.ai.rag.rag_optimized import get_rag

    # First attempt to find the full path if user gave a partial name
    rag = get_rag(warmup=False)
    client = rag.client

    # Fetch all known sources
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

    needle = args.name.lower()
    matches = [
        s
        for s in all_sources
        if needle in os.path.basename(s).lower() or needle in s.lower()
    ]

    if not matches:
        print(f"No source matching '{args.name}'. Available sources:")
        for s in all_sources:
            print(f"  - {os.path.basename(s)}")
        return

    if len(matches) > 1 and not args.force:
        print(f"Warning: Multiple sources match '{args.name}':")
        for m in matches:
            print(f"  - {m}")
        print(
            "Please be more specific, or use --force if you meant to delete multiple (currently unsupported by this CLI wrapper)."
        )
        return

    target_source = matches[0]
    print(f"Deleting all chunks for: {target_source}")
    rag.delete_document(target_source)
    print("Deletion completed.")


def cmd_toc(args):
    """Fast TOC lookup for a document (no semantic search)."""
    from scripts.ai.rag.rag_optimized import get_rag

    rag = get_rag(warmup=False)
    toc = rag.get_toc(args.name)

    if not toc:
        print(f"No Table of Contents found for document matching '{args.name}'.")
        print("Try 'rebuild-toc' if you think it should be there.")
        return

    print(f"Table of Contents for match: {args.name}")
    print("-" * 40)
    print(toc)


def cmd_rebuild_toc(args):
    """Delete and re-extract TOC for a document."""
    from scripts.ai.rag.rag_optimized import get_rag

    rag = get_rag(warmup=False)
    sources = rag.list_sources()
    needle = args.name.lower()
    matches = [
        s["source"] for s in sources if needle in os.path.basename(s["source"]).lower()
    ]

    if not matches:
        print(f"No document matching '{args.name}' found.")
        return

    target = matches[0]
    filename = os.path.basename(target)
    print(f"Target: {filename}")

    # 1. Delete old TOC
    success = rag.delete_toc(args.name)
    if success:
        print("✅ Old TOC chunk deleted.")
    else:
        print("ℹ️ No existing TOC chunk found to delete.")

    # 2. Re-extract
    print(f"Re-extracting TOC for {filename}...")
    new_toc = rag._extract_toc(target)

    if not new_toc:
        print("❌ Extraction failed or rejected by quality scoring.")
        return

    # 3. Add to store (manually creating a TOC chunk)
    from langchain_core.documents import Document
    import hashlib

    # Compute a hash for dedup if needed (though we just deleted the old one)
    sha256 = hashlib.sha256()
    with open(target, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    file_hash = sha256.hexdigest()

    toc_doc = Document(
        page_content=new_toc,
        metadata={
            "source": target,
            "is_toc": True,
            "file_hash": file_hash,
            "content_type": "toc",
        },
    )

    # We use a special key for TOC to make it easy to find
    toc_key = f"toc_{file_hash[:16]}"
    rag.store.mset([(toc_key, toc_doc)])

    print(f"✅ Successfully rebuilt TOC for {filename}!")
    print(f"   Score: {rag._score_toc(new_toc):.2f}")


def cmd_summarize(args):
    """Get a 2-3 sentence summary of a book using its first content chunks."""
    from scripts.ai.rag.rag_optimized import get_rag
    from langchain_google_genai import ChatGoogleGenerativeAI

    rag = get_rag(warmup=False)
    sources = rag.list_sources()
    needle = args.name.lower()
    matches = [
        s["source"] for s in sources if needle in os.path.basename(s["source"]).lower()
    ]

    if not matches:
        print(f"No document matching '{args.name}' found.")
        return

    target = matches[0]
    print(f"Summarizing: {os.path.basename(target)}...")

    # Get first 3 chunks (excluding TOC)
    chunks = []
    for key in rag.store.yield_keys():
        doc = rag.store.mget([key])[0]
        if (
            doc
            and doc.metadata.get("source") == target
            and not doc.metadata.get("is_toc")
        ):
            chunks.append(doc.page_content)
            if len(chunks) >= 3:
                break

    if not chunks:
        print("No content chunks found to summarize.")
        return

    context = "\n\n".join(chunks)[:10000]
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
    prompt = f"""Provide a concise 2-3 sentence summary of the following book content.
    Focus on the main topic and target audience. Do not include introductory filler.

    CONTENT:
    {context}
    """
    response = llm.invoke(prompt)
    print("-" * 40)
    print(response.content.strip())


def cmd_catalog(args):
    """List all books with their TOC status and a one-line summary."""
    from scripts.ai.rag.rag_optimized import get_rag

    rag = get_rag(warmup=False)
    info = rag.get_library_info()

    print(f"{'Document':<40} | {'TOC':<5} | {'Chunks':<6}")
    print("-" * 60)
    for s in sorted(
        info["sources"], key=lambda x: os.path.basename(x["source"]).lower()
    ):
        fname = os.path.basename(s["source"])
        if len(fname) > 37:
            fname = fname[:34] + "..."
        toc_status = "YES" if s.get("has_toc") else "NO"
        print(f"{fname:<40} | {toc_status:<5} | {s['chunk_count']:<6}")


def cmd_rebuild_all_tocs(args):
    """Scan all documents and rebuild missing or requested TOCs."""
    from scripts.ai.rag.rag_optimized import get_rag
    import os

    rag = get_rag(warmup=False)
    info = rag.get_library_info()

    targets = info["sources"]
    if not args.force:
        targets = [s for s in targets if not s.get("has_toc")]
        print(f"Found {len(targets)} documents missing TOCs. Starting rebuild...")
    else:
        print(f"Force-rebuilding TOCs for all {len(targets)} documents...")

    success_count = 0
    fail_count = 0

    for s in targets:
        path = s["source"]
        fname = os.path.basename(path)
        print(f"\nProcessing: {fname}")

        # 1. Delete if exists
        rag.delete_toc(fname)

        # 2. Extract
        new_toc = rag._extract_toc(path)
        if new_toc:
            # 3. Save (Replicating logic from cmd_rebuild_toc for now)
            from langchain_core.documents import Document
            import hashlib

            sha256 = hashlib.sha256()
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    sha256.update(chunk)
            file_hash = sha256.hexdigest()

            toc_doc = Document(
                page_content=new_toc,
                metadata={
                    "source": path,
                    "is_toc": True,
                    "file_hash": file_hash,
                    "content_type": "toc",
                },
            )
            toc_key = f"toc_{file_hash[:16]}"
            rag.store.mset([(toc_key, toc_doc)])

            score = rag._score_toc(new_toc)
            print(f"✅ Rebuilt! Score: {score:.2f}")
            success_count += 1
        else:
            print(f"❌ Failed to extract high-quality TOC for {fname}")
            fail_count += 1

    print("\nBatch Rebuild Complete.")
    print(f"  Success: {success_count}")
    print(f"  Failed:  {fail_count}")


def main():
    parser = argparse.ArgumentParser(description="Antigravity RAG CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # search
    sp_search = subparsers.add_parser("search", help="Semantic search")
    sp_search.add_argument("query", help="Search query")
    sp_search.add_argument("--top-k", type=int, default=5, help="Number of results")

    # toc
    sp_toc = subparsers.add_parser("toc", help="Fast TOC lookup")
    sp_toc.add_argument("name", help="Partial document name")

    # rebuild-toc
    sp_rebuild = subparsers.add_parser("rebuild-toc", help="Delete and re-extract TOC")
    sp_rebuild.add_argument("name", help="Partial document name")

    # rebuild-all-tocs
    sp_rebuild_all = subparsers.add_parser(
        "rebuild-all-tocs", help="Rebuild all missing or low-quality TOCs"
    )
    sp_rebuild_all.add_argument(
        "--force", action="store_true", help="Force rebuild even if TOC exists"
    )

    # summarize
    sp_summ = subparsers.add_parser("summarize", help="Fast book summary")
    sp_summ.add_argument("name", help="Partial document name")

    # catalog
    subparsers.add_parser("catalog", help="List all books with TOC status")

    # list
    sp_list = subparsers.add_parser("list", help="List all indexed documents")
    sp_list.add_argument(
        "--detailed",
        action="store_true",
        help="Show detailed info with hashes and TOC status",
    )

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
    sp_ingest.add_argument(
        "--force", action="store_true", help="Force re-ingestion even if duplicate"
    )

    # delete
    sp_delete = subparsers.add_parser("delete", help="Delete a document from RAG")
    sp_delete.add_argument("name", help="Partial or exact filename to delete")
    sp_delete.add_argument("--force", action="store_true", help="Force deletion")

    # stats
    subparsers.add_parser("stats", help="Show library statistics")

    # info
    sp_info = subparsers.add_parser("info", help="Show info for a specific document")
    sp_info.add_argument("name", help="Partial document name to search for")

    # check-duplicates
    subparsers.add_parser(
        "check-duplicates", help="Find documents with identical content"
    )

    args = parser.parse_args()

    commands = {
        "search": cmd_search,
        "list": cmd_list,
        "get-source": cmd_get_source,
        "scan": cmd_scan,
        "ingest": cmd_ingest,
        "delete": cmd_delete,
        "stats": cmd_stats,
        "info": cmd_info,
        "check-duplicates": cmd_check_duplicates,
        "toc": cmd_toc,
        "rebuild-toc": cmd_rebuild_toc,
        "rebuild-all-tocs": cmd_rebuild_all_tocs,
        "summarize": cmd_summarize,
        "catalog": cmd_catalog,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

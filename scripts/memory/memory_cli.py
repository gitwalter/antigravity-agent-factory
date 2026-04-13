"""
Memory CLI
Phase 6 of the Automated Cognitive Memory System.
Provides a command-line interface to interact with the Dual-Storage Memory Tier.
Allows fetching history, semantic searches, triggering reflection, and archiving logs.
"""

import argparse
import logging
from pprint import pprint

import os
import sys

# Ensure the root directory is in PYTHONPATH for script execution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from scripts.memory.memory_database import MemoryDatabase
from scripts.memory.memory_store import get_memory_store
from scripts.memory.memory_config import (
    COLLECTION_SEMANTIC,
    COLLECTION_SUMMARY,
    COLLECTION_ENTITY,
    COLLECTION_TOOLBOX,
    COLLECTION_PROCEDURAL,
)
from scripts.memory.experience_collector import ExperienceCollector
from scripts.memory.reflection_engine import ReflectionEngine
from scripts.memory.procedural_indexer import ProceduralIndexer
from scripts.memory.entity_store import get_entity_store

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("memory_cli")


def cmd_query_sql(args):
    db = MemoryDatabase()
    if args.entity == "chat":
        results = db.get_chat_history(args.session_id, limit=args.limit)
    else:
        results = db.get_tool_logs(args.session_id, limit=args.limit)

    for r in results:
        print(r)


def cmd_query_vector(args):
    store = get_memory_store()
    results = store.search(
        args.query, memory_type=args.collection, k=args.limit, threshold=0.1
    )

    print(f"Results from {args.collection} for query '{args.query}':")
    for r in results:
        score = r.metadata.get("similarity", 0.0)
        print(f"\n[Score: {score:.3f}] ID: {r.id}")
        print(f"Content: {r.content}")
        print(f"Metadata: {r.metadata}")


def cmd_run_collector(args):
    collector = ExperienceCollector()
    n = collector.process_uncollected_logs()
    print(f"Collected {n} episodic log files.")


def cmd_run_reflection(args):
    engine = ReflectionEngine()
    print("Running consolidation loop...")
    promoted = engine.run_consolidation_loop()
    print(f"Reflection complete. Promoted {promoted} insights to Semantic Knowledge.")
    print("Pruning decayed memories...")
    engine.prune_decayed_memories()


def cmd_run_indexer(args):
    print("Indexing procedural memory...")
    indexer = ProceduralIndexer()
    w, s, b, t, m = indexer.index_all()
    print(
        f"Index complete: {w} workflows, {s} skills, {b} blueprints, {t} templates, {m} MCPs."
    )


def main():
    parser = argparse.ArgumentParser(description="Antigravity Memory System CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Query SQL
    parser_sql = subparsers.add_parser("sql", help="Query SQLite exact-match memory")
    parser_sql.add_argument(
        "entity", choices=["chat", "tool"], help="Entity type to query"
    )
    parser_sql.add_argument("--session-id", "-s", help="Filter by session ID thread")
    parser_sql.add_argument("--limit", "-l", type=int, default=50, help="Max rows")
    parser_sql.set_defaults(func=cmd_query_sql)

    # Query Vector
    parser_vector = subparsers.add_parser("vector", help="Query Qdrant semantic memory")
    parser_vector.add_argument(
        "collection",
        choices=[
            COLLECTION_SEMANTIC,
            COLLECTION_SUMMARY,
            COLLECTION_ENTITY,
            COLLECTION_TOOLBOX,
            COLLECTION_PROCEDURAL,
        ],
        help="Target vector collection",
    )
    parser_vector.add_argument("query", help="Search query")
    parser_vector.add_argument(
        "--limit", "-l", type=int, default=5, help="Top K results"
    )
    parser_vector.set_defaults(func=cmd_query_vector)

    # Trigger Jobs
    parser_job = subparsers.add_parser("run", help="Trigger memory background jobs")
    parser_job.add_argument(
        "job", choices=["collect", "reflect", "index"], help="Job to trigger"
    )

    args = parser.parse_args()

    if args.command == "run":
        if args.job == "collect":
            cmd_run_collector(args)
        elif args.job == "reflect":
            cmd_run_reflection(args)
        elif args.job == "index":
            cmd_run_indexer(args)
    else:
        args.func(args)


if __name__ == "__main__":
    main()

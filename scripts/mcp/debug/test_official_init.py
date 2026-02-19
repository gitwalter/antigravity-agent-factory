import os
import sys
import logging

# Ensure env vars are set
os.environ["QDRANT_URL"] = "http://localhost:6333"
os.environ["COLLECTION_NAME"] = "ebook_library"

try:
    print("DEBUG: Importing mcp_server_qdrant.server...", file=sys.stderr)
    from mcp_server_qdrant.server import mcp

    print("DEBUG: Server imported successfully.", file=sys.stderr)

    # Check settings
    print(f"DEBUG: Qdrant URL: {mcp.qdrant_settings.location}", file=sys.stderr)
    print(f"DEBUG: Collection: {mcp.qdrant_settings.collection_name}", file=sys.stderr)
    print(
        f"DEBUG: Provider: {mcp.embedding_provider_settings.provider_type}",
        file=sys.stderr,
    )

    # Try to initialize the provider (this might trigger model download)
    print("DEBUG: Checking embedding provider...", file=sys.stderr)
    name = mcp.embedding_provider.get_vector_name()
    size = mcp.embedding_provider.get_vector_size()
    print(f"DEBUG: Vector name: {name}, size: {size}", file=sys.stderr)

except Exception as e:
    import traceback

    print("CRITICAL: Server initialization failed!", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)

print("DEBUG: Initialization test passed.", file=sys.stderr)

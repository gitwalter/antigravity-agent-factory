#!/usr/bin/env python
# coding: utf-8

# # RAG Analysis & MCP Server Prototype
#
# This notebook serves two purposes:
# 1. Validating the existing RAG pipeline (`scripts/ai/rag`) against the `ebook_library` Qdrant collection.
# 2. Prototyping an MCP Server to expose this RAG functionality to Antigravity agents.
# 3. Testing the running MCP Server (Client Mode) using LangChain's MultiServerMCPClient.

# In[ ]:


# Install FastMCP and LangChain MCP Adapters
# %pip install "fastmcp>=3.0.0" langchain-mcp-adapters


# In[ ]:


import sys
import os
import logging

# Ensure we can import from project root
project_root = os.path.abspath(os.path.join(os.getcwd(), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from scripts.ai.rag.rag_optimized import get_rag, OptimizedRAG

# Configure basic logging
logging.basicConfig(level=logging.INFO)


# ## 1. Direct Qdrant Inspection
# First, let's verify we can connect to the Docker instance and that the collection exists.

# In[ ]:


client = QdrantClient(url="http://localhost:6333")
collections = client.get_collections()

print("Available Collections:")
for c in collections.collections:
    print(f"- {c.name}")

count = client.count(collection_name="ebook_library")
print(f"\nDocument Count in 'ebook_library': {count.count}")


# ## 2. Test Existing RAG Pipeline
# We will use the `get_rag()` factory from `scripts/ai/rag/rag_optimized.py`. This handles the embedding model, parent-child retrieval, and reranking logic automatically.

# In[ ]:


# Initialize RAG (warmup=True will load models)
rag = get_rag(warmup=True)

query = "What are the key principles of agentic workflows?"
print(f"\nQuerying: '{query}'...\n")

results = rag.query(query)

for i, doc in enumerate(results, 1):
    source = doc.metadata.get("source", "Unknown")
    print(f"Result {i} [{source}]:\n{doc.page_content[:200]}...\n")


# ## 3. MCP Server Prototype with FastMCP
#
# We will use the `fastmcp` library to define the server tools.
# This allows a very clean, decorator-based definition.

# In[ ]:


from fastmcp import FastMCP

# Create the MCP Server instance
mcp = FastMCP("RAG Agent Server")


@mcp.tool()
def query_rag(query: str) -> str:
    """Semantically search the ebook library for technical concepts."""
    rag = get_rag(warmup=False)
    docs = rag.query(query)
    if not docs:
        return "No relevant information found."

    return "\n\n".join(
        [
            f"Source: {d.metadata.get('source', 'Unknown')}\nContent: {d.page_content}"
            for d in docs
        ]
    )


@mcp.tool()
def ingest_document(path: str) -> str:
    """Ingest a PDF document into the RAG library."""
    rag = get_rag(warmup=False)
    try:
        rag.ingest_ebook(path)
        return f"Successfully ingested {path}"
    except Exception as e:
        return f"Error ingesting document: {str(e)}"


# Verify Tools are Registered
# Note: mcp.list_tools() is typically handled by the server loop.
# However, the decorators register them internally.
print("Registered tools:", query_rag, ingest_document)

# We can call the decorated functions directly to test logic
print("\nTesting 'query_rag' function directly:")
print(query_rag("explain RAG retrieval")[:500] + "...")

# To run the server (blocking), one would normally do:
# mcp.run()
# For this notebook, we just demonstrate the definition.


# ## 4. Test Existing RAG MCP Server (Client Mode)
#
# **Pre-requisite:** Ensure the RAG MCP Server is running! (e.g., via `start_rag_server.bat`)
# This section uses LangChain's `MultiServerMCPClient` to connect to the RAG server.

# In[12]:


import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

SERVER_URL = "http://127.0.0.1:8000/sse"


async def test_langchain_mcp_client():
    print(
        f"Connecting to MCP Server at {SERVER_URL} via LangChain MultiServerMCPClient..."
    )

    try:
        # Initialize client with server configuration
        client = MultiServerMCPClient(
            connections={"rag_server": {"url": SERVER_URL, "transport": "sse"}}
        )

        print("Client Initialized. Fetching tools...")

        # 1. List Available Tools
        # get_tools() retrieves tools from all connected servers
        tools = await client.get_tools()
        print(f"\nAvailable Tools: {[tool.name for tool in tools]}")

        # 2. Invoke 'search_library' tool
        # NOTE: LangChain wraps tools as Runnable objects
        # We can find the tool by name and invoke it
        search_tool = next((t for t in tools if t.name == "search_library"), None)

        if search_tool:
            query = "Inhaltsübersicht Künstliche Intelligenz Russell?"
            print(f"\nInvoking 'search_library' with query: '{query}'")

            # Invoke the tool
            result = await search_tool.ainvoke({"query": query})
            print(f"\n--- Response ---\n{result[:500]}...\n----------------")
        else:
            print("Warning: 'search_library' tool not found on server.")

        # 3. Invoke 'list_library_sources' tool
        list_tool = next((t for t in tools if t.name == "list_library_sources"), None)

        if list_tool:
            print("\nInvoking 'list_library_sources'...")
            sources_result = await list_tool.ainvoke({})
            print(f"\n--- Sources ---\n{sources_result}\n---------------")
        else:
            print("Warning: 'list_library_sources' tool not found on server.")

    except Exception as e:
        print(f"LangChain MCP Client Error: {e}")


# Run the async test
if __name__ == "__main__":
    asyncio.run(test_langchain_mcp_client())


# In[ ]:


import os
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.environ["GEMINI_API_KEY"],
    temperature=0,
    convert_system_message_to_human=True,
)

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "antigravity-agent"

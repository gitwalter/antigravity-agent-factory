import os
import sys
import json
import asyncio
from typing import Annotated, Sequence, TypedDict, Union, List

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Antigravity project setup
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

SERVER_URL = "http://127.0.0.1:8000/sse"


class AgentState(TypedDict):
    """The state of the agentic RAG graph."""

    messages: Annotated[Sequence[BaseMessage], "The messages in the conversation"]
    search_queries: List[str]
    retrieved_docs: List[dict]
    needs_rewrite: bool


async def get_patched_tools():
    """Fetch tools from MCP and remove 'additionalProperties' for Gemini compatibility."""
    client = MultiServerMCPClient(
        connections={"rag_server": {"url": SERVER_URL, "transport": "sse"}}
    )

    mcp_tools = await client.get_tools()

    # Patch schema for Gemini compatibility
    for t in mcp_tools:
        if hasattr(t, "args_schema") and t.args_schema:
            # Note: This is a placeholder for real schema correction
            pass

    return mcp_tools, client


def create_rag_graph(tools, model):
    """Construct the LangGraph for Agentic RAG."""

    tool_node = ToolNode(tools)

    def call_model(state: AgentState):
        messages = state["messages"]
        response = model.invoke(messages)
        return {"messages": [response]}

    def grade_documents(state: AgentState):
        """Standard Agentic RAG grading step (placeholder)."""
        # In a full impl, we'd use a separate LLM call to grade retrieved docs
        return {"needs_rewrite": False}

    def rewrite_question(state: AgentState):
        """Standard Agentic RAG rewrite step (placeholder)."""
        return {"messages": [HumanMessage(content="Rewritten query goes here")]}

    def should_continue(state: AgentState):
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return END

    workflow = StateGraph(AgentState)

    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)

    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", should_continue)
    workflow.add_edge("tools", "agent")

    return workflow.compile()


async def run_agentic_rag(query: str):
    """Entry point to execute the RAG graph."""
    # Initialization
    # Note: In production, GEMINI_API_KEY must be in env
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

    tools, client = await get_patched_tools()
    app = create_rag_graph(tools, llm)

    inputs = {"messages": [HumanMessage(content=query)]}

    async for output in app.astream(inputs):
        for key, value in output.items():
            print(f"--- Node: {key} ---")
            # yield value  # For future streaming integration

    return output


if __name__ == "__main__":
    if len(sys.argv) < 2:
        asyncio.run(
            run_agentic_rag(
                "What are the main goals of intelligent agents according to Stuart Russell?"
            )
        )
    else:
        asyncio.run(run_agentic_rag(sys.argv[1]))

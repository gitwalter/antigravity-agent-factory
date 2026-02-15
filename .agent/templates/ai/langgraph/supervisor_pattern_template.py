"""
LangGraph Supervisor Multi-Agent Pattern Template

This template demonstrates a supervisor pattern where a lead agent coordinates
multiple worker agents to accomplish complex tasks.

Usage:
    supervisor = SupervisorAgent(worker_agents=[researcher, coder, writer])
    result = await supervisor.run("Build a web scraper for news articles")
"""

from typing import Annotated, TypedDict
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
import operator


class SupervisorState(TypedDict):
    """State for the supervisor graph."""

    messages: Annotated[list[BaseMessage], operator.add]
    next: str


class SupervisorAgent:
    """
    Supervisor pattern for multi-agent coordination.

    The supervisor:
    1. Receives a task
    2. Decides which worker agent should handle it
    3. Delegates to the appropriate worker
    4. Synthesizes results from multiple workers
    5. Returns the final output
    """

    def __init__(
        self,
        worker_agents: dict,
        llm: ChatOpenAI = None,
        checkpointer: MemorySaver = None,
    ):
        """
        Initialize the supervisor agent.

        Args:
            worker_agents: Dictionary of {name: agent} for worker agents
            llm: Language model for the supervisor
            checkpointer: Optional checkpointer for persistence
        """
        self.worker_agents = worker_agents
        self.llm = llm or ChatOpenAI(model="gpt-4o", temperature=0)
        self.checkpointer = checkpointer or MemorySaver()

        # Build the graph
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the supervisor graph."""
        workflow = StateGraph(SupervisorState)

        # Add worker nodes
        for name, agent in self.worker_agents.items():
            workflow.add_node(name, agent)

        # Add supervisor node
        workflow.add_node("supervisor", self._supervisor_node)

        # Add edges
        workflow.add_edge(START, "supervisor")

        # Conditional edges from supervisor to workers
        for name in self.worker_agents.keys():
            workflow.add_edge(name, "supervisor")

        # Conditional routing from supervisor
        workflow.add_conditional_edges(
            "supervisor",
            self._should_continue,
            {name: name for name in self.worker_agents.keys()} | {"FINISH": END},
        )

        return workflow.compile(checkpointer=self.checkpointer)

    async def _supervisor_node(self, state: SupervisorState):
        """Supervisor decides which worker to call next."""
        members = list(self.worker_agents.keys())

        system_prompt = f"""You are a supervisor managing these workers: {members}.

Given the user request and conversation history, decide which worker should act next.
Each worker has specific capabilities:
- researcher: Gathers information and conducts research
- coder: Writes and debugs code
- writer: Creates written content and documentation

Respond with ONLY the name of the worker who should act next, or FINISH if the task is complete.
"""

        messages = [{"role": "system", "content": system_prompt}, *state["messages"]]

        response = await self.llm.ainvoke(messages)
        next_agent = response.content.strip()

        return {"next": next_agent}

    def _should_continue(self, state: SupervisorState) -> str:
        """Determine if we should continue or finish."""
        next_agent = state["next"]

        if next_agent == "FINISH":
            return "FINISH"

        return next_agent

    async def run(self, task: str, thread_id: str = "default"):
        """
        Run the supervisor on a task.

        Args:
            task: The task to accomplish
            thread_id: Thread ID for conversation persistence

        Returns:
            The final result
        """
        config = {"configurable": {"thread_id": thread_id}}

        result = await self.graph.ainvoke(
            {"messages": [HumanMessage(content=task)]}, config=config
        )

        return result["messages"][-1].content


# Example usage
if __name__ == "__main__":
    import asyncio
    from langchain.tools import Tool

    # Create worker agents
    researcher_tools = [
        Tool(
            name="search",
            func=lambda x: f"Search results for: {x}",
            description="Search the internet",
        )
    ]

    coder_tools = [
        Tool(
            name="python_repl",
            func=lambda x: f"Executed: {x}",
            description="Execute Python code",
        )
    ]

    writer_tools = []

    # Create worker agents using create_react_agent
    llm = ChatOpenAI(model="gpt-4o")

    researcher = create_react_agent(llm, researcher_tools)
    coder = create_react_agent(llm, coder_tools)
    writer = create_react_agent(llm, writer_tools)

    worker_agents = {"researcher": researcher, "coder": coder, "writer": writer}

    # Create supervisor
    supervisor = SupervisorAgent(worker_agents=worker_agents)

    # Run task
    async def main():
        result = await supervisor.run(
            "Research the latest trends in AI agents, write code to analyze them, and create a summary report"
        )
        print(f"\nFinal Result: {result}")

    asyncio.run(main())

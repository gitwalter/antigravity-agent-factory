---
name: langgraph-agent-building
description: Build stateful agents and workflows with LangGraph 1.x
type: skill
agents: [code-reviewer, test-generator]
knowledge: [langgraph-workflows.json]
---

# LangGraph Agent Building Skill

Build stateful agents and multi-agent workflows with LangGraph.

## When to Use

- Building agents with complex state management
- Creating multi-step workflows
- Implementing human-in-the-loop patterns
- Building supervisor/worker architectures
- Needing persistent checkpointing

## Prerequisites

```bash
pip install langgraph
```

## Process

### Step 1: Define State

```python
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """State for the agent graph."""
    messages: Annotated[list, add_messages]
    next_action: str
    context: dict
    iteration: int
```

### Step 2: Create Nodes

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

async def chat_node(state: AgentState) -> AgentState:
    """Process chat messages."""
    response = await llm.ainvoke(state["messages"])
    return {"messages": [response]}

async def tool_node(state: AgentState) -> AgentState:
    """Execute tools based on LLM decision."""
    last_message = state["messages"][-1]
    
    if hasattr(last_message, "tool_calls"):
        for tool_call in last_message.tool_calls:
            result = await execute_tool(tool_call)
            state["messages"].append(result)
    
    return state

async def decision_node(state: AgentState) -> AgentState:
    """Decide next action."""
    # Analyze state and decide
    return {"next_action": "continue"}
```

### Step 3: Build Graph

```python
from langgraph.graph import StateGraph, END

def create_agent_graph() -> StateGraph:
    # Create graph with state schema
    graph = StateGraph(AgentState)
    
    # Add nodes
    graph.add_node("chat", chat_node)
    graph.add_node("tools", tool_node)
    graph.add_node("decide", decision_node)
    
    # Set entry point
    graph.set_entry_point("chat")
    
    # Add edges
    graph.add_edge("chat", "decide")
    graph.add_conditional_edges(
        "decide",
        lambda state: state["next_action"],
        {
            "use_tools": "tools",
            "continue": "chat",
            "finish": END,
        }
    )
    graph.add_edge("tools", "chat")
    
    return graph.compile()
```

### Step 4: Supervisor Pattern

```python
from langgraph.graph import StateGraph, END
from pydantic import BaseModel

class SupervisorDecision(BaseModel):
    next_agent: str
    reasoning: str

async def supervisor_node(state: AgentState) -> AgentState:
    """Supervisor decides which worker to call."""
    workers = ["researcher", "writer", "reviewer"]
    
    prompt = f"""You are a supervisor. Available workers: {workers}
    Decide which worker should act next, or 'FINISH' if done."""
    
    response = await llm.ainvoke(state["messages"] + [HumanMessage(content=prompt)])
    
    # Parse decision
    next_agent = parse_decision(response.content)
    return {"next_action": next_agent}

async def researcher_node(state: AgentState) -> AgentState:
    """Research worker."""
    # Perform research
    return {"messages": [AIMessage(content="Research complete...")]}

async def writer_node(state: AgentState) -> AgentState:
    """Writing worker."""
    # Write content
    return {"messages": [AIMessage(content="Draft complete...")]}

def create_supervisor_graph():
    graph = StateGraph(AgentState)
    
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("writer", writer_node)
    
    graph.set_entry_point("supervisor")
    
    graph.add_conditional_edges(
        "supervisor",
        lambda s: s["next_action"],
        {
            "researcher": "researcher",
            "writer": "writer",
            "FINISH": END,
        }
    )
    
    # Workers return to supervisor
    graph.add_edge("researcher", "supervisor")
    graph.add_edge("writer", "supervisor")
    
    return graph.compile()
```

### Step 5: Human-in-the-Loop

```python
from langgraph.checkpoint.memory import MemorySaver

# Create graph with checkpointing
checkpointer = MemorySaver()
graph = create_agent_graph()
app = graph.compile(checkpointer=checkpointer)

# Add interrupt points
def create_hitl_graph():
    graph = StateGraph(AgentState)
    
    graph.add_node("propose", propose_node)
    graph.add_node("execute", execute_node)
    
    # Interrupt before execution
    graph.add_node("human_review", lambda s: s)  # Passthrough
    
    graph.set_entry_point("propose")
    graph.add_edge("propose", "human_review")
    graph.add_edge("human_review", "execute")
    
    return graph.compile(
        checkpointer=checkpointer,
        interrupt_before=["human_review"]
    )

# Usage with interruption
async def run_with_approval():
    config = {"configurable": {"thread_id": "task_1"}}
    
    # Run until interrupt
    result = await app.ainvoke(initial_state, config)
    
    # Get proposed action and show to user
    proposed = result["proposed_action"]
    
    # User approves...
    approved_state = {"approved": True, **result}
    
    # Continue execution
    final = await app.ainvoke(approved_state, config)
```

### Step 6: Streaming

```python
async def stream_agent():
    """Stream agent execution."""
    async for event in app.astream(
        {"messages": [HumanMessage(content="Hello")]},
        stream_mode="values"
    ):
        print(f"Node: {event}")

async def stream_with_updates():
    """Stream with node updates."""
    async for event in app.astream_events(
        {"messages": [HumanMessage(content="Hello")]},
        version="v1"
    ):
        kind = event["event"]
        if kind == "on_chat_model_stream":
            print(event["data"]["chunk"].content, end="")
```

## Graph Patterns

| Pattern | Use Case |
|---------|----------|
| Linear | Sequential processing |
| Branching | Conditional logic |
| Parallel | Fan-out/fan-in |
| Supervisor | Multi-agent coordination |
| ReAct | Tool-using agents |
| HITL | Human approval workflows |

## State Management

```python
# Reducer for accumulating values
from operator import add
from typing import Annotated

class AccumulatorState(TypedDict):
    values: Annotated[list, add]  # Accumulates across updates
    count: int  # Overwrites on each update
```

## Best Practices

- Define clear state schemas with TypedDict
- Use reducers for accumulating state
- Implement checkpointing for long-running workflows
- Add interrupt points for human oversight
- Use conditional edges for dynamic routing
- Stream for responsive UIs

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Mutable state | Use state updates, not mutation |
| No checkpointing | Add `MemorySaver` or Redis checkpointer |
| Complex node logic | Break into smaller nodes |
| No error edges | Add error handling paths |

## Related

- Knowledge: `knowledge/langgraph-workflows.json`
- Skill: `langchain-usage`
- Skill: `langsmith-tracing`

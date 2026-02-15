# LangGraph Stateful Agent Workflows

> **Stack:** LangGraph | **Level:** Intermediate | **Duration:** 2.5 hours

## Overview

**Workshop ID:** `L3_langgraph_workflows`

**Technology:** Python with LangGraph (LangGraph 0.2+)

## Prerequisites

**Required Workshops:**
- L7_langchain_fundamentals

**Required Knowledge:**
- LangChain basics (chains, tools, agents)
- Python async/await
- State machines and graph concepts
- LLM prompt engineering

**Required Tools:**
- Python 3.10+
- OpenAI or Anthropic API key
- VS Code with Python extension

## Learning Objectives

By the end of this workshop, you will be able to:

1. **Understand LangGraph's state-based architecture and when to use it over chains** (Understand)
2. **Define typed state schemas with TypedDict and Annotated reducers** (Apply)
3. **Build multi-step agent workflows with conditional branching** (Apply)
4. **Implement human-in-the-loop patterns with interrupts and checkpoints** (Apply)
5. **Design supervisor-worker patterns for multi-agent orchestration** (Create)

## Workshop Timeline

| Phase | Duration |
|-------|----------|
| Concept | 30 min |
| Demo | 30 min |
| Exercise | 45 min |
| Challenge | 30 min |
| Reflection | 15 min |
| **Total** | **2.5 hours** |

## Workshop Phases

### Concept: LangGraph Architecture and Mental Models

*Understanding LangGraph's graph-based execution model*

**Topics Covered:**
- Why LangGraph: Limitations of chains for complex workflows
- StateGraph: Nodes, edges, and state flow
- State management: TypedDict, Annotated, reducers
- Conditional edges and routing patterns
- Checkpointing and persistence
- Human-in-the-loop and interrupts
- Multi-agent patterns: Supervisor, hierarchical, swarm

**Key Points:**
- LangGraph treats agents as state machines, not pipelines
- State flows through nodes; reducers handle concurrent updates
- Conditional edges enable dynamic routing based on state
- Checkpoints allow pause/resume and human oversight
- Supervisor pattern delegates to specialized workers

### Demo: Building a Research Agent with Tool Routing

*Live coding a multi-tool research agent with LangGraph*

**Topics Covered:**
- Define state schema with messages and tool calls
- Create tool nodes (search, calculator, code executor)
- Build router node with conditional edges
- Add cycle detection and max iterations
- Compile and invoke the graph
- Visualize the graph structure

**Key Points:**
- Each node receives and returns state
- The router decides which tool to call next
- END is a special node that terminates the graph
- graph.get_graph().draw_mermaid() visualizes the flow

### Exercise: State Management and Routing

*Create a graph with custom state and conditional routing*

**Topics Covered:**
- Define a custom state with multiple fields
- Create nodes that modify state
- Implement conditional routing based on state
- Handle the END condition

### Exercise: Human-in-the-Loop Workflow

*Implement a workflow that pauses for human approval*

**Topics Covered:**
- Add checkpointer for persistence
- Create interrupt points
- Resume with human input
- Handle approval/rejection

### Challenge: Supervisor-Worker Multi-Agent System

*Build a supervisor that orchestrates multiple worker agents*

**Topics Covered:**
- Design supervisor that routes to workers
- Create specialized worker agents
- Handle worker responses and aggregation
- Implement error handling and fallbacks

### Reflection: Production Patterns and Next Steps

*Consolidate learning and explore advanced patterns*

**Topics Covered:**
- When to use LangGraph in production
- Testing and debugging strategies
- LangSmith integration for observability
- Advanced patterns: subgraphs, parallel execution

**Key Points:**
- LangGraph excels at complex, stateful workflows
- Checkpointing enables reliable human oversight
- Supervisor pattern scales to many agents
- LangSmith provides visibility into execution

## Hands-On Exercises

### Exercise: State Management and Routing

Create a graph with custom state and conditional routing

**Difficulty:** Medium | **Duration:** 20 minutes

**Hints:**
- Use Annotated[list, add_messages] for automatic message accumulation
- Conditional edges use a function that returns the next node name
- Each node should return a dict with only the fields it modifies

**Common Mistakes to Avoid:**
- Returning full state instead of just modified fields
- Forgetting to set entry point
- Not handling the END condition

### Exercise: Human-in-the-Loop Workflow

Implement workflow with human approval checkpoint

**Difficulty:** Hard | **Duration:** 25 minutes

**Hints:**
- Use MemorySaver() for in-memory checkpointing
- interrupt_before=['node'] pauses execution before that node
- Resume by calling invoke() again with the same thread_id

**Common Mistakes to Avoid:**
- Forgetting to pass checkpointer to compile()
- Not using the same thread_id to resume
- Not handling the None case for approved

## Challenges

### Challenge: Supervisor-Worker Multi-Agent System

Build a supervisor that orchestrates multiple specialized worker agents

**Requirements:**
- Create a supervisor agent that analyzes tasks and routes to workers
- Implement at least 3 specialized worker agents (researcher, writer, critic)
- Handle worker responses and aggregate results
- Implement error handling when workers fail
- Add maximum iteration limit to prevent infinite loops

**Evaluation Criteria:**
- Supervisor correctly routes tasks to appropriate workers
- Workers return properly formatted responses
- Results are aggregated into final output
- Errors are handled gracefully
- Graph terminates correctly

**Stretch Goals:**
- Add parallel worker execution
- Implement worker-to-worker communication
- Add human oversight at key decision points
- Integrate with LangSmith for tracing

## Resources

**Official Documentation:**
- https://langchain-ai.github.io/langgraph/
- https://langchain-ai.github.io/langgraph/concepts/
- https://langchain-ai.github.io/langgraph/tutorials/

**Tutorials:**
- LangGraph Quick Start - Official
- Building Agents with LangGraph - LangChain Blog
- Multi-Agent Systems with LangGraph

**Videos:**
- LangGraph Explained - LangChain YouTube
- Building Production Agents - AI Engineer Summit

## Self-Assessment

Ask yourself these questions:

- [ ] Can I explain when LangGraph is better than chains?
- [ ] Can I define proper state schemas with reducers?
- [ ] Can I implement conditional routing?
- [ ] Can I add human-in-the-loop checkpoints?
- [ ] Can I design a supervisor-worker pattern?

## Next Steps

**Next Workshop:** `L5_crewai_multiagent`

**Practice Projects:**
- Build a code review agent with approve/reject flow
- Create a research assistant with parallel workers
- Implement a customer support bot with escalation

**Deeper Learning:**
- LangGraph Platform for deployment
- Subgraphs for modular design
- Streaming with LangGraph

## Related Knowledge Files

- `langgraph-workflows.json`
- `langchain-patterns.json`
- `multi-agent-patterns.json`

---

*Part of the Antigravity Agent Factory Learning Workshop Ecosystem*

**Workshop Definition:** `.agent/patterns/workshops/L3_langgraph_workflows.json`

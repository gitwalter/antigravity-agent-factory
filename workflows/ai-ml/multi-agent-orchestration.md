# Multi-Agent Orchestration Workflow

## Overview

Workflow for designing, implementing, and deploying multi-agent AI systems. Covers topology selection, agent implementation, coordination patterns, and testing using LangGraph, CrewAI, or AutoGen.

**Version:** 1.0.0  
**Created:** 2026-02-02  
**Applies To:** ai-agent-development, multi-agent-systems, python-multi-agent

## Trigger Conditions

This workflow is activated when:

- Multi-agent system design needed
- Agent coordination required
- Complex AI workflow needed
- Autonomous agent deployment

**Trigger Examples:**
- "Design a research agent team"
- "Create agents for code review"
- "Build a multi-agent customer service system"
- "Orchestrate agents for data analysis"

## Phases

### Phase 1: Topology Design

**Description:** Design the agent coordination topology.

**Entry Criteria:** Use case defined  
**Exit Criteria:** Topology selected

#### Step 1.1: Analyze Requirements

**Actions:**
- Identify tasks to accomplish
- Determine agent specializations
- Map information flows
- Identify coordination needs

**Skills:**
- `agent-coordination`: Topology patterns

#### Step 1.2: Select Topology

**Actions:**
- Choose coordination pattern
- Design agent graph
- Define handoff protocols
- Plan state management

**Topologies:**

| Topology | Use Case |
|----------|----------|
| Supervisor-Worker | Task delegation |
| Hierarchical | Complex organizations |
| Collaborative | Peer brainstorming |
| Sequential | Pipeline processing |
| Distributed | Independent agents |

**Topology Example (Supervisor-Worker):**
```
          ┌─────────────┐
          │  Supervisor │
          └──────┬──────┘
       ┌─────────┼─────────┐
       ▼         ▼         ▼
   ┌───────┐ ┌───────┐ ┌───────┐
   │Research│ │Writer │ │Critic │
   └───────┘ └───────┘ └───────┘
```

**Outputs:**
- Topology diagram
- Agent roles

**Is Mandatory:** Yes

---

### Phase 2: Agent Implementation

**Description:** Implement individual agents.

**Entry Criteria:** Topology designed  
**Exit Criteria:** Agents implemented

#### Step 2.1: Define Agent Specifications

**Actions:**
- Define each agent's role
- Specify capabilities/tools
- Set system prompts
- Configure models

**Agent Specification:**
```python
researcher = Agent(
    role="Research Specialist",
    goal="Find accurate, relevant information",
    backstory="Expert at web research and synthesis",
    tools=[search_tool, scrape_tool],
    llm=ChatOpenAI(model="gpt-4")
)
```

#### Step 2.2: Implement Agents

**Actions:**
- Create agent classes
- Implement tool functions
- Add memory/state
- Configure prompts

**LangGraph Example:**
```python
from langgraph.graph import StateGraph
from typing import TypedDict

class AgentState(TypedDict):
    messages: list
    current_agent: str
    research: str
    draft: str

def research_node(state: AgentState) -> AgentState:
    # Research agent logic
    result = research_agent.invoke(state["messages"])
    return {"research": result}

def writer_node(state: AgentState) -> AgentState:
    # Writer agent logic
    draft = writer_agent.invoke(state["research"])
    return {"draft": draft}

workflow = StateGraph(AgentState)
workflow.add_node("researcher", research_node)
workflow.add_node("writer", writer_node)
workflow.add_edge("researcher", "writer")
```

**Outputs:**
- Agent implementations
- Tool definitions

**Is Mandatory:** Yes

---

### Phase 3: Coordination Logic

**Description:** Implement coordination between agents.

**Entry Criteria:** Agents implemented  
**Exit Criteria:** Coordination working

#### Step 3.1: Implement Handoffs

**Actions:**
- Define handoff conditions
- Implement state passing
- Add error handling
- Configure routing

**Handoff Patterns:**

| Pattern | Implementation |
|---------|---------------|
| Explicit | Agent decides next |
| Conditional | Router function |
| Tool-based | Handoff as tool |
| Event-driven | State triggers |

#### Step 3.2: Implement Supervisor

**Actions:**
- Create supervisor agent
- Define delegation logic
- Handle agent responses
- Manage task completion

**Supervisor Example:**
```python
def supervisor_node(state: AgentState):
    response = supervisor.invoke({
        "task": state["task"],
        "agents": ["researcher", "writer", "critic"],
        "history": state["messages"]
    })
    return {"next_agent": response.next}

workflow.add_conditional_edges(
    "supervisor",
    lambda x: x["next_agent"],
    {
        "researcher": "researcher",
        "writer": "writer",
        "critic": "critic",
        "FINISH": END
    }
)
```

**Outputs:**
- Coordination logic
- Routing configuration

**Is Mandatory:** Yes

---

### Phase 4: Testing

**Description:** Test the multi-agent system.

**Entry Criteria:** Coordination implemented  
**Exit Criteria:** Tests passing

#### Step 4.1: Unit Test Agents

**Actions:**
- Test individual agents
- Verify tool execution
- Check response quality
- Test error handling

#### Step 4.2: Integration Testing

**Actions:**
- Test full workflow
- Verify handoffs
- Check state management
- Test edge cases

**Test Cases:**
- Happy path completion
- Agent failure recovery
- Infinite loop prevention
- State corruption handling

#### Step 4.3: Evaluation

**Actions:**
- Measure task completion
- Assess response quality
- Check latency
- Evaluate cost

**Outputs:**
- Test results
- Evaluation metrics

**Is Mandatory:** Yes

---

### Phase 5: Deployment

**Description:** Deploy the multi-agent system.

**Entry Criteria:** Tests passing  
**Exit Criteria:** System deployed

#### Step 5.1: Configure Production

**Actions:**
- Set up production LLMs
- Configure rate limits
- Add monitoring
- Set up logging

**Production Configuration:**
```python
from langsmith import traceable

@traceable(name="multi-agent-workflow")
def run_workflow(task: str):
    result = workflow.invoke({"task": task})
    return result
```

#### Step 5.2: Deploy

**Actions:**
- Package application
- Deploy to cloud
- Configure endpoints
- Set up alerting

**Outputs:**
- Deployed system
- API endpoints

**Is Mandatory:** Yes

---

## Decision Points

### Decision: Framework Selection

| Need | Framework |
|------|-----------|
| Complex graphs | LangGraph |
| Role-based teams | CrewAI |
| Microsoft stack | AutoGen |
| Simple chains | LangChain |

### Decision: Agent Failure

| Situation | Action |
|-----------|--------|
| Transient error | Retry with backoff |
| Invalid response | Fallback agent |
| Repeated failure | Human escalation |

---

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| Agent fails to respond | Retry with timeout |
| LLM rate limit | Fall back to slower model |
| Infinite loop detected | Break after max iterations |
| State corruption | Restore from checkpoint |
| Tool execution fails | Use fallback tool or manual |

---

## Example Session

```
User: Create a research and writing agent team

Agent:
━━━ PHASE 1: Topology Design ━━━
Analyzing requirements...
- Task: Research topics and write articles
- Agents needed: Researcher, Writer, Editor

Selected topology: Sequential with feedback loop

```
┌──────────┐    ┌────────┐    ┌────────┐
│Researcher│ -> │ Writer │ -> │ Editor │
└──────────┘    └────────┘    └───┬────┘
                      ↑           │
                      └───────────┘
                      (revision loop)
```

━━━ PHASE 2: Agent Implementation ━━━
Creating agents...

✓ Researcher: Web search, document analysis
✓ Writer: Content generation, formatting
✓ Editor: Quality review, feedback

━━━ PHASE 3: Coordination Logic ━━━
Implementing workflow...

```python
workflow = StateGraph(ArticleState)
workflow.add_node("research", research_node)
workflow.add_node("write", write_node)
workflow.add_node("edit", edit_node)

workflow.add_edge("research", "write")
workflow.add_conditional_edges(
    "edit",
    should_revise,
    {"revise": "write", "publish": END}
)
```

━━━ PHASE 4: Testing ━━━
Running tests...

✓ Research retrieves relevant information
✓ Writer produces coherent draft
✓ Editor provides actionable feedback
✓ Revision loop terminates correctly
✓ Full workflow completes in < 60s

━━━ PHASE 5: Deployment ━━━
Deploying to production...

✓ LangSmith tracing enabled
✓ Rate limiting configured
✓ API endpoint: /api/generate-article

✨ Multi-agent system deployed!
```

---

## Related Artifacts

- **Skills**: `patterns/skills/agent-coordination.json`
- **Blueprints**: `blueprints/python-multi-agent/blueprint.json`

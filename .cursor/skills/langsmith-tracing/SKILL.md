---
name: langsmith-tracing
description: Debugging and tracing LangChain/LangGraph with LangSmith MCP
type: skill
agents: [code-reviewer, test-generator, debug-conductor]
knowledge: [mcp-patterns.json]
---

# LangSmith Tracing Skill

Debug, trace, and monitor LangChain/LangGraph applications with LangSmith.

## When to Use

- Debugging agent behavior
- Tracing chain execution
- Monitoring production performance
- Analyzing prompt effectiveness
- Identifying bottlenecks

## Prerequisites

```bash
pip install langsmith
```

Set environment variables:
```bash
LANGSMITH_API_KEY=your_api_key
LANGSMITH_PROJECT=your_project_name
LANGSMITH_TRACING=true
```

## Process

### Step 1: Enable Automatic Tracing

```python
import os

# Enable tracing via environment
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "langchain-agent-platform"

# All LangChain operations are now traced automatically
```

### Step 2: Use @traceable Decorator

```python
from langsmith import traceable

@traceable(name="market_analysis", tags=["trading", "analysis"])
async def analyze_market(symbol: str) -> dict:
    """Analyze market - this function is traced."""
    # Your analysis code
    return {"symbol": symbol, "recommendation": "buy"}

@traceable(run_type="chain")
async def process_document(doc: str) -> str:
    """Process document - traced as a chain."""
    return await chain.ainvoke({"input": doc})

@traceable(run_type="tool")
def calculate_metrics(data: list) -> dict:
    """Calculate metrics - traced as a tool."""
    return {"mean": sum(data) / len(data)}
```

### Step 3: Custom Tracing Context

```python
from langsmith import trace
from langsmith.run_helpers import get_current_run_tree

@traceable
async def complex_workflow(input_data: dict):
    # Access current trace
    run_tree = get_current_run_tree()
    run_id = run_tree.id if run_tree else None
    
    # Add metadata to trace
    if run_tree:
        run_tree.extra["custom_field"] = "value"
    
    # Nested traces
    result1 = await step_one(input_data)
    result2 = await step_two(result1)
    
    return result2

# Manual trace context
async def manual_trace_example():
    with trace(
        name="manual_operation",
        run_type="chain",
        tags=["manual", "example"],
        metadata={"version": "1.0"}
    ) as run:
        # Your code here
        run.end(outputs={"result": "success"})
```

### Step 4: Trace LangGraph Workflows

```python
from langgraph.graph import StateGraph
from langsmith import traceable

# Graph nodes are automatically traced
async def traced_node(state: dict) -> dict:
    # This is traced as part of the graph
    return state

# Add custom tracing to nodes
@traceable(name="custom_node", tags=["langgraph"])
async def custom_traced_node(state: dict) -> dict:
    # Explicit tracing with custom name
    return state

# Compile with tracing
graph = StateGraph(AgentState)
graph.add_node("my_node", traced_node)
app = graph.compile()

# Invoke - entire graph execution is traced
result = await app.ainvoke(
    {"messages": []},
    config={"run_name": "my_workflow_run"}
)
```

### Step 5: MCP Integration for Debugging

Use LangSmith MCP server for IDE-integrated debugging:

```python
# In aisuite with MCP
import aisuite as ai

client = ai.Client()

response = client.chat.completions.create(
    model="google:gemini-2.5-flash",
    messages=[{"role": "user", "content": "Debug this workflow"}],
    tools=[{
        "type": "mcp",
        "name": "langsmith",
        "command": "npx",
        "args": ["-y", "@langchain/langsmith-mcp"]
    }],
    max_turns=3
)
```

### Step 6: Analyze Traces

```python
from langsmith import Client

client = Client()

# Get recent runs
runs = client.list_runs(
    project_name="langchain-agent-platform",
    filter='eq(status, "error")',  # Filter for errors
    limit=10
)

for run in runs:
    print(f"Run: {run.name}")
    print(f"  Status: {run.status}")
    print(f"  Latency: {run.latency_ms}ms")
    print(f"  Error: {run.error}")

# Get run details
run = client.read_run(run_id="...")
print(f"Inputs: {run.inputs}")
print(f"Outputs: {run.outputs}")
print(f"Trace: {run.trace_id}")
```

### Step 7: Feedback and Evaluation

```python
from langsmith import Client

client = Client()

# Add feedback to a run
client.create_feedback(
    run_id="run_123",
    key="correctness",
    score=1.0,
    comment="Response was accurate"
)

# Create dataset for evaluation
dataset = client.create_dataset("qa_pairs")
client.create_example(
    dataset_id=dataset.id,
    inputs={"question": "What is 2+2?"},
    outputs={"answer": "4"}
)

# Run evaluation
from langsmith.evaluation import evaluate

def accuracy_evaluator(run, example):
    return {"score": 1.0 if run.outputs == example.outputs else 0.0}

results = evaluate(
    my_chain.invoke,
    data="qa_pairs",
    evaluators=[accuracy_evaluator]
)
```

## Tracing Patterns

| Pattern | Decorator |
|---------|-----------|
| Function | `@traceable` |
| Chain | `@traceable(run_type="chain")` |
| Tool | `@traceable(run_type="tool")` |
| LLM | `@traceable(run_type="llm")` |
| Retriever | `@traceable(run_type="retriever")` |

## Debugging Tips

### Find Slow Operations
```python
runs = client.list_runs(
    project_name="my_project",
    filter='gt(latency_ms, 5000)',  # > 5 seconds
)
```

### Find Errors by Type
```python
runs = client.list_runs(
    project_name="my_project",
    filter='and(eq(status, "error"), contains(error, "rate limit"))',
)
```

### Compare Runs
```python
# Get similar runs for comparison
run_a = client.read_run("run_a_id")
run_b = client.read_run("run_b_id")

# Compare latencies, outputs, etc.
print(f"Run A: {run_a.latency_ms}ms")
print(f"Run B: {run_b.latency_ms}ms")
```

## Best Practices

- Always set `LANGSMITH_PROJECT` for organization
- Use meaningful run names and tags
- Add metadata for filtering
- Create datasets for regression testing
- Set up alerts for error rates
- Review traces regularly during development

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| No project set | Always set `LANGSMITH_PROJECT` |
| Missing tags | Add relevant tags for filtering |
| No error handling | Wrap traced functions in try/catch |
| Ignoring traces | Review traces during development |

## Environment Variables

```bash
# Required
LANGSMITH_API_KEY=lsv2_...

# Recommended
LANGSMITH_PROJECT=langchain-agent-platform
LANGSMITH_TRACING=true

# Optional
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
```

## Related

- Knowledge: `knowledge/mcp-patterns.json`
- Skill: `langchain-usage`
- Skill: `langgraph-agent-building`
- MCP: LangSmith MCP Server

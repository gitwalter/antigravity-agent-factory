---
agents:
- none
category: parallel
description: Build multi-agent workflows using CrewAI patterns
knowledge:
- none
name: orchestrating-crewai-workflows
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# Crewai Workflow

Build multi-agent workflows using CrewAI patterns

Build production-ready multi-agent workflows using CrewAI best practices.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Define Agents

Create specialized agents with clear roles:

```python
from crewai import Agent

researcher = Agent(
    role='Research Analyst',
    goal='Find accurate information on topics',
    backstory='Expert researcher with attention to detail',
    verbose=True,
    memory=True,
    max_iter=3
)

writer = Agent(
    role='Content Writer',
    goal='Create engaging content from research',
    backstory='Skilled writer who transforms data into stories',
    verbose=True
)
```

### Step 2: Define Tasks

Create tasks with clear expected outputs:

```python
from crewai import Task

research_task = Task(
    description='Research the topic: {topic}',
    agent=researcher,
    expected_output='Comprehensive research report with key findings'
)

writing_task = Task(
    description='Write an article based on research',
    agent=writer,
    expected_output='Engaging article in markdown format',
    context=[research_task]  # Depends on research
)
```

### Step 3: Create Crew

Assemble agents and tasks into a crew:

```python
from crewai import Crew, Process

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    verbose=True,
    memory=True
)

result = crew.kickoff(inputs={"topic": "AI Agents"})
print(result.raw)
```

### Step 4: Add Flows (Optional)

For complex state management:

```python
from crewai.flow.flow import Flow, listen, start

class MyFlow(Flow):
    @start()
    def begin(self):
        return crew.kickoff(inputs={"topic": "AI"})

    @listen(begin)
    def process_result(self, result):
        return result.raw

flow = MyFlow()
final_result = flow.kickoff()
```

## What Gets Created

| File | Purpose |
|------|---------|
| `agents/` | Agent definitions with roles |
| `tasks/` | Task definitions with dependencies |
| `crews/` | Crew configurations |
| `flows/` | Flow orchestrations (optional) |

## Process Types

| Type | Use Case |
|------|----------|
| `Process.sequential` | Tasks run one after another |
| `Process.hierarchical` | Manager delegates to workers |

## Best Practices

1. **Clear Roles**: Each agent should have ONE clear responsibility
2. **Detailed Backstories**: Guide agent behavior with context
3. **Set max_iter**: Prevent infinite loops (typically 3-5)
4. **Use Context**: Chain tasks with the `context` parameter
5. **Enable Memory**: Use `memory=True` for better context

## Common Patterns

### Research → Write → Review Pipeline

```python
crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[research_task, write_task, review_task],
    process=Process.sequential
)
```

### Hierarchical with Manager

```python
crew = Crew(
    agents=[manager, worker1, worker2],
    tasks=[complex_task],
    process=Process.hierarchical,
    manager_llm=ChatOpenAI(model='gpt-4')
)
```

## Fallback Procedures

| Issue | Solution |
|-------|----------|
| Agent loops infinitely | Set `max_iter=3` |
| Wrong task order | Use `context` parameter |
| Tool failures | Add error handling in tools |
| LLM errors | Use `max_retry_limit` |

### Advanced: CrewAI Flows

CrewAI Flows provide structured event-driven orchestration:

```python
from crewai.flow.flow import Flow, listen, start, router

class ResearchFlow(Flow):
    @start()
    def gather_requirements(self):
        # First step - always runs
        return {"topic": self.state.topic}

    @listen(gather_requirements)
    def research(self, requirements):
        # Triggered after gather_requirements
        crew = Crew(agents=[researcher], tasks=[research_task])
        return crew.kickoff(inputs=requirements)

    @router(research)
    def evaluate_quality(self, result):
        if result.quality_score > 0.8:
            return "publish"
        return "revise"

    @listen("publish")
    def publish_results(self, result):
        return result

    @listen("revise")
    def revise_research(self, result):
        return self.research(result)

flow = ResearchFlow()
flow.kickoff(inputs={"topic": "AI trends"})
```

### Advanced: CrewAI with MCP Tools

```python
from crewai import Agent
from crewai_tools import MCPServerAdapter

# Connect to MCP servers for tool access
mcp_tools = MCPServerAdapter(
    server_params={"url": "http://localhost:3000/mcp"}
).tools

agent = Agent(
    role="Data Analyst",
    tools=mcp_tools,
    llm="gpt-4"
)
```

### Advanced: Memory and Guardrails

```python
crew = Crew(
    agents=[...],
    tasks=[...],
    memory=True,  # Enable short-term + long-term memory
    embedder={
        "provider": "openai",
        "config": {"model": "text-embedding-3-small"}
    },
    max_rpm=10,  # Rate limiting guardrail
    max_tokens=4096  # Token limit guardrail
)
```

## Related Artifacts

- **Knowledge**: `{directories.knowledge}/crewai-patterns.json`
- **Templates**: `{directories.templates}/ai/crewai/`
- **Examples**: `{directories.docs}/examples/04-multi-agent-research-system/`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

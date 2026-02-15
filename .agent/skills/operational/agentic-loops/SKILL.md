---
description: ReAct pattern implementation, reflection and self-correction, planning
  and task decomposition, iterative refinement patterns
name: agentic-loops
type: skill
---
# Agentic Loops

ReAct pattern implementation, reflection and self-correction, planning and task decomposition, iterative refinement patterns

Implement agentic reasoning loops - ReAct pattern, reflection, planning, and iterative refinement for autonomous agent behavior.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Basic ReAct Pattern

Implement the core ReAct loop: Reason → Act → Observe → Repeat:

```python
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from typing import List

llm = ChatOpenAI(model="gpt-4", temperature=0.7)

@tool
def search_knowledge_base(query: str) -> str:
    """Search internal knowledge base for information.

    Args:
        query: Search query
    """
    # Implementation
    return f"Knowledge base results for: {query}"

@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression.

    Args:
        expression: Math expression like '2 + 2'
    """
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

tools = [search_knowledge_base, calculate]
llm_with_tools = llm.bind_tools(tools)

async def react_loop(user_query: str, max_iterations: int = 10) -> str:
    """Basic ReAct pattern implementation."""
    messages: List = [HumanMessage(content=user_query)]
    iteration = 0

    while iteration < max_iterations:
        # REASON: LLM generates reasoning and decides on actions
        response = await llm_with_tools.ainvoke(messages)
        messages.append(response)

        # Check if agent is done
        if not response.tool_calls:
            return response.content

        # ACT: Execute tool calls
        tool_map = {t.name: t for t in tools}
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id = tool_call["id"]

            if tool_name in tool_map:
                try:
                    # OBSERVE: Get tool result
                    if asyncio.iscoroutinefunction(tool_map[tool_name].func):
                        result = await tool_map[tool_name].ainvoke(tool_args)
                    else:
                        result = tool_map[tool_name].invoke(tool_args)

                    messages.append(ToolMessage(
                        content=str(result),
                        tool_call_id=tool_id
                    ))
                except Exception as e:
                    messages.append(ToolMessage(
                        content=f"Error: {str(e)}",
                        tool_call_id=tool_id
                    ))

        iteration += 1

    return "Maximum iterations reached."

# Usage
result = await react_loop("What is 15 * 23 and search for information about Python?")
```

### Step 2: Reflection and Self-Correction

Add reflection step to evaluate and correct actions:

```python
from langchain_core.prompts import ChatPromptTemplate

class ReflectiveAgent:
    """Agent with reflection and self-correction capabilities."""

    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.llm_with_tools = llm.bind_tools(tools)

        # Reflection prompt
        self.reflection_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a reflective agent. After taking actions, evaluate:
1. Did the actions achieve the goal?
2. Were there any errors or issues?
3. What should be done differently?
4. Should we continue or stop?"""),
            ("user", "{history}")
        ])

    async def reflect(self, messages: List, goal: str) -> dict:
        """Reflect on current progress toward goal."""
        history = "\n".join([
            f"{msg.__class__.__name__}: {msg.content}"
            for msg in messages[-10:]  # Last 10 messages
        ])

        reflection = await self.reflection_prompt.ainvoke({
            "history": f"Goal: {goal}\n\nConversation:\n{history}"
        })

        # Parse reflection
        content = reflection.content.lower()
        should_continue = "continue" in content or "retry" in content
        errors_found = "error" in content or "failed" in content

        return {
            "reflection": reflection.content,
            "should_continue": should_continue,
            "errors_found": errors_found
        }

    async def execute(self, user_query: str, max_iterations: int = 10) -> str:
        """Execute with reflection."""
        messages = [HumanMessage(content=user_query)]
        iteration = 0

        while iteration < max_iterations:
            # Act
            response = await self.llm_with_tools.ainvoke(messages)
            messages.append(response)

            if not response.tool_calls:
                # Reflect before finishing
                reflection = await self.reflect(messages, user_query)
                if reflection["errors_found"] and reflection["should_continue"]:
                    # Self-correct
                    correction_msg = HumanMessage(
                        content=f"Reflection: {reflection['reflection']}\n\nPlease correct any errors."
                    )
                    messages.append(correction_msg)
                    continue
                return response.content

            # Execute tools
            tool_map = {t.name: t for t in self.tools}
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_id = tool_call["id"]

                if tool_name in tool_map:
                    try:
                        if asyncio.iscoroutinefunction(tool_map[tool_name].func):
                            result = await tool_map[tool_name].ainvoke(tool_args)
                        else:
                            result = tool_map[tool_name].invoke(tool_args)
                        messages.append(ToolMessage(
                            content=str(result),
                            tool_call_id=tool_id
                        ))
                    except Exception as e:
                        messages.append(ToolMessage(
                            content=f"Error: {str(e)}",
                            tool_call_id=tool_id
                        ))

            # Reflect every few iterations
            if iteration % 3 == 0:
                reflection = await self.reflect(messages, user_query)
                if not reflection["should_continue"]:
                    return f"Task completed. Reflection: {reflection['reflection']}"

            iteration += 1

        return "Maximum iterations reached."

# Usage
agent = ReflectiveAgent(llm, tools)
result = await agent.execute("Research Python best practices and summarize them")
```

### Step 3: Planning and Task Decomposition

Break complex tasks into subtasks:

```python
from pydantic import BaseModel, Field
from typing import List

class Subtask(BaseModel):
    """Represents a subtask in a plan."""
    id: int
    description: str
    dependencies: List[int] = Field(default_factory=list)
    status: str = "pending"  # pending, in_progress, completed, failed

class Planner:
    """Agent that plans and decomposes tasks."""

    def __init__(self, llm):
        self.llm = llm
        self.planning_prompt = ChatPromptTemplate.from_messages([
            ("system", """Break down the task into subtasks. For each subtask, identify:
1. What needs to be done
2. Dependencies on other subtasks
3. Order of execution

Return subtasks as a structured list."""),
            ("user", "{task}")
        ])

    async def create_plan(self, task: str) -> List[Subtask]:
        """Decompose task into subtasks."""
        response = await self.planning_prompt.ainvoke({"task": task})

        # Parse response into subtasks (simplified - in practice use structured output)
        # For now, return example structure
        subtasks = [
            Subtask(id=1, description="Research topic", dependencies=[]),
            Subtask(id=2, description="Analyze findings", dependencies=[1]),
            Subtask(id=3, description="Generate summary", dependencies=[2]),
        ]

        return subtasks

    async def execute_plan(self, task: str, tools: List) -> str:
        """Execute plan by running subtasks in order."""
        plan = await self.create_plan(task)
        results = {}
        llm_with_tools = self.llm.bind_tools(tools)

        for subtask in plan:
            # Check dependencies
            if any(results.get(dep_id) == "failed" for dep_id in subtask.dependencies):
                subtask.status = "failed"
                results[subtask.id] = "failed"
                continue

            subtask.status = "in_progress"

            # Execute subtask
            query = f"Subtask {subtask.id}: {subtask.description}"
            messages = [HumanMessage(content=query)]

            iteration = 0
            while iteration < 5:  # Max iterations per subtask
                response = await llm_with_tools.ainvoke(messages)
                messages.append(response)

                if not response.tool_calls:
                    results[subtask.id] = response.content
                    subtask.status = "completed"
                    break

                # Execute tools
                tool_map = {t.name: t for t in tools}
                for tool_call in response.tool_calls:
                    tool_name = tool_call["name"]
                    tool_args = tool_call["args"]
                    tool_id = tool_call["id"]

                    if tool_name in tool_map:
                        try:
                            if asyncio.iscoroutinefunction(tool_map[tool_name].func):
                                result = await tool_map[tool_name].ainvoke(tool_args)
                            else:
                                result = tool_map[tool_name].invoke(tool_args)
                            messages.append(ToolMessage(
                                content=str(result),
                                tool_call_id=tool_id
                            ))
                        except Exception as e:
                            messages.append(ToolMessage(
                                content=f"Error: {str(e)}",
                                tool_call_id=tool_id
                            ))

                iteration += 1

            if iteration >= 5:
                subtask.status = "failed"
                results[subtask.id] = "failed"

        # Compile final result
        return f"Plan execution complete. Results: {results}"

# Usage
planner = Planner(llm)
result = await planner.execute_plan("Research and summarize Python async patterns", tools)
```

### Step 4: Iterative Refinement Pattern

Refine outputs through multiple iterations:

```python
class RefinementAgent:
    """Agent that iteratively refines its output."""

    def __init__(self, llm):
        self.llm = llm
        self.refinement_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an agent that improves outputs iteratively.
Given the current output and feedback, refine it to be better.
Continue refining until the output meets quality standards."""),
            ("user", """Original request: {request}
Current output: {current_output}
Feedback: {feedback}
Iteration: {iteration}

Refine the output based on the feedback.""")
        ])

    async def refine(
        self,
        request: str,
        initial_output: str = None,
        max_iterations: int = 5,
        quality_threshold: float = 0.8
    ) -> str:
        """Iteratively refine output."""
        current_output = initial_output or ""
        iteration = 0

        while iteration < max_iterations:
            # Generate or refine
            if iteration == 0 and not initial_output:
                # First iteration - generate initial output
                response = await self.llm.ainvoke(request)
                current_output = response.content
            else:
                # Refinement iteration
                feedback = await self._evaluate_quality(request, current_output)

                if feedback["score"] >= quality_threshold:
                    return current_output

                response = await self.refinement_prompt.ainvoke({
                    "request": request,
                    "current_output": current_output,
                    "feedback": feedback["feedback"],
                    "iteration": iteration + 1
                })
                current_output = response.content

            iteration += 1

        return current_output

    async def _evaluate_quality(self, request: str, output: str) -> dict:
        """Evaluate output quality (simplified - use LLM or metrics)."""
        eval_prompt = ChatPromptTemplate.from_messages([
            ("system", """Evaluate the output quality on a scale of 0-1.
Provide a score and specific feedback for improvement."""),
            ("user", f"Request: {request}\n\nOutput: {output}")
        ])

        response = await self.llm.ainvoke(eval_prompt.format(request=request, output=output))

        # Parse score (simplified)
        content = response.content.lower()
        score = 0.7  # Default
        if "excellent" in content or "perfect" in content:
            score = 0.9
        elif "good" in content:
            score = 0.8
        elif "needs improvement" in content:
            score = 0.6

        return {
            "score": score,
            "feedback": response.content
        }

# Usage
refiner = RefinementAgent(llm)
refined = await refiner.refine(
    "Write a comprehensive guide to Python async programming",
    max_iterations=3
)
```

### Step 5: Parallel Tool Execution

Execute multiple tools in parallel for efficiency:

```python
import asyncio
from typing import List, Dict

async def parallel_react_loop(user_query: str, tools: List, max_iterations: int = 10) -> str:
    """ReAct loop with parallel tool execution."""
    llm_with_tools = llm.bind_tools(tools)
    messages = [HumanMessage(content=user_query)]
    iteration = 0

    while iteration < max_iterations:
        response = await llm_with_tools.ainvoke(messages)
        messages.append(response)

        if not response.tool_calls:
            return response.content

        # Execute all tool calls in parallel
        tool_map = {t.name: t for t in tools}
        tool_tasks = []

        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id = tool_call["id"]

            if tool_name in tool_map:
                tool = tool_map[tool_name]

                async def execute_tool(tool, args, tool_id):
                    try:
                        if asyncio.iscoroutinefunction(tool.func):
                            result = await tool.ainvoke(args)
                        else:
                            result = tool.invoke(args)
                        return ToolMessage(
                            content=str(result),
                            tool_call_id=tool_id
                        )
                    except Exception as e:
                        return ToolMessage(
                            content=f"Error: {str(e)}",
                            tool_call_id=tool_id
                        )

                tool_tasks.append(execute_tool(tool, tool_args, tool_id))

        # Wait for all tools to complete
        tool_results = await asyncio.gather(*tool_tasks)
        messages.extend(tool_results)

        iteration += 1

    return "Maximum iterations reached."
```

### Step 6: Conditional Loop Control

Add conditions to control loop behavior:

```python
class ConditionalAgent:
    """Agent with conditional loop control."""

    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.llm_with_tools = llm.bind_tools(tools)

    async def execute(
        self,
        user_query: str,
        stop_conditions: List[str] = None,
        max_iterations: int = 10,
        min_confidence: float = 0.7
    ) -> str:
        """Execute with conditional stopping."""
        messages = [HumanMessage(content=user_query)]
        iteration = 0
        stop_conditions = stop_conditions or []

        while iteration < max_iterations:
            response = await self.llm_with_tools.ainvoke(messages)
            messages.append(response)

            # Check stop conditions
            content_lower = response.content.lower()
            if any(condition.lower() in content_lower for condition in stop_conditions):
                return f"Stopped due to condition. {response.content}"

            if not response.tool_calls:
                # Check confidence (simplified)
                confidence = await self._estimate_confidence(response.content)
                if confidence >= min_confidence:
                    return response.content
                else:
                    # Low confidence - try again
                    messages.append(HumanMessage(
                        content="The response seems uncertain. Please try again with more confidence."
                    ))
                    continue

            # Execute tools
            tool_map = {t.name: t for t in self.tools}
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_id = tool_call["id"]

                if tool_name in tool_map:
                    try:
                        if asyncio.iscoroutinefunction(tool_map[tool_name].func):
                            result = await tool_map[tool_name].ainvoke(tool_args)
                        else:
                            result = tool_map[tool_name].invoke(tool_args)
                        messages.append(ToolMessage(
                            content=str(result),
                            tool_call_id=tool_id
                        ))
                    except Exception as e:
                        messages.append(ToolMessage(
                            content=f"Error: {str(e)}",
                            tool_call_id=tool_id
                        ))

            iteration += 1

        return "Maximum iterations reached."

    async def _estimate_confidence(self, content: str) -> float:
        """Estimate confidence in response (simplified)."""
        uncertainty_words = ["maybe", "perhaps", "uncertain", "not sure"]
        content_lower = content.lower()

        if any(word in content_lower for word in uncertainty_words):
            return 0.5
        return 0.8

# Usage
agent = ConditionalAgent(llm, tools)
result = await agent.execute(
    "Research Python async patterns",
    stop_conditions=["error", "cannot"],
    min_confidence=0.8
)
```

```

### Step 7: Sequential Thinking Integration (New)

Use the `sequential-thinking` MCP server for complex problem solving:

```python
# Decompose a complex problem
response = await client.chat.completions.create(
    messages=[{"role": "user", "content": "Design a scalable microservices architecture for a banking app"}],
    tools=[{
        "type": "mcp",
        "name": "sequential-thinking",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    }]
)
```

## Agentic Loop Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **ReAct** | Reason → Act → Observe → Repeat | General agentic tasks |
| **Reflection** | Act → Reflect → Correct → Repeat | Quality-critical tasks |
| **Planning** | Plan → Decompose → Execute → Aggregate | Complex multi-step tasks |
| **Refinement** | Generate → Evaluate → Refine → Repeat | Content generation |
| **Parallel** | Act → Execute tools in parallel → Observe | Performance-critical |
| **Conditional** | Act → Check conditions → Continue/Stop | Controlled execution |

## Best Practices

- Set appropriate `max_iterations` to prevent infinite loops
- Implement proper error handling for tool calls
- Use reflection for quality-critical tasks
- Decompose complex tasks into subtasks
- Execute independent tools in parallel
- Add stop conditions for controlled execution
- Monitor token usage in long-running loops
- Log loop iterations for debugging
- Use structured outputs for planning
- Implement confidence thresholds

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| No iteration limit | Set `max_iterations` |
| Sequential tool execution | Use `asyncio.gather` for parallel execution |
| No error handling | Wrap tool calls in try/except |
| No reflection | Add reflection step for quality |
| Ignoring tool errors | Report errors back to agent |
| No planning | Decompose complex tasks |
| Infinite loops | Add stop conditions |
| No confidence checking | Evaluate response quality |
| Synchronous execution | Use async/await throughout |
| No logging | Log iterations and decisions |

## Related

- Knowledge: `{directories.knowledge}/agentic-loop-patterns.json`
- Skill: `anthropic-patterns`
- Skill: `tool-usage`
- Skill: `langchain-usage`
- Skill: `langgraph-agent-building`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

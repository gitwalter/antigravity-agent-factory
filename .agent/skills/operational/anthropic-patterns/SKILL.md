---
description: Claude agentic loop patterns - tool use until done, extended thinking
  for complex reasoning, safety and alignment patterns, LangChain ChatAnthropic integration
name: anthropic-patterns
type: skill
---
# Anthropic Patterns

Claude agentic loop patterns - tool use until done, extended thinking for complex reasoning, safety and alignment patterns, LangChain ChatAnthropic integration

Implement Claude-powered agents using Anthropic's agentic loop patterns, extended thinking, and safety best practices.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Basic Claude Agentic Loop

Implement the tool-use-until-done pattern:

```python
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
import json

llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.7,
    max_tokens=4096
)

# Define tools
@tool
def get_weather(location: str) -> str:
    """Get current weather for a location.
    
    Args:
        location: City name or coordinates
    """
    # Implementation
    return f"Sunny, 72°F in {location}"

@tool
def search_database(query: str) -> str:
    """Search internal database for information.
    
    Args:
        query: Search query
    """
    # Implementation
    return f"Database results for: {query}"

tools = [get_weather, search_database]
llm_with_tools = llm.bind_tools(tools)

# Agentic loop - continue until done
async def claude_agentic_loop(user_query: str, max_iterations: int = 10):
    """Run Claude agentic loop until completion."""
    messages = [HumanMessage(content=user_query)]
    iteration = 0
    
    while iteration < max_iterations:
        # Get Claude's response
        response = await llm_with_tools.ainvoke(messages)
        messages.append(response)
        
        # Check if Claude is done
        if not response.tool_calls:
            # No more tool calls - agent is finished
            return response.content
        
        # Execute tool calls
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id = tool_call["id"]
            
            # Find and execute tool
            tool_map = {t.name: t for t in tools}
            if tool_name in tool_map:
                tool_result = await tool_map[tool_name].ainvoke(tool_args)
                messages.append(ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_id
                ))
            else:
                messages.append(ToolMessage(
                    content=f"Error: Tool {tool_name} not found",
                    tool_call_id=tool_id
                ))
        
        iteration += 1
    
    # Max iterations reached
    return "Maximum iterations reached. Agent may not have completed the task."

# Usage
result = await claude_agentic_loop("What's the weather in NYC and search for AI articles?")
print(result)
```

### Step 2: Extended Thinking Pattern

Use Claude's extended thinking for complex reasoning:

```python
from langchain_anthropic import ChatAnthropic

llm_thinking = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.7,
    thinking={
        "type": "enabled",  # Enable extended thinking
        "budget_tokens": 10000  # Token budget for thinking
    }
)

async def complex_reasoning_task(problem: str):
    """Use extended thinking for complex problems."""
    prompt = f"""Solve this complex problem step by step. Think through
    all aspects carefully before providing your answer.
    
    Problem: {problem}
    
    Show your reasoning process."""
    
    response = await llm_thinking.ainvoke(prompt)
    
    # Access thinking content if available
    if hasattr(response, 'thinking'):
        print("Thinking process:", response.thinking)
    
    return response.content

# Usage
result = await complex_reasoning_task(
    "Design an optimal database schema for a multi-tenant SaaS application"
)
```

### Step 3: LangChain ChatAnthropic Integration

Integrate Claude with LangChain chains:

```python
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Initialize Claude
claude = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.7,
    max_tokens=4096
)

# Create chain with Claude
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant powered by Claude."),
    ("user", "{input}")
])

chain = prompt | claude | StrOutputParser()

# Use chain
result = await chain.ainvoke({"input": "Explain quantum computing"})
print(result)
```

### Step 4: Tool Use with Error Handling

Robust tool execution with error handling:

```python
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
import asyncio

@tool
async def risky_api_call(endpoint: str) -> str:
    """Call an API that might fail."""
    import httpx
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(endpoint)
            response.raise_for_status()
            return response.text
    except Exception as e:
        return f"Error: {str(e)}"

async def robust_agentic_loop(user_query: str):
    """Agentic loop with error handling."""
    messages = [HumanMessage(content=user_query)]
    tools = [risky_api_call]
    llm_with_tools = claude.bind_tools(tools)
    
    max_iterations = 10
    iteration = 0
    
    while iteration < max_iterations:
        try:
            response = await llm_with_tools.ainvoke(messages)
            messages.append(response)
            
            if not response.tool_calls:
                return response.content
            
            # Execute tools with error handling
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_id = tool_call["id"]
                
                tool_map = {t.name: t for t in tools}
                if tool_name in tool_map:
                    try:
                        tool_result = await tool_map[tool_name].ainvoke(tool_args)
                        messages.append(ToolMessage(
                            content=str(tool_result),
                            tool_call_id=tool_id
                        ))
                    except Exception as e:
                        # Report error to Claude
                        messages.append(ToolMessage(
                            content=f"Tool execution error: {str(e)}",
                            tool_call_id=tool_id
                        ))
                else:
                    messages.append(ToolMessage(
                        content=f"Unknown tool: {tool_name}",
                        tool_call_id=tool_id
                    ))
            
            iteration += 1
            
        except Exception as e:
            # Handle LLM errors
            messages.append(AIMessage(
                content=f"I encountered an error: {str(e)}. Let me try a different approach."
            ))
            iteration += 1
    
    return "Task incomplete after maximum iterations."
```

### Step 5: Safety and Alignment Patterns

Implement safety controls:

```python
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage

# Claude with safety system message
safe_claude = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.3,  # Lower temperature for more consistent behavior
    max_tokens=2048
)

# Safety system prompt
safety_prompt = """You are a helpful AI assistant. Follow these guidelines:

1. Never provide harmful, illegal, or unethical information
2. If asked to do something unsafe, politely decline and explain why
3. Protect user privacy and data
4. Be honest about your capabilities and limitations
5. Cite sources when providing factual information
"""

async def safe_agent_query(user_query: str):
    """Query Claude with safety controls."""
    messages = [
        SystemMessage(content=safety_prompt),
        HumanMessage(content=user_query)
    ]
    
    response = await safe_claude.ainvoke(messages)
    
    # Check for safety concerns (custom logic)
    if is_unsafe_response(response.content):
        return "I cannot help with that request as it may be unsafe or unethical."
    
    return response.content

def is_unsafe_response(content: str) -> bool:
    """Check if response contains unsafe content."""
    unsafe_keywords = ["hack", "exploit", "illegal"]
    content_lower = content.lower()
    return any(keyword in content_lower for keyword in unsafe_keywords)
```

### Step 6: Structured Outputs with Claude

Use Claude for structured data extraction:

```python
from pydantic import BaseModel, Field
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import PydanticOutputParser

class AnalysisResult(BaseModel):
    """Analysis result structure."""
    summary: str = Field(description="Brief summary")
    key_points: list[str] = Field(description="List of key points")
    sentiment: str = Field(description="positive, negative, or neutral")
    confidence: float = Field(ge=0, le=1, description="Confidence score")

claude = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.3  # Lower temperature for structured outputs
)

# Bind structured output
structured_llm = claude.with_structured_output(AnalysisResult)

async def analyze_text(text: str) -> AnalysisResult:
    """Analyze text and return structured result."""
    prompt = f"Analyze this text and provide structured analysis:\n\n{text}"
    result = await structured_llm.ainvoke(prompt)
    return result

# Usage
analysis = await analyze_text("This product is amazing! Highly recommend.")
print(analysis.summary)
print(analysis.key_points)
```

### Step 7: Streaming Agentic Loop

Stream responses for better UX:

```python
async def streaming_agentic_loop(user_query: str):
    """Stream Claude's responses during agentic loop."""
    messages = [HumanMessage(content=user_query)]
    tools = [get_weather, search_database]
    llm_with_tools = claude.bind_tools(tools)
    
    async for chunk in llm_with_tools.astream(messages):
        # Stream text content
        if hasattr(chunk, 'content') and chunk.content:
            print(chunk.content, end="", flush=True)
        
        # Handle tool calls as they arrive
        if hasattr(chunk, 'tool_calls') and chunk.tool_calls:
            for tool_call in chunk.tool_calls:
                print(f"\n[Calling tool: {tool_call['name']}]")
```

### Step 8: Multi-Turn Conversation with Memory

Maintain context across turns:

```python
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

claude = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.7
)

# Create chain
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Remember our conversation."),
    ("placeholder", "{messages}")
])

chain = prompt | claude | StrOutputParser()

# Add memory
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="messages",
    history_messages_key="messages",
)

# Multi-turn conversation
session_id = "user_123"

# Turn 1
result1 = await chain_with_memory.ainvoke(
    {"messages": [HumanMessage(content="My name is Alice")]},
    config={"configurable": {"session_id": session_id}}
)

# Turn 2 - Claude remembers Alice
result2 = await chain_with_memory.ainvoke(
    {"messages": [HumanMessage(content="What's my name?")]},
    config={"configurable": {"session_id": session_id}}
)
```

## Claude Model Variants

| Model | Best For | Token Limit |
|-------|----------|-------------|
| `claude-3-5-sonnet-20241022` | General purpose, balanced | 200K context |
| `claude-3-opus-20240229` | Complex reasoning | 200K context |
| `claude-3-haiku-20240307` | Fast, cost-effective | 200K context |

## Agentic Loop Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **Tool-Use-Until-Done** | Continue until no tool calls | Multi-step tasks |
| **Iterative Refinement** | Multiple passes with feedback | Content generation |
| **Parallel Tool Execution** | Execute multiple tools simultaneously | Data gathering |
| **Conditional Tool Use** | Use tools based on conditions | Adaptive workflows |

## Extended Thinking Configuration

```python
# Enable thinking with budget
thinking_config = {
    "type": "enabled",
    "budget_tokens": 10000  # Max tokens for thinking
}

claude_thinking = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    thinking=thinking_config
)
```

## Safety Best Practices

1. **System Prompts**: Define clear safety guidelines
2. **Temperature Control**: Lower temperature (0.3-0.5) for consistent behavior
3. **Output Validation**: Check responses for unsafe content
4. **Rate Limiting**: Implement rate limits to prevent abuse
5. **Error Handling**: Gracefully handle failures
6. **User Feedback**: Allow users to report issues
7. **Content Filtering**: Filter sensitive or harmful outputs

## Best Practices

- Use `claude-3-5-sonnet` for best balance of capability and cost
- Implement proper tool error handling in agentic loops
- Set appropriate `max_iterations` to prevent infinite loops
- Use extended thinking for complex reasoning tasks
- Enable streaming for better user experience
- Implement safety checks and validation
- Use structured outputs for reliable data extraction
- Maintain conversation context with memory
- Monitor token usage and costs
- Test agentic loops with various inputs

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| No iteration limit | Set `max_iterations` in loops |
| Ignoring tool errors | Handle and report tool errors to Claude |
| No safety checks | Implement safety validation |
| High temperature for structured outputs | Use 0.3-0.5 for structured data |
| No memory for multi-turn | Use `RunnableWithMessageHistory` |
| Synchronous tool calls | Use async/await for I/O |
| No error handling | Wrap tool calls in try/except |
| Ignoring token limits | Monitor and handle token limits |

## Related

- Knowledge: `{directories.knowledge}/anthropic-patterns.json`
- Skill: `langchain-usage`
- Skill: `tool-usage`
- Skill: `agentic-loops`
- Skill: `memory-management`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

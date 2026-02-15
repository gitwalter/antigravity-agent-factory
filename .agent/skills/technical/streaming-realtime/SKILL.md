---
description: Token streaming from LLMs, event streaming with astream_events, WebSocket
  agent patterns, and real-time UI updates
name: streaming-realtime
type: skill
---
# Streaming Realtime

Token streaming from LLMs, event streaming with astream_events, WebSocket agent patterns, and real-time UI updates

Implement streaming responses, event-based architectures, and real-time agent interactions for responsive user experiences.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Basic Token Streaming

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", streaming=True)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])

chain = prompt | llm

# Stream tokens
async for chunk in chain.astream({"input": "Tell me a story"}):
    if chunk.content:
        print(chunk.content, end="", flush=True)
```

### Step 2: Server-Sent Events (SSE) API

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
import json

app = FastAPI()

@app.get("/stream")
async def stream_chat(query: str):
    """Stream LLM response as Server-Sent Events."""
    
    async def event_generator():
        async for chunk in chain.astream({"input": query}):
            if chunk.content:
                yield {
                    "event": "token",
                    "data": json.dumps({
                        "content": chunk.content,
                        "type": "token"
                    })
                }
        yield {
            "event": "done",
            "data": json.dumps({"status": "complete"})
        }
    
    return EventSourceResponse(event_generator())
```

### Step 3: WebSocket Streaming

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from langchain_core.messages import HumanMessage, AIMessage

app = FastAPI()

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_json()
            user_message = data.get("message", "")
            
            # Send acknowledgment
            await websocket.send_json({
                "type": "status",
                "content": "Processing..."
            })
            
            # Stream response
            full_response = ""
            async for chunk in chain.astream({"input": user_message}):
                if chunk.content:
                    full_response += chunk.content
                    await websocket.send_json({
                        "type": "token",
                        "content": chunk.content
                    })
            
            # Send completion
            await websocket.send_json({
                "type": "complete",
                "content": full_response
            })
            
    except WebSocketDisconnect:
        print("Client disconnected")
```

### Step 4: Event Streaming with astream_events

```python
from langchain_core.runnables import RunnableConfig

async def stream_agent_events(chain, input_data: dict):
    """Stream detailed execution events from chain."""
    
    async for event in chain.astream_events(
        input_data,
        version="v2",
        include_names=["ChatGoogleGenerativeAI", "ChatPromptTemplate"]
    ):
        kind = event["event"]
        
        if kind == "on_chat_model_stream":
            # Token streaming
            chunk = event["data"]["chunk"]
            if chunk.content:
                yield {
                    "type": "token",
                    "content": chunk.content,
                    "model": event["name"]
                }
        
        elif kind == "on_chain_start":
            # Chain started
            yield {
                "type": "chain_start",
                "name": event["name"],
                "input": event["data"]["input"]
            }
        
        elif kind == "on_chain_end":
            # Chain completed
            yield {
                "type": "chain_end",
                "name": event["name"],
                "output": event["data"]["output"]
            }
        
        elif kind == "on_tool_start":
            # Tool execution started
            yield {
                "type": "tool_start",
                "name": event["name"],
                "input": event["data"]["input"]
            }
        
        elif kind == "on_tool_end":
            # Tool execution completed
            yield {
                "type": "tool_end",
                "name": event["name"],
                "output": event["data"]["output"]
            }

# Usage
async for event in stream_agent_events(chain, {"input": "Hello"}):
    print(f"[{event['type']}] {event.get('content', event.get('name', ''))}")
```

### Step 5: Real-time Agent State Updates

```python
from langchain_core.runnables import RunnableConfig
from typing import AsyncIterator

class StreamingAgent:
    """Agent that streams state updates in real-time."""
    
    def __init__(self, chain):
        self.chain = chain
    
    async def stream_with_state(self, input_data: dict, websocket: WebSocket):
        """Stream agent execution with state updates."""
        
        async def send_update(update_type: str, data: dict):
            await websocket.send_json({
                "type": update_type,
                "timestamp": datetime.now().isoformat(),
                **data
            })
        
        # Track state
        state = {
            "status": "starting",
            "tokens_received": 0,
            "tools_called": [],
            "current_step": None
        }
        
        await send_update("state", state)
        
        async for event in self.chain.astream_events(input_data, version="v2"):
            kind = event["event"]
            
            if kind == "on_chat_model_stream":
                state["tokens_received"] += len(event["data"]["chunk"].content)
                await send_update("token", {
                    "content": event["data"]["chunk"].content,
                    "total_tokens": state["tokens_received"]
                })
            
            elif kind == "on_tool_start":
                tool_name = event["name"]
                state["tools_called"].append(tool_name)
                state["current_step"] = f"Calling {tool_name}"
                await send_update("state", state)
            
            elif kind == "on_tool_end":
                state["current_step"] = None
                await send_update("state", state)
            
            elif kind == "on_chain_end":
                state["status"] = "complete"
                await send_update("state", state)
```

### Step 6: Streaming with Memory

```python
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

# Session store
session_store: dict[str, InMemoryChatMessageHistory] = {}

def get_session_history(session_id: str):
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()
    return session_store[session_id]

chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

async def stream_with_memory(query: str, session_id: str):
    """Stream response with conversation memory."""
    
    config = {"configurable": {"session_id": session_id}}
    
    async for chunk in chain_with_memory.astream(
        {"input": query},
        config=config
    ):
        if chunk.content:
            yield chunk.content
```

### Step 7: Client-Side Streaming Handler

```python
# JavaScript/TypeScript example for frontend
async function streamChat(message: string, onToken: (token: string) => void) {
    const response = await fetch('/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
    });
    
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');
        
        for (const line of lines) {
            if (line.startsWith('data: ')) {
                const data = JSON.parse(line.slice(6));
                if (data.type === 'token') {
                    onToken(data.content);
                }
            }
        }
    }
}

// WebSocket client
const ws = new WebSocket('ws://localhost:8000/ws/chat');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    switch (data.type) {
        case 'token':
            appendTokenToUI(data.content);
            break;
        case 'state':
            updateAgentStateUI(data);
            break;
        case 'complete':
            finalizeResponse(data.content);
            break;
    }
};
```

### Step 8: Streaming Tool Results

```python
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage

@tool
async def stream_search(query: str) -> str:
    """Search with streaming results."""
    # Simulate streaming search results
    results = []
    async for result in search_api.stream(query):
        results.append(result)
        yield result  # Stream partial results
    
    return "\n".join(results)

# Agent that streams tool execution
async def stream_agent_with_tools(input_text: str):
    """Agent that streams both LLM and tool outputs."""
    
    llm_with_tools = llm.bind_tools([stream_search])
    response = await llm_with_tools.ainvoke(input_text)
    
    if response.tool_calls:
        for tool_call in response.tool_calls:
            # Stream tool execution
            async for tool_chunk in stream_search.astream(tool_call["args"]):
                yield {
                    "type": "tool_output",
                    "tool": tool_call["name"],
                    "chunk": tool_chunk
                }
```

## Streaming Patterns

| Pattern | Use Case | Implementation |
|---------|----------|----------------|
| Token Streaming | Chat interfaces | `astream()` with SSE/WebSocket |
| Event Streaming | Debugging, monitoring | `astream_events()` |
| State Streaming | Real-time UI updates | Custom event handlers |
| Tool Streaming | Long-running tools | Async generators in tools |
| Batch Streaming | Multiple requests | `astream_batch()` |

## Best Practices

- Always use `streaming=True` for LLM initialization
- Use async generators for streaming endpoints
- Implement proper error handling in streams
- Send heartbeat messages for long streams
- Use WebSocket for bidirectional communication
- Stream state updates for better UX
- Handle client disconnections gracefully
- Buffer tokens for better performance

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Blocking streams | Use async generators |
| No error handling | Wrap in try/except |
| Missing heartbeats | Send periodic pings |
| Unbuffered tokens | Buffer and flush chunks |
| No disconnection handling | Handle WebSocketDisconnect |
| Sync in async context | Use `astream` not `stream` |
| Memory leaks in sessions | Clean up on disconnect |

## Related

- Skill: `langchain-usage`
- Skill: `langgraph-agent-building`
- Skill: `logging-monitoring`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

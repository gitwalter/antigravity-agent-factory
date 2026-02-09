---
description: LangChain 1.x patterns for chains, tools, memory, and structured outputs
---

# Langchain Usage

LangChain 1.x patterns for chains, tools, memory, and structured outputs

## 
# LangChain Usage Skill

Build production LangChain applications using LCEL, tools, memory, and structured outputs.

## 
# LangChain Usage Skill

Build production LangChain applications using LCEL, tools, memory, and structured outputs.

## Process
### Step 1: Initialize LLM with aisuite

Use the provider-agnostic approach:

```python
import aisuite as ai

# Provider-agnostic client
client = ai.Client()

response = client.chat.completions.create(
    model="google:gemini-2.5-flash",  # Easy to switch providers
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)
```

Or with LangChain's native integration:

```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
)
```

### Step 2: Create Chains with LCEL

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Simple chain
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])

chain = prompt | llm | StrOutputParser()
result = await chain.ainvoke({"input": "Hello!"})
```

### Step 3: Structured Outputs

```python
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class Analysis(BaseModel):
    summary: str = Field(description="Brief summary")
    sentiment: str = Field(description="positive, negative, or neutral")
    confidence: float = Field(ge=0, le=1)

parser = PydanticOutputParser(pydantic_object=Analysis)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Analyze the text. {format_instructions}"),
    ("user", "{text}")
]).partial(format_instructions=parser.get_format_instructions())

chain = prompt | llm | parser
result = await chain.ainvoke({"text": "Great product!"})
```

### Step 4: Tool Calling

```python
from langchain_core.tools import tool

@tool
def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"Sunny, 72°F in {location}"

@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"

# Bind tools to model
llm_with_tools = llm.bind_tools([get_weather, search_web])

# Invoke with tool selection
response = await llm_with_tools.ainvoke("What's the weather in NYC?")
```

### Step 5: Memory and Context

```python
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Session store
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# Chain with memory
chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# Use with session
result = await chain_with_memory.ainvoke(
    {"input": "Hi, I'm Alice"},
    config={"configurable": {"session_id": "user_123"}}
)
```

### Step 6: Document Loaders

```python
from langchain_community.document_loaders import (
    PyPDFLoader,
    WebBaseLoader,
    CSVLoader,
)

# PDF
pdf_loader = PyPDFLoader("document.pdf")
pdf_docs = pdf_loader.load()

# Web page
web_loader = WebBaseLoader("https://example.com")
web_docs = web_loader.load()

# CSV
csv_loader = CSVLoader("data.csv")
csv_docs = csv_loader.load()
```

```python
import aisuite as ai

# Provider-agnostic client
client = ai.Client()

response = client.chat.completions.create(
    model="google:gemini-2.5-flash",  # Easy to switch providers
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)
```

```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
)
```

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Simple chain
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])

chain = prompt | llm | StrOutputParser()
result = await chain.ainvoke({"input": "Hello!"})
```

```python
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class Analysis(BaseModel):
    summary: str = Field(description="Brief summary")
    sentiment: str = Field(description="positive, negative, or neutral")
    confidence: float = Field(ge=0, le=1)

parser = PydanticOutputParser(pydantic_object=Analysis)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Analyze the text. {format_instructions}"),
    ("user", "{text}")
]).partial(format_instructions=parser.get_format_instructions())

chain = prompt | llm | parser
result = await chain.ainvoke({"text": "Great product!"})
```

```python
from langchain_core.tools import tool

@tool
def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"Sunny, 72°F in {location}"

@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"

# Bind tools to model
llm_with_tools = llm.bind_tools([get_weather, search_web])

# Invoke with tool selection
response = await llm_with_tools.ainvoke("What's the weather in NYC?")
```

```python
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Session store
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# Chain with memory
chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# Use with session
result = await chain_with_memory.ainvoke(
    {"input": "Hi, I'm Alice"},
    config={"configurable": {"session_id": "user_123"}}
)
```

```python
from langchain_community.document_loaders import (
    PyPDFLoader,
    WebBaseLoader,
    CSVLoader,
)

# PDF
pdf_loader = PyPDFLoader("document.pdf")
pdf_docs = pdf_loader.load()

# Web page
web_loader = WebBaseLoader("https://example.com")
web_docs = web_loader.load()

# CSV
csv_loader = CSVLoader("data.csv")
csv_docs = csv_loader.load()
```

## LCEL Patterns
| Pattern | Example |
|---------|---------|
| Sequential | `chain1 \| chain2 \| chain3` |
| Parallel | `RunnableParallel(a=chain1, b=chain2)` |
| Conditional | `RunnableBranch((condition, chain1), chain2)` |
| Fallback | `chain.with_fallbacks([backup])` |
| Retry | `chain.with_retry(stop_after_attempt=3)` |

## Best Practices
- Use LCEL pipe syntax for chain composition
- Always use async methods (`ainvoke`, `astream`) for I/O
- Define tools with proper docstrings for LLM understanding
- Use Pydantic for structured outputs
- Enable tracing with LangSmith
- Handle errors with fallbacks

## Anti-Patterns
| Anti-Pattern | Fix |
|--------------|-----|
| Sync in async context | Use `ainvoke` not `invoke` |
| No error handling | Add `.with_fallbacks()` |
| Hardcoded prompts | Use `ChatPromptTemplate` |
| No type hints | Use Pydantic models |

## Related
- Knowledge: `knowledge/langchain-patterns.json`
- Skill: `langgraph-agent-building`
- Skill: `langsmith-tracing`

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Packages: langchain, langchain-core, langchain-community, langchain-google-genai
> - Knowledge: langchain-patterns.json

---
description: LangChain 1.x patterns for chains, tools, memory, and structured outputs
name: langchain-usage
type: skill
---
# Langchain Usage

LangChain 1.x patterns for chains, tools, memory, and structured outputs

Build production LangChain applications using LCEL, tools, memory, and structured outputs.

## Process

1. **Initialize LLM** – Use aisuite for provider-agnostic access or LangChain native integrations (e.g. `ChatGoogleGenerativeAI`). See REFERENCE.md.
2. **Create Chains** – Compose with LCEL pipe syntax: `prompt | llm | parser`. Use `ChatPromptTemplate` for templated prompts.
3. **Structured Outputs** – Define Pydantic models; use `PydanticOutputParser` for type-safe responses.
4. **Tool Calling** – Decorate functions with `@tool`, bind with `llm.bind_tools()`, invoke and handle tool calls.
5. **Memory** – Use `RunnableWithMessageHistory` with `InMemoryChatMessageHistory` for session-scoped context.
6. **Document Loaders** – Use `PyPDFLoader`, `WebBaseLoader`, `CSVLoader` from `langchain_community`.

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

## MCP Integration (New)

Use the `docs-langchain` MCP server to search for the latest patterns and API references directly:

```python
# Search for specific patterns
response = await client.chat.completions.create(
    messages=[{"role": "user", "content": "How do I use RunnableWithMessageHistory?"}],
    tools=[{
        "type": "mcp",
        "name": "docs-langchain",
        "command": "npx", # Managed by MCP config
        "args": [] 
    }]
)
```

## Bundled Resources

- **QUICKSTART.md** – 5-minute getting started guide
- **REFERENCE.md** – Detailed code (LLM init, LCEL chains, structured outputs, tools, memory, document loaders)
- **scripts/verify.py** – Validate project follows LangChain patterns (`--project-dir`)
- **examples/basic_chain/** – Simple LCEL chain with structured output

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

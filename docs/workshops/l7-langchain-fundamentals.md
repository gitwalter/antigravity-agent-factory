# LangChain Agent Development Fundamentals

> **Stack:** LangChain + LangGraph | **Level:** Fundamentals | **Duration:** 2.5 hours

## Overview

**Workshop ID:** `L7_langchain_fundamentals`

**Technology:** Python with LangChain + LangGraph (LangChain 0.3+)

## Prerequisites

**Required Knowledge:**
- Python programming (functions, classes, async)
- Basic understanding of LLMs and prompts
- HTTP APIs and JSON

**Required Tools:**
- Python 3.10+
- OpenAI API key (or other LLM provider)
- VS Code or similar IDE

## Learning Objectives

By the end of this workshop, you will be able to:

1. **Understand LangChain's architecture: models, prompts, chains, and agents** (Understand)
2. **Create chains using LCEL (LangChain Expression Language)** (Apply)
3. **Build tools and integrate them with agents** (Apply)
4. **Implement a RAG (Retrieval Augmented Generation) pipeline** (Apply)
5. **Apply best practices for prompt engineering and error handling** (Apply)

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

### Concept: LangChain Architecture Overview

*Understand the building blocks of LangChain applications*

**Topics Covered:**
- Chat Models vs Completion Models
- Prompt Templates and Message Types
- LCEL: Runnables and Composition
- Chains vs Agents: When to use each
- Tools and Tool Calling
- Memory and State Management

**Key Points:**
- LCEL uses pipe operator for readable chain composition
- Agents decide which tools to use; chains follow fixed paths
- Structured outputs enable reliable parsing
- Memory enables conversational context

### Demo: Building a Research Assistant

*Live coding a practical LangChain application*

**Topics Covered:**
- Setting up LangChain with OpenAI
- Creating prompt templates
- Building chains with LCEL
- Adding tools for web search
- Implementing structured output
- Adding observability with LangSmith

**Key Points:**
- Always use structured outputs for reliability
- Enable tracing for debugging
- Handle errors gracefully with fallbacks

### Exercise: Building Your First Chain

*Create a multi-step processing chain*

**Topics Covered:**
- Create a text summarization chain
- Add translation as second step
- Implement parallel processing with RunnableParallel
- Add error handling

### Exercise: Creating Custom Tools

*Build tools and integrate with an agent*

**Topics Covered:**
- Define tool with @tool decorator
- Add Pydantic schema for inputs
- Create agent with tools
- Test tool calling

### Challenge: Document Q&A System

*Build a complete RAG application*

**Topics Covered:**
- Load and split documents
- Create embeddings and vector store
- Build retrieval chain
- Add conversation memory
- Handle follow-up questions

### Reflection: Key Takeaways and Production Considerations

*Consolidate learning and discuss production deployment*

**Topics Covered:**
- Summary of LangChain patterns
- Production considerations (rate limits, caching, monitoring)
- Security (prompt injection, data privacy)
- Resources for continued learning

**Key Points:**
- Use structured outputs for reliability
- Implement proper error handling and retries
- Monitor with LangSmith or similar
- Be aware of prompt injection risks

## Hands-On Exercises

### Exercise: Multi-Step Processing Chain

Build a chain that summarizes and translates text

**Difficulty:** Easy | **Duration:** 20 minutes

**Hints:**
- Use StrOutputParser() to get text from LLM response
- Pass through the language parameter for the second step
- Dictionary syntax creates RunnableParallel for multiple values

**Common Mistakes to Avoid:**
- Forgetting output parser between steps
- Not passing language to second prompt
- Invoking with wrong input keys

### Exercise: Custom Tool Agent

Create an agent with custom tools

**Difficulty:** Medium | **Duration:** 25 minutes

**Common Mistakes to Avoid:**
- Using eval() which is unsafe
- Missing agent_scratchpad placeholder
- Not including chat_history in invoke

## Challenges

### Challenge: Document Q&A System

Build a complete RAG system that can answer questions about documents

**Requirements:**
- Load and process PDF or text documents
- Split into chunks with appropriate overlap
- Create embeddings and store in vector database
- Build retrieval chain with context injection
- Add conversation memory for follow-up questions
- Include source citations in responses

**Evaluation Criteria:**
- Successfully loads and indexes documents
- Retrieves relevant chunks for questions
- Answers are grounded in document content
- Handles follow-up questions with context
- Includes source citations

**Stretch Goals:**
- Add multi-query retrieval for complex questions
- Implement hybrid search (vector + keyword)
- Add streaming responses
- Deploy as web API with FastAPI

## Resources

**Official Documentation:**
- https://python.langchain.com/docs/
- https://langchain-ai.github.io/langgraph/

**Tutorials:**
- https://python.langchain.com/docs/tutorials/
- https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/

## Self-Assessment

Ask yourself these questions:

- [ ] Can I explain the difference between chains and agents?
- [ ] Do I understand how to create and use custom tools?
- [ ] Can I implement a basic RAG pipeline?
- [ ] Do I know how to handle errors and add observability?

## Next Steps

**Next Workshop:** `L8_langgraph_workflows`

**Practice Projects:**
- Customer support chatbot with knowledge base
- Code review assistant with GitHub integration
- Research assistant with web search and citation

**Deeper Learning:**
- LangGraph for complex workflows
- Fine-tuning and embeddings optimization
- Production deployment patterns

## Related Knowledge Files

- `langchain-patterns.json`
- `rag-patterns.json`
- `prompt-engineering-patterns.json`

---

*Part of the Antigravity Agent Factory Learning Workshop Ecosystem*

**Workshop Definition:** `.agent/patterns/workshops/L7_langchain_fundamentals.json`
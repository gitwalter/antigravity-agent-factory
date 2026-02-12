---
description: AI Agent Development with LangChain and LangGraph
name: ai-agent-dev
type: skill
---

# AI Agent Development Skill

This skill provides expertise in building AI agents using modern frameworks like LangChain, LangGraph, CrewAI, and AutoGen.

## Core Capabilities

### 1. Agent Architecture Design
- Choose appropriate agent patterns (ReAct, Plan-Execute, Reflection)
- Design multi-agent systems with proper coordination
- Implement state management and memory
- Structure agent workflows for complex tasks

### 2. Tool Integration
- Create custom tools for specific domains
- Integrate external APIs and services
- Implement tool error handling and fallbacks
- Optimize tool selection and usage

### 3. LangChain Expertise
- Build agents with LCEL (LangChain Expression Language)
- Implement RAG systems with vector databases
- Use LangSmith for observability and debugging
- Deploy with LangServe

### 4. LangGraph Workflows
- Design state graphs for complex workflows
- Implement checkpointing and persistence
- Add human-in-the-loop capabilities
- Build supervisor and worker patterns

### 5. Multi-Agent Orchestration
- Coordinate multiple specialized agents
- Implement communication protocols
- Handle agent delegation and task routing
- Manage shared state and context

## Key Patterns

### ReAct Pattern
```python
# Reasoning + Acting loop
# 1. Thought: What should I do?
# 2. Action: Execute tool
# 3. Observation: See result
# 4. Repeat until done
```

### Supervisor Pattern
```python
# Central coordinator delegates to workers
# - Supervisor: Routes tasks
# - Workers: Execute specialized tasks
# - Synthesis: Combine results
```

### Plan-and-Execute
```python
# Strategic planning before execution
# 1. Create comprehensive plan
# 2. Execute steps sequentially
# 3. Replan if needed
# 4. Synthesize results
```

## Tools and Technologies

- **LangChain**: Core framework for agents
- **LangGraph**: State machine workflows
- **CrewAI**: Role-based multi-agent systems
- **AutoGen**: Microsoft's agent framework
- **Vector DBs**: ChromaDB, Pinecone, Qdrant
- **LLMs**: GPT-4o, Claude Opus 4.6, Gemini 3 Pro
- **Observability**: LangSmith, Weights & Biases

## Best Practices

1. **Start Simple**: Begin with basic agents, add complexity gradually
2. **Use Structured Outputs**: Leverage Pydantic models for reliability
3. **Implement Logging**: Track all agent actions and decisions
4. **Set Limits**: Max iterations, token limits, timeouts
5. **Error Handling**: Graceful degradation and fallbacks
6. **Test Thoroughly**: Unit tests, integration tests, end-to-end tests
7. **Monitor Costs**: Track API usage and optimize
8. **Human Oversight**: Add human-in-the-loop for critical decisions

## Common Challenges and Solutions

### Challenge: Agent Loops
**Solution**: Set max_iterations, implement loop detection, add explicit termination conditions

### Challenge: High Costs
**Solution**: Use cheaper models for planning, cache results, implement rate limiting

### Challenge: Unreliable Outputs
**Solution**: Use structured outputs, add validation, implement retry logic

### Challenge: Context Overflow
**Solution**: Implement memory management, use summarization, offload to vector DB

### Challenge: Tool Selection Errors
**Solution**: Improve tool descriptions, add examples, implement fallbacks

## Example Projects

1. **Research Assistant**: Multi-agent system for comprehensive research
2. **Code Review Agent**: Automated code analysis and suggestions
3. **Customer Support**: Intelligent ticket routing and response
4. **Data Analysis**: Automated data exploration and insights
5. **Content Creation**: Multi-step content generation pipeline

## Resources

- LangChain Documentation: https://python.langchain.com
- LangGraph Documentation: https://langchain-ai.github.io/langgraph/
- LangSmith: https://smith.langchain.com
- Example Repositories: See github-agent-templates.json

## Usage in Antigravity

This skill is automatically available when using the `ai-agent-development` or `multi-agent-systems` blueprints. It provides:

- Template selection guidance
- Architecture recommendations
- Code generation assistance
- Debugging support
- Best practices enforcement

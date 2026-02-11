# Anthropic Claude Agents with Tool Use

> **Stack:** Anthropic Claude + MCP | **Level:** Intermediate | **Duration:** 2.5 hours

## Overview

**Workshop ID:** `L17_anthropic_tool_agents`

**Technology:** Python with Anthropic Claude + MCP (Claude 3.5+)

## Prerequisites

**Required Knowledge:**
- Python programming (async/await, classes, dict manipulation)
- Understanding of LLMs and API basics
- JSON Schema fundamentals
- Basic understanding of agent architectures

**Required Tools:**
- Python 3.10+
- Anthropic API key
- anthropic SDK (pip install anthropic)
- mcp SDK (pip install mcp)
- VS Code or similar IDE

## Learning Objectives

By the end of this workshop, you will be able to:

1. **Understand Anthropic's philosophy on safe, helpful AI agents** (Understand)
2. **Implement tool use with Claude's native tool calling API** (Apply)
3. **Build agentic loops with proper error handling and retries** (Apply)
4. **Integrate Model Context Protocol (MCP) servers for extended capabilities** (Apply)
5. **Apply best practices: system prompts, tool descriptions, structured outputs** (Apply)

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

### Concept: Anthropic Agent Philosophy and Tool Use Architecture

*Understanding Anthropic's approach to AI agents and tool use*

**Topics Covered:**
- Anthropic's AI safety principles: helpful, harmless, honest
- Tool use as structured output: input_schema with JSON Schema
- Agentic loop: tool_use → tool_result → continue
- System prompts for agent behavior and safety
- Model Context Protocol (MCP) overview and architecture
- Tool descriptions: clarity and specificity
- tool_choice parameter: auto, required, or specific tool
- Error handling and retry strategies
- Graceful degradation when tools fail

**Key Points:**
- Anthropic emphasizes safety and helpfulness in agent design
- Tools are defined with JSON Schema input_schema
- Claude returns tool_use blocks that must be executed
- System prompts guide agent behavior and tool selection
- MCP provides standardized protocol for tool integration
- Clear tool descriptions improve tool selection accuracy
- Always implement error handling and retries
- Graceful degradation maintains user experience

### Demo: Building a Research Agent with Multiple Tools

*Live coding a research agent with search, calculator, and file read tools*

**Topics Covered:**
- Define tools with JSON Schema input_schema
- Create system prompt for agent behavior
- Implement tool execution functions
- Build agentic loop: handle tool_use blocks
- Process tool_result and continue conversation
- Handle multiple tool calls in one response
- Implement error handling and retries
- Add graceful degradation

**Key Points:**
- JSON Schema must match tool function parameters exactly
- System prompts guide tool selection and usage
- Each tool_use block requires a tool_result response
- Continue conversation with tool results in context
- Handle errors gracefully and retry transient failures

### Exercise: Tool Calling with Proper Schemas and Error Handling

*Implement tool calling with proper JSON Schema and error handling*

**Topics Covered:**
- Define tools with comprehensive input_schema
- Implement tool execution functions
- Build agentic loop
- Add error handling and retries
- Handle edge cases

### Exercise: Create MCP Server and Connect to Claude

*Create an MCP server and integrate it with Claude agent*

**Topics Covered:**
- Create MCP server with tools
- Define tool handlers
- Connect MCP client to Claude
- Execute tools through MCP
- Handle MCP errors

### Challenge: Multi-Tool Agent with Graceful Degradation

*Build a robust agent that handles tool failures gracefully*

**Topics Covered:**
- Design multi-tool agent
- Implement fallback strategies
- Handle partial tool failures
- Provide meaningful error messages
- Maintain user experience during failures

### Reflection: Safety Considerations and Prompt Engineering

*Consolidate learning and discuss production considerations*

**Topics Covered:**
- Anthropic safety principles in practice
- Prompt engineering for agents
- Tool selection strategies
- Production deployment considerations
- Monitoring and observability
- Resources for continued learning

**Key Points:**
- Safety should be built into system prompts and tool design
- Clear tool descriptions improve reliability
- Error handling is critical for production
- Monitor tool usage and success rates
- MCP enables standardized tool integration
- Structured outputs via tool_choice improve reliability

## Hands-On Exercises

### Exercise: Tool Calling with Proper Schemas and Error Handling

Implement tool calling with proper JSON Schema and comprehensive error handling

**Difficulty:** Medium | **Duration:** 20 minutes

**Hints:**
- Use JSON Schema for input_schema with type, properties, required fields
- Check response.content for tool_use blocks
- Each tool_use block needs a corresponding tool_result message
- Continue conversation by adding tool results to messages
- Use retry decorator for transient API errors
- Validate tool inputs before execution

**Common Mistakes to Avoid:**
- Missing required fields in input_schema
- Not handling multiple tool_use blocks
- Forgetting to add tool_result messages
- Not continuing conversation after tool execution
- Missing error handling for tool execution
- Incorrect JSON Schema format

### Exercise: Create MCP Server and Connect to Claude

Create an MCP server with tools and integrate it with Claude agent

**Difficulty:** Hard | **Duration:** 25 minutes

**Hints:**
- MCP tools use inputSchema (camelCase) vs Anthropic's input_schema (snake_case)
- Convert MCP Tool format to Anthropic tool format
- Use async/await for MCP server operations
- MCP call_tool returns list of result dicts
- Combine multiple result blocks into single response
- Handle errors in tool execution

**Common Mistakes to Avoid:**
- Not converting MCP tool format to Anthropic format
- Forgetting async/await in MCP operations
- Not handling MCP result list format
- Missing error handling in tool execution
- Incorrect inputSchema vs input_schema naming

## Challenges

### Challenge: Multi-Tool Agent with Graceful Degradation

Build a robust agent that handles tool failures gracefully and maintains user experience

**Requirements:**
- Create agent with at least 3 tools (search, calculator, file operations)
- Implement fallback strategies when tools fail
- Handle partial tool failures (some tools work, others don't)
- Provide meaningful error messages to users
- Continue operation even when non-critical tools fail
- Implement retry logic with exponential backoff
- Log tool usage and failures for monitoring
- Use structured outputs via tool_choice when appropriate

**Evaluation Criteria:**
- Agent continues operating when tools fail
- Error messages are helpful and actionable
- Fallback strategies work correctly
- Retry logic handles transient failures
- Tool usage is logged appropriately
- User experience remains smooth during failures
- Structured outputs work correctly

**Stretch Goals:**
- Implement tool health checks
- Add circuit breaker pattern for failing tools
- Create tool usage analytics dashboard
- Implement tool versioning
- Add tool usage rate limiting
- Create tool testing framework

## Resources

**Official Documentation:**
- https://docs.anthropic.com/claude/docs/tool-use
- https://docs.anthropic.com/claude/docs/system-prompts
- https://modelcontextprotocol.io/
- https://github.com/modelcontextprotocol/python-sdk

**Tutorials:**
- Anthropic Tool Use Guide
- Building Agents with Claude - Anthropic Blog
- MCP Server Development Guide
- Anthropic API Python SDK Documentation

**Videos:**
- Anthropic Tool Use Tutorial
- Building AI Agents with Claude - Conference Talk
- MCP Protocol Deep Dive

## Self-Assessment

Ask yourself these questions:

- [ ] Can I explain Anthropic's safety principles?
- [ ] Do I understand how tool_use blocks work?
- [ ] Can I implement a complete agentic loop?
- [ ] Do I know how to create and integrate MCP servers?
- [ ] Can I write effective system prompts for agents?
- [ ] Do I understand error handling and retry strategies?
- [ ] Can I implement graceful degradation?

## Next Steps

**Next Workshop:** `L18_advanced_agent_patterns`

**Practice Projects:**
- Build a research assistant with multiple data sources
- Create a code analysis agent with file operations
- Implement a customer support agent with knowledge base
- Build a data analysis agent with calculation tools

**Deeper Learning:**
- Advanced prompt engineering for agents
- Multi-agent orchestration with Claude
- Production deployment and monitoring
- Tool versioning and migration strategies
- Advanced MCP patterns (gateways, load balancing)

## Related Knowledge Files

- `anthropic-patterns.json`
- `mcp-patterns.json`
- `tool-use-patterns.json`

---

*Part of the Antigravity Agent Factory Learning Workshop Ecosystem*

**Workshop Definition:** `patterns/workshops/L17_anthropic_tool_agents.json`
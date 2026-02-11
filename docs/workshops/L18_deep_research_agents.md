# Deep Research Agents: Multi-Step Reasoning and Discovery

> **Stack:** LangGraph + Research Tools | **Level:** Advanced | **Duration:** 2.5 hours

## Overview

**Workshop ID:** `L18_deep_research_agents`

**Technology:** Python with LangGraph + Research Tools (LangGraph 0.2+)

## Prerequisites

**Required Workshops:**
- L3_langgraph_workflows
- L7_langchain_fundamentals

**Required Knowledge:**
- LangGraph state machines and conditional routing
- LangChain tools and agents
- Python async/await patterns
- Understanding of search APIs (Tavily, SerpAPI)
- Basic knowledge of reasoning patterns (chain-of-thought, reflection)

**Required Tools:**
- Python 3.10+
- OpenAI or Anthropic API key
- Tavily API key or SerpAPI key (for search)
- VS Code with Python extension

## Learning Objectives

By the end of this workshop, you will be able to:

1. **Design multi-step research workflows with iterative refinement** (Create)
2. **Implement chain-of-thought and reflection patterns for reasoning** (Apply)
3. **Build source discovery and validation pipelines** (Apply)
4. **Create synthesis agents that aggregate and summarize findings** (Apply)
5. **Implement human-in-the-loop for research quality control** (Apply)

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

### Concept: Deep Research Architecture and Reasoning Patterns

*Understanding deep research systems like Perplexity/Gemini Deep Research and reasoning patterns*

**Topics Covered:**
- Deep Research Architecture: Query decomposition, iterative search, synthesis
- Multi-step reasoning: Chain-of-thought, tree-of-thought, reflection loops
- Query planning: Breaking complex questions into sub-queries
- Iterative refinement: Using search results to generate better queries
- Source discovery: Finding diverse, credible sources
- Credibility scoring: Domain authority, recency, citation count
- Reflection patterns: Self-critique, verification, confidence scoring
- Synthesis: Aggregating findings with proper citation and attribution
- Uncertainty handling: Expressing confidence levels and gaps
- Human-in-the-loop: Quality gates and approval checkpoints

**Key Points:**
- Deep research requires multiple search iterations, not single queries
- Query decomposition enables parallel exploration of sub-topics
- Reflection loops improve quality through self-critique
- Source validation prevents misinformation
- Synthesis must preserve attribution and handle conflicts
- Confidence scoring helps users understand reliability
- Human oversight ensures quality and ethical research

### Demo: Building a Deep Research Agent

*Live coding a research agent that searches, validates, and synthesizes*

**Topics Covered:**
- Setting up LangGraph state for research workflow
- Implementing query decomposition node
- Creating search nodes with Tavily/SerpAPI
- Building source validation and credibility scoring
- Implementing reflection node for self-critique
- Creating synthesis node with citation
- Adding confidence scoring and uncertainty handling
- Integrating human approval checkpoint
- Visualizing the research graph

**Key Points:**
- State should track queries, sources, findings, and confidence
- Query decomposition improves coverage
- Credibility scoring prevents low-quality sources
- Reflection catches gaps and inconsistencies
- Synthesis must cite sources properly
- Confidence scores help users interpret results

### Exercise: Chain-of-Thought Reasoning with Self-Critique

*Implement reasoning with reflection loops*

**Topics Covered:**
- Create reasoning node that generates chain-of-thought
- Implement self-critique node that evaluates reasoning
- Build reflection loop that refines answers
- Add confidence scoring based on critique
- Handle cases where reflection improves vs degrades quality

### Exercise: Source Discovery with Credibility Scoring

*Build source validation pipeline*

**Topics Covered:**
- Implement search tool integration
- Create source metadata extraction
- Build credibility scoring function
- Filter sources by credibility threshold
- Rank sources by relevance and credibility
- Handle source diversity (avoid duplicates)

### Challenge: Full Deep Research Pipeline

*Create complete deep research system with multi-source synthesis*

**Topics Covered:**
- Query decomposition and planning
- Iterative search with refinement
- Source validation and credibility scoring
- Reflection and self-critique loops
- Multi-source synthesis with citation
- Confidence scoring and uncertainty handling
- Human approval checkpoint

### Reflection: Research Ethics, Citation, and Bias Awareness

*Consolidate learning and discuss ethical considerations*

**Topics Covered:**
- Summary of deep research patterns
- Research ethics: Attribution, bias, misinformation
- Citation best practices
- Handling conflicting sources
- Bias detection and mitigation
- Transparency in AI research
- Production considerations: Rate limits, costs, monitoring

**Key Points:**
- Always cite sources to enable verification
- Be transparent about confidence and uncertainty
- Detect and mitigate bias in sources
- Handle conflicts by presenting multiple perspectives
- Human oversight ensures ethical research
- Monitor for misinformation and low-quality sources

## Hands-On Exercises

### Exercise: Chain-of-Thought Reasoning with Self-Critique

Implement reasoning with reflection loops that improve answer quality

**Difficulty:** Medium | **Duration:** 20 minutes

**Hints:**
- Use ChatPromptTemplate for structured prompts
- Chain-of-thought should show step-by-step thinking
- Critique should identify specific issues, not just praise
- Refinement should address each critique point
- Confidence should increase after successful refinement

**Common Mistakes to Avoid:**
- Not showing actual reasoning steps in chain-of-thought
- Critique being too generic or not actionable
- Refinement not addressing specific critique points
- Not updating confidence scores
- Forgetting to add messages to state

### Exercise: Source Discovery with Credibility Scoring

Build source validation pipeline with credibility scoring

**Difficulty:** Hard | **Duration:** 25 minutes

**Hints:**
- Use domain-based heuristics for credibility scoring
- Consider URL patterns (.edu, .gov) for authority
- Filter by threshold and remove duplicates
- Sort sources by credibility score
- In production, use real search APIs (Tavily, SerpAPI)

**Common Mistakes to Avoid:**
- Not implementing actual credibility scoring logic
- Forgetting to filter low-quality sources
- Not handling duplicate sources
- Not sorting by credibility
- Using mock data instead of real search APIs

## Challenges

### Challenge: Full Deep Research Pipeline with Multi-Source Synthesis

Build a complete deep research system that decomposes queries, performs iterative searches, validates sources, reflects on findings, and synthesizes results

**Requirements:**
- Implement query decomposition that breaks complex questions into sub-queries
- Create iterative search with refinement (at least 2 iterations)
- Build source validation with credibility scoring
- Implement reflection loop with self-critique
- Create synthesis agent that aggregates findings with proper citation
- Add confidence scoring and uncertainty handling
- Include human approval checkpoint before final output
- Handle maximum iteration limits to prevent infinite loops
- Provide source citations in final output

**Evaluation Criteria:**
- Query decomposition creates meaningful sub-queries
- Iterative search improves result quality
- Sources are validated and filtered by credibility
- Reflection identifies gaps and improves answers
- Synthesis combines sources with proper attribution
- Confidence scores reflect actual uncertainty
- Human checkpoint works correctly
- System handles edge cases (no results, conflicting sources)
- Final output includes citations

**Stretch Goals:**
- Implement parallel sub-query execution
- Add source diversity scoring (avoid similar sources)
- Create visual graph of research flow
- Integrate with LangSmith for tracing
- Add bias detection in sources
- Implement query rewriting based on initial results

## Resources

**Official Documentation:**
- https://langchain-ai.github.io/langgraph/
- https://python.langchain.com/docs/use_cases/research/
- https://docs.tavily.com/
- https://serpapi.com/

**Tutorials:**
- LangGraph Research Agent Tutorial
- Building Deep Research Systems - LangChain Blog
- Chain-of-Thought Reasoning Patterns

**Videos:**
- Deep Research Agents Explained
- Building Perplexity-like Research Systems

## Self-Assessment

Ask yourself these questions:

- [ ] Can I design multi-step research workflows?
- [ ] Do I understand chain-of-thought and reflection patterns?
- [ ] Can I implement source discovery and validation?
- [ ] Can I create synthesis agents with proper citation?
- [ ] Do I know when to add human-in-the-loop checkpoints?
- [ ] Can I handle uncertainty and express confidence appropriately?

## Next Steps

**Next Workshop:** `L5_crewai_multiagent`

**Practice Projects:**
- Build a research assistant for academic papers
- Create a fact-checking agent with source validation
- Implement a competitive analysis research system
- Build a news aggregation system with bias detection

**Deeper Learning:**
- Advanced reasoning patterns (tree-of-thought, self-consistency)
- Multi-agent research systems with specialized agents
- Bias detection and mitigation techniques
- Production deployment of research agents

## Related Knowledge Files

- `research-agent-patterns.json`
- `langgraph-workflows.json`
- `reasoning-patterns.json`

---

*Part of the Antigravity Agent Factory Learning Workshop Ecosystem*

**Workshop Definition:** `patterns/workshops/L18_deep_research_agents.json`
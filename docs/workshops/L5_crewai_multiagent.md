# CrewAI Multi-Agent Systems

> **Stack:** CrewAI | **Level:** Fundamentals | **Duration:** 2.5 hours

## Overview

**Workshop ID:** `L5_crewai_multiagent`

**Technology:** Python with CrewAI (CrewAI 0.30+)

## Prerequisites

**Required Knowledge:**
- Python programming (classes, decorators)
- Basic understanding of LLMs and agents
- Object-oriented programming concepts

**Required Tools:**
- Python 3.10+
- OpenAI API key (or other LLM provider)
- VS Code or similar IDE

## Learning Objectives

By the end of this workshop, you will be able to:

1. **Understand CrewAI's core concepts: agents, tasks, and crews** (Understand)
2. **Create specialized agents with roles, goals, and backstories** (Apply)
3. **Define tasks with expected outputs and agent assignments** (Apply)
4. **Orchestrate crews with sequential and hierarchical execution patterns** (Apply)
5. **Implement Flows for complex state management and multi-step workflows** (Apply)

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

### Concept: CrewAI Architecture Overview

*Understand the building blocks of CrewAI multi-agent systems*

**Topics Covered:**
- Agent: Role, Goal, Backstory, and Tools
- Task: Description, Expected Output, and Agent Assignment
- Crew: Sequential vs Hierarchical Execution
- Process: How agents collaborate and share context
- Flows: State management and complex workflows
- Memory: Context sharing between agents

**Key Points:**
- Agents are specialized with clear roles and goals
- Tasks define what needs to be done and by whom
- Crews orchestrate agent collaboration
- Sequential crews execute tasks one after another
- Hierarchical crews enable manager-worker patterns
- Flows provide state management for complex workflows

### Demo: Building a Research Crew

*Live coding a multi-agent research system*

**Topics Covered:**
- Creating researcher agent with web search tool
- Creating writer agent for report generation
- Defining research and writing tasks
- Orchestrating crew with sequential execution
- Adding memory for context sharing
- Handling errors and retries

**Key Points:**
- Clear role definition improves agent performance
- Expected outputs guide agent behavior
- Sequential execution ensures proper task ordering
- Memory enables context sharing between agents

### Exercise: Creating an Analyst Team

*Build a crew of specialized analysts*

**Topics Covered:**
- Create data analyst agent
- Create market analyst agent
- Create report writer agent
- Define analysis tasks
- Orchestrate crew execution
- Handle task dependencies

### Challenge: Multi-Step Workflow with Flows

*Build a complex workflow using Flows*

**Topics Covered:**
- Design workflow state machine
- Create Flow with state transitions
- Implement conditional logic
- Handle error states
- Add human-in-the-loop steps

### Reflection: Key Takeaways and Best Practices

*Consolidate learning and discuss production considerations*

**Topics Covered:**
- Summary of CrewAI patterns
- Agent design best practices
- Task orchestration strategies
- Production considerations (costs, monitoring, error handling)
- Resources for continued learning

**Key Points:**
- Clear role definition is critical for agent performance
- Task ordering matters in sequential crews
- Use Flows for complex stateful workflows
- Monitor token usage and costs
- Implement proper error handling

## Hands-On Exercises

### Exercise: Analyst Team Crew

Create a crew of specialized analysts working together

**Difficulty:** Medium | **Duration:** 45 minutes

**Hints:**
- Define clear, specific roles for each agent
- Make goals actionable and measurable
- Backstories should provide context for agent behavior
- Expected outputs should be specific and clear
- Use sequential process for dependent tasks

**Common Mistakes to Avoid:**
- Vague role or goal definitions
- Unclear expected outputs
- Wrong task ordering
- Missing agent assignments
- Not using sequential process when tasks depend on each other

## Challenges

### Challenge: Multi-Step Workflow with Flows

Build a complex workflow using CrewAI Flows for state management

**Requirements:**
- Design a workflow with at least 3 states
- Create Flow with state transitions
- Implement conditional logic based on state
- Handle error states gracefully
- Include at least one human-in-the-loop step
- Use multiple agents in the workflow

**Evaluation Criteria:**
- Flow correctly transitions between states
- Conditional logic works as expected
- Error handling is implemented
- Human-in-the-loop step is functional
- Agents collaborate effectively
- Final output is produced

**Stretch Goals:**
- Add parallel agent execution
- Implement retry logic with exponential backoff
- Add workflow visualization
- Create API endpoint for workflow execution

## Resources

**Official Documentation:**
- https://docs.crewai.com/
- https://github.com/joaomdmoura/crewAI

**Tutorials:**
- https://docs.crewai.com/tutorials/
- https://docs.crewai.com/how-to/Flows/

## Self-Assessment

Ask yourself these questions:

- [ ] Can I explain the relationship between agents, tasks, and crews?
- [ ] Do I understand how to create effective agent roles and goals?
- [ ] Can I orchestrate a crew with proper task ordering?
- [ ] Do I know when to use Flows vs simple Crews?

## Next Steps

**Next Workshop:** `L7_langchain_fundamentals`

**Practice Projects:**
- Customer research crew with multiple analysts
- Code review crew with specialized reviewers
- Content creation crew with writer, editor, and publisher

**Deeper Learning:**
- Advanced Flow patterns
- Custom tool development
- Production deployment and monitoring

## Related Knowledge Files

- `crewai-patterns.json`
- `multi-agent-patterns.json`

---

*Part of the Antigravity Agent Factory Learning Workshop Ecosystem*

**Workshop Definition:** `patterns/workshops/L5_crewai_multiagent.json`
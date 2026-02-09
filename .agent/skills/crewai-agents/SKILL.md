---
description: Detailed CrewAI agent design patterns - role design, backstories, collaboration, hierarchical vs sequential processes, tool integration
---

# Crewai Agents

Detailed CrewAI agent design patterns - role design, backstories, collaboration, hierarchical vs sequential processes, tool integration

## 
# CrewAI Agents Skill

Design and implement production-ready CrewAI agents with proper role design, backstories, collaboration patterns, and tool integration.

## 
# CrewAI Agents Skill

Design and implement production-ready CrewAI agents with proper role design, backstories, collaboration patterns, and tool integration.

## Process
### Step 1: Design Agent Roles

Create agents with clear, focused roles:

```python
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Research Agent - Focused on information gathering
researcher = Agent(
    role='Senior Research Analyst',
    goal='Conduct thorough research and provide accurate, well-sourced information',
    backstory="""You are an experienced research analyst with a PhD in data science.
    You have spent 15 years analyzing complex topics and synthesizing information
    from multiple sources. You are meticulous, detail-oriented, and never accept
    information at face value. You always verify sources and cross-reference data.""",
    verbose=True,
    allow_delegation=False,
    max_iter=5,
    llm=llm
)

# Writer Agent - Focused on content creation
writer = Agent(
    role='Technical Content Writer',
    goal='Transform research into engaging, clear, and well-structured content',
    backstory="""You are a skilled technical writer with 10 years of experience
    translating complex technical concepts into accessible content. You have written
    for major tech publications and understand how to balance technical accuracy
    with readability. You excel at creating narratives that engage readers while
    maintaining precision.""",
    verbose=True,
    allow_delegation=False,
    max_iter=3,
    llm=llm
)

# Reviewer Agent - Focused on quality assurance
reviewer = Agent(
    role='Quality Assurance Editor',
    goal='Ensure content accuracy, clarity, and adherence to standards',
    backstory="""You are a meticulous editor with a background in technical
    documentation. You have an eagle eye for inconsistencies, factual errors,
    and unclear explanations. You are known for your constructive feedback and
    ability to improve content without losing the author's voice.""",
    verbose=True,
    allow_delegation=False,
    max_iter=3,
    llm=llm
)
```

### Step 2: Craft Effective Backstories

Backstories guide agent behavior and decision-making:

```python
# Good: Specific, detailed backstory
expert_analyst = Agent(
    role='Financial Market Analyst',
    goal='Analyze market trends and provide investment insights',
    backstory="""You are a CFA-certified financial analyst with 20 years of
    experience in equity research. You've worked at top-tier investment banks
    and have a track record of accurate market predictions. You specialize in
    technology sector analysis and have deep knowledge of SaaS business models.
    You are conservative in your approach, always considering downside risks,
    and you never make recommendations without thorough due diligence.""",
    verbose=True
)

# Bad: Vague backstory
vague_analyst = Agent(
    role='Analyst',
    goal='Analyze things',
    backstory='You are an analyst.',
    verbose=True
)
```

### Step 3: Configure Agent Collaboration

Control how agents interact and delegate:

```python
# Manager agent that can delegate
manager = Agent(
    role='Project Manager',
    goal='Coordinate team efforts and ensure quality deliverables',
    backstory="""You are an experienced project manager who excels at breaking
    down complex projects into manageable tasks and assigning them to the right
    team members. You understand each team member's strengths and delegate
    accordingly.""",
    verbose=True,
    allow_delegation=True,  # Can delegate to other agents
    max_iter=10,
    llm=llm
)

# Worker agent that cannot delegate
worker = Agent(
    role='Data Processor',
    goal='Process and clean data according to specifications',
    backstory="""You are a data processing specialist focused on data quality
    and accuracy. You follow procedures precisely and don't delegate your work.""",
    verbose=True,
    allow_delegation=False,  # Cannot delegate
    max_iter=5,
    llm=llm
)
```

### Step 4: Integrate Tools with Agents

Attach tools to agents for extended capabilities:

```python
from crewai_tools import (
    FileReadTool,
    DirectoryReadTool,
    WebSearchTool,
    WebsiteSearchTool,
    SerperDevTool,
    CodeDocsSearchTool,
)

# Research agent with web search capabilities
researcher_with_tools = Agent(
    role='Research Analyst',
    goal='Find accurate, up-to-date information',
    backstory='Expert researcher with access to web search tools',
    verbose=True,
    tools=[
        WebSearchTool(),
        SerperDevTool(),  # Requires SERPER_API_KEY
        WebsiteSearchTool(website='https://docs.crewai.com'),
    ],
    llm=llm
)

# Developer agent with code tools
developer = Agent(
    role='Senior Software Engineer',
    goal='Write clean, maintainable code',
    backstory='Experienced developer who writes production-quality code',
    verbose=True,
    tools=[
        FileReadTool(),
        DirectoryReadTool(),
        CodeDocsSearchTool(),
    ],
    llm=llm
)

# Custom tool integration
from crewai.tools import tool

@tool("Custom API Tool")
def fetch_user_data(user_id: str) -> str:
    """Fetch user data from internal API.
    
    Args:
        user_id: The unique identifier for the user
    """
    # Implementation
    return f"User data for {user_id}"

api_agent = Agent(
    role='API Integration Specialist',
    goal='Integrate with external APIs',
    backstory='Expert in API integration and data transformation',
    verbose=True,
    tools=[fetch_user_data],
    llm=llm
)
```

### Step 5: Sequential Process

Tasks execute one after another:

```python
from crewai import Crew, Task, Process

# Define tasks with dependencies
research_task = Task(
    description='Research the topic: {topic}. Focus on recent developments and key insights.',
    agent=researcher,
    expected_output='Comprehensive research report with key findings, sources, and insights'
)

writing_task = Task(
    description='Write an engaging article based on the research. Target audience: {audience}',
    agent=writer,
    expected_output='Well-structured article in markdown format with introduction, body, and conclusion',
    context=[research_task]  # Depends on research_task output
)

review_task = Task(
    description='Review the article for accuracy, clarity, and quality. Check facts and suggest improvements.',
    agent=reviewer,
    expected_output='Reviewed article with feedback and corrections',
    context=[writing_task]  # Depends on writing_task output
)

# Sequential crew - tasks run in order
sequential_crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[research_task, writing_task, review_task],
    process=Process.sequential,
    verbose=True,
    memory=True
)

result = sequential_crew.kickoff(
    inputs={
        "topic": "AI Agents in Production",
        "audience": "technical professionals"
    }
)
```

### Step 6: Hierarchical Process

Manager delegates to workers:

```python
# Manager agent
manager = Agent(
    role='Content Production Manager',
    goal='Oversee content creation process and ensure quality',
    backstory="""You are a seasoned content production manager with expertise
    in coordinating multi-stage content creation workflows. You break down
    complex projects and delegate to specialists.""",
    verbose=True,
    allow_delegation=True,
    max_iter=15,
    llm=llm
)

# Worker agents
researcher = Agent(
    role='Research Specialist',
    goal='Conduct thorough research',
    backstory='Expert researcher',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

writer = Agent(
    role='Content Writer',
    goal='Create engaging content',
    backstory='Skilled writer',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Single complex task delegated by manager
content_task = Task(
    description='Create comprehensive content about {topic} for {audience}',
    agent=manager,
    expected_output='Complete, reviewed content ready for publication'
)

# Hierarchical crew
hierarchical_crew = Crew(
    agents=[manager, researcher, writer, reviewer],
    tasks=[content_task],
    process=Process.hierarchical,
    manager_llm=llm,
    verbose=True
)

result = hierarchical_crew.kickoff(
    inputs={
        "topic": "LangChain Agents",
        "audience": "developers"
    }
)
```

### Step 7: Agent Memory Configuration

Enable memory for better context retention:

```python
# Agent with memory enabled
memory_agent = Agent(
    role='Conversational Assistant',
    goal='Maintain context across conversations',
    backstory='Helpful assistant that remembers previous interactions',
    verbose=True,
    memory=True,  # Enables conversation memory
    max_iter=5,
    llm=llm
)

# Crew with memory
memory_crew = Crew(
    agents=[memory_agent],
    tasks=[conversation_task],
    process=Process.sequential,
    memory=True,  # Crew-level memory
    verbose=True
)
```

### Step 8: Advanced Agent Configuration

Fine-tune agent behavior:

```python
# Agent with custom LLM configuration
custom_agent = Agent(
    role='Creative Writer',
    goal='Generate creative content',
    backstory='Imaginative writer with unique style',
    verbose=True,
    llm=ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.9,  # Higher creativity
        max_tokens=2000
    ),
    max_iter=5,
    allow_delegation=False
)

# Agent with step callback
def agent_callback(step):
    print(f"Agent: {step.agent.role}")
    print(f"Action: {step.action}")
    print(f"Observation: {step.observation}")

monitored_agent = Agent(
    role='Monitored Agent',
    goal='Execute tasks with monitoring',
    backstory='Agent with execution monitoring',
    verbose=True,
    step_callback=agent_callback,
    llm=llm
)
```

```python
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Research Agent - Focused on information gathering
researcher = Agent(
    role='Senior Research Analyst',
    goal='Conduct thorough research and provide accurate, well-sourced information',
    backstory="""You are an experienced research analyst with a PhD in data science.
    You have spent 15 years analyzing complex topics and synthesizing information
    from multiple sources. You are meticulous, detail-oriented, and never accept
    information at face value. You always verify sources and cross-reference data.""",
    verbose=True,
    allow_delegation=False,
    max_iter=5,
    llm=llm
)

# Writer Agent - Focused on content creation
writer = Agent(
    role='Technical Content Writer',
    goal='Transform research into engaging, clear, and well-structured content',
    backstory="""You are a skilled technical writer with 10 years of experience
    translating complex technical concepts into accessible content. You have written
    for major tech publications and understand how to balance technical accuracy
    with readability. You excel at creating narratives that engage readers while
    maintaining precision.""",
    verbose=True,
    allow_delegation=False,
    max_iter=3,
    llm=llm
)

# Reviewer Agent - Focused on quality assurance
reviewer = Agent(
    role='Quality Assurance Editor',
    goal='Ensure content accuracy, clarity, and adherence to standards',
    backstory="""You are a meticulous editor with a background in technical
    documentation. You have an eagle eye for inconsistencies, factual errors,
    and unclear explanations. You are known for your constructive feedback and
    ability to improve content without losing the author's voice.""",
    verbose=True,
    allow_delegation=False,
    max_iter=3,
    llm=llm
)
```

```python
# Good: Specific, detailed backstory
expert_analyst = Agent(
    role='Financial Market Analyst',
    goal='Analyze market trends and provide investment insights',
    backstory="""You are a CFA-certified financial analyst with 20 years of
    experience in equity research. You've worked at top-tier investment banks
    and have a track record of accurate market predictions. You specialize in
    technology sector analysis and have deep knowledge of SaaS business models.
    You are conservative in your approach, always considering downside risks,
    and you never make recommendations without thorough due diligence.""",
    verbose=True
)

# Bad: Vague backstory
vague_analyst = Agent(
    role='Analyst',
    goal='Analyze things',
    backstory='You are an analyst.',
    verbose=True
)
```

```python
# Manager agent that can delegate
manager = Agent(
    role='Project Manager',
    goal='Coordinate team efforts and ensure quality deliverables',
    backstory="""You are an experienced project manager who excels at breaking
    down complex projects into manageable tasks and assigning them to the right
    team members. You understand each team member's strengths and delegate
    accordingly.""",
    verbose=True,
    allow_delegation=True,  # Can delegate to other agents
    max_iter=10,
    llm=llm
)

# Worker agent that cannot delegate
worker = Agent(
    role='Data Processor',
    goal='Process and clean data according to specifications',
    backstory="""You are a data processing specialist focused on data quality
    and accuracy. You follow procedures precisely and don't delegate your work.""",
    verbose=True,
    allow_delegation=False,  # Cannot delegate
    max_iter=5,
    llm=llm
)
```

```python
from crewai_tools import (
    FileReadTool,
    DirectoryReadTool,
    WebSearchTool,
    WebsiteSearchTool,
    SerperDevTool,
    CodeDocsSearchTool,
)

# Research agent with web search capabilities
researcher_with_tools = Agent(
    role='Research Analyst',
    goal='Find accurate, up-to-date information',
    backstory='Expert researcher with access to web search tools',
    verbose=True,
    tools=[
        WebSearchTool(),
        SerperDevTool(),  # Requires SERPER_API_KEY
        WebsiteSearchTool(website='https://docs.crewai.com'),
    ],
    llm=llm
)

# Developer agent with code tools
developer = Agent(
    role='Senior Software Engineer',
    goal='Write clean, maintainable code',
    backstory='Experienced developer who writes production-quality code',
    verbose=True,
    tools=[
        FileReadTool(),
        DirectoryReadTool(),
        CodeDocsSearchTool(),
    ],
    llm=llm
)

# Custom tool integration
from crewai.tools import tool

@tool("Custom API Tool")
def fetch_user_data(user_id: str) -> str:
    """Fetch user data from internal API.
    
    Args:
        user_id: The unique identifier for the user
    """
    # Implementation
    return f"User data for {user_id}"

api_agent = Agent(
    role='API Integration Specialist',
    goal='Integrate with external APIs',
    backstory='Expert in API integration and data transformation',
    verbose=True,
    tools=[fetch_user_data],
    llm=llm
)
```

```python
from crewai import Crew, Task, Process

# Define tasks with dependencies
research_task = Task(
    description='Research the topic: {topic}. Focus on recent developments and key insights.',
    agent=researcher,
    expected_output='Comprehensive research report with key findings, sources, and insights'
)

writing_task = Task(
    description='Write an engaging article based on the research. Target audience: {audience}',
    agent=writer,
    expected_output='Well-structured article in markdown format with introduction, body, and conclusion',
    context=[research_task]  # Depends on research_task output
)

review_task = Task(
    description='Review the article for accuracy, clarity, and quality. Check facts and suggest improvements.',
    agent=reviewer,
    expected_output='Reviewed article with feedback and corrections',
    context=[writing_task]  # Depends on writing_task output
)

# Sequential crew - tasks run in order
sequential_crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[research_task, writing_task, review_task],
    process=Process.sequential,
    verbose=True,
    memory=True
)

result = sequential_crew.kickoff(
    inputs={
        "topic": "AI Agents in Production",
        "audience": "technical professionals"
    }
)
```

```python
# Manager agent
manager = Agent(
    role='Content Production Manager',
    goal='Oversee content creation process and ensure quality',
    backstory="""You are a seasoned content production manager with expertise
    in coordinating multi-stage content creation workflows. You break down
    complex projects and delegate to specialists.""",
    verbose=True,
    allow_delegation=True,
    max_iter=15,
    llm=llm
)

# Worker agents
researcher = Agent(
    role='Research Specialist',
    goal='Conduct thorough research',
    backstory='Expert researcher',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

writer = Agent(
    role='Content Writer',
    goal='Create engaging content',
    backstory='Skilled writer',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Single complex task delegated by manager
content_task = Task(
    description='Create comprehensive content about {topic} for {audience}',
    agent=manager,
    expected_output='Complete, reviewed content ready for publication'
)

# Hierarchical crew
hierarchical_crew = Crew(
    agents=[manager, researcher, writer, reviewer],
    tasks=[content_task],
    process=Process.hierarchical,
    manager_llm=llm,
    verbose=True
)

result = hierarchical_crew.kickoff(
    inputs={
        "topic": "LangChain Agents",
        "audience": "developers"
    }
)
```

```python
# Agent with memory enabled
memory_agent = Agent(
    role='Conversational Assistant',
    goal='Maintain context across conversations',
    backstory='Helpful assistant that remembers previous interactions',
    verbose=True,
    memory=True,  # Enables conversation memory
    max_iter=5,
    llm=llm
)

# Crew with memory
memory_crew = Crew(
    agents=[memory_agent],
    tasks=[conversation_task],
    process=Process.sequential,
    memory=True,  # Crew-level memory
    verbose=True
)
```

```python
# Agent with custom LLM configuration
custom_agent = Agent(
    role='Creative Writer',
    goal='Generate creative content',
    backstory='Imaginative writer with unique style',
    verbose=True,
    llm=ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.9,  # Higher creativity
        max_tokens=2000
    ),
    max_iter=5,
    allow_delegation=False
)

# Agent with step callback
def agent_callback(step):
    print(f"Agent: {step.agent.role}")
    print(f"Action: {step.action}")
    print(f"Observation: {step.observation}")

monitored_agent = Agent(
    role='Monitored Agent',
    goal='Execute tasks with monitoring',
    backstory='Agent with execution monitoring',
    verbose=True,
    step_callback=agent_callback,
    llm=llm
)
```

## Agent Design Patterns
| Pattern | Use Case | Example |
|---------|----------|---------|
| **Specialist** | Single focused responsibility | Research-only agent |
| **Generalist** | Multiple related capabilities | Full-stack developer agent |
| **Manager** | Coordination and delegation | Project manager agent |
| **Worker** | Task execution | Data processor agent |
| **Reviewer** | Quality assurance | Editor agent |
| **Collaborator** | Peer-to-peer interaction | Pair programming agent |

## Role Design Best Practices
1. **Single Responsibility**: Each agent should have ONE clear purpose
2. **Specific Goals**: Goals should be measurable and actionable
3. **Rich Backstories**: Include experience level, expertise areas, and behavioral traits
4. **Appropriate Constraints**: Set `max_iter` to prevent infinite loops
5. **Delegation Control**: Use `allow_delegation` strategically
6. **Tool Selection**: Match tools to agent capabilities

## Backstory Guidelines
| Element | Description | Example |
|---------|-------------|---------|
| **Experience** | Years/level of expertise | "15 years of experience" |
| **Specialization** | Specific domain knowledge | "SaaS business models" |
| **Behavioral Traits** | How agent approaches tasks | "Meticulous, detail-oriented" |
| **Context** | Relevant background | "Worked at top-tier banks" |
| **Constraints** | What agent won't do | "Never accepts unverified data" |

## Process Comparison
| Aspect | Sequential | Hierarchical |
|--------|-----------|--------------|
| **Control Flow** | Linear, predefined | Manager-driven |
| **Delegation** | Explicit task dependencies | Dynamic delegation |
| **Use Case** | Pipeline workflows | Complex coordination |
| **Flexibility** | Lower | Higher |
| **Complexity** | Simpler | More complex |

## Tool Integration Patterns
```python
# Pattern 1: Agent-specific tools
researcher.tools = [WebSearchTool(), SerperDevTool()]

# Pattern 2: Shared tools across agents
shared_tools = [FileReadTool(), DirectoryReadTool()]
researcher.tools = shared_tools
writer.tools = shared_tools

# Pattern 3: Custom tool creation
@tool("Domain-specific tool")
def specialized_function(param: str) -> str:
    """Tool description for LLM."""
    return result

agent.tools = [specialized_function]
```

```python
# Pattern 1: Agent-specific tools
researcher.tools = [WebSearchTool(), SerperDevTool()]

# Pattern 2: Shared tools across agents
shared_tools = [FileReadTool(), DirectoryReadTool()]
researcher.tools = shared_tools
writer.tools = shared_tools

# Pattern 3: Custom tool creation
@tool("Domain-specific tool")
def specialized_function(param: str) -> str:
    """Tool description for LLM."""
    return result

agent.tools = [specialized_function]
```

## Best Practices
- Design roles with clear boundaries and responsibilities
- Write detailed backstories that guide behavior
- Set appropriate `max_iter` limits (3-10 typically)
- Use `allow_delegation` strategically based on agent role
- Match tools to agent capabilities and needs
- Enable memory for conversational or multi-turn workflows
- Use sequential process for pipelines, hierarchical for coordination
- Test agents individually before combining into crews
- Monitor agent execution with callbacks for debugging

## Anti-Patterns
| Anti-Pattern | Fix |
|--------------|-----|
| Vague roles | Define specific, focused roles |
| Generic backstories | Add experience, expertise, and behavioral details |
| No max_iter limit | Set appropriate iteration limits |
| Over-delegation | Use `allow_delegation=False` for workers |
| Tool mismatch | Match tools to agent responsibilities |
| No memory for multi-turn | Enable `memory=True` when needed |
| Wrong process type | Use sequential for pipelines, hierarchical for coordination |
| Too many agents | Consolidate overlapping roles |

## Related
- Knowledge: `knowledge/crewai-patterns.json`
- Skill: `crewai-workflow`
- Skill: `tool-usage`
- Skill: `memory-management`

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Packages: crewai, crewai-tools
> - Knowledge: crewai-patterns.json

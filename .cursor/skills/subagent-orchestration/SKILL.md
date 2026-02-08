---
name: subagent-orchestration
description: Spawning subagents dynamically, parent-child agent communication, task delegation and result aggregation, resource management and cleanup
type: skill
agents: [code-reviewer, test-generator]
knowledge: [subagent-patterns.json]
---

# Subagent Orchestration Skill

Design and implement systems that spawn and manage subagents dynamically, coordinate parent-child communication, and handle resource management.

## When to Use

- Building agents that need to delegate to specialized subagents
- Creating hierarchical agent architectures
- Implementing dynamic task decomposition
- Managing multiple concurrent agent instances
- Coordinating complex multi-agent workflows

## Prerequisites

```bash
pip install langchain langchain-core langgraph
# Or framework-specific packages
pip install crewai  # For CrewAI subagents
```

## Process

### Step 1: Basic Subagent Spawning

Create a parent agent that spawns subagents:

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from typing import Dict, List
import asyncio

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class Subagent:
    """Represents a spawned subagent."""
    def __init__(self, agent_id: str, role: str, llm):
        self.agent_id = agent_id
        self.role = role
        self.llm = llm
        self.messages = []
        self.status = "idle"
    
    async def execute_task(self, task: str) -> str:
        """Execute a task assigned by parent."""
        self.status = "working"
        self.messages.append(HumanMessage(content=task))
        
        response = await self.llm.ainvoke(self.messages)
        self.messages.append(response)
        self.status = "completed"
        
        return response.content

class ParentAgent:
    """Parent agent that spawns and manages subagents."""
    def __init__(self, llm):
        self.llm = llm
        self.subagents: Dict[str, Subagent] = {}
        self.task_queue = []
    
    async def spawn_subagent(self, agent_id: str, role: str) -> Subagent:
        """Spawn a new subagent."""
        subagent = Subagent(agent_id, role, self.llm)
        self.subagents[agent_id] = subagent
        return subagent
    
    async def delegate_task(self, agent_id: str, task: str) -> str:
        """Delegate a task to a subagent."""
        if agent_id not in self.subagents:
            raise ValueError(f"Subagent {agent_id} not found")
        
        subagent = self.subagents[agent_id]
        result = await subagent.execute_task(task)
        return result
    
    async def cleanup_subagent(self, agent_id: str):
        """Clean up a subagent."""
        if agent_id in self.subagents:
            del self.subagents[agent_id]

# Usage
parent = ParentAgent(llm)

# Spawn subagents
researcher = await parent.spawn_subagent("researcher_1", "Research Specialist")
writer = await parent.spawn_subagent("writer_1", "Content Writer")

# Delegate tasks
research_result = await parent.delegate_task("researcher_1", "Research AI trends")
content = await parent.delegate_task("writer_1", f"Write article based on: {research_result}")

# Cleanup
await parent.cleanup_subagent("researcher_1")
await parent.cleanup_subagent("writer_1")
```

### Step 2: Dynamic Task Decomposition

Parent agent decomposes tasks and spawns subagents as needed:

```python
class TaskDecomposer:
    """Decomposes complex tasks into subtasks."""
    def __init__(self, llm):
        self.llm = llm
    
    async def decompose_task(self, task: str) -> List[Dict]:
        """Break down a task into subtasks with agent assignments."""
        prompt = f"""Break down this task into subtasks and assign each to a specialist agent.
        
        Task: {task}
        
        Return a JSON list of subtasks, each with:
        - subtask: description
        - agent_role: required specialist role
        - dependencies: list of subtask IDs this depends on
        
        Example format:
        [
            {{"id": 1, "subtask": "Research topic", "agent_role": "Researcher", "dependencies": []}},
            {{"id": 2, "subtask": "Write content", "agent_role": "Writer", "dependencies": [1]}}
        ]"""
        
        response = await self.llm.ainvoke(prompt)
        # Parse JSON response
        import json
        subtasks = json.loads(response.content)
        return subtasks

class Orchestrator:
    """Orchestrates subagents for complex tasks."""
    def __init__(self, llm):
        self.llm = llm
        self.decomposer = TaskDecomposer(llm)
        self.subagents: Dict[str, Subagent] = {}
        self.results: Dict[int, str] = {}
    
    async def execute_complex_task(self, task: str):
        """Execute a complex task by decomposing and delegating."""
        # Decompose task
        subtasks = await self.decomposer.decompose_task(task)
        
        # Spawn subagents as needed
        agent_roles = set(st["agent_role"] for st in subtasks)
        for role in agent_roles:
            agent_id = f"{role.lower()}_1"
            if agent_id not in self.subagents:
                await self.spawn_subagent(agent_id, role)
        
        # Execute subtasks respecting dependencies
        completed = set()
        while len(completed) < len(subtasks):
            for subtask in subtasks:
                subtask_id = subtask["id"]
                if subtask_id in completed:
                    continue
                
                # Check dependencies
                deps_met = all(dep in completed for dep in subtask.get("dependencies", []))
                if deps_met:
                    # Execute subtask
                    agent_id = f"{subtask['agent_role'].lower()}_1"
                    result = await self.delegate_task(agent_id, subtask["subtask"])
                    self.results[subtask_id] = result
                    completed.add(subtask_id)
        
        # Aggregate results
        final_result = await self.aggregate_results(subtasks)
        return final_result
    
    async def spawn_subagent(self, agent_id: str, role: str):
        """Spawn a subagent."""
        subagent = Subagent(agent_id, role, self.llm)
        self.subagents[agent_id] = subagent
    
    async def delegate_task(self, agent_id: str, task: str) -> str:
        """Delegate task to subagent."""
        return await self.subagents[agent_id].execute_task(task)
    
    async def aggregate_results(self, subtasks: List[Dict]) -> str:
        """Aggregate subagent results into final output."""
        results_text = "\n".join([
            f"Subtask {st['id']}: {self.results[st['id']]}"
            for st in subtasks
        ])
        
        prompt = f"""Synthesize these subagent results into a cohesive final output:
        
        {results_text}
        
        Provide a comprehensive summary."""
        
        response = await self.llm.ainvoke(prompt)
        return response.content

# Usage
orchestrator = Orchestrator(llm)
result = await orchestrator.execute_complex_task(
    "Create a comprehensive guide to LangChain agents"
)
```

### Step 3: Parent-Child Communication

Implement bidirectional communication:

```python
from dataclasses import dataclass
from typing import Optional
from enum import Enum

class MessageType(Enum):
    TASK = "task"
    RESULT = "result"
    QUERY = "query"
    STATUS = "status"

@dataclass
class AgentMessage:
    """Message between parent and child agents."""
    message_type: MessageType
    content: str
    sender_id: str
    receiver_id: Optional[str] = None
    task_id: Optional[str] = None
    metadata: Optional[Dict] = None

class CommunicatingSubagent(Subagent):
    """Subagent with communication capabilities."""
    def __init__(self, agent_id: str, role: str, llm, parent_id: str):
        super().__init__(agent_id, role, llm)
        self.parent_id = parent_id
        self.message_queue = []
    
    async def send_to_parent(self, message_type: MessageType, content: str, task_id: str = None):
        """Send message to parent agent."""
        message = AgentMessage(
            message_type=message_type,
            content=content,
            sender_id=self.agent_id,
            receiver_id=self.parent_id,
            task_id=task_id
        )
        self.message_queue.append(message)
        return message
    
    async def receive_from_parent(self) -> Optional[AgentMessage]:
        """Receive message from parent."""
        if self.message_queue:
            return self.message_queue.pop(0)
        return None

class CommunicatingParentAgent(ParentAgent):
    """Parent agent with communication capabilities."""
    def __init__(self, llm, parent_id: str = "parent"):
        super().__init__(llm)
        self.parent_id = parent_id
        self.message_queue = []
    
    async def send_to_subagent(self, agent_id: str, message_type: MessageType, content: str, task_id: str = None):
        """Send message to subagent."""
        if agent_id not in self.subagents:
            raise ValueError(f"Subagent {agent_id} not found")
        
        message = AgentMessage(
            message_type=message_type,
            content=content,
            sender_id=self.parent_id,
            receiver_id=agent_id,
            task_id=task_id
        )
        
        subagent = self.subagents[agent_id]
        if isinstance(subagent, CommunicatingSubagent):
            subagent.message_queue.append(message)
        
        return message
    
    async def receive_from_subagent(self) -> Optional[AgentMessage]:
        """Receive message from any subagent."""
        # Check all subagents for messages
        for subagent in self.subagents.values():
            if isinstance(subagent, CommunicatingSubagent):
                message = await subagent.receive_from_parent()
                if message:
                    self.message_queue.append(message)
                    return message
        return None
    
    async def query_subagent_status(self, agent_id: str) -> str:
        """Query subagent status."""
        message = await self.send_to_subagent(
            agent_id,
            MessageType.QUERY,
            "What is your current status?"
        )
        # Wait for response
        await asyncio.sleep(0.1)
        response = await self.receive_from_subagent()
        return response.content if response else "No response"

# Usage
parent = CommunicatingParentAgent(llm, "parent_1")

# Spawn communicating subagent
subagent = CommunicatingSubagent("worker_1", "Worker", llm, "parent_1")
parent.subagents["worker_1"] = subagent

# Send task
await parent.send_to_subagent("worker_1", MessageType.TASK, "Process this data")

# Subagent sends result
await subagent.send_to_parent(MessageType.RESULT, "Task completed", task_id="task_1")

# Parent receives result
result_message = await parent.receive_from_subagent()
print(f"Received: {result_message.content}")
```

### Step 4: Result Aggregation Patterns

Aggregate results from multiple subagents:

```python
class ResultAggregator:
    """Aggregates results from multiple subagents."""
    def __init__(self, llm):
        self.llm = llm
    
    async def aggregate_parallel_results(self, results: Dict[str, str]) -> str:
        """Aggregate results from parallel subagent execution."""
        results_text = "\n".join([
            f"Agent {agent_id}: {result}"
            for agent_id, result in results.items()
        ])
        
        prompt = f"""Synthesize these parallel results into a unified output:
        
        {results_text}
        
        Provide a comprehensive synthesis."""
        
        response = await self.llm.ainvoke(prompt)
        return response.content
    
    async def aggregate_sequential_results(self, results: List[str], context: str = "") -> str:
        """Aggregate results from sequential subagent execution."""
        results_text = "\n\n".join([
            f"Step {i+1}: {result}"
            for i, result in enumerate(results)
        ])
        
        prompt = f"""Synthesize these sequential results into a final output:
        
        Context: {context}
        
        {results_text}
        
        Provide a cohesive final result."""
        
        response = await self.llm.ainvoke(prompt)
        return response.content
    
    async def aggregate_with_voting(self, results: List[str], question: str) -> str:
        """Aggregate results using voting/consensus."""
        results_text = "\n".join([
            f"Agent {i+1}: {result}"
            for i, result in enumerate(results)
        ])
        
        prompt = f"""Multiple agents answered this question. Determine the consensus:
        
        Question: {question}
        
        Answers:
        {results_text}
        
        Provide the consensus answer, noting any disagreements."""
        
        response = await self.llm.ainvoke(prompt)
        return response.content

# Usage
aggregator = ResultAggregator(llm)

# Parallel aggregation
parallel_results = {
    "researcher_1": "Found 10 sources on topic X",
    "researcher_2": "Found 8 sources on topic Y",
    "researcher_3": "Found 12 sources on topic Z"
}
synthesis = await aggregator.aggregate_parallel_results(parallel_results)

# Sequential aggregation
sequential_results = [
    "Research completed",
    "Analysis done",
    "Report written"
]
final = await aggregator.aggregate_sequential_results(sequential_results)
```

### Step 5: Resource Management and Cleanup

Manage subagent lifecycle and resources:

```python
import weakref
from contextlib import asynccontextmanager

class ResourceManager:
    """Manages subagent resources and cleanup."""
    def __init__(self):
        self.subagents: Dict[str, Subagent] = {}
        self.resource_tracking: Dict[str, Dict] = {}
    
    async def spawn_with_tracking(self, agent_id: str, role: str, llm) -> Subagent:
        """Spawn subagent with resource tracking."""
        subagent = Subagent(agent_id, role, llm)
        self.subagents[agent_id] = subagent
        
        # Track resources
        self.resource_tracking[agent_id] = {
            "created_at": asyncio.get_event_loop().time(),
            "status": "active",
            "task_count": 0,
            "memory_usage": 0
        }
        
        return subagent
    
    async def cleanup_subagent(self, agent_id: str):
        """Clean up subagent and release resources."""
        if agent_id not in self.subagents:
            return
        
        subagent = self.subagents[agent_id]
        
        # Save any necessary state
        # Clear messages if not needed
        subagent.messages = []
        subagent.status = "terminated"
        
        # Update tracking
        if agent_id in self.resource_tracking:
            self.resource_tracking[agent_id]["status"] = "terminated"
            self.resource_tracking[agent_id]["terminated_at"] = asyncio.get_event_loop().time()
        
        # Remove from active subagents
        del self.subagents[agent_id]
    
    async def cleanup_all(self):
        """Clean up all subagents."""
        agent_ids = list(self.subagents.keys())
        for agent_id in agent_ids:
            await self.cleanup_subagent(agent_id)
    
    def get_resource_stats(self) -> Dict:
        """Get resource usage statistics."""
        return {
            "active_agents": len([a for a in self.subagents.values() if a.status != "terminated"]),
            "total_agents": len(self.resource_tracking),
            "resource_tracking": self.resource_tracking
        }
    
    @asynccontextmanager
    async def managed_subagent(self, agent_id: str, role: str, llm):
        """Context manager for automatic cleanup."""
        subagent = await self.spawn_with_tracking(agent_id, role, llm)
        try:
            yield subagent
        finally:
            await self.cleanup_subagent(agent_id)

# Usage with context manager
resource_manager = ResourceManager()

async def use_managed_subagent():
    async with resource_manager.managed_subagent("temp_agent", "Worker", llm) as agent:
        result = await agent.execute_task("Do something")
        return result
    # Agent automatically cleaned up

# Manual cleanup
resource_manager = ResourceManager()
agent = await resource_manager.spawn_with_tracking("agent_1", "Worker", llm)
# ... use agent ...
await resource_manager.cleanup_subagent("agent_1")

# Cleanup all
await resource_manager.cleanup_all()
```

### Step 6: Concurrent Subagent Execution

Execute multiple subagents concurrently:

```python
async def execute_concurrent_subagents(
    parent: ParentAgent,
    tasks: Dict[str, str]
) -> Dict[str, str]:
    """Execute multiple subagents concurrently."""
    async def execute_task(agent_id: str, task: str):
        return agent_id, await parent.delegate_task(agent_id, task)
    
    # Create tasks for concurrent execution
    coroutines = [
        execute_task(agent_id, task)
        for agent_id, task in tasks.items()
    ]
    
    # Execute concurrently
    results = await asyncio.gather(*coroutines)
    
    # Convert to dictionary
    return {agent_id: result for agent_id, result in results}

# Usage
parent = ParentAgent(llm)
await parent.spawn_subagent("agent_1", "Worker 1")
await parent.spawn_subagent("agent_2", "Worker 2")
await parent.spawn_subagent("agent_3", "Worker 3")

tasks = {
    "agent_1": "Task 1",
    "agent_2": "Task 2",
    "agent_3": "Task 3"
}

results = await execute_concurrent_subagents(parent, tasks)
```

### Step 7: Subagent Pool Pattern

Maintain a pool of reusable subagents:

```python
class SubagentPool:
    """Pool of reusable subagents."""
    def __init__(self, llm, pool_size: int = 5):
        self.llm = llm
        self.pool_size = pool_size
        self.available: List[Subagent] = []
        self.in_use: Dict[str, Subagent] = {}
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize the subagent pool."""
        for i in range(self.pool_size):
            agent = Subagent(f"pool_agent_{i}", "Worker", self.llm)
            self.available.append(agent)
    
    async def acquire(self) -> Subagent:
        """Acquire a subagent from the pool."""
        if self.available:
            agent = self.available.pop()
            self.in_use[agent.agent_id] = agent
            return agent
        else:
            # Create new agent if pool exhausted
            agent_id = f"pool_agent_{len(self.in_use)}"
            agent = Subagent(agent_id, "Worker", self.llm)
            self.in_use[agent_id] = agent
            return agent
    
    async def release(self, agent: Subagent):
        """Release a subagent back to the pool."""
        if agent.agent_id in self.in_use:
            del self.in_use[agent.agent_id]
            # Reset agent state
            agent.messages = []
            agent.status = "idle"
            self.available.append(agent)
    
    @asynccontextmanager
    async def get_agent(self):
        """Context manager for acquiring/releasing agents."""
        agent = await self.acquire()
        try:
            yield agent
        finally:
            await self.release(agent)

# Usage
pool = SubagentPool(llm, pool_size=3)

async def use_pool():
    async with pool.get_agent() as agent:
        result = await agent.execute_task("Process data")
        return result
    # Agent automatically returned to pool
```

## Orchestration Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **Dynamic Spawning** | Create subagents on demand | Variable workloads |
| **Pool Pattern** | Reuse subagents from pool | High-throughput tasks |
| **Hierarchical** | Parent delegates to children | Complex decomposition |
| **Parallel Execution** | Run subagents concurrently | Independent tasks |
| **Sequential Pipeline** | Chain subagents in sequence | Dependent tasks |

## Communication Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **Task Delegation** | Parent assigns tasks to children | Work distribution |
| **Result Aggregation** | Combine child results | Synthesis |
| **Status Queries** | Parent checks child status | Monitoring |
| **Bidirectional** | Two-way communication | Interactive workflows |

## Best Practices

- Always clean up subagents when done
- Use context managers for automatic cleanup
- Track resource usage and limit concurrent subagents
- Implement proper error handling for subagent failures
- Use result aggregation for combining outputs
- Monitor subagent status and health
- Set timeouts for subagent operations
- Use pools for high-throughput scenarios
- Implement graceful shutdown procedures
- Log subagent activities for debugging

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Not cleaning up subagents | Use context managers or explicit cleanup |
| Spawning unlimited subagents | Set limits and use pools |
| No error handling | Wrap subagent calls in try/except |
| Blocking on subagents | Use async/await and concurrent execution |
| No resource tracking | Implement resource monitoring |
| Ignoring subagent failures | Handle and propagate errors |
| No timeout on operations | Set timeouts for subagent tasks |
| Memory leaks | Clear agent state on cleanup |

## Related

- Knowledge: `knowledge/subagent-patterns.json`
- Skill: `agentic-loops`
- Skill: `langgraph-agent-building`
- Skill: `crewai-agents`
- Skill: `state-management`

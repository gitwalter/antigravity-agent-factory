---
name: human-in-the-loop
description: Approval workflows, interrupts, and feedback patterns for agents
type: skill
agents: [code-reviewer, test-generator]
knowledge: [hitl-patterns.json]
---

# Human-in-the-Loop Skill

Implement human oversight, approval workflows, and feedback collection in agent systems.

## When to Use

- High-stakes decisions requiring approval
- Sensitive operations (payments, deletions)
- Quality assurance checkpoints
- Collecting user feedback
- Escalation handling

## Prerequisites

```bash
pip install langgraph
```

## Process

### Step 1: Basic Interrupt Pattern

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

class WorkflowState(TypedDict):
    task: str
    proposed_action: dict
    approved: bool | None
    result: str | None

async def propose_action(state: WorkflowState) -> dict:
    """Generate proposed action for review."""
    # LLM generates proposal
    proposal = await generate_proposal(state["task"])
    return {"proposed_action": proposal, "approved": None}

async def execute_action(state: WorkflowState) -> dict:
    """Execute approved action."""
    if not state["approved"]:
        return {"result": "Action rejected by user"}
    
    result = await execute(state["proposed_action"])
    return {"result": result}

def create_hitl_graph():
    graph = StateGraph(WorkflowState)
    
    graph.add_node("propose", propose_action)
    graph.add_node("execute", execute_action)
    
    graph.set_entry_point("propose")
    graph.add_edge("propose", "execute")
    graph.add_edge("execute", END)
    
    # Compile with interrupt BEFORE execute
    return graph.compile(
        checkpointer=MemorySaver(),
        interrupt_before=["execute"]
    )
```

### Step 2: Running with Interrupts

```python
app = create_hitl_graph()

async def run_with_approval(task: str, thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    
    # Run until interrupt
    result = await app.ainvoke(
        {"task": task, "approved": None},
        config
    )
    
    # Show proposal to user
    print(f"Proposed action: {result['proposed_action']}")
    
    # Get user approval (in real app, this would be async/UI)
    approved = input("Approve? (y/n): ").lower() == "y"
    
    # Continue with approval decision
    final = await app.ainvoke(
        {"approved": approved},
        config
    )
    
    return final
```

### Step 3: Multi-Step Approval

```python
class MultiStepState(TypedDict):
    steps: list[dict]
    current_step: int
    approvals: list[bool]
    completed: bool

async def process_step(state: MultiStepState) -> dict:
    """Process current step."""
    step = state["steps"][state["current_step"]]
    # Process and generate proposal
    return {"current_step": state["current_step"]}

def should_continue(state: MultiStepState) -> str:
    if state["current_step"] >= len(state["steps"]) - 1:
        return "complete"
    return "next_step"

def create_multi_approval_graph():
    graph = StateGraph(MultiStepState)
    
    graph.add_node("process", process_step)
    graph.add_node("review", lambda s: s)  # Interrupt point
    
    graph.set_entry_point("process")
    graph.add_edge("process", "review")
    graph.add_conditional_edges(
        "review",
        should_continue,
        {"next_step": "process", "complete": END}
    )
    
    return graph.compile(
        checkpointer=MemorySaver(),
        interrupt_after=["process"]  # Pause after each step
    )
```

### Step 4: Confirmation Dialog Pattern

```python
from pydantic import BaseModel
from enum import Enum

class ConfirmationLevel(str, Enum):
    INFO = "info"       # Just notify
    CONFIRM = "confirm" # Simple yes/no
    VERIFY = "verify"   # Require typing confirmation
    
class ConfirmationRequest(BaseModel):
    action: str
    level: ConfirmationLevel
    details: dict
    verification_phrase: str | None = None

async def request_confirmation(request: ConfirmationRequest) -> bool:
    """Request user confirmation based on level."""
    
    if request.level == ConfirmationLevel.INFO:
        print(f"[INFO] {request.action}")
        return True
    
    elif request.level == ConfirmationLevel.CONFIRM:
        print(f"[CONFIRM] {request.action}")
        print(f"Details: {request.details}")
        response = input("Proceed? (y/n): ")
        return response.lower() == "y"
    
    elif request.level == ConfirmationLevel.VERIFY:
        print(f"[VERIFY] {request.action}")
        print(f"Details: {request.details}")
        print(f"Type '{request.verification_phrase}' to confirm:")
        response = input("> ")
        return response == request.verification_phrase
    
    return False

# Usage in agent
async def delete_resource(resource_id: str):
    confirmed = await request_confirmation(ConfirmationRequest(
        action=f"Delete resource {resource_id}",
        level=ConfirmationLevel.VERIFY,
        details={"resource_id": resource_id, "type": "database"},
        verification_phrase=f"DELETE {resource_id}"
    ))
    
    if confirmed:
        await perform_deletion(resource_id)
```

### Step 5: Feedback Collection

```python
from langsmith import Client
from pydantic import BaseModel

class UserFeedback(BaseModel):
    run_id: str
    score: float  # 0-1
    feedback_type: str  # "correctness", "helpfulness", etc.
    comment: str | None = None

async def collect_feedback(run_id: str, output: str) -> UserFeedback:
    """Collect user feedback on agent output."""
    print(f"Agent output: {output}")
    
    score = float(input("Rate 0-1: "))
    comment = input("Comments (optional): ") or None
    
    feedback = UserFeedback(
        run_id=run_id,
        score=score,
        feedback_type="helpfulness",
        comment=comment
    )
    
    # Log to LangSmith
    client = Client()
    client.create_feedback(
        run_id=run_id,
        key=feedback.feedback_type,
        score=feedback.score,
        comment=feedback.comment
    )
    
    return feedback
```

### Step 6: Escalation Pattern

```python
from enum import Enum

class EscalationLevel(str, Enum):
    AGENT = "agent"
    SENIOR_AGENT = "senior_agent"
    HUMAN = "human"
    MANAGER = "manager"

class EscalationManager:
    def __init__(self):
        self.current_level = EscalationLevel.AGENT
        self.escalation_history = []
    
    def should_escalate(self, result: dict) -> bool:
        """Determine if escalation is needed."""
        confidence = result.get("confidence", 1.0)
        error = result.get("error")
        sensitive = result.get("sensitive", False)
        
        return confidence < 0.7 or error or sensitive
    
    def escalate(self, reason: str) -> EscalationLevel:
        """Escalate to next level."""
        levels = list(EscalationLevel)
        current_idx = levels.index(self.current_level)
        
        if current_idx < len(levels) - 1:
            self.current_level = levels[current_idx + 1]
            self.escalation_history.append({
                "from": levels[current_idx],
                "to": self.current_level,
                "reason": reason
            })
        
        return self.current_level

# In workflow
async def process_with_escalation(state: dict) -> dict:
    escalation = EscalationManager()
    
    result = await agent_process(state)
    
    while escalation.should_escalate(result):
        level = escalation.escalate(result.get("error", "low confidence"))
        
        if level == EscalationLevel.HUMAN:
            # Wait for human input
            result = await wait_for_human_review(state, result)
            break
        else:
            # Try with more capable agent
            result = await escalated_agent_process(state, level)
    
    return result
```

## HITL Patterns

| Pattern | Use Case |
|---------|----------|
| Interrupt Before | Review before action |
| Interrupt After | Review after generation |
| Multi-Step | Sequential approvals |
| Escalation | Progressive human involvement |
| Feedback Loop | Continuous improvement |

## Best Practices

- Use checkpointing for resumable workflows
- Implement timeouts for human responses
- Log all human decisions for audit
- Provide clear context for decisions
- Allow humans to modify, not just approve/reject
- Design for async human response

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Blocking on sync input | Use async with timeouts |
| No context | Provide full details for decision |
| Binary only | Allow modifications |
| No audit trail | Log all decisions |

## Related

- Knowledge: `knowledge/hitl-patterns.json`
- Skill: `state-management`
- Skill: `langgraph-agent-building`

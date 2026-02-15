"""
DeepAgent Task Planning Template

This template demonstrates task planning with progress tracking and dynamic replanning
using the DeepAgent pattern.

Usage:
    agent = TaskPlanningAgent()
    result = await agent.execute("Build a web application for task management")
"""

from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
import operator


class TaskPlanState(TypedDict):
    """State for task planning."""

    objective: str
    plan: List[dict]
    current_step: int
    completed_steps: Annotated[List[dict], operator.add]
    context: dict
    needs_replan: bool


class TaskPlanningAgent:
    """
    Task planning agent with progress tracking and dynamic replanning.

    Features:
    - Breaks down complex objectives into steps
    - Tracks progress through execution
    - Dynamically replans when needed
    - Maintains context across steps
    """

    def __init__(self, llm: ChatOpenAI = None):
        """
        Initialize the task planning agent.

        Args:
            llm: Language model to use
        """
        self.llm = llm or ChatOpenAI(model="gpt-4o", temperature=0)
        self.checkpointer = MemorySaver()
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the task planning graph."""
        workflow = StateGraph(TaskPlanState)

        # Add nodes
        workflow.add_node("plan", self._create_plan)
        workflow.add_node("execute", self._execute_step)
        workflow.add_node("evaluate", self._evaluate_progress)
        workflow.add_node("replan", self._replan)

        # Set entry point
        workflow.set_entry_point("plan")

        # Add edges
        workflow.add_edge("plan", "execute")
        workflow.add_edge("execute", "evaluate")

        # Conditional edges from evaluate
        workflow.add_conditional_edges(
            "evaluate",
            self._should_continue,
            {"continue": "execute", "replan": "replan", "end": END},
        )

        workflow.add_edge("replan", "execute")

        return workflow.compile(checkpointer=self.checkpointer)

    async def _create_plan(self, state: TaskPlanState):
        """Create initial plan for the objective."""
        prompt = f"""Create a detailed step-by-step plan for this objective:
{state["objective"]}

Provide a numbered list of concrete, actionable steps.
Each step should have:
1. Clear description
2. Success criteria
3. Estimated complexity (1-10)

Format as JSON array of steps."""

        response = await self.llm.ainvoke(prompt)

        # Parse plan (simplified - would use structured output in production)
        plan = self._parse_plan(response.content)

        return {"plan": plan, "current_step": 0, "needs_replan": False}

    async def _execute_step(self, state: TaskPlanState):
        """Execute the current step."""
        if state["current_step"] >= len(state["plan"]):
            return state

        current = state["plan"][state["current_step"]]

        # Build context from previous steps
        context_summary = self._build_context(state["completed_steps"])

        prompt = f"""Execute this step:
Step: {current["description"]}
Success Criteria: {current.get("success_criteria", "Complete the task")}

Context from previous steps:
{context_summary}

Provide detailed results of execution."""

        response = await self.llm.ainvoke(prompt)

        completed_step = {
            **current,
            "result": response.content,
            "step_number": state["current_step"],
        }

        return {
            "completed_steps": [completed_step],
            "current_step": state["current_step"] + 1,
        }

    async def _evaluate_progress(self, state: TaskPlanState):
        """Evaluate progress and determine if replanning is needed."""
        if not state["completed_steps"]:
            return {"needs_replan": False}

        last_step = state["completed_steps"][-1]

        prompt = f"""Evaluate this step execution:
Step: {last_step["description"]}
Result: {last_step["result"]}
Success Criteria: {last_step.get("success_criteria", "N/A")}

Was this step successful? Does the plan need adjustment?
Respond with JSON: {{"successful": true/false, "needs_replan": true/false, "reason": "..."}}"""

        response = await self.llm.ainvoke(prompt)

        # Parse evaluation (simplified)
        evaluation = self._parse_evaluation(response.content)

        return {"needs_replan": evaluation.get("needs_replan", False)}

    async def _replan(self, state: TaskPlanState):
        """Replan based on current progress."""
        context = self._build_context(state["completed_steps"])
        remaining_objective = self._get_remaining_objective(state)

        prompt = f"""Replan the remaining work:
Original Objective: {state["objective"]}
Completed Steps: {len(state["completed_steps"])}
Current Context: {context}
Remaining Objective: {remaining_objective}

Create a new plan for the remaining work."""

        response = await self.llm.ainvoke(prompt)
        new_plan = self._parse_plan(response.content)

        return {"plan": new_plan, "current_step": 0, "needs_replan": False}

    def _should_continue(self, state: TaskPlanState) -> str:
        """Determine next action."""
        if state["needs_replan"]:
            return "replan"

        if state["current_step"] >= len(state["plan"]):
            return "end"

        return "continue"

    def _parse_plan(self, content: str) -> List[dict]:
        """Parse plan from LLM response."""
        # Simplified parsing - would use structured output in production
        steps = []
        for i, line in enumerate(content.split("\n")):
            if line.strip() and line[0].isdigit():
                steps.append(
                    {
                        "description": line.strip(),
                        "success_criteria": "Complete the task",
                        "complexity": 5,
                    }
                )
        return steps

    def _parse_evaluation(self, content: str) -> dict:
        """Parse evaluation from LLM response."""
        # Simplified - would use structured output
        return {"successful": True, "needs_replan": False}

    def _build_context(self, completed_steps: List[dict]) -> str:
        """Build context summary from completed steps."""
        if not completed_steps:
            return "No previous steps"

        summary = []
        for step in completed_steps[-3:]:  # Last 3 steps
            summary.append(f"Step {step['step_number']}: {step['description']}")
            summary.append(f"Result: {step['result'][:100]}...")

        return "\n".join(summary)

    def _get_remaining_objective(self, state: TaskPlanState) -> str:
        """Determine remaining objective."""
        completed = len(state["completed_steps"])
        total = len(state["plan"])
        return f"Complete steps {completed + 1} through {total}"

    async def execute(self, objective: str, thread_id: str = "default"):
        """
        Execute the task planning agent.

        Args:
            objective: The objective to accomplish
            thread_id: Thread ID for persistence

        Returns:
            Final state with all completed steps
        """
        config = {"configurable": {"thread_id": thread_id}}

        initial_state = {
            "objective": objective,
            "plan": [],
            "current_step": 0,
            "completed_steps": [],
            "context": {},
            "needs_replan": False,
        }

        result = await self.graph.ainvoke(initial_state, config=config)

        return result


# Example usage
if __name__ == "__main__":
    import asyncio

    async def main():
        agent = TaskPlanningAgent()

        result = await agent.execute(
            "Build a web application for task management with user authentication"
        )

        print("\n" + "=" * 80)
        print("Task Planning Complete")
        print("=" * 80)
        print(f"\nObjective: {result['objective']}")
        print(f"Steps Completed: {len(result['completed_steps'])}")
        print("\nCompleted Steps:")
        for step in result["completed_steps"]:
            print(f"\n{step['step_number'] + 1}. {step['description']}")
            print(f"   Result: {step['result'][:200]}...")

    asyncio.run(main())

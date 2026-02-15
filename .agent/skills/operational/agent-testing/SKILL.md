---
description: Unit testing with mocks, integration testing, LangSmith evaluation, benchmarking
name: agent-testing
type: skill
---
# Agent Testing

Unit testing with mocks, integration testing, LangSmith evaluation, benchmarking

Implement comprehensive testing strategies for agents - unit tests with mocks, integration tests, LangSmith evaluation, and benchmarking.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.

### Step 0: Test Execution Configuration

**CRITICAL:** Always run tests in parallel using `pytest-xdist` to ensure efficiency.
**NEVER** run tests in the background (detached process).

```bash
# Correct usage
pytest -n auto

# Incorrect usage
pytest &  # Do not do this
```### Step 1: Unit Testing with Mocks

Write unit tests with mocked LLM and tools:

```python
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool

# Simple agent function to test
async def simple_agent(prompt: str, llm, tools: list) -> str:
    """Simple agent that uses LLM and tools."""
    llm_with_tools = llm.bind_tools(tools)
    response = await llm_with_tools.ainvoke(prompt)

    if response.tool_calls:
        # Execute tools (simplified)
        return "Tool executed"

    return response.content

# Unit test with mocked LLM
@pytest.mark.asyncio
async def test_simple_agent_with_mock():
    """Test agent with mocked LLM."""
    # Create mock LLM
    mock_llm = AsyncMock()
    mock_response = AIMessage(content="Test response")
    mock_llm.bind_tools.return_value.ainvoke = AsyncMock(return_value=mock_response)

    # Test
    result = await simple_agent("test prompt", mock_llm, [])

    assert result == "Test response"
    mock_llm.bind_tools.return_value.ainvoke.assert_called_once()

# Test with tool calls
@pytest.mark.asyncio
async def test_agent_with_tool_calls():
    """Test agent that calls tools."""
    mock_llm = AsyncMock()
    mock_response = AIMessage(
        content="",
        tool_calls=[{
            "name": "test_tool",
            "args": {"arg1": "value1"},
            "id": "call_123"
        }]
    )
    mock_llm.bind_tools.return_value.ainvoke = AsyncMock(return_value=mock_response)

    @tool
    def test_tool(arg1: str) -> str:
        """Test tool."""
        return f"Result: {arg1}"

    result = await simple_agent("test prompt", mock_llm, [test_tool])
    assert result == "Tool executed"

# Using pytest fixtures
@pytest.fixture
def mock_llm():
    """Fixture for mocked LLM."""
    llm = AsyncMock()
    llm.bind_tools.return_value.ainvoke = AsyncMock(
        return_value=AIMessage(content="Mocked response")
    )
    return llm

@pytest.fixture
def sample_tools():
    """Fixture for sample tools."""
    @tool
    def get_weather(location: str) -> str:
        """Get weather for location."""
        return f"Weather in {location}: Sunny"

    return [get_weather]

@pytest.mark.asyncio
async def test_agent_with_fixtures(mock_llm, sample_tools):
    """Test using fixtures."""
    result = await simple_agent("What's the weather?", mock_llm, sample_tools)
    assert result is not None
```

### Step 2: Integration Testing

Test agents with real or test LLMs:

```python
import pytest
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import os

# Integration test with test LLM
@pytest.mark.asyncio
@pytest.mark.integration
async def test_agent_integration():
    """Integration test with real LLM."""
    # Use test API key or test model
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",  # Cheaper model for testing
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )

    @tool
    def add_numbers(a: int, b: int) -> str:
        """Add two numbers."""
        return str(a + b)

    # Test agent
    result = await simple_agent("Add 2 and 3", llm, [add_numbers])

    # Verify result contains expected content
    assert "5" in result or "tool" in result.lower()

# Test with test database
@pytest.fixture
def test_db():
    """Fixture for test database."""
    # Setup test database
    db = {}
    yield db
    # Teardown
    db.clear()

@pytest.mark.asyncio
@pytest.mark.integration
async def test_agent_with_database(test_db):
    """Test agent that interacts with database."""
    @tool
    def store_data(key: str, value: str) -> str:
        """Store data in test database."""
        test_db[key] = value
        return f"Stored {key}"

    @tool
    def get_data(key: str) -> str:
        """Get data from test database."""
        return test_db.get(key, "Not found")

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # Test storing and retrieving
    await simple_agent("Store test_key with value test_value", llm, [store_data])
    assert test_db["test_key"] == "test_value"
```

### Step 3: LangSmith Evaluation

Use LangSmith for agent evaluation:

```python
from langsmith import Client, evaluate
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import os

# Initialize LangSmith client
client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))

# Define evaluation dataset
dataset_name = "agent_test_dataset"

# Create dataset
dataset = client.create_dataset(
    dataset_name=dataset_name,
    description="Test dataset for agent evaluation"
)

# Add examples
client.create_examples(
    inputs=[
        {"input": "What is Python?"},
        {"input": "Add 2 and 3"},
        {"input": "What's the weather in NYC?"}
    ],
    outputs=[
        {"output": "Python is a programming language"},
        {"output": "5"},
        {"output": "Weather information"}
    ],
    dataset_id=dataset.id
)

# Define agent function
async def test_agent(input: dict) -> dict:
    """Agent function for evaluation."""
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    response = await llm.ainvoke(input["input"])
    return {"output": response.content}

# Evaluation function
def evaluate_agent(run, example):
    """Custom evaluation function."""
    predicted = run.outputs.get("output", "")
    expected = example.outputs.get("output", "")

    # Simple accuracy check
    accuracy = 1.0 if expected.lower() in predicted.lower() else 0.0

    return {
        "accuracy": accuracy,
        "predicted": predicted,
        "expected": expected
    }

# Run evaluation
results = evaluate(
    test_agent,
    data=dataset_name,
    evaluators=[evaluate_agent],
    experiment_prefix="agent_test"
)

# View results
for result in results:
    print(f"Accuracy: {result['accuracy']}")
    print(f"Predicted: {result['predicted']}")
    print(f"Expected: {result['expected']}")

# Using LangSmith's built-in evaluators
from langsmith.evaluation import LangChainStringEvaluator

# Create evaluator
evaluator = LangChainStringEvaluator(
    "labeled_score_string",
    criteria={
        "helpfulness": "Is the response helpful?",
        "accuracy": "Is the response accurate?"
    }
)

# Run evaluation with built-in evaluator
results = evaluate(
    test_agent,
    data=dataset_name,
    evaluators=[evaluator],
    experiment_prefix="agent_eval"
)
```

### Step 4: Benchmarking Agents

Measure agent performance:

```python
import time
import asyncio
from typing import List, Dict
import statistics

class AgentBenchmark:
    """Benchmark agent performance."""

    def __init__(self, agent_func):
        self.agent_func = agent_func
        self.results: List[Dict] = []

    async def benchmark(
        self,
        test_cases: List[str],
        iterations: int = 10
    ) -> Dict:
        """Run benchmark on test cases."""
        latencies = []
        successes = 0
        errors = 0

        for test_case in test_cases:
            for _ in range(iterations):
                start_time = time.time()

                try:
                    result = await self.agent_func(test_case)
                    latency = time.time() - start_time
                    latencies.append(latency)
                    successes += 1
                except Exception as e:
                    errors += 1
                    self.results.append({
                        "test_case": test_case,
                        "success": False,
                        "error": str(e),
                        "latency": None
                    })
                    continue

                self.results.append({
                    "test_case": test_case,
                    "success": True,
                    "latency": latency,
                    "result_length": len(str(result))
                })

        return {
            "total_tests": len(test_cases) * iterations,
            "successes": successes,
            "errors": errors,
            "success_rate": successes / (successes + errors) if (successes + errors) > 0 else 0,
            "avg_latency": statistics.mean(latencies) if latencies else 0,
            "median_latency": statistics.median(latencies) if latencies else 0,
            "p95_latency": statistics.quantiles(latencies, n=20)[18] if len(latencies) >= 20 else 0,
            "min_latency": min(latencies) if latencies else 0,
            "max_latency": max(latencies) if latencies else 0
        }

# Usage
async def benchmark_agent(prompt: str) -> str:
    """Agent function to benchmark."""
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    response = await llm.ainvoke(prompt)
    return response.content

benchmark = AgentBenchmark(benchmark_agent)
results = await benchmark.benchmark(
    test_cases=["What is Python?", "Explain async/await"],
    iterations=5
)

print(f"Success Rate: {results['success_rate']:.2%}")
print(f"Average Latency: {results['avg_latency']:.2f}s")
print(f"P95 Latency: {results['p95_latency']:.2f}s")
```

### Step 5: Testing Tool Execution

Test agent tool usage:

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_tool_execution():
    """Test that agent executes tools correctly."""
    @tool
    def test_tool(param: str) -> str:
        """Test tool."""
        return f"Result: {param}"

    # Mock tool execution
    with patch.object(test_tool, 'invoke', return_value="Result: test") as mock_tool:
        # Test agent that uses tool
        # ... agent code ...

        # Verify tool was called
        mock_tool.assert_called_once_with({"param": "test"})

# Test tool error handling
@pytest.mark.asyncio
async def test_tool_error_handling():
    """Test agent handles tool errors."""
    @tool
    def failing_tool() -> str:
        """Tool that always fails."""
        raise ValueError("Tool error")

    # Agent should handle tool errors gracefully
    # ... test implementation ...
```

### Step 6: End-to-End Testing

Test complete agent workflows:

```python
import pytest
from langchain_core.messages import HumanMessage

@pytest.mark.asyncio
@pytest.mark.e2e
async def test_complete_agent_workflow():
    """End-to-end test of agent workflow."""
    # Setup
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    @tool
    def get_weather(location: str) -> str:
        """Get weather."""
        return f"Weather in {location}: Sunny, 72°F"

    @tool
    def search_kb(query: str) -> str:
        """Search knowledge base."""
        return f"Results for: {query}"

    tools = [get_weather, search_kb]
    llm_with_tools = llm.bind_tools(tools)

    # Execute workflow
    messages = [HumanMessage(content="What's the weather in NYC and search for Python?")]

    response = await llm_with_tools.ainvoke(messages)

    # Verify response
    assert response is not None
    assert len(response.tool_calls) > 0

    # Verify tool calls
    tool_names = [tc["name"] for tc in response.tool_calls]
    assert "get_weather" in tool_names or "search_kb" in tool_names

# Test multi-turn conversation
@pytest.mark.asyncio
@pytest.mark.e2e
async def test_multi_turn_conversation():
    """Test agent maintains context across turns."""
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    messages = []

    # Turn 1
    messages.append(HumanMessage(content="My name is Alice"))
    response1 = await llm.ainvoke(messages)
    messages.append(response1)

    # Turn 2
    messages.append(HumanMessage(content="What's my name?"))
    response2 = await llm.ainvoke(messages)

    # Verify agent remembers
    assert "Alice" in response2.content.lower()
```

### Step 7: Property-Based Testing

Test agent properties:

```python
from hypothesis import given, strategies as st
import pytest
import time
import asyncio

@given(st.text(min_size=1, max_size=100))
@pytest.mark.asyncio
async def test_agent_always_responds(prompt: str):
    """Property: Agent always returns a response."""
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    response = await llm.ainvoke(prompt)

    assert response is not None
    assert hasattr(response, 'content')
    assert len(response.content) > 0

@given(st.text(min_size=1, max_size=50))
@pytest.mark.asyncio
async def test_agent_response_time(prompt: str):
    """Property: Agent responds within timeout."""
    llm = ChatOpenAI(model="gpt-3.5-turbo")

    start_time = time.time()
    response = await asyncio.wait_for(
        llm.ainvoke(prompt),
        timeout=30.0
    )
    latency = time.time() - start_time

    assert latency < 30.0
    assert response is not None
```

## Testing Strategies

| Strategy | Use Case | Tools |
|----------|----------|-------|
| **Unit Tests** | Isolated components | pytest, unittest.mock |
| **Integration Tests** | Component interactions | pytest, test databases |
| **E2E Tests** | Complete workflows | pytest, real LLMs |
| **Property Tests** | Invariants | hypothesis |
| **Performance Tests** | Latency, throughput | Custom benchmarks |
| **Evaluation** | Quality metrics | LangSmith |

## Best Practices

- Mock external dependencies in unit tests
- Use fixtures for common test setup
- Test error cases and edge cases
- Use LangSmith for evaluation
- Benchmark performance regularly
- Test tool execution separately
- Use property-based testing for invariants
- Maintain test coverage > 80%
- Test async code with pytest-asyncio
- Use test databases for integration tests
- **Run tests in parallel (`pytest -n auto`)** for speed
- **Do not run tests in the background**

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Testing with production LLM | Use test models or mocks |
| No error case testing | Test all error paths |
| Slow tests | Mock expensive operations |
| No test isolation | Use fixtures and teardown |
| Testing implementation details | Test behavior, not implementation |
| No performance testing | Add benchmarks |
| Ignoring flaky tests | Fix or remove flaky tests |
| No test data management | Use fixtures and factories |
| Synchronous async tests | Use pytest-asyncio |
| No evaluation metrics | Use LangSmith evaluation |

## Related

- Knowledge: `{directories.knowledge}/agent-testing-patterns.json`
- Skill: `langsmith-tracing`
- Skill: `langsmith-prompts`
- Skill: `error-handling`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

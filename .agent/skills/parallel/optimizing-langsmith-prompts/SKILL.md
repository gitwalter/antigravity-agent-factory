---
agents:
- none
category: parallel
description: Prompt management with LangSmith Hub - versioning, testing, and evaluation
knowledge:
- none
name: optimizing-langsmith-prompts
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# Langsmith Prompts

Prompt management with LangSmith Hub - versioning, testing, and evaluation

Manage prompts professionally with versioning, A/B testing, and evaluation using LangSmith Hub.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Push Prompts to Hub

```python
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate

# Create prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {role}. {instructions}"),
    ("human", "{input}")
])

# Push to Hub (creates versioned prompt)
hub.push("my-org/agent-prompt", prompt, new_repo_is_public=False)
```

### Step 2: Pull Prompts from Hub

```python
from langchain import hub

# Pull latest version
prompt = hub.pull("my-org/agent-prompt")

# Pull specific version
prompt_v2 = hub.pull("my-org/agent-prompt:v2")

# Use in chain
chain = prompt | llm | parser
```

### Step 3: Prompt Versioning Strategy

```python
# Development workflow
def update_prompt(prompt_name: str, new_prompt: ChatPromptTemplate):
    """Update prompt with version tracking."""
    # Pull current to compare
    try:
        current = hub.pull(prompt_name)
        print(f"Current: {current}")
    except Exception:
        print("Creating new prompt")

    # Push new version
    hub.push(prompt_name, new_prompt)
    print(f"Pushed new version of {prompt_name}")
```

### Step 4: A/B Testing Prompts

```python
import random
from langsmith import traceable

@traceable(tags=["ab-test"])
async def run_with_ab_test(input_data: dict, test_name: str = "prompt_v1_vs_v2"):
    """Run A/B test between prompt versions."""

    # Select variant
    variant = random.choice(["control", "treatment"])

    if variant == "control":
        prompt = hub.pull("my-org/agent-prompt:v1")
    else:
        prompt = hub.pull("my-org/agent-prompt:v2")

    chain = prompt | llm | parser
    result = await chain.ainvoke(input_data)

    # Log variant for analysis
    return {"result": result, "variant": variant}
```

### Step 5: Prompt Evaluation

```python
from langsmith import Client
from langsmith.evaluation import evaluate

client = Client()

# Create evaluation dataset
dataset = client.create_dataset("prompt-eval")

# Add examples
client.create_example(
    dataset_id=dataset.id,
    inputs={"input": "What is Python?"},
    outputs={"expected": "Python is a programming language..."}
)

# Define evaluator
def relevance_evaluator(run, example):
    """Check if response is relevant to input."""
    output = run.outputs.get("output", "")
    expected = example.outputs.get("expected", "")

    # Simple keyword overlap (use LLM for better eval)
    overlap = len(set(output.split()) & set(expected.split()))
    return {"score": min(overlap / 10, 1.0)}

# Run evaluation
results = evaluate(
    lambda x: chain.invoke(x),
    data="prompt-eval",
    evaluators=[relevance_evaluator]
)
```

### Step 6: Prompt Templates with Variables

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Complex prompt with all features
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a {role} assistant.

Context: {context}

Instructions:
{instructions}

Output Format: {output_format}
"""),
    MessagesPlaceholder("history", optional=True),
    ("human", "{input}")
])

# Partial application for reuse
analyst_prompt = prompt.partial(
    role="data analyst",
    output_format="JSON with 'analysis' and 'confidence' keys"
)

# Use
result = await (analyst_prompt | llm).ainvoke({
    "context": "Sales data Q4 2024",
    "instructions": "Analyze trends and anomalies",
    "input": "What are the key insights?"
})
```

## Prompt Organization

```
prompts/
├── agents/
│   ├── analyst-v1
│   ├── analyst-v2
│   └── researcher
├── tools/
│   ├── sql-generator
│   └── api-caller
└── evaluation/
    ├── relevance-judge
    └── quality-judge
```

## Best Practices

- Use semantic versioning for prompts (v1, v2, etc.)
- Include clear descriptions when pushing
- Test prompts before deploying to production
- Use evaluation datasets for regression testing
- Tag prompts by use case and domain
- Keep production and dev prompts separate

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Hardcoded prompts | Use Hub for all prompts |
| No versioning | Always version prompts |
| No testing | Create evaluation datasets |
| Shared dev/prod | Separate environments |

## Related

- Knowledge: `{directories.knowledge}/langsmith-prompts-patterns.json`
- Skill: `langsmith-tracing`
- Skill: `agent-testing`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

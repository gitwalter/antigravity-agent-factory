---
description: DSPy integration for declarative prompt optimization, prompt versioning,
  A/B testing, few-shot optimization, chain-of-thought patterns, prompt caching
name: prompt-optimization
type: skill
---
# Prompt Optimization

DSPy integration for declarative prompt optimization, prompt versioning, A/B testing, few-shot optimization, chain-of-thought patterns, prompt caching

Optimize LLM prompts using DSPy's declarative optimization framework, implement prompt versioning and A/B testing, optimize few-shot examples, and leverage prompt caching for cost reduction.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: DSPy Setup and Basic Optimization

DSPy provides a declarative approach to prompt optimization:

```python
import dspy
from dspy.teleprompt import BootstrapFewShot
from dspy.evaluate import Evaluate

# Configure LLM
lm = dspy.LM(model="google:gemini-2.5-flash")
dspy.configure(lm=lm)

# Define a simple module
class AnswerQuestion(dspy.Module):
    """Answer questions based on context."""
    
    def __init__(self):
        super().__init__()
        self.generate_answer = dspy.ChainOfThought("context, question -> answer")
    
    def forward(self, context, question):
        return self.generate_answer(context=context, question=question)

# Create training examples
trainset = [
    dspy.Example(context="Python is a programming language", question="What is Python?", answer="A programming language"),
    dspy.Example(context="ML is machine learning", question="What is ML?", answer="Machine learning"),
]

# Optimize the module
teleprompter = BootstrapFewShot(metric=dspy.evaluate.answer_exact_match)
optimized_module = teleprompter.compile(
    AnswerQuestion(),
    trainset=trainset
)

# Use optimized module
result = optimized_module(context="LangChain is a framework", question="What is LangChain?")
print(result.answer)
```

### Step 2: Advanced DSPy Optimization with Custom Metrics

Implement custom evaluation metrics for optimization:

```python
import dspy
from dspy.teleprompt import MIPRO
from dspy.evaluate import Evaluate

class RAGAnswer(dspy.Module):
    """RAG system with optimized prompts."""
    
    def __init__(self):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=3)
        self.generate_answer = dspy.ChainOfThought(
            "context, question -> answer, reasoning"
        )
    
    def forward(self, question):
        context = self.retrieve(question).passages
        result = self.generate_answer(context=context, question=question)
        return dspy.Prediction(answer=result.answer, reasoning=result.reasoning)

def custom_metric(gold, pred, trace=None):
    """Custom metric combining accuracy and reasoning quality."""
    answer_match = gold.answer.lower() in pred.answer.lower()
    has_reasoning = len(pred.reasoning) > 20
    return answer_match and has_reasoning

# Optimize with MIPRO (Multi-prompt Instruction Proposal and Refinement Optimization)
teleprompter = MIPRO(
    metric=custom_metric,
    num_candidates=10,
    init_temperature=1.0
)

optimized_rag = teleprompter.compile(
    RAGAnswer(),
    trainset=trainset,
    valset=valset
)

# Evaluate
evaluate = Evaluate(metric=custom_metric, num_threads=4)
score = evaluate(optimized_rag, valset=valset)
print(f"Optimized score: {score}")
```

### Step 3: Prompt Versioning and A/B Testing

Implement prompt versioning with A/B testing:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith import Client
import uuid
from datetime import datetime

class PromptVersionManager:
    """Manage prompt versions and A/B testing."""
    
    def __init__(self, langsmith_client: Client = None):
        self.versions = {}
        self.langsmith_client = langsmith_client or Client()
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    
    def register_version(self, name: str, prompt_template: str, metadata: dict = None):
        """Register a new prompt version."""
        version_id = str(uuid.uuid4())
        self.versions[version_id] = {
            "name": name,
            "template": prompt_template,
            "metadata": metadata or {},
            "created_at": datetime.now(),
            "stats": {"calls": 0, "success": 0, "errors": 0}
        }
        return version_id
    
    async def test_version(self, version_id: str, test_cases: list[dict]):
        """Test a prompt version."""
        version = self.versions[version_id]
        prompt = ChatPromptTemplate.from_template(version["template"])
        chain = prompt | self.llm
        
        results = []
        for test_case in test_cases:
            try:
                response = await chain.ainvoke(test_case)
                results.append({
                    "input": test_case,
                    "output": response.content,
                    "success": True
                })
                version["stats"]["success"] += 1
            except Exception as e:
                results.append({
                    "input": test_case,
                    "error": str(e),
                    "success": False
                })
                version["stats"]["errors"] += 1
            version["stats"]["calls"] += 1
        
        return results
    
    async def ab_test(self, version_a_id: str, version_b_id: str, test_cases: list[dict], 
                     evaluation_func=None):
        """Run A/B test between two versions."""
        results_a = await self.test_version(version_a_id, test_cases)
        results_b = await self.test_version(version_b_id, test_cases)
        
        if evaluation_func:
            scores_a = [evaluation_func(r["input"], r.get("output", "")) for r in results_a]
            scores_b = [evaluation_func(r["input"], r.get("output", "")) for r in results_b]
            
            avg_a = sum(scores_a) / len(scores_a) if scores_a else 0
            avg_b = sum(scores_b) / len(scores_b) if scores_b else 0
            
            return {
                "version_a": {"id": version_a_id, "avg_score": avg_a, "results": results_a},
                "version_b": {"id": version_b_id, "avg_score": avg_b, "results": results_b},
                "winner": "A" if avg_a > avg_b else "B"
            }
        
        return {"version_a": results_a, "version_b": results_b}

# Usage
manager = PromptVersionManager()

# Register versions
v1_id = manager.register_version(
    "v1_basic",
    "Answer this question: {question}",
    {"description": "Basic prompt"}
)

v2_id = manager.register_version(
    "v2_cot",
    """Answer this question step by step:
    
Question: {question}

Think through the problem and provide a detailed answer.""",
    {"description": "Chain-of-thought prompt"}
)

# A/B test
test_cases = [{"question": "What is machine learning?"}, {"question": "Explain RAG"}]
results = await manager.ab_test(v1_id, v2_id, test_cases)
print(f"Winner: {results['winner']}")
```

### Step 4: Few-Shot Example Optimization

Optimize few-shot examples selection:

```python
from langchain_core.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import numpy as np

class FewShotOptimizer:
    """Optimize few-shot example selection."""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        self.embeddings = HuggingFaceEmbeddings()
    
    def select_examples_semantic(self, examples: list[dict], query: str, k: int = 3):
        """Select examples using semantic similarity."""
        # Create vector store from examples
        example_texts = [ex["input"] for ex in examples]
        vectorstore = Chroma.from_texts(
            texts=example_texts,
            embedding=self.embeddings
        )
        
        # Select similar examples
        selector = SemanticSimilarityExampleSelector(
            vectorstore=vectorstore,
            k=k
        )
        
        selected = selector.select_examples({"input": query})
        return selected
    
    def optimize_examples_diversity(self, examples: list[dict], k: int = 3):
        """Select diverse examples using clustering."""
        from sklearn.cluster import KMeans
        
        # Embed all examples
        example_texts = [ex["input"] for ex in examples]
        embeddings_matrix = self.embeddings.embed_documents(example_texts)
        
        # Cluster
        kmeans = KMeans(n_clusters=k, random_state=42)
        clusters = kmeans.fit_predict(embeddings_matrix)
        
        # Select one example from each cluster
        selected_indices = []
        for cluster_id in range(k):
            cluster_examples = [i for i, c in enumerate(clusters) if c == cluster_id]
            if cluster_examples:
                # Select example closest to cluster center
                center = kmeans.cluster_centers_[cluster_id]
                distances = [
                    np.linalg.norm(embeddings_matrix[i] - center)
                    for i in cluster_examples
                ]
                selected_indices.append(cluster_examples[np.argmin(distances)])
        
        return [examples[i] for i in selected_indices]
    
    def create_optimized_prompt(self, examples: list[dict], query: str, 
                                selection_method: str = "semantic"):
        """Create prompt with optimized examples."""
        if selection_method == "semantic":
            selected = self.select_examples_semantic(examples, query, k=3)
        else:
            selected = self.optimize_examples_diversity(examples, k=3)
        
        # Format examples
        example_prompt = FewShotChatMessagePromptTemplate(
            examples=selected,
            example_selector=None,
            input_variables=["input"],
            example_prompt=ChatPromptTemplate.from_messages([
                ("human", "{input}"),
                ("ai", "{output}")
            ])
        )
        
        # Create final prompt
        final_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Follow these examples:"),
            example_prompt,
            ("human", "{input}")
        ])
        
        return final_prompt

# Usage
optimizer = FewShotOptimizer()

examples = [
    {"input": "What is Python?", "output": "Python is a programming language."},
    {"input": "Explain ML", "output": "ML stands for machine learning."},
    # ... more examples
]

optimized_prompt = optimizer.create_optimized_prompt(
    examples=examples,
    query="What is RAG?",
    selection_method="semantic"
)

chain = optimized_prompt | optimizer.llm
response = await chain.ainvoke({"input": "What is RAG?"})
```

### Step 5: Chain-of-Thought Design Patterns

Implement effective chain-of-thought prompts:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

class ChainOfThoughtPrompt:
    """Chain-of-thought prompt patterns."""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    
    def zero_shot_cot(self, question: str) -> ChatPromptTemplate:
        """Zero-shot chain-of-thought."""
        return ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant that thinks step by step."),
            ("user", """{question}

Let's think step by step:""")
        ])
    
    def few_shot_cot(self, examples: list[dict]) -> ChatPromptTemplate:
        """Few-shot chain-of-thought."""
        example_text = "\n\n".join([
            f"Q: {ex['question']}\nA: {ex['reasoning']}\nTherefore: {ex['answer']}"
            for ex in examples
        ])
        
        return ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant that thinks step by step."),
            ("user", f"""Follow these examples:

{example_text}

Now answer this question step by step:
{{question}}""")
        ])
    
    def self_consistency_cot(self, question: str, num_paths: int = 5):
        """Self-consistency: generate multiple reasoning paths."""
        prompt = self.zero_shot_cot(question)
        chain = prompt | self.llm
        
        # Generate multiple paths
        paths = []
        for _ in range(num_paths):
            response = await chain.ainvoke({"question": question})
            paths.append(response.content)
        
        # Aggregate answers (simplified - in practice, extract and vote)
        return paths

# Usage
cot_prompt = ChainOfThoughtPrompt()

# Zero-shot CoT
prompt = cot_prompt.zero_shot_cot("Solve: 2x + 5 = 15")
chain = prompt | cot_prompt.llm
response = await chain.ainvoke({"question": "Solve: 2x + 5 = 15"})

# Few-shot CoT
examples = [
    {
        "question": "Solve: x + 3 = 7",
        "reasoning": "Subtract 3 from both sides: x = 7 - 3 = 4",
        "answer": "x = 4"
    }
]
prompt = cot_prompt.few_shot_cot(examples)
```

### Step 6: Prompt Caching Strategies

Implement prompt caching to reduce costs:

```python
from anthropic import Anthropic
from langchain_anthropic import ChatAnthropic
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache
import hashlib
import json

class PromptCache:
    """Prompt caching for cost optimization."""
    
    def __init__(self, cache_type: str = "memory"):
        self.cache_type = cache_type
        if cache_type == "memory":
            set_llm_cache(InMemoryCache())
        elif cache_type == "custom":
            self.cache = {}
    
    def cache_key(self, prompt: str, model: str, temperature: float = 0.0) -> str:
        """Generate cache key."""
        content = f"{prompt}:{model}:{temperature}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, key: str):
        """Get from cache."""
        if self.cache_type == "custom":
            return self.cache.get(key)
        return None
    
    def set(self, key: str, value: str):
        """Set cache value."""
        if self.cache_type == "custom":
            self.cache[key] = value
    
    async def cached_invoke(self, prompt: str, llm, temperature: float = 0.0):
        """Invoke LLM with caching."""
        # For deterministic caching, use temperature=0
        if temperature == 0.0:
            cache_key = self.cache_key(prompt, llm.model_name, temperature)
            cached = self.get(cache_key)
            if cached:
                return cached
        
        # Invoke LLM
        response = await llm.ainvoke(prompt)
        
        # Cache if deterministic
        if temperature == 0.0:
            self.set(cache_key, response.content)
        
        return response

# Anthropic prompt caching (built-in)
class AnthropicPromptCache:
    """Use Anthropic's built-in prompt caching."""
    
    def __init__(self):
        self.client = Anthropic()
    
    async def invoke_with_cache(self, messages: list, cache_control: dict = None):
        """Invoke with prompt caching."""
        if cache_control is None:
            cache_control = {"type": "ephemeral"}  # or "ephemeral" or "ephemeral-dedupe"
        
        response = await self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=messages,
            cache_control=cache_control
        )
        return response

# Usage
cache = PromptCache(cache_type="memory")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Use caching (works automatically with InMemoryCache)
response = await cache.cached_invoke("What is Python?", llm, temperature=0.0)
```

### Step 7: Evaluation-Driven Prompt Iteration

Iterate on prompts based on evaluation metrics:

```python
from langsmith import Client, RunEvaluator
from langchain_core.runnables import RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI

class PromptIteration:
    """Iterate on prompts using evaluation feedback."""
    
    def __init__(self):
        self.client = Client()
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        self.versions = []
    
    async def evaluate_prompt(self, prompt_template: str, test_dataset: list[dict], 
                             metric_func=None):
        """Evaluate a prompt version."""
        from langchain_core.prompts import ChatPromptTemplate
        
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = prompt | self.llm
        
        results = []
        for test_case in test_dataset:
            response = await chain.ainvoke(test_case)
            
            score = None
            if metric_func:
                score = metric_func(test_case, response.content)
            
            results.append({
                "input": test_case,
                "output": response.content,
                "score": score
            })
        
        avg_score = sum(r["score"] for r in results if r["score"]) / len(results)
        
        return {
            "template": prompt_template,
            "results": results,
            "avg_score": avg_score
        }
    
    async def iterate(self, base_template: str, variations: list[str], 
                     test_dataset: list[dict], metric_func=None):
        """Test multiple variations and select best."""
        evaluations = []
        
        for variation in variations:
            eval_result = await self.evaluate_prompt(
                variation,
                test_dataset,
                metric_func
            )
            evaluations.append(eval_result)
        
        # Sort by score
        evaluations.sort(key=lambda x: x["avg_score"], reverse=True)
        
        return {
            "best": evaluations[0],
            "all_results": evaluations
        }

# Usage
iterator = PromptIteration()

base = "Answer: {question}"
variations = [
    "Answer this question: {question}",
    "Please provide a detailed answer to: {question}",
    "Question: {question}\n\nAnswer step by step:"
]

test_data = [{"question": "What is ML?"}, {"question": "Explain RAG"}]

def accuracy_metric(input_dict, output):
    """Simple accuracy metric."""
    # In practice, compare with ground truth
    return 1.0 if len(output) > 10 else 0.5

results = await iterator.iterate(base, variations, test_data, accuracy_metric)
print(f"Best prompt: {results['best']['template']}")
print(f"Score: {results['best']['avg_score']}")
```

## Output

After optimizing prompts, you'll have:

1. **Optimized Prompts** - DSPy-optimized prompt modules
2. **Version Management** - Tracked prompt versions with metadata
3. **A/B Test Results** - Comparison data between versions
4. **Few-Shot Selection** - Optimized example selection strategies
5. **Caching Setup** - Cost-reducing prompt caching
6. **Evaluation Metrics** - Performance tracking and iteration

## Best Practices

- Use DSPy for systematic prompt optimization
- A/B test major prompt changes
- Optimize few-shot examples for diversity and relevance
- Use prompt caching for deterministic queries
- Iterate based on evaluation metrics
- Version control all prompts
- Document prompt design decisions

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| No evaluation | Always measure prompt performance |
| Hardcoded examples | Use dynamic example selection |
| Ignoring caching | Cache deterministic prompts |
| No versioning | Track all prompt versions |
| Single iteration | Iterate based on feedback |

## Related

- Knowledge: `{directories.knowledge}/prompt-engineering.json`
- Skill: `llm-evaluation`
- Skill: `langsmith-prompts`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

---
description: RAGAS evaluation setup, DeepEval integration, LangSmith evaluation runs,
  custom metrics, retrieval quality metrics, regression testing for LLM outputs
name: evaluating-llms
type: skill
---
# Llm Evaluation

RAGAS evaluation setup, DeepEval integration, LangSmith evaluation runs, custom metrics, retrieval quality metrics, regression testing for LLM outputs

Implement comprehensive evaluation frameworks for LLM applications including RAGAS for RAG systems, DeepEval for CI/CD testing, LangSmith evaluation, custom metrics, and regression testing.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: RAGAS Evaluation Setup

Evaluate RAG systems with RAGAS metrics:

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
    answer_correctness
)
from datasets import Dataset
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

class RAGASEvaluator:
    """RAGAS evaluation for RAG systems."""

    def __init__(self, llm_model: str = "gpt-3.5-turbo", embeddings_model: str = "text-embedding-ada-002"):
        self.llm = ChatOpenAI(model=llm_model, temperature=0)
        self.embeddings = OpenAIEmbeddings(model=embeddings_model)

    def prepare_dataset(
        self,
        questions: list[str],
        ground_truths: list[str],
        answers: list[str],
        contexts: list[list[str]]
    ) -> Dataset:
        """Prepare dataset for RAGAS evaluation."""
        data = {
            "question": questions,
            "answer": answers,
            "contexts": contexts,
            "ground_truth": ground_truths
        }
        return Dataset.from_dict(data)

    def evaluate_ragas(
        self,
        dataset: Dataset,
        metrics: list = None
    ) -> dict:
        """Run RAGAS evaluation."""
        if metrics is None:
            metrics = [
                faithfulness,
                answer_relevancy,
                context_precision,
                context_recall,
                answer_correctness
            ]

        result = evaluate(
            dataset=dataset,
            metrics=metrics,
            llm=self.llm,
            embeddings=self.embeddings
        )

        return result

    def evaluate_rag_system(
        self,
        questions: list[str],
        ground_truths: list[str],
        rag_pipeline
    ) -> dict:
        """Evaluate a RAG system end-to-end."""
        answers = []
        contexts = []

        # Get answers and contexts from RAG system
        for question in questions:
            response = rag_pipeline.query(question)
            answers.append(response["answer"])
            contexts.append([ctx["text"] for ctx in response.get("contexts", [])])

        # Prepare dataset
        dataset = self.prepare_dataset(
            questions=questions,
            ground_truths=ground_truths,
            answers=answers,
            contexts=contexts
        )

        # Evaluate
        results = self.evaluate_ragas(dataset)

        return {
            "scores": results,
            "answers": answers,
            "contexts": contexts
        }

# Usage
evaluator = RAGASEvaluator()

# Example evaluation
questions = [
    "What is machine learning?",
    "Explain RAG systems"
]
ground_truths = [
    "Machine learning is a subset of AI...",
    "RAG combines retrieval and generation..."
]

# Prepare dataset
dataset = evaluator.prepare_dataset(
    questions=questions,
    ground_truths=ground_truths,
    answers=["ML is AI...", "RAG uses retrieval..."],
    contexts=[["Context 1", "Context 2"], ["Context 3", "Context 4"]]
)

# Evaluate
results = evaluator.evaluate_ragas(dataset)
print(results)
```

### Step 2: DeepEval Integration for CI/CD

Set up DeepEval for automated testing in CI/CD:

```python
from deepeval import evaluate, assert_test
from deepeval.metrics import GEval, AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.test_case import LLMTestCase
from deepeval.dataset import EvaluationDataset

class DeepEvalTestSuite:
    """DeepEval test suite for LLM applications."""

    def __init__(self):
        self.test_cases = []

    def create_test_case(
        self,
        input_text: str,
        actual_output: str,
        expected_output: str = None,
        context: list[str] = None,
        retrieval_context: list[str] = None
    ):
        """Create a test case."""
        test_case = LLMTestCase(
            input=input_text,
            actual_output=actual_output,
            expected_output=expected_output,
            context=context,
            retrieval_context=retrieval_context
        )
        self.test_cases.append(test_case)
        return test_case

    def test_answer_relevancy(self, test_case: LLMTestCase, threshold: float = 0.5):
        """Test answer relevancy."""
        metric = AnswerRelevancyMetric(threshold=threshold)
        metric.measure(test_case)
        assert_test(test_case, [metric])
        return metric.score

    def test_faithfulness(self, test_case: LLMTestCase, threshold: float = 0.5):
        """Test faithfulness to context."""
        metric = FaithfulnessMetric(threshold=threshold)
        metric.measure(test_case)
        assert_test(test_case, [metric])
        return metric.score

    def test_custom_geval(self, test_case: LLMTestCase, criteria: str, threshold: float = 0.5):
        """Test with custom GEval criteria."""
        metric = GEval(
            name="Custom Evaluation",
            criteria=criteria,
            threshold=threshold,
            model="gpt-4"
        )
        metric.measure(test_case)
        assert_test(test_case, [metric])
        return metric.score

    def run_suite(self, test_cases: list[LLMTestCase] = None):
        """Run test suite."""
        if test_cases is None:
            test_cases = self.test_cases

        results = []
        for test_case in test_cases:
            # Run all metrics
            relevancy_score = self.test_answer_relevancy(test_case)
            faithfulness_score = self.test_faithfulness(test_case)

            results.append({
                "test_case": test_case.input,
                "answer_relevancy": relevancy_score,
                "faithfulness": faithfulness_score
            })

        return results

# Usage
test_suite = DeepEvalTestSuite()

# Create test cases
test_case = test_suite.create_test_case(
    input_text="What is machine learning?",
    actual_output="Machine learning is a subset of AI...",
    expected_output="Machine learning is AI...",
    context=["ML is AI", "ML uses data"]
)

# Run tests
relevancy = test_suite.test_answer_relevancy(test_case, threshold=0.7)
faithfulness = test_suite.test_faithfulness(test_case, threshold=0.7)

# Custom evaluation
custom_score = test_suite.test_custom_geval(
    test_case,
    criteria="The answer should be concise and accurate",
    threshold=0.6
)
```

### Step 3: LangSmith Evaluation Runs

Use LangSmith for evaluation and dataset management:

```python
from langsmith import Client, evaluate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

class LangSmithEvaluator:
    """LangSmith evaluation setup."""

    def __init__(self, api_key: str = None):
        self.client = Client(api_key=api_key)
        self.llm = ChatOpenAI(model="gpt-3.5-turbo")

    def create_dataset(self, examples: list[dict], dataset_name: str):
        """Create evaluation dataset in LangSmith."""
        dataset = self.client.create_dataset(
            dataset_name=dataset_name,
            description="Evaluation dataset for LLM"
        )

        for example in examples:
            self.client.create_example(
                inputs=example["inputs"],
                outputs=example.get("outputs"),
                dataset_id=dataset.id
            )

        return dataset

    def evaluate_chain(
        self,
        chain,
        dataset_name: str,
        evaluators: list = None
    ):
        """Evaluate a LangChain chain."""
        if evaluators is None:
            # Default evaluators
            from langsmith.evaluation import LangChainStringEvaluator

            evaluators = [
                LangChainStringEvaluator("helpfulness"),
                LangChainStringEvaluator("correctness")
            ]

        results = evaluate(
            chain,
            data=dataset_name,
            evaluators=evaluators,
            experiment_prefix="evaluation_run"
        )

        return results

    def compare_models(
        self,
        chain1,
        chain2,
        dataset_name: str,
        experiment_name: str = "model_comparison"
    ):
        """Compare two models/chains."""
        results1 = evaluate(
            chain1,
            data=dataset_name,
            experiment_prefix=f"{experiment_name}_model1"
        )

        results2 = evaluate(
            chain2,
            data=dataset_name,
            experiment_prefix=f"{experiment_name}_model2"
        )

        return {
            "model1_results": results1,
            "model2_results": results2
        }

# Usage
evaluator = LangSmithEvaluator()

# Create dataset
examples = [
    {
        "inputs": {"question": "What is ML?"},
        "outputs": {"answer": "Machine learning is..."}
    }
]
dataset = evaluator.create_dataset(examples, "my_eval_dataset")

# Evaluate chain
chain = ChatPromptTemplate.from_template("{question}") | evaluator.llm
results = evaluator.evaluate_chain(chain, "my_eval_dataset")
```

### Step 4: Custom Metrics Creation

Create custom evaluation metrics:

```python
from typing import List, Dict
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class CustomMetrics:
    """Custom evaluation metrics."""

    def __init__(self):
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

    def semantic_similarity(self, reference: str, candidate: str) -> float:
        """Calculate semantic similarity."""
        ref_embedding = self.embedder.encode([reference])
        cand_embedding = self.embedder.encode([candidate])
        similarity = cosine_similarity(ref_embedding, cand_embedding)[0][0]
        return float(similarity)

    def answer_length_score(self, answer: str, min_length: int = 10, max_length: int = 500) -> float:
        """Score based on answer length."""
        length = len(answer.split())
        if length < min_length:
            return 0.0
        elif length > max_length:
            return 0.5
        else:
            return 1.0

    def keyword_coverage(self, answer: str, required_keywords: List[str]) -> float:
        """Check coverage of required keywords."""
        answer_lower = answer.lower()
        found = sum(1 for keyword in required_keywords if keyword.lower() in answer_lower)
        return found / len(required_keywords) if required_keywords else 0.0

    def factual_consistency(self, answer: str, context: List[str]) -> float:
        """Check if answer is consistent with context."""
        if not context:
            return 0.0

        answer_embedding = self.embedder.encode([answer])
        context_embeddings = self.embedder.encode(context)

        similarities = cosine_similarity(answer_embedding, context_embeddings)[0]
        max_similarity = float(np.max(similarities))

        return max_similarity

    def comprehensive_score(
        self,
        reference: str,
        candidate: str,
        context: List[str] = None,
        required_keywords: List[str] = None
    ) -> Dict[str, float]:
        """Calculate comprehensive score."""
        scores = {
            "semantic_similarity": self.semantic_similarity(reference, candidate),
            "length_score": self.answer_length_score(candidate),
        }

        if context:
            scores["factual_consistency"] = self.factual_consistency(candidate, context)

        if required_keywords:
            scores["keyword_coverage"] = self.keyword_coverage(candidate, required_keywords)

        # Weighted average
        weights = {
            "semantic_similarity": 0.4,
            "length_score": 0.2,
            "factual_consistency": 0.3,
            "keyword_coverage": 0.1
        }

        overall_score = sum(
            scores.get(key, 0) * weights.get(key, 0)
            for key in weights.keys()
        )

        scores["overall_score"] = overall_score
        return scores

# Usage
metrics = CustomMetrics()

score = metrics.comprehensive_score(
    reference="Machine learning is a subset of artificial intelligence.",
    candidate="ML is part of AI that learns from data.",
    context=["ML is AI", "ML uses data"],
    required_keywords=["machine learning", "AI", "data"]
)

print(f"Overall score: {score['overall_score']:.2f}")
```

### Step 5: Retrieval Quality Metrics

Evaluate retrieval quality:

```python
from typing import List, Dict
import numpy as np

class RetrievalMetrics:
    """Metrics for retrieval quality."""

    def precision_at_k(self, retrieved: List[str], relevant: List[str], k: int = 5) -> float:
        """Precision@K metric."""
        retrieved_k = retrieved[:k]
        relevant_set = set(relevant)
        retrieved_set = set(retrieved_k)

        if len(retrieved_set) == 0:
            return 0.0

        intersection = len(retrieved_set & relevant_set)
        return intersection / len(retrieved_set)

    def recall_at_k(self, retrieved: List[str], relevant: List[str], k: int = 5) -> float:
        """Recall@K metric."""
        retrieved_k = retrieved[:k]
        relevant_set = set(relevant)
        retrieved_set = set(retrieved_k)

        if len(relevant_set) == 0:
            return 0.0

        intersection = len(retrieved_set & relevant_set)
        return intersection / len(relevant_set)

    def mean_reciprocal_rank(self, retrieved: List[str], relevant: List[str]) -> float:
        """Mean Reciprocal Rank (MRR)."""
        relevant_set = set(relevant)

        for i, doc in enumerate(retrieved, 1):
            if doc in relevant_set:
                return 1.0 / i

        return 0.0

    def mean_average_precision(self, retrieved: List[str], relevant: List[str]) -> float:
        """Mean Average Precision (MAP)."""
        relevant_set = set(relevant)
        if len(relevant_set) == 0:
            return 0.0

        precisions = []
        relevant_found = 0

        for i, doc in enumerate(retrieved, 1):
            if doc in relevant_set:
                relevant_found += 1
                precision = relevant_found / i
                precisions.append(precision)

        if len(precisions) == 0:
            return 0.0

        return sum(precisions) / len(relevant_set)

    def ndcg_at_k(self, retrieved: List[str], relevant: List[str], k: int = 5) -> float:
        """Normalized Discounted Cumulative Gain@K."""
        retrieved_k = retrieved[:k]
        relevant_set = set(relevant)

        dcg = 0.0
        for i, doc in enumerate(retrieved_k, 1):
            if doc in relevant_set:
                dcg += 1.0 / np.log2(i + 1)

        # Ideal DCG
        ideal_relevant = min(len(relevant_set), k)
        idcg = sum(1.0 / np.log2(i + 1) for i in range(1, ideal_relevant + 1))

        if idcg == 0:
            return 0.0

        return dcg / idcg

    def evaluate_retrieval(
        self,
        queries: List[str],
        retrieved_docs: List[List[str]],
        relevant_docs: List[List[str]],
        k_values: List[int] = [1, 3, 5, 10]
    ) -> Dict[str, float]:
        """Comprehensive retrieval evaluation."""
        results = {}

        for k in k_values:
            precisions = []
            recalls = []
            ndcgs = []

            for retrieved, relevant in zip(retrieved_docs, relevant_docs):
                precisions.append(self.precision_at_k(retrieved, relevant, k))
                recalls.append(self.recall_at_k(retrieved, relevant, k))
                ndcgs.append(self.ndcg_at_k(retrieved, relevant, k))

            results[f"precision@{k}"] = np.mean(precisions)
            results[f"recall@{k}"] = np.mean(recalls)
            results[f"ndcg@{k}"] = np.mean(ndcgs)

        # MRR and MAP
        mrrs = [self.mean_reciprocal_rank(ret, rel) for ret, rel in zip(retrieved_docs, relevant_docs)]
        maps = [self.mean_average_precision(ret, rel) for ret, rel in zip(retrieved_docs, relevant_docs)]

        results["mrr"] = np.mean(mrrs)
        results["map"] = np.mean(maps)

        return results

# Usage
retrieval_metrics = RetrievalMetrics()

queries = ["What is ML?", "Explain RAG"]
retrieved = [
    ["doc1", "doc2", "doc3"],
    ["doc4", "doc5", "doc6"]
]
relevant = [
    ["doc1", "doc3"],
    ["doc4", "doc6"]
]

results = retrieval_metrics.evaluate_retrieval(queries, retrieved, relevant)
print(results)
```

### Step 6: Regression Testing for LLM Outputs

Implement regression testing to detect output changes:

```python
import hashlib
import json
from datetime import datetime
from pathlib import Path

class LLMRegressionTester:
    """Regression testing for LLM outputs."""

    def __init__(self, baseline_dir: str = "./baselines"):
        self.baseline_dir = Path(baseline_dir)
        self.baseline_dir.mkdir(exist_ok=True)

    def hash_output(self, output: str) -> str:
        """Create hash of output."""
        return hashlib.md5(output.encode()).hexdigest()

    def save_baseline(self, test_name: str, inputs: dict, output: str, metadata: dict = None):
        """Save baseline output."""
        baseline = {
            "test_name": test_name,
            "inputs": inputs,
            "output": output,
            "output_hash": self.hash_output(output),
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }

        baseline_path = self.baseline_dir / f"{test_name}.json"
        with open(baseline_path, "w") as f:
            json.dump(baseline, f, indent=2)

    def load_baseline(self, test_name: str) -> dict:
        """Load baseline."""
        baseline_path = self.baseline_dir / f"{test_name}.json"
        if not baseline_path.exists():
            return None

        with open(baseline_path, "r") as f:
            return json.load(f)

    def test_regression(
        self,
        test_name: str,
        inputs: dict,
        current_output: str,
        threshold: float = 0.9,
        similarity_func=None
    ) -> dict:
        """Test for regression."""
        baseline = self.load_baseline(test_name)

        if baseline is None:
            # No baseline, save current as baseline
            self.save_baseline(test_name, inputs, current_output)
            return {
                "status": "new_baseline",
                "message": "No baseline found, saved current output as baseline"
            }

        baseline_output = baseline["output"]
        baseline_hash = baseline["output_hash"]
        current_hash = self.hash_output(current_output)

        # Exact match
        if baseline_hash == current_hash:
            return {
                "status": "pass",
                "message": "Output matches baseline exactly"
            }

        # Semantic similarity check
        if similarity_func:
            similarity = similarity_func(baseline_output, current_output)
            if similarity >= threshold:
                return {
                    "status": "pass",
                    "similarity": similarity,
                    "message": f"Output is similar to baseline (similarity: {similarity:.2f})"
                }
            else:
                return {
                    "status": "fail",
                    "similarity": similarity,
                    "baseline": baseline_output,
                    "current": current_output,
                    "message": f"Output differs from baseline (similarity: {similarity:.2f} < {threshold})"
                }

        # No similarity function, check for significant differences
        return {
            "status": "warning",
            "baseline": baseline_output,
            "current": current_output,
            "message": "Output differs from baseline (no similarity function provided)"
        }

    def update_baseline(self, test_name: str, new_output: str, reason: str = None):
        """Update baseline (after manual review)."""
        baseline = self.load_baseline(test_name)
        if baseline:
            baseline["output"] = new_output
            baseline["output_hash"] = self.hash_output(new_output)
            baseline["updated_at"] = datetime.now().isoformat()
            baseline["update_reason"] = reason

            baseline_path = self.baseline_dir / f"{test_name}.json"
            with open(baseline_path, "w") as f:
                json.dump(baseline, f, indent=2)

# Usage
regression_tester = LLMRegressionTester()

# Test regression
result = regression_tester.test_regression(
    test_name="test_ml_question",
    inputs={"question": "What is ML?"},
    current_output="Machine learning is a subset of AI...",
    threshold=0.9,
    similarity_func=lambda a, b: metrics.semantic_similarity(a, b)
)

if result["status"] == "fail":
    print(f"Regression detected: {result['message']}")
```

## Output

After evaluation, you'll have:

1. **Evaluation Results** - Comprehensive scores and metrics
2. **Test Reports** - Pass/fail status for test cases
3. **Comparison Data** - Model/prompt comparison results
4. **Baseline Data** - Regression test baselines
5. **Visualizations** - Charts and graphs of metrics
6. **CI/CD Integration** - Automated test results

## Best Practices

- Use RAGAS for RAG system evaluation
- Set up DeepEval for CI/CD testing
- Track evaluations in LangSmith
- Create custom metrics for domain-specific needs
- Measure retrieval quality separately
- Implement regression testing for stability
- Document evaluation criteria and thresholds
- Automate evaluation in CI/CD pipelines

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| No evaluation | Always evaluate before deployment |
| Single metric | Use multiple metrics |
| No baseline | Establish baselines for regression |
| Manual testing only | Automate with CI/CD |
| Ignoring retrieval | Evaluate retrieval separately |
| No documentation | Document evaluation criteria |

## Related

- Knowledge: `{directories.knowledge}/llm-evaluation-patterns.json`, `{directories.knowledge}/llm-evaluation-frameworks.json`
- Skill: `model-training`
- Skill: `model-fine-tuning`
- Skill: `agent-testing`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.

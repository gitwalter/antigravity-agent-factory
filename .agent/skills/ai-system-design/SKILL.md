---
description: Architecture patterns, technology selection, scalability planning, and
  vector DB selection for AI applications
name: ai-system-design
type: skill
---

# Ai System Design

Architecture patterns, technology selection, scalability planning, and vector DB selection for AI applications

## 
# AI System Design Skill

Design scalable AI systems with appropriate architecture patterns, technology selection, and infrastructure planning.

## 
# AI System Design Skill

Design scalable AI systems with appropriate architecture patterns, technology selection, and infrastructure planning.

## Process
### Step 1: Architecture Patterns

```python
# architecture_patterns.py
from enum import Enum
from typing import Dict, List
from dataclasses import dataclass

class ArchitecturePattern(Enum):
    MONOLITH = "monolith"
    MICROSERVICES = "microservices"
    SERVERLESS = "serverless"
    EDGE = "edge"

@dataclass
class ArchitectureDecision:
    pattern: ArchitecturePattern
    use_cases: List[str]
    pros: List[str]
    cons: List[str]
    best_for: str

ARCHITECTURE_GUIDE = {
    ArchitecturePattern.MONOLITH: ArchitectureDecision(
        pattern=ArchitecturePattern.MONOLITH,
        use_cases=[
            "Small to medium applications",
            "Rapid prototyping",
            "Single team ownership",
        ],
        pros=[
            "Simpler deployment",
            "Easier debugging",
            "Lower operational overhead",
        ],
        cons=[
            "Harder to scale components independently",
            "Tight coupling",
            "Single point of failure",
        ],
        best_for="Applications with < 10K requests/day",
    ),
    ArchitecturePattern.MICROSERVICES: ArchitectureDecision(
        pattern=ArchitecturePattern.MICROSERVICES,
        use_cases=[
            "Large-scale applications",
            "Multiple teams",
            "Independent scaling needs",
        ],
        pros=[
            "Independent scaling",
            "Technology diversity",
            "Fault isolation",
        ],
        cons=[
            "Complex deployment",
            "Network latency",
            "Distributed debugging",
        ],
        best_for="Applications with > 100K requests/day",
    ),
    ArchitecturePattern.SERVERLESS: ArchitectureDecision(
        pattern=ArchitecturePattern.SERVERLESS,
        use_cases=[
            "Event-driven workloads",
            "Variable traffic",
            "Cost optimization",
        ],
        pros=[
            "Auto-scaling",
            "Pay-per-use",
            "No infrastructure management",
        ],
        cons=[
            "Cold start latency",
            "Vendor lock-in",
            "Limited execution time",
        ],
        best_for="Sporadic or event-driven workloads",
    ),
}

def select_architecture(
    expected_traffic: int,
    team_size: int,
    latency_requirement_ms: int,
) -> ArchitecturePattern:
    """Select architecture pattern based on requirements."""
    
    if expected_traffic < 10000 and team_size < 5:
        return ArchitecturePattern.MONOLITH
    elif latency_requirement_ms < 100:
        return ArchitecturePattern.EDGE
    elif expected_traffic > 100000:
        return ArchitecturePattern.MICROSERVICES
    else:
        return ArchitecturePattern.SERVERLESS
```

### Step 2: Technology Selection Framework

```python
# technology_selection.py
from enum import Enum
from typing import Dict, List
from dataclasses import dataclass

class FrameworkType(Enum):
    LANGCHAIN = "langchain"
    LANGGRAPH = "langgraph"
    CREWAI = "crewai"
    DSPY = "dspy"
    CUSTOM = "custom"

@dataclass
class FrameworkComparison:
    name: str
    best_for: List[str]
    strengths: List[str]
    weaknesses: List[str]
    complexity: str  # "low", "medium", "high"

FRAMEWORK_GUIDE = {
    FrameworkType.LANGCHAIN: FrameworkComparison(
        name="LangChain",
        best_for=[
            "RAG applications",
            "Tool-using agents",
            "Chain composition",
            "Integration with many providers",
        ],
        strengths=[
            "Large ecosystem",
            "Many integrations",
            "Good documentation",
            "Flexible",
        ],
        weaknesses=[
            "Can be verbose",
            "Steeper learning curve",
            "Less opinionated",
        ],
        complexity="medium",
    ),
    FrameworkType.LANGGRAPH: FrameworkComparison(
        name="LangGraph",
        best_for=[
            "Stateful agents",
            "Complex workflows",
            "Multi-step reasoning",
            "Agentic loops",
        ],
        strengths=[
            "State management",
            "Cycles and loops",
            "Checkpointing",
            "Visualization",
        ],
        weaknesses=[
            "Newer framework",
            "Smaller community",
            "Requires LangChain knowledge",
        ],
        complexity="medium-high",
    ),
    FrameworkType.CREWAI: FrameworkComparison(
        name="CrewAI",
        best_for=[
            "Multi-agent systems",
            "Collaborative agents",
            "Role-based agents",
            "Workflow orchestration",
        ],
        strengths=[
            "Agent collaboration",
            "Role definitions",
            "Task delegation",
            "Built-in planning",
        ],
        weaknesses=[
            "Less flexible",
            "Opinionated structure",
            "Smaller ecosystem",
        ],
        complexity="low-medium",
    ),
    FrameworkType.DSPY: FrameworkComparison(
        name="DSPy",
        best_for=[
            "Prompt optimization",
            "Systematic prompt engineering",
            "Research applications",
            "Optimization-focused workflows",
        ],
        strengths=[
            "Prompt optimization",
            "Systematic approach",
            "Research-oriented",
            "Composable modules",
        ],
        weaknesses=[
            "Steeper learning curve",
            "Smaller community",
            "Less production-ready",
        ],
        complexity="high",
    ),
}

def select_framework(
    use_case: str,
    needs_state_management: bool,
    needs_multi_agent: bool,
    needs_optimization: bool,
) -> FrameworkType:
    """Select framework based on requirements."""
    
    if needs_multi_agent and not needs_state_management:
        return FrameworkType.CREWAI
    elif needs_state_management or needs_optimization:
        if needs_optimization:
            return FrameworkType.DSPY
        else:
            return FrameworkType.LANGGRAPH
    else:
        return FrameworkType.LANGCHAIN
```

### Step 3: Vector Database Selection Guide

```python
# vector_db_selection.py
from enum import Enum
from typing import Dict, List
from dataclasses import dataclass

class VectorDB(Enum):
    PINECONE = "pinecone"
    QDRANT = "qdrant"
    WEAVIATE = "weaviate"
    CHROMADB = "chromadb"
    MILVUS = "milvus"

@dataclass
class VectorDBComparison:
    name: str
    deployment: str  # "managed", "self-hosted", "both"
    scalability: str  # "low", "medium", "high"
    cost: str  # "free", "low", "medium", "high"
    features: List[str]
    best_for: str

VECTOR_DB_GUIDE = {
    VectorDB.PINECONE: VectorDBComparison(
        name="Pinecone",
        deployment="managed",
        scalability="high",
        cost="medium-high",
        features=[
            "Fully managed",
            "High performance",
            "Easy to use",
            "Serverless option",
        ],
        best_for="Production applications needing reliability",
    ),
    VectorDB.QDRANT: VectorDBComparison(
        name="Qdrant",
        deployment="both",
        scalability="high",
        cost="low-medium",
        features=[
            "Self-hostable",
            "High performance",
            "Filtering support",
            "Docker deployment",
        ],
        best_for="Self-hosted production deployments",
    ),
    VectorDB.WEAVIATE: VectorDBComparison(
        name="Weaviate",
        deployment="both",
        scalability="high",
        cost="low-medium",
        features=[
            "GraphQL API",
            "Hybrid search",
            "Multi-tenancy",
            "Built-in ML models",
        ],
        best_for="Applications needing hybrid search",
    ),
    VectorDB.CHROMADB: VectorDBComparison(
        name="ChromaDB",
        deployment="both",
        scalability="medium",
        cost="free",
        features=[
            "Easy to use",
            "Embedding functions",
            "Local-first",
            "Python-native",
        ],
        best_for="Development and small-scale production",
    ),
    VectorDB.MILVUS: VectorDBComparison(
        name="Milvus",
        deployment="self-hosted",
        scalability="very-high",
        cost="low",
        features=[
            "Distributed",
            "High throughput",
            "Advanced indexing",
            "Kubernetes-native",
        ],
        best_for="Large-scale self-hosted deployments",
    ),
}

def select_vector_db(
    scale: str,  # "small", "medium", "large"
    budget: str,  # "free", "low", "medium", "high"
    managed_preference: bool,
) -> VectorDB:
    """Select vector database based on requirements."""
    
    if budget == "free" or scale == "small":
        return VectorDB.CHROMADB
    elif managed_preference and budget != "free":
        return VectorDB.PINECONE
    elif scale == "large" and not managed_preference:
        return VectorDB.MILVUS
    elif managed_preference:
        return VectorDB.WEAVIATE
    else:
        return VectorDB.QDRANT
```

### Step 4: LLM Provider Comparison Framework

```python
# llm_provider_comparison.py
from enum import Enum
from typing import Dict, List
from dataclasses import dataclass

class LLMProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    MISTRAL = "mistral"
    COHERE = "cohere"
    OPEN_SOURCE = "open_source"

@dataclass
class ProviderComparison:
    name: str
    models: List[str]
    strengths: List[str]
    weaknesses: List[str]
    cost_tier: str  # "low", "medium", "high"
    best_for: str

PROVIDER_GUIDE = {
    LLMProvider.OPENAI: ProviderComparison(
        name="OpenAI",
        models=["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
        strengths=[
            "Best performance",
            "Large context windows",
            "Function calling",
            "Wide adoption",
        ],
        weaknesses=[
            "Higher cost",
            "Rate limits",
            "API dependency",
        ],
        cost_tier="high",
        best_for="Applications needing best quality",
    ),
    LLMProvider.ANTHROPIC: ProviderComparison(
        name="Anthropic",
        models=["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
        strengths=[
            "Long context (200K tokens)",
            "Safety-focused",
            "Good reasoning",
            "Constitutional AI",
        ],
        weaknesses=[
            "Higher cost",
            "Smaller ecosystem",
            "Fewer integrations",
        ],
        cost_tier="high",
        best_for="Long-context and safety-critical applications",
    ),
    LLMProvider.GOOGLE: ProviderComparison(
        name="Google",
        models=["gemini-pro", "gemini-ultra"],
        strengths=[
            "Multimodal",
            "Good performance",
            "Competitive pricing",
            "Google Cloud integration",
        ],
        weaknesses=[
            "Newer API",
            "Less mature",
            "Fewer examples",
        ],
        cost_tier="medium",
        best_for="Multimodal and Google Cloud users",
    ),
    LLMProvider.MISTRAL: ProviderComparison(
        name="Mistral AI",
        models=["mistral-large", "mistral-medium", "mistral-small"],
        strengths=[
            "Good performance",
            "Competitive pricing",
            "Open source models",
            "European company",
        ],
        weaknesses=[
            "Smaller community",
            "Fewer integrations",
            "Less documentation",
        ],
        cost_tier="medium",
        best_for="Cost-conscious applications",
    ),
    LLMProvider.OPEN_SOURCE: ProviderComparison(
        name="Open Source",
        models=["Llama 2", "Mistral 7B", "Mixtral"],
        strengths=[
            "No API costs",
            "Full control",
            "Privacy",
            "Customizable",
        ],
        weaknesses=[
            "Infrastructure costs",
            "Lower performance",
            "More maintenance",
        ],
        cost_tier="low",
        best_for="Privacy-sensitive and high-volume applications",
    ),
}

def select_provider(
    quality_requirement: str,  # "high", "medium", "low"
    budget: str,  # "high", "medium", "low"
    privacy_requirement: bool,
    volume: str,  # "low", "medium", "high"
) -> LLMProvider:
    """Select LLM provider based on requirements."""
    
    if privacy_requirement or volume == "high":
        return LLMProvider.OPEN_SOURCE
    elif quality_requirement == "high" and budget != "low":
        return LLMProvider.OPENAI
    elif budget == "low":
        return LLMProvider.MISTRAL
    else:
        return LLMProvider.ANTHROPIC
```

### Step 5: Embedding Model Selection

```python
# embedding_selection.py
from enum import Enum
from typing import Dict
from dataclasses import dataclass

class EmbeddingModel(Enum):
    OPENAI_ADA = "text-embedding-ada-002"
    OPENAI_3_SMALL = "text-embedding-3-small"
    OPENAI_3_LARGE = "text-embedding-3-large"
    COHERE_V3 = "cohere-v3"
    SENTENCE_TRANSFORMERS = "sentence-transformers"

@dataclass
class EmbeddingComparison:
    name: str
    dimensions: int
    cost_per_1M_tokens: float
    quality: str  # "low", "medium", "high"
    best_for: str

EMBEDDING_GUIDE = {
    EmbeddingModel.OPENAI_ADA: EmbeddingComparison(
        name="OpenAI Ada-002",
        dimensions=1536,
        cost_per_1M_tokens=0.10,
        quality="high",
        best_for="General-purpose embeddings",
    ),
    EmbeddingModel.OPENAI_3_SMALL: EmbeddingComparison(
        name="OpenAI 3 Small",
        dimensions=1536,
        cost_per_1M_tokens=0.02,
        quality="high",
        best_for="Cost-effective high-quality embeddings",
    ),
    EmbeddingModel.OPENAI_3_LARGE: EmbeddingComparison(
        name="OpenAI 3 Large",
        dimensions=3072,
        cost_per_1M_tokens=0.13,
        quality="very-high",
        best_for="Applications needing best quality",
    ),
    EmbeddingModel.COHERE_V3: EmbeddingComparison(
        name="Cohere v3",
        dimensions=1024,
        cost_per_1M_tokens=0.10,
        quality="high",
        best_for="Multilingual applications",
    ),
    EmbeddingModel.SENTENCE_TRANSFORMERS: EmbeddingComparison(
        name="Sentence Transformers",
        dimensions=384,
        cost_per_1M_tokens=0.0,  # Free
        quality="medium-high",
        best_for="Self-hosted and cost-sensitive applications",
    ),
}

def select_embedding_model(
    budget: str,
    quality_requirement: str,
    self_hosted: bool,
) -> EmbeddingModel:
    """Select embedding model."""
    
    if self_hosted:
        return EmbeddingModel.SENTENCE_TRANSFORMERS
    elif budget == "low":
        return EmbeddingModel.OPENAI_3_SMALL
    elif quality_requirement == "very-high":
        return EmbeddingModel.OPENAI_3_LARGE
    else:
        return EmbeddingModel.OPENAI_ADA
```

### Step 6: Scalability Planning

```python
# scalability_planning.py
from typing import Dict
from dataclasses import dataclass

@dataclass
class ScalabilityPlan:
    horizontal_scaling: bool
    vertical_scaling: bool
    gpu_allocation: str
    caching_strategy: str
    load_balancing: bool

def plan_scalability(
    expected_rps: int,  # Requests per second
    avg_latency_ms: int,
    gpu_available: bool,
) -> ScalabilityPlan:
    """Plan scalability strategy."""
    
    # Calculate required capacity
    required_capacity = expected_rps * (avg_latency_ms / 1000)
    
    if required_capacity < 10:
        # Low traffic: vertical scaling
        return ScalabilityPlan(
            horizontal_scaling=False,
            vertical_scaling=True,
            gpu_allocation="single",
            caching_strategy="in-memory",
            load_balancing=False,
        )
    elif required_capacity < 100:
        # Medium traffic: horizontal with caching
        return ScalabilityPlan(
            horizontal_scaling=True,
            vertical_scaling=False,
            gpu_allocation="distributed",
            caching_strategy="redis",
            load_balancing=True,
        )
    else:
        # High traffic: full horizontal scaling
        return ScalabilityPlan(
            horizontal_scaling=True,
            vertical_scaling=False,
            gpu_allocation="kubernetes",
            caching_strategy="distributed-cache",
            load_balancing=True,
        )
```

### Step 7: Sync vs Async Decision Tree

```python
# sync_async_design.py
from enum import Enum
from typing import Dict

class RequestPattern(Enum):
    SYNC = "synchronous"
    ASYNC = "asynchronous"
    HYBRID = "hybrid"

def select_request_pattern(
    latency_requirement_ms: int,
    user_waiting: bool,
    batch_processing: bool,
) -> RequestPattern:
    """Select sync vs async pattern."""
    
    if latency_requirement_ms < 1000 and user_waiting:
        return RequestPattern.SYNC
    elif batch_processing or not user_waiting:
        return RequestPattern.ASYNC
    else:
        return RequestPattern.HYBRID

# Async implementation example
import asyncio
from typing import List

async def process_batch_async(requests: List[str]):
    """Process batch asynchronously."""
    tasks = [process_single(req) for req in requests]
    results = await asyncio.gather(*tasks)
    return results
```

```python
# architecture_patterns.py
from enum import Enum
from typing import Dict, List
from dataclasses import dataclass

class ArchitecturePattern(Enum):
    MONOLITH = "monolith"
    MICROSERVICES = "microservices"
    SERVERLESS = "serverless"
    EDGE = "edge"

@dataclass
class ArchitectureDecision:
    pattern: ArchitecturePattern
    use_cases: List[str]
    pros: List[str]
    cons: List[str]
    best_for: str

ARCHITECTURE_GUIDE = {
    ArchitecturePattern.MONOLITH: ArchitectureDecision(
        pattern=ArchitecturePattern.MONOLITH,
        use_cases=[
            "Small to medium applications",
            "Rapid prototyping",
            "Single team ownership",
        ],
        pros=[
            "Simpler deployment",
            "Easier debugging",
            "Lower operational overhead",
        ],
        cons=[
            "Harder to scale components independently",
            "Tight coupling",
            "Single point of failure",
        ],
        best_for="Applications with < 10K requests/day",
    ),
    ArchitecturePattern.MICROSERVICES: ArchitectureDecision(
        pattern=ArchitecturePattern.MICROSERVICES,
        use_cases=[
            "Large-scale applications",
            "Multiple teams",
            "Independent scaling needs",
        ],
        pros=[
            "Independent scaling",
            "Technology diversity",
            "Fault isolation",
        ],
        cons=[
            "Complex deployment",
            "Network latency",
            "Distributed debugging",
        ],
        best_for="Applications with > 100K requests/day",
    ),
    ArchitecturePattern.SERVERLESS: ArchitectureDecision(
        pattern=ArchitecturePattern.SERVERLESS,
        use_cases=[
            "Event-driven workloads",
            "Variable traffic",
            "Cost optimization",
        ],
        pros=[
            "Auto-scaling",
            "Pay-per-use",
            "No infrastructure management",
        ],
        cons=[
            "Cold start latency",
            "Vendor lock-in",
            "Limited execution time",
        ],
        best_for="Sporadic or event-driven workloads",
    ),
}

def select_architecture(
    expected_traffic: int,
    team_size: int,
    latency_requirement_ms: int,
) -> ArchitecturePattern:
    """Select architecture pattern based on requirements."""
    
    if expected_traffic < 10000 and team_size < 5:
        return ArchitecturePattern.MONOLITH
    elif latency_requirement_ms < 100:
        return ArchitecturePattern.EDGE
    elif expected_traffic > 100000:
        return ArchitecturePattern.MICROSERVICES
    else:
        return ArchitecturePattern.SERVERLESS
```

```python
# technology_selection.py
from enum import Enum
from typing import Dict, List
from dataclasses import dataclass

class FrameworkType(Enum):
    LANGCHAIN = "langchain"
    LANGGRAPH = "langgraph"
    CREWAI = "crewai"
    DSPY = "dspy"
    CUSTOM = "custom"

@dataclass
class FrameworkComparison:
    name: str
    best_for: List[str]
    strengths: List[str]
    weaknesses: List[str]
    complexity: str  # "low", "medium", "high"

FRAMEWORK_GUIDE = {
    FrameworkType.LANGCHAIN: FrameworkComparison(
        name="LangChain",
        best_for=[
            "RAG applications",
            "Tool-using agents",
            "Chain composition",
            "Integration with many providers",
        ],
        strengths=[
            "Large ecosystem",
            "Many integrations",
            "Good documentation",
            "Flexible",
        ],
        weaknesses=[
            "Can be verbose",
            "Steeper learning curve",
            "Less opinionated",
        ],
        complexity="medium",
    ),
    FrameworkType.LANGGRAPH: FrameworkComparison(
        name="LangGraph",
        best_for=[
            "Stateful agents",
            "Complex workflows",
            "Multi-step reasoning",
            "Agentic loops",
        ],
        strengths=[
            "State management",
            "Cycles and loops",
            "Checkpointing",
            "Visualization",
        ],
        weaknesses=[
            "Newer framework",
            "Smaller community",
            "Requires LangChain knowledge",
        ],
        complexity="medium-high",
    ),
    FrameworkType.CREWAI: FrameworkComparison(
        name="CrewAI",
        best_for=[
            "Multi-agent systems",
            "Collaborative agents",
            "Role-based agents",
            "Workflow orchestration",
        ],
        strengths=[
            "Agent collaboration",
            "Role definitions",
            "Task delegation",
            "Built-in planning",
        ],
        weaknesses=[
            "Less flexible",
            "Opinionated structure",
            "Smaller ecosystem",
        ],
        complexity="low-medium",
    ),
    FrameworkType.DSPY: FrameworkComparison(
        name="DSPy",
        best_for=[
            "Prompt optimization",
            "Systematic prompt engineering",
            "Research applications",
            "Optimization-focused workflows",
        ],
        strengths=[
            "Prompt optimization",
            "Systematic approach",
            "Research-oriented",
            "Composable modules",
        ],
        weaknesses=[
            "Steeper learning curve",
            "Smaller community",
            "Less production-ready",
        ],
        complexity="high",
    ),
}

def select_framework(
    use_case: str,
    needs_state_management: bool,
    needs_multi_agent: bool,
    needs_optimization: bool,
) -> FrameworkType:
    """Select framework based on requirements."""
    
    if needs_multi_agent and not needs_state_management:
        return FrameworkType.CREWAI
    elif needs_state_management or needs_optimization:
        if needs_optimization:
            return FrameworkType.DSPY
        else:
            return FrameworkType.LANGGRAPH
    else:
        return FrameworkType.LANGCHAIN
```

```python
# vector_db_selection.py
from enum import Enum
from typing import Dict, List
from dataclasses import dataclass

class VectorDB(Enum):
    PINECONE = "pinecone"
    QDRANT = "qdrant"
    WEAVIATE = "weaviate"
    CHROMADB = "chromadb"
    MILVUS = "milvus"

@dataclass
class VectorDBComparison:
    name: str
    deployment: str  # "managed", "self-hosted", "both"
    scalability: str  # "low", "medium", "high"
    cost: str  # "free", "low", "medium", "high"
    features: List[str]
    best_for: str

VECTOR_DB_GUIDE = {
    VectorDB.PINECONE: VectorDBComparison(
        name="Pinecone",
        deployment="managed",
        scalability="high",
        cost="medium-high",
        features=[
            "Fully managed",
            "High performance",
            "Easy to use",
            "Serverless option",
        ],
        best_for="Production applications needing reliability",
    ),
    VectorDB.QDRANT: VectorDBComparison(
        name="Qdrant",
        deployment="both",
        scalability="high",
        cost="low-medium",
        features=[
            "Self-hostable",
            "High performance",
            "Filtering support",
            "Docker deployment",
        ],
        best_for="Self-hosted production deployments",
    ),
    VectorDB.WEAVIATE: VectorDBComparison(
        name="Weaviate",
        deployment="both",
        scalability="high",
        cost="low-medium",
        features=[
            "GraphQL API",
            "Hybrid search",
            "Multi-tenancy",
            "Built-in ML models",
        ],
        best_for="Applications needing hybrid search",
    ),
    VectorDB.CHROMADB: VectorDBComparison(
        name="ChromaDB",
        deployment="both",
        scalability="medium",
        cost="free",
        features=[
            "Easy to use",
            "Embedding functions",
            "Local-first",
            "Python-native",
        ],
        best_for="Development and small-scale production",
    ),
    VectorDB.MILVUS: VectorDBComparison(
        name="Milvus",
        deployment="self-hosted",
        scalability="very-high",
        cost="low",
        features=[
            "Distributed",
            "High throughput",
            "Advanced indexing",
            "Kubernetes-native",
        ],
        best_for="Large-scale self-hosted deployments",
    ),
}

def select_vector_db(
    scale: str,  # "small", "medium", "large"
    budget: str,  # "free", "low", "medium", "high"
    managed_preference: bool,
) -> VectorDB:
    """Select vector database based on requirements."""
    
    if budget == "free" or scale == "small":
        return VectorDB.CHROMADB
    elif managed_preference and budget != "free":
        return VectorDB.PINECONE
    elif scale == "large" and not managed_preference:
        return VectorDB.MILVUS
    elif managed_preference:
        return VectorDB.WEAVIATE
    else:
        return VectorDB.QDRANT
```

```python
# llm_provider_comparison.py
from enum import Enum
from typing import Dict, List
from dataclasses import dataclass

class LLMProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    MISTRAL = "mistral"
    COHERE = "cohere"
    OPEN_SOURCE = "open_source"

@dataclass
class ProviderComparison:
    name: str
    models: List[str]
    strengths: List[str]
    weaknesses: List[str]
    cost_tier: str  # "low", "medium", "high"
    best_for: str

PROVIDER_GUIDE = {
    LLMProvider.OPENAI: ProviderComparison(
        name="OpenAI",
        models=["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
        strengths=[
            "Best performance",
            "Large context windows",
            "Function calling",
            "Wide adoption",
        ],
        weaknesses=[
            "Higher cost",
            "Rate limits",
            "API dependency",
        ],
        cost_tier="high",
        best_for="Applications needing best quality",
    ),
    LLMProvider.ANTHROPIC: ProviderComparison(
        name="Anthropic",
        models=["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
        strengths=[
            "Long context (200K tokens)",
            "Safety-focused",
            "Good reasoning",
            "Constitutional AI",
        ],
        weaknesses=[
            "Higher cost",
            "Smaller ecosystem",
            "Fewer integrations",
        ],
        cost_tier="high",
        best_for="Long-context and safety-critical applications",
    ),
    LLMProvider.GOOGLE: ProviderComparison(
        name="Google",
        models=["gemini-pro", "gemini-ultra"],
        strengths=[
            "Multimodal",
            "Good performance",
            "Competitive pricing",
            "Google Cloud integration",
        ],
        weaknesses=[
            "Newer API",
            "Less mature",
            "Fewer examples",
        ],
        cost_tier="medium",
        best_for="Multimodal and Google Cloud users",
    ),
    LLMProvider.MISTRAL: ProviderComparison(
        name="Mistral AI",
        models=["mistral-large", "mistral-medium", "mistral-small"],
        strengths=[
            "Good performance",
            "Competitive pricing",
            "Open source models",
            "European company",
        ],
        weaknesses=[
            "Smaller community",
            "Fewer integrations",
            "Less documentation",
        ],
        cost_tier="medium",
        best_for="Cost-conscious applications",
    ),
    LLMProvider.OPEN_SOURCE: ProviderComparison(
        name="Open Source",
        models=["Llama 2", "Mistral 7B", "Mixtral"],
        strengths=[
            "No API costs",
            "Full control",
            "Privacy",
            "Customizable",
        ],
        weaknesses=[
            "Infrastructure costs",
            "Lower performance",
            "More maintenance",
        ],
        cost_tier="low",
        best_for="Privacy-sensitive and high-volume applications",
    ),
}

def select_provider(
    quality_requirement: str,  # "high", "medium", "low"
    budget: str,  # "high", "medium", "low"
    privacy_requirement: bool,
    volume: str,  # "low", "medium", "high"
) -> LLMProvider:
    """Select LLM provider based on requirements."""
    
    if privacy_requirement or volume == "high":
        return LLMProvider.OPEN_SOURCE
    elif quality_requirement == "high" and budget != "low":
        return LLMProvider.OPENAI
    elif budget == "low":
        return LLMProvider.MISTRAL
    else:
        return LLMProvider.ANTHROPIC
```

```python
# embedding_selection.py
from enum import Enum
from typing import Dict
from dataclasses import dataclass

class EmbeddingModel(Enum):
    OPENAI_ADA = "text-embedding-ada-002"
    OPENAI_3_SMALL = "text-embedding-3-small"
    OPENAI_3_LARGE = "text-embedding-3-large"
    COHERE_V3 = "cohere-v3"
    SENTENCE_TRANSFORMERS = "sentence-transformers"

@dataclass
class EmbeddingComparison:
    name: str
    dimensions: int
    cost_per_1M_tokens: float
    quality: str  # "low", "medium", "high"
    best_for: str

EMBEDDING_GUIDE = {
    EmbeddingModel.OPENAI_ADA: EmbeddingComparison(
        name="OpenAI Ada-002",
        dimensions=1536,
        cost_per_1M_tokens=0.10,
        quality="high",
        best_for="General-purpose embeddings",
    ),
    EmbeddingModel.OPENAI_3_SMALL: EmbeddingComparison(
        name="OpenAI 3 Small",
        dimensions=1536,
        cost_per_1M_tokens=0.02,
        quality="high",
        best_for="Cost-effective high-quality embeddings",
    ),
    EmbeddingModel.OPENAI_3_LARGE: EmbeddingComparison(
        name="OpenAI 3 Large",
        dimensions=3072,
        cost_per_1M_tokens=0.13,
        quality="very-high",
        best_for="Applications needing best quality",
    ),
    EmbeddingModel.COHERE_V3: EmbeddingComparison(
        name="Cohere v3",
        dimensions=1024,
        cost_per_1M_tokens=0.10,
        quality="high",
        best_for="Multilingual applications",
    ),
    EmbeddingModel.SENTENCE_TRANSFORMERS: EmbeddingComparison(
        name="Sentence Transformers",
        dimensions=384,
        cost_per_1M_tokens=0.0,  # Free
        quality="medium-high",
        best_for="Self-hosted and cost-sensitive applications",
    ),
}

def select_embedding_model(
    budget: str,
    quality_requirement: str,
    self_hosted: bool,
) -> EmbeddingModel:
    """Select embedding model."""
    
    if self_hosted:
        return EmbeddingModel.SENTENCE_TRANSFORMERS
    elif budget == "low":
        return EmbeddingModel.OPENAI_3_SMALL
    elif quality_requirement == "very-high":
        return EmbeddingModel.OPENAI_3_LARGE
    else:
        return EmbeddingModel.OPENAI_ADA
```

```python
# scalability_planning.py
from typing import Dict
from dataclasses import dataclass

@dataclass
class ScalabilityPlan:
    horizontal_scaling: bool
    vertical_scaling: bool
    gpu_allocation: str
    caching_strategy: str
    load_balancing: bool

def plan_scalability(
    expected_rps: int,  # Requests per second
    avg_latency_ms: int,
    gpu_available: bool,
) -> ScalabilityPlan:
    """Plan scalability strategy."""
    
    # Calculate required capacity
    required_capacity = expected_rps * (avg_latency_ms / 1000)
    
    if required_capacity < 10:
        # Low traffic: vertical scaling
        return ScalabilityPlan(
            horizontal_scaling=False,
            vertical_scaling=True,
            gpu_allocation="single",
            caching_strategy="in-memory",
            load_balancing=False,
        )
    elif required_capacity < 100:
        # Medium traffic: horizontal with caching
        return ScalabilityPlan(
            horizontal_scaling=True,
            vertical_scaling=False,
            gpu_allocation="distributed",
            caching_strategy="redis",
            load_balancing=True,
        )
    else:
        # High traffic: full horizontal scaling
        return ScalabilityPlan(
            horizontal_scaling=True,
            vertical_scaling=False,
            gpu_allocation="kubernetes",
            caching_strategy="distributed-cache",
            load_balancing=True,
        )
```

```python
# sync_async_design.py
from enum import Enum
from typing import Dict

class RequestPattern(Enum):
    SYNC = "synchronous"
    ASYNC = "asynchronous"
    HYBRID = "hybrid"

def select_request_pattern(
    latency_requirement_ms: int,
    user_waiting: bool,
    batch_processing: bool,
) -> RequestPattern:
    """Select sync vs async pattern."""
    
    if latency_requirement_ms < 1000 and user_waiting:
        return RequestPattern.SYNC
    elif batch_processing or not user_waiting:
        return RequestPattern.ASYNC
    else:
        return RequestPattern.HYBRID

# Async implementation example
import asyncio
from typing import List

async def process_batch_async(requests: List[str]):
    """Process batch asynchronously."""
    tasks = [process_single(req) for req in requests]
    results = await asyncio.gather(*tasks)
    return results
```

## Output
- Architecture decision document
- Technology stack selection
- Vector database recommendation
- LLM provider comparison
- Scalability plan
- Implementation roadmap

## Decision Trees
### Framework Selection
```
Need multi-agent? → Yes → CrewAI
                    ↓ No
Need state management? → Yes → LangGraph
                    ↓ No
Need optimization? → Yes → DSPy
                    ↓ No
→ LangChain
```

### Vector DB Selection
```
Budget = Free? → Yes → ChromaDB
            ↓ No
Need managed? → Yes → Pinecone
            ↓ No
Scale > 1M vectors? → Yes → Milvus
                    ↓ No
→ Qdrant
```

```
Need multi-agent? → Yes → CrewAI
                    ↓ No
Need state management? → Yes → LangGraph
                    ↓ No
Need optimization? → Yes → DSPy
                    ↓ No
→ LangChain
```

```
Budget = Free? → Yes → ChromaDB
            ↓ No
Need managed? → Yes → Pinecone
            ↓ No
Scale > 1M vectors? → Yes → Milvus
                    ↓ No
→ Qdrant
```

## Best Practices
- Start with monolith, evolve to microservices
- Use LangChain for most applications
- Choose managed vector DBs for production
- Consider cost vs quality trade-offs
- Plan for horizontal scaling from start
- Use async for batch processing
- Cache aggressively
- Monitor and optimize continuously

## Related
- Skill: `ai-cost-optimization`
- Skill: `ai-security`
- Skill: `model-serving`

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Packages: langchain, langgraph, crewai, dspy, pinecone-client, qdrant-client, weaviate-client, chromadb
> - Knowledge: ai-cost-patterns.json, ai-security-patterns.json

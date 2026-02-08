---
name: advanced-retrieval
description: Multi-index RAG, query decomposition, contextual compression, and self-querying retrievers
type: skill
agents: [code-reviewer, test-generator]
knowledge: []
---

# Advanced Retrieval Skill

Implement sophisticated retrieval patterns including multi-index systems, query decomposition, contextual compression, and self-querying retrievers.

## When to Use

- Building complex knowledge bases
- Handling multi-domain queries
- Optimizing retrieval precision
- Creating adaptive retrieval systems
- Building enterprise RAG applications

## Prerequisites

```bash
pip install langchain langchain-core langchain-community
pip install chromadb faiss-cpu
pip install sentence-transformers
pip install pydantic
```

## Process

### Step 1: Multi-Index RAG

```python
from langchain_community.vectorstores import Chroma, FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from typing import List, Dict

class MultiIndexRAG:
    """RAG system with multiple specialized indices."""
    
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.indices = {}
    
    def create_index(self, name: str, documents: List[Document], index_type: str = "chroma"):
        """Create a specialized index.
        
        Args:
            name: Index name (e.g., "technical", "legal", "general")
            documents: Documents for this index
            index_type: "chroma" or "faiss"
        """
        if index_type == "chroma":
            vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                collection_name=name
            )
        else:  # faiss
            vectorstore = FAISS.from_documents(
                documents=documents,
                embedding=self.embeddings
            )
            vectorstore.save_local(f"./faiss_{name}")
        
        self.indices[name] = {
            "vectorstore": vectorstore,
            "retriever": vectorstore.as_retriever(search_kwargs={"k": 5}),
            "metadata": {"type": index_type, "doc_count": len(documents)}
        }
    
    def route_query(self, query: str) -> List[str]:
        """Route query to appropriate indices."""
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        
        index_names = list(self.indices.keys())
        prompt = f"""Given the query: "{query}"

Available indices: {', '.join(index_names)}

Which indices are most relevant? Return only the index names, comma-separated."""
        
        response = llm.invoke(prompt)
        selected = [name.strip() for name in response.content.split(",")]
        
        # Filter to existing indices
        return [name for name in selected if name in self.indices]
    
    def retrieve_multi_index(self, query: str, max_results: int = 10) -> List[Document]:
        """Retrieve from multiple indices."""
        # Route query
        relevant_indices = self.route_query(query)
        
        if not relevant_indices:
            relevant_indices = list(self.indices.keys())  # Fallback to all
        
        # Retrieve from each index
        all_results = []
        for index_name in relevant_indices:
            retriever = self.indices[index_name]["retriever"]
            docs = retriever.get_relevant_documents(query)
            
            # Add index metadata
            for doc in docs:
                doc.metadata["index_source"] = index_name
            
            all_results.extend(docs)
        
        # Deduplicate and rank
        seen_content = set()
        unique_results = []
        for doc in all_results:
            content_hash = hash(doc.page_content[:100])
            if content_hash not in seen_content:
                seen_content.add(content_hash)
                unique_results.append(doc)
        
        return unique_results[:max_results]

# Usage
rag = MultiIndexRAG()
rag.create_index("technical", technical_docs)
rag.create_index("legal", legal_docs)
rag.create_index("general", general_docs)

results = rag.retrieve_multi_index("What are the API requirements?")
```

### Step 2: Query Decomposition

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from pydantic import BaseModel
from typing import List

class QueryDecomposer:
    """Decompose complex queries into sub-queries."""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    
    def decompose(self, query: str) -> List[str]:
        """Break down complex query into sub-queries."""
        prompt = PromptTemplate(
            template="""Break down this query into simpler sub-queries that can be answered independently:

Query: {query}

Return only the sub-queries, one per line, without numbering.""",
            input_variables=["query"]
        )
        
        chain = prompt | self.llm
        response = chain.invoke({"query": query})
        
        sub_queries = [
            q.strip() 
            for q in response.content.split("\n") 
            if q.strip() and not q.strip().startswith("#")
        ]
        
        return sub_queries if sub_queries else [query]
    
    def decompose_with_types(self, query: str) -> Dict[str, List[str]]:
        """Decompose query and categorize sub-queries."""
        sub_queries = self.decompose(query)
        
        prompt = PromptTemplate(
            template="""Categorize these queries by type (factual, analytical, comparison, procedural):

Queries:
{queries}

Return JSON: {{"factual": [...], "analytical": [...], "comparison": [...], "procedural": [...]}}""",
            input_variables=["queries"]
        )
        
        chain = prompt | self.llm
        response = chain.invoke({"queries": "\n".join(sub_queries)})
        
        # Parse JSON (simplified - use proper JSON parsing in production)
        import json
        try:
            return json.loads(response.content)
        except:
            return {"all": sub_queries}

class DecomposedRetriever:
    """Retriever that uses query decomposition."""
    
    def __init__(self, base_retriever):
        self.base_retriever = base_retriever
        self.decomposer = QueryDecomposer()
    
    def get_relevant_documents(self, query: str) -> List[Document]:
        """Retrieve using decomposed queries."""
        # Decompose
        sub_queries = self.decomposer.decompose(query)
        
        # Retrieve for each sub-query
        all_docs = []
        for sub_query in sub_queries:
            docs = self.base_retriever.get_relevant_documents(sub_query)
            all_docs.extend(docs)
        
        # Deduplicate
        seen = set()
        unique_docs = []
        for doc in all_docs:
            content_id = hash(doc.page_content[:100])
            if content_id not in seen:
                seen.add(content_id)
                unique_docs.append(doc)
        
        return unique_docs
```

### Step 3: Contextual Compression

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers.document_compressors import EmbeddingsRedundantFilter
from langchain.retrievers.document_compressors import DocumentCompressorPipeline
from langchain_community.embeddings import HuggingFaceEmbeddings

class CompressedRetriever:
    """Retriever with contextual compression."""
    
    def __init__(self, base_retriever, llm):
        self.base_retriever = base_retriever
        self.llm = llm
        
        # Create compressor pipeline
        embeddings = HuggingFaceEmbeddings()
        
        # Remove redundant documents
        redundant_filter = EmbeddingsRedundantFilter(embeddings=embeddings)
        
        # Extract relevant parts
        relevant_extractor = LLMChainExtractor.from_llm(llm)
        
        # Combine compressors
        pipeline_compressor = DocumentCompressorPipeline(
            transformers=[redundant_filter, relevant_extractor]
        )
        
        # Create compressed retriever
        self.compressed_retriever = ContextualCompressionRetriever(
            base_compressor=pipeline_compressor,
            base_retriever=base_retriever
        )
    
    def get_relevant_documents(self, query: str) -> List[Document]:
        """Retrieve and compress documents."""
        return self.compressed_retriever.get_relevant_documents(query)

class CustomCompressor:
    """Custom document compressor."""
    
    def __init__(self, llm):
        self.llm = llm
    
    def compress_documents(self, documents: List[Document], query: str) -> List[Document]:
        """Compress documents by extracting relevant parts."""
        from langchain.prompts import PromptTemplate
        
        compressed = []
        
        for doc in documents:
            prompt = PromptTemplate(
                template="""Extract only the parts of this document relevant to the query. If nothing is relevant, return "NOT_RELEVANT".

Document: {document}

Query: {query}

Relevant excerpt:""",
                input_variables=["document", "query"]
            )
            
            chain = prompt | self.llm
            result = chain.invoke({
                "document": doc.page_content,
                "query": query
            })
            
            excerpt = result.content if hasattr(result, "content") else str(result)
            
            if excerpt.strip() != "NOT_RELEVANT":
                compressed_doc = Document(
                    page_content=excerpt,
                    metadata=doc.metadata
                )
                compressed.append(compressed_doc)
        
        return compressed
```

### Step 4: Self-Querying Retrievers

```python
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI

class SelfQueryingRAG:
    """RAG system with self-querying capabilities."""
    
    def __init__(self, documents: List[Document]):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        self.embeddings = HuggingFaceEmbeddings()
        
        # Create vector store
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings
        )
        
        # Define metadata fields
        metadata_field_info = [
            AttributeInfo(
                name="source",
                description="The source document name",
                type="string"
            ),
            AttributeInfo(
                name="page",
                description="The page number in the document",
                type="integer"
            ),
            AttributeInfo(
                name="category",
                description="The category of the document (e.g., technical, legal, general)",
                type="string"
            ),
            AttributeInfo(
                name="date",
                description="The date of the document",
                type="string"
            )
        ]
        
        # Create self-query retriever
        self.retriever = SelfQueryRetriever.from_llm(
            llm=self.llm,
            vectorstore=self.vectorstore,
            document_contents="Documents contain various types of information",
            metadata_field_info=metadata_field_info
        )
    
    def query(self, query: str) -> List[Document]:
        """Query with automatic metadata filtering."""
        return self.retriever.get_relevant_documents(query)

# Usage
rag = SelfQueryingRAG(documents)
# Query like: "Find technical documents from 2024 about APIs"
results = rag.query("technical documents from 2024 about APIs")
```

### Step 5: Adaptive Retrieval

```python
from langchain.retrievers import EnsembleRetriever
from langchain.retrievers import BM25Retriever
from langchain_community.vectorstores import Chroma
from typing import List, Dict

class AdaptiveRetriever:
    """Adaptive retriever that selects best method based on query."""
    
    def __init__(self, documents: List[Document]):
        self.documents = documents
        self.embeddings = HuggingFaceEmbeddings()
        
        # Create multiple retrievers
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings
        )
        
        self.semantic_retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 10}
        )
        
        self.bm25_retriever = BM25Retriever.from_documents(documents)
        self.bm25_retriever.k = 10
        
        # Ensemble retriever
        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[self.semantic_retriever, self.bm25_retriever],
            weights=[0.5, 0.5]
        )
    
    def select_retrieval_method(self, query: str) -> str:
        """Select best retrieval method for query."""
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        
        prompt = f"""Analyze this query and determine the best retrieval method:
- "semantic": For conceptual, meaning-based queries
- "keyword": For specific term matching
- "ensemble": For complex queries needing both

Query: "{query}"

Return only: semantic, keyword, or ensemble"""
        
        response = llm.invoke(prompt)
        method = response.content.strip().lower()
        
        return method if method in ["semantic", "keyword", "ensemble"] else "ensemble"
    
    def get_relevant_documents(self, query: str) -> List[Document]:
        """Retrieve using adaptive method selection."""
        method = self.select_retrieval_method(query)
        
        if method == "semantic":
            return self.semantic_retriever.get_relevant_documents(query)
        elif method == "keyword":
            return self.bm25_retriever.get_relevant_documents(query)
        else:  # ensemble
            return self.ensemble_retriever.get_relevant_documents(query)
```

### Step 6: Complete Advanced RAG System

```python
class AdvancedRAGSystem:
    """Complete advanced RAG system combining all techniques."""
    
    def __init__(self, documents_by_index: Dict[str, List[Document]]):
        self.multi_index = MultiIndexRAG()
        
        # Create indices
        for index_name, docs in documents_by_index.items():
            self.multi_index.create_index(index_name, docs)
        
        # Initialize components
        self.decomposer = QueryDecomposer()
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    
    def query(self, query: str, use_decomposition: bool = True, 
              use_compression: bool = True, max_results: int = 10) -> Dict:
        """Complete query pipeline."""
        # Decompose if complex
        if use_decomposition:
            sub_queries = self.decomposer.decompose(query)
        else:
            sub_queries = [query]
        
        # Retrieve from multi-index
        all_docs = []
        for sub_query in sub_queries:
            docs = self.multi_index.retrieve_multi_index(sub_query, max_results=max_results)
            all_docs.extend(docs)
        
        # Compress if enabled
        if use_compression:
            compressor = CustomCompressor(self.llm)
            all_docs = compressor.compress_documents(all_docs, query)
        
        # Build context
        context = "\n\n".join([
            f"[{i+1}] {doc.page_content}\nSource: {doc.metadata.get('index_source', 'unknown')}"
            for i, doc in enumerate(all_docs[:max_results])
        ])
        
        # Generate answer
        from langchain.prompts import PromptTemplate
        prompt = PromptTemplate(
            template="""Answer the question using the provided context. Include citations.

Context:
{context}

Question: {question}

Answer:""",
            input_variables=["context", "question"]
        )
        
        chain = prompt | self.llm
        answer = chain.invoke({"context": context, "question": query})
        
        return {
            "answer": answer.content if hasattr(answer, "content") else str(answer),
            "sources": [
                {
                    "text": doc.page_content[:200],
                    "index": doc.metadata.get("index_source", "unknown")
                }
                for doc in all_docs[:max_results]
            ],
            "sub_queries": sub_queries
        }
```

## Retrieval Patterns Comparison

| Pattern | Use Case | Pros | Cons |
|---------|----------|------|------|
| Multi-Index | Domain-specific data | Specialized retrieval | More setup |
| Query Decomposition | Complex queries | Better coverage | More API calls |
| Contextual Compression | Long documents | Focused context | Processing overhead |
| Self-Querying | Metadata filtering | Automatic filtering | Requires structured metadata |
| Adaptive | Variable query types | Optimal method | Selection overhead |

## Best Practices

- Use multi-index for clearly separated domains
- Decompose complex queries into simpler sub-queries
- Compress long documents to focus on relevant parts
- Add structured metadata for self-querying
- Combine multiple retrieval methods (ensemble)
- Cache retrieval results when possible
- Monitor retrieval quality and adjust weights
- Use appropriate chunk sizes for your use case

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Single retrieval method | Use ensemble or adaptive retrieval |
| No query decomposition | Break down complex queries |
| Ignoring metadata | Add and use structured metadata |
| No compression | Compress long documents |
| Fixed retrieval weights | Tune weights based on performance |
| No deduplication | Remove duplicate results |
| Ignoring query type | Adapt method to query characteristics |

## Related

- Skill: `rag-patterns`
- Skill: `knowledge-graphs`
- Skill: `memory-management`

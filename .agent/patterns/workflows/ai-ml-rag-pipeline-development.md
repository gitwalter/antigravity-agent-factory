# RAG Pipeline Development Workflow

## Overview

End-to-end workflow for developing Retrieval-Augmented Generation (RAG) systems. Covers document ingestion, embedding, vector storage, retrieval optimization, and generation with evaluation.

**Version:** 1.0.0  
**Created:** 2026-02-02  
**Applies To:** python-rag-system, starter-rag

## Trigger Conditions

This workflow is activated when:

- RAG system development needed
- Document Q&A system required
- Knowledge base chatbot
- Context-aware generation

**Trigger Examples:**
- "Build a RAG system for documentation"
- "Create a document Q&A chatbot"
- "Develop a knowledge base search"
- "Implement semantic document retrieval"

## Phases

### Phase 1: Document Ingestion

**Description:** Load and preprocess documents.

**Entry Criteria:** Documents available  
**Exit Criteria:** Documents chunked

#### Step 1.1: Load Documents

**Actions:**
- Identify document sources
- Load with appropriate loaders
- Handle different formats
- Extract metadata

**Document Loaders:**

| Format | Loader |
|--------|--------|
| PDF | PyPDFLoader, PDFMiner |
| Web | WebBaseLoader |
| Markdown | UnstructuredMarkdownLoader |
| Code | LanguageParser |

**Example:**
```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("document.pdf")
documents = loader.load()
```

#### Step 1.2: Chunk Documents

**Actions:**
- Select chunking strategy
- Configure chunk size
- Handle overlap
- Preserve structure

**Chunking Strategies:**

| Strategy | Use Case |
|----------|----------|
| Recursive Character | General text |
| Token-based | LLM context limits |
| Semantic | Meaning preservation |
| Code | Programming languages |

**Example:**
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = splitter.split_documents(documents)
```

**Outputs:**
- Chunked documents
- Preserved metadata

**Is Mandatory:** Yes

---

### Phase 2: Embedding & Indexing

**Description:** Create embeddings and store in vector database.

**Entry Criteria:** Documents chunked  
**Exit Criteria:** Vector store populated

#### Step 2.1: Select Embedding Model

**Actions:**
- Choose embedding model
- Consider dimensionality
- Evaluate quality vs speed
- Configure batch size

**Embedding Options:**

| Model | Dimensions | Quality |
|-------|-----------|---------|
| OpenAI ada-002 | 1536 | High |
| Cohere embed-v3 | 1024 | High |
| HuggingFace | Variable | Good |
| Local (Ollama) | Variable | Good |

#### Step 2.2: Create Vector Store

**Actions:**
- Select vector database
- Configure index type
- Create embeddings
- Store with metadata

**Vector Databases:**

| Database | Use Case |
|----------|----------|
| ChromaDB | Local development |
| Pinecone | Production scale |
| Qdrant | Self-hosted |
| FAISS | In-memory |
| Weaviate | Multi-modal |

**Example:**
```python
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
```

**Outputs:**
- Vector store
- Index configuration

**Is Mandatory:** Yes

---

### Phase 3: Retrieval Configuration

**Description:** Configure and optimize retrieval.

**Entry Criteria:** Vector store populated  
**Exit Criteria:** Retrieval optimized

#### Step 3.1: Configure Retriever

**Actions:**
- Set retrieval method
- Configure k (top results)
- Add filtering
- Tune similarity threshold

**Retrieval Methods:**

| Method | Description |
|--------|-------------|
| Similarity | Cosine similarity |
| MMR | Maximal Marginal Relevance |
| Self-query | Metadata filtering |
| Multi-query | Query expansion |
| Ensemble | Multiple retrievers |

**Example:**
```python
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "fetch_k": 20}
)
```

#### Step 3.2: Add Reranking (Optional)

**Actions:**
- Add reranker model
- Configure rerank threshold
- Reduce final results

**Reranking:**
```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank

reranker = CohereRerank(top_n=3)
retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=base_retriever
)
```

**Outputs:**
- Configured retriever
- Retrieval metrics

**Is Mandatory:** Yes

---

### Phase 4: Generation Pipeline

**Description:** Build the generation component.

**Entry Criteria:** Retrieval configured  
**Exit Criteria:** RAG chain complete

#### Step 4.1: Create Prompt Template

**Actions:**
- Design system prompt
- Add context placeholder
- Include instructions
- Handle edge cases

**Prompt Template:**
```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant answering questions based on the provided context.

Context:
{context}

Question: {question}

Instructions:
- Answer based only on the context provided
- If the answer is not in the context, say "I don't have that information"
- Be concise but complete

Answer:
""")
```

#### Step 4.2: Build RAG Chain

**Actions:**
- Connect retriever to LLM
- Add context formatting
- Handle history (if needed)
- Add output parsing

**RAG Chain:**
```python
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

**Outputs:**
- RAG chain
- Generation configuration

**Is Mandatory:** Yes

---

### Phase 5: Evaluation

**Description:** Evaluate RAG system performance.

**Entry Criteria:** RAG chain complete  
**Exit Criteria:** Performance validated

#### Step 5.1: Create Test Set

**Actions:**
- Generate test questions
- Create ground truth answers
- Include edge cases
- Add retrieval ground truth

#### Step 5.2: Run RAGAS Evaluation

**Actions:**
- Evaluate faithfulness
- Measure answer relevancy
- Assess context recall
- Calculate context precision

**RAGAS Metrics:**

| Metric | Description | Target |
|--------|-------------|--------|
| Faithfulness | Answer grounded in context | >0.9 |
| Answer Relevancy | Answer addresses question | >0.8 |
| Context Recall | Retrieved relevant docs | >0.8 |
| Context Precision | No irrelevant context | >0.7 |

**Evaluation:**
```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

results = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy]
)
```

**Outputs:**
- Evaluation metrics
- Performance report

**Is Mandatory:** Yes

---

### Phase 6: Deployment

**Description:** Deploy the RAG system.

**Entry Criteria:** Evaluation passed  
**Exit Criteria:** System deployed

#### Step 6.1: Create API

**Actions:**
- Build FastAPI endpoint
- Add authentication
- Configure rate limiting
- Add monitoring

**API Example:**
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask(query: Query):
    response = rag_chain.invoke(query.question)
    return {"answer": response}
```

#### Step 6.2: Deploy

**Actions:**
- Package application
- Deploy vector store
- Configure endpoints
- Set up monitoring

**Outputs:**
- Deployed API
- Monitoring dashboard

**Is Mandatory:** Yes

---

## Decision Points

### Decision: Embedding Model Selection

| Condition | Choice | Rationale |
|-----------|--------|-----------|
| Production, cost-sensitive | OpenAI ada-002 | Balance of quality/cost |
| Local/private data | HuggingFace or Ollama | Data stays local |
| Highest quality | OpenAI text-embedding-3-large | Best performance |

### Decision: Vector Store Selection

| Scale | Choice | Rationale |
|-------|--------|-----------|
| Development | ChromaDB | Easy local setup |
| Production | Pinecone/Qdrant | Scalability |
| In-memory | FAISS | Speed |

### Decision: Retrieval Quality

| RAGAS Score | Action |
|-------------|--------|
| All metrics > 0.8 | Deploy |
| Any metric < 0.7 | Iterate on retrieval |
| Faithfulness < 0.7 | Review prompt engineering |

---

## Fallback Procedures

| Condition | Action |
|-----------|--------|
| Document loading fails | Try alternative loader |
| Embedding API unavailable | Use local embeddings |
| Vector store error | Fall back to keyword search |
| Low retrieval quality | Add reranking step |
| Evaluation fails | Manual testing with sample queries |

---

## Example Session

```
User: Build a RAG system for our product documentation

Agent:
━━━ PHASE 1: Document Ingestion ━━━
Loading documents...
- Source: docs/ folder
- Files: 45 markdown files

Chunking...
- Strategy: Recursive Character
- Chunk size: 1000
- Overlap: 200
- Result: 312 chunks

━━━ PHASE 2: Embedding & Indexing ━━━
Configuring embeddings...
- Model: OpenAI text-embedding-3-small
- Dimensions: 1536

Creating vector store...
- Database: ChromaDB (local)
✓ 312 documents indexed

━━━ PHASE 3: Retrieval Configuration ━━━
Configuring retriever...
- Method: MMR (diversity)
- k: 5
- fetch_k: 20

Adding reranking...
- Model: Cohere rerank-v3
- top_n: 3

━━━ PHASE 4: Generation Pipeline ━━━
Creating prompt template...
✓ Context-aware prompt configured

Building RAG chain...
- LLM: GPT-4
- Chain: retriever → formatter → prompt → LLM

━━━ PHASE 5: Evaluation ━━━
Creating test set...
- 50 test questions generated

Running RAGAS evaluation...
- Faithfulness: 0.92 ✓
- Answer Relevancy: 0.88 ✓
- Context Recall: 0.85 ✓
- Context Precision: 0.78 ✓

━━━ PHASE 6: Deployment ━━━
Creating FastAPI app...
✓ POST /ask endpoint created
✓ Authentication added
✓ Rate limiting: 100 req/min

Deploying...
✓ API: https://docs-rag.company.com/ask

✨ RAG system deployed!
```

---

## Related Artifacts

- **Blueprints**: `blueprints/python-rag-system/blueprint.json`
- **Skills**: `patterns/skills/prompt-engineering.json`

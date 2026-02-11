# RAG System Architecture

> **Stack:** LangChain + Vector DB | **Level:** Fundamentals | **Duration:** 2.5 hours

## Overview

**Workshop ID:** `L8_rag_systems`

**Technology:** Python with LangChain + Vector DB (LangChain 0.3+)

## Prerequisites

**Required Workshops:**
- L7_langchain_fundamentals

**Required Knowledge:**
- Python programming
- Basic understanding of embeddings and vector similarity
- LangChain fundamentals (chains, retrievers)
- Understanding of document processing

**Required Tools:**
- Python 3.10+
- OpenAI API key (or other LLM provider)
- Vector database (Chroma, Pinecone, or FAISS)
- VS Code or similar IDE

## Learning Objectives

By the end of this workshop, you will be able to:

1. **Implement document loading and chunking strategies for different document types** (Apply)
2. **Select and use embedding models for different use cases** (Apply)
3. **Perform vector store operations: indexing, querying, and updating** (Apply)
4. **Implement different retrieval strategies: similarity search, MMR, and hybrid search** (Apply)
5. **Evaluate RAG systems using RAGAS metrics** (Apply)

## Workshop Timeline

| Phase | Duration |
|-------|----------|
| Concept | 30 min |
| Demo | 30 min |
| Exercise | 45 min |
| Challenge | 30 min |
| Reflection | 15 min |
| **Total** | **2.5 hours** |

## Workshop Phases

### Concept: RAG Architecture Overview

*Understand the components and flow of RAG systems*

**Topics Covered:**
- RAG Pipeline: Load → Chunk → Embed → Store → Retrieve → Generate
- Document Loaders: PDF, HTML, Markdown, CSV
- Text Splitting: Chunk size, overlap, and strategies
- Embeddings: Model selection and dimensionality
- Vector Stores: Chroma, Pinecone, FAISS, Weaviate
- Retrieval Strategies: Similarity, MMR, Hybrid
- Generation: Context injection and prompt engineering
- Evaluation: RAGAS metrics (faithfulness, answer relevance, context precision)

**Key Points:**
- Chunk size affects retrieval quality (too small = fragmented, too large = noisy)
- Overlap prevents context loss at chunk boundaries
- Embedding model choice impacts retrieval accuracy
- MMR balances relevance and diversity
- Hybrid search combines semantic and keyword matching
- Evaluation is crucial for production RAG systems

### Demo: Building a Simple RAG

*Live coding a complete RAG system*

**Topics Covered:**
- Loading documents with LangChain loaders
- Splitting text with RecursiveCharacterTextSplitter
- Creating embeddings with OpenAI
- Storing in Chroma vector store
- Building retrieval chain
- Testing retrieval quality
- Adding conversation memory

**Key Points:**
- Chunk size of 1000 with 200 overlap works well for most cases
- Always test retrieval quality before generation
- Include source citations in responses
- Memory enables follow-up questions

### Exercise: Chunking Experiments

*Experiment with different chunking strategies*

**Topics Covered:**
- Try different chunk sizes
- Experiment with overlap values
- Test semantic chunking
- Compare retrieval quality
- Analyze chunk boundaries

### Challenge: Conversational RAG

*Build a RAG system with conversation memory*

**Topics Covered:**
- Add conversation memory
- Handle follow-up questions
- Implement query rewriting
- Add source citations
- Evaluate with RAGAS

### Reflection: Key Takeaways and Production Considerations

*Consolidate learning and discuss production deployment*

**Topics Covered:**
- Summary of RAG patterns
- Chunking best practices
- Retrieval strategy selection
- Production considerations (scaling, monitoring, costs)
- Evaluation and continuous improvement
- Resources for continued learning

**Key Points:**
- Chunking strategy is critical for retrieval quality
- Test retrieval before optimizing generation
- Use MMR for diverse results
- Hybrid search improves recall
- Regular evaluation ensures quality

## Hands-On Exercises

### Exercise: Chunking Experiments

Experiment with different chunking strategies and compare results

**Difficulty:** Medium | **Duration:** 45 minutes

**Hints:**
- Use RecursiveCharacterTextSplitter for text documents
- Chunk size is in characters, not tokens
- Overlap prevents losing context at boundaries
- Test with real queries to see quality differences
- Consider document type when choosing chunk size

**Common Mistakes to Avoid:**
- Confusing chunk size (characters) with token count
- Too much overlap wastes tokens
- Not testing retrieval quality
- Using same chunk size for all document types
- Not considering document structure

## Challenges

### Challenge: Conversational RAG System

Build a RAG system with conversation memory and advanced retrieval

**Requirements:**
- Load and process documents (at least 3 documents)
- Implement appropriate chunking strategy
- Create vector store and index documents
- Add conversation memory for context
- Implement query rewriting for follow-up questions
- Use MMR retrieval for diverse results
- Add source citations to responses
- Evaluate system with RAGAS metrics

**Evaluation Criteria:**
- Successfully loads and indexes documents
- Retrieves relevant chunks for questions
- Handles follow-up questions with context
- Provides source citations
- RAGAS metrics show good performance
- System handles edge cases gracefully

**Stretch Goals:**
- Implement hybrid search (vector + keyword)
- Add multi-query retrieval
- Implement reranking
- Add streaming responses
- Create web interface

## Resources

**Official Documentation:**
- https://python.langchain.com/docs/use_cases/question_answering/
- https://python.langchain.com/docs/integrations/vectorstores/
- https://docs.ragas.io/

**Tutorials:**
- LangChain RAG Tutorial
- RAGAS Evaluation Guide

## Self-Assessment

Ask yourself these questions:

- [ ] Can I implement document loading and chunking?
- [ ] Do I understand how to choose embedding models?
- [ ] Can I create and query vector stores?
- [ ] Do I know when to use different retrieval strategies?
- [ ] Can I evaluate RAG systems with RAGAS?

## Next Steps

**Next Workshop:** `L9_advanced_rag`

**Practice Projects:**
- Documentation Q&A system
- Research assistant with web search
- Codebase knowledge base

**Deeper Learning:**
- Advanced retrieval techniques (reranking, multi-query)
- Hybrid search implementation
- Production RAG optimization

## Related Knowledge Files

- `rag-patterns.json`
- `vector-database-patterns.json`
- `langchain-patterns.json`

---

*Part of the Antigravity Agent Factory Learning Workshop Ecosystem*

**Workshop Definition:** `patterns/workshops/L8_rag_systems.json`
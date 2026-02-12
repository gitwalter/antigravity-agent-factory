---
description: Document chunking strategies, hybrid retrieval (semantic + keyword),
  reranking patterns, and citation/attribution
name: rag-patterns
type: skill
---

# Rag Patterns

Document chunking strategies, hybrid retrieval (semantic + keyword), reranking patterns, and citation/attribution

## 
# RAG Patterns Skill

Implement Retrieval-Augmented Generation with effective chunking, hybrid retrieval, reranking, and proper citation.

## 
# RAG Patterns Skill

Implement Retrieval-Augmented Generation with effective chunking, hybrid retrieval, reranking, and proper citation.

## Process
### Step 1: Document Chunking Strategies

```python
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TokenTextSplitter,
    MarkdownHeaderTextSplitter
)
from langchain.docstore.document import Document

def chunk_by_character(docs: list[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> list[Document]:
    """Simple character-based chunking."""
    text_splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separator="\n\n"
    )
    return text_splitter.split_documents(docs)

def chunk_recursive(docs: list[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> list[Document]:
    """Recursive chunking that respects document structure."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    return text_splitter.split_documents(docs)

def chunk_by_tokens(docs: list[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> list[Document]:
    """Chunk by token count (more accurate for LLM context)."""
    text_splitter = TokenTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(docs)

def chunk_markdown_by_headers(docs: list[Document]) -> list[Document]:
    """Chunk markdown documents by headers."""
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on
    )
    
    chunks = []
    for doc in docs:
        md_chunks = markdown_splitter.split_text(doc.page_content)
        for chunk in md_chunks:
            chunk.metadata.update(doc.metadata)
            chunks.append(chunk)
    
    return chunks

def chunk_semantic(docs: list[Document], min_chunk_size: int = 100, max_chunk_size: int = 1000) -> list[Document]:
    """Semantic chunking that groups related sentences."""
    from langchain_experimental.text_splitter import SemanticChunker
    from langchain_community.embeddings import HuggingFaceEmbeddings
    
    embeddings = HuggingFaceEmbeddings()
    text_splitter = SemanticChunker(
        embeddings=embeddings,
        breakpoint_threshold_type="percentile"
    )
    
    chunks = []
    for doc in docs:
        doc_chunks = text_splitter.split_text(doc.page_content)
        for chunk_text in doc_chunks:
            if min_chunk_size <= len(chunk_text) <= max_chunk_size:
                chunks.append(Document(
                    page_content=chunk_text,
                    metadata=doc.metadata
                ))
    
    return chunks
```

### Step 2: Hybrid Retrieval (Semantic + Keyword)

```python
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from rank_bm25 import BM25Okapi
from typing import List

class HybridRetriever:
    """Combine semantic and keyword search."""
    
    def __init__(self, documents: list[Document], embedding_model: str = "all-MiniLM-L6-v2"):
        self.documents = documents
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        
        # Semantic retriever
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings
        )
        
        # Keyword retriever (BM25)
        tokenized_docs = [doc.page_content.lower().split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized_docs)
    
    def retrieve(self, query: str, k: int = 5, alpha: float = 0.5) -> list[Document]:
        """Retrieve documents using hybrid search.
        
        Args:
            query: Search query
            k: Number of results
            alpha: Weight for semantic search (1-alpha for keyword)
        """
        # Semantic search
        semantic_results = self.vectorstore.similarity_search_with_score(query, k=k*2)
        semantic_scores = {doc.metadata.get("source", i): score 
                          for i, (doc, score) in enumerate(semantic_results)}
        
        # Keyword search
        tokenized_query = query.lower().split()
        keyword_scores = self.bm25.get_scores(tokenized_query)
        keyword_results = sorted(
            enumerate(keyword_scores),
            key=lambda x: x[1],
            reverse=True
        )[:k*2]
        
        # Normalize scores
        max_semantic = max(semantic_scores.values()) if semantic_scores else 1
        max_keyword = max([s for _, s in keyword_results]) if keyword_results else 1
        
        # Combine scores
        combined_scores = {}
        for i, (doc, score) in enumerate(semantic_results):
            doc_id = doc.metadata.get("source", i)
            normalized_semantic = score / max_semantic if max_semantic > 0 else 0
            combined_scores[doc_id] = alpha * (1 - normalized_semantic)  # Lower is better for distance
        
        for i, score in keyword_results:
            doc_id = self.documents[i].metadata.get("source", i)
            normalized_keyword = score / max_keyword if max_keyword > 0 else 0
            if doc_id in combined_scores:
                combined_scores[doc_id] += (1 - alpha) * normalized_keyword
            else:
                combined_scores[doc_id] = (1 - alpha) * normalized_keyword
        
        # Get top k
        top_doc_ids = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:k]
        
        # Return documents
        results = []
        for doc_id, _ in top_doc_ids:
            # Find document
            for doc in self.documents:
                if doc.metadata.get("source") == doc_id:
                    results.append(doc)
                    break
        
        return results

# Usage
retriever = HybridRetriever(documents)
results = retriever.retrieve("machine learning algorithms", k=5, alpha=0.7)
```

### Step 3: Reranking Patterns

```python
from langchain_community.llms import Cohere
from typing import List, Tuple

class Reranker:
    """Rerank retrieved documents for better relevance."""
    
    def __init__(self, cohere_api_key: str = None):
        if cohere_api_key:
            self.cohere = Cohere(cohere_api_key=cohere_api_key)
        else:
            self.cohere = None
    
    def rerank_cohere(self, query: str, documents: list[Document], top_n: int = 5) -> list[Document]:
        """Rerank using Cohere API."""
        if not self.cohere:
            raise ValueError("Cohere API key required")
        
        doc_texts = [doc.page_content for doc in documents]
        
        # Cohere rerank API
        import cohere
        co = cohere.Client(api_key=self.cohere.cohere_api_key)
        
        results = co.rerank(
            model="rerank-english-v3.0",
            query=query,
            documents=doc_texts,
            top_n=top_n
        )
        
        # Map back to documents
        reranked = []
        for result in results:
            idx = result.index
            reranked.append(documents[idx])
        
        return reranked
    
    def rerank_cross_encoder(self, query: str, documents: list[Document], top_n: int = 5) -> list[Document]:
        """Rerank using cross-encoder model (local)."""
        from sentence_transformers import CrossEncoder
        
        model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        
        # Prepare pairs
        pairs = [[query, doc.page_content] for doc in documents]
        
        # Get scores
        scores = model.predict(pairs)
        
        # Sort by score
        scored_docs = list(zip(documents, scores))
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        return [doc for doc, _ in scored_docs[:top_n]]
    
    def rerank_llm(self, query: str, documents: list[Document], top_n: int = 5, llm=None) -> list[Document]:
        """Rerank using LLM reasoning."""
        if not llm:
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        
        # Create prompt
        doc_texts = "\n\n".join([
            f"Document {i+1}:\n{doc.page_content[:500]}"
            for i, doc in enumerate(documents)
        ])
        
        prompt = f"""Rank these documents by relevance to the query: "{query}"

Documents:
{doc_texts}

Return only the numbers of the top {top_n} most relevant documents, separated by commas."""
        
        response = llm.invoke(prompt)
        
        # Parse response
        try:
            indices = [int(x.strip()) - 1 for x in response.content.split(",")]
            return [documents[i] for i in indices if 0 <= i < len(documents)]
        except:
            return documents[:top_n]  # Fallback
```

### Step 4: Citation and Attribution

```python
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from typing import List, Dict

class CitationRAG:
    """RAG system with citation support."""
    
    def __init__(self, retriever, llm):
        self.retriever = retriever
        self.llm = llm
    
    def answer_with_citations(self, query: str, k: int = 5) -> Dict:
        """Answer query with source citations."""
        # Retrieve documents
        docs = self.retriever.get_relevant_documents(query)
        
        # Format context with citations
        context_parts = []
        for i, doc in enumerate(docs[:k], 1):
            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", "")
            citation = f"[{i}]"
            context_parts.append(f"{citation} {doc.page_content}\nSource: {source}{f', Page {page}' if page else ''}")
        
        context = "\n\n".join(context_parts)
        
        # Create prompt with citation instructions
        prompt = PromptTemplate(
            template="""Answer the question using the provided context. Include citations [1], [2], etc. when referencing information.

Context:
{context}

Question: {question}

Answer with citations:""",
            input_variables=["context", "question"]
        )
        
        # Generate answer
        chain = prompt | self.llm
        answer = chain.invoke({"context": context, "question": query})
        
        # Extract citations
        citations = []
        for i, doc in enumerate(docs[:k], 1):
            citations.append({
                "id": i,
                "text": doc.page_content[:200],
                "source": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", ""),
                "metadata": doc.metadata
            })
        
        return {
            "answer": answer.content if hasattr(answer, "content") else str(answer),
            "citations": citations,
            "sources": [c["source"] for c in citations]
        }
    
    def answer_with_quote_attribution(self, query: str) -> Dict:
        """Answer with direct quote attribution."""
        docs = self.retriever.get_relevant_documents(query)
        
        # Build context
        context_parts = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "Unknown")
            context_parts.append(f"[{i}] {doc.page_content}\n(Source: {source})")
        
        context = "\n\n".join(context_parts)
        
        prompt = PromptTemplate(
            template="""Answer the question using quotes from the provided sources. Format quotes as: "quote text" [source number].

Context:
{context}

Question: {question}

Answer with quoted evidence:""",
            input_variables=["context", "question"]
        )
        
        chain = prompt | self.llm
        answer = chain.invoke({"context": context, "question": query})
        
        return {
            "answer": answer.content if hasattr(answer, "content") else str(answer),
            "sources": [
                {
                    "id": i+1,
                    "source": doc.metadata.get("source", "Unknown"),
                    "excerpt": doc.page_content[:300]
                }
                for i, doc in enumerate(docs)
            ]
        }
```

### Step 5: Complete RAG Pipeline

```python
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

class CompleteRAGPipeline:
    """Complete RAG pipeline with chunking, retrieval, reranking, and citation."""
    
    def __init__(self, documents: list[Document], embedding_model: str = "all-MiniLM-L6-v2"):
        # Chunk documents
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.chunks = text_splitter.split_documents(documents)
        
        # Create embeddings and vector store
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        self.vectorstore = Chroma.from_documents(
            documents=self.chunks,
            embedding=self.embeddings
        )
        
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        
        # Create retriever
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": 10, "score_threshold": 0.5}
        )
    
    def query(self, question: str, use_reranking: bool = True, use_citations: bool = True) -> Dict:
        """Query the RAG system."""
        # Retrieve
        docs = self.retriever.get_relevant_documents(question)
        
        # Rerank if enabled
        if use_reranking and len(docs) > 5:
            reranker = Reranker()
            docs = reranker.rerank_cross_encoder(question, docs, top_n=5)
        
        # Build context
        if use_citations:
            context_parts = []
            for i, doc in enumerate(docs, 1):
                source = doc.metadata.get("source", "Unknown")
                context_parts.append(f"[{i}] {doc.page_content}\nSource: {source}")
            context = "\n\n".join(context_parts)
            citation_note = " Include citations [1], [2], etc. in your answer."
        else:
            context = "\n\n".join([doc.page_content for doc in docs])
            citation_note = ""
        
        # Create prompt
        prompt = PromptTemplate(
            template=f"""Answer the question using the provided context.{citation_note}

Context:
{{context}}

Question: {{question}}

Answer:""",
            input_variables=["context", "question"]
        )
        
        # Generate answer
        chain = prompt | self.llm
        answer = chain.invoke({"context": context, "question": question})
        
        result = {
            "answer": answer.content if hasattr(answer, "content") else str(answer),
            "num_sources": len(docs)
        }
        
        if use_citations:
            result["sources"] = [
                {
                    "id": i+1,
                    "source": doc.metadata.get("source", "Unknown"),
                    "excerpt": doc.page_content[:200]
                }
                for i, doc in enumerate(docs)
            ]
        
        return result
```

```python
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TokenTextSplitter,
    MarkdownHeaderTextSplitter
)
from langchain.docstore.document import Document

def chunk_by_character(docs: list[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> list[Document]:
    """Simple character-based chunking."""
    text_splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separator="\n\n"
    )
    return text_splitter.split_documents(docs)

def chunk_recursive(docs: list[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> list[Document]:
    """Recursive chunking that respects document structure."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    return text_splitter.split_documents(docs)

def chunk_by_tokens(docs: list[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> list[Document]:
    """Chunk by token count (more accurate for LLM context)."""
    text_splitter = TokenTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(docs)

def chunk_markdown_by_headers(docs: list[Document]) -> list[Document]:
    """Chunk markdown documents by headers."""
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on
    )
    
    chunks = []
    for doc in docs:
        md_chunks = markdown_splitter.split_text(doc.page_content)
        for chunk in md_chunks:
            chunk.metadata.update(doc.metadata)
            chunks.append(chunk)
    
    return chunks

def chunk_semantic(docs: list[Document], min_chunk_size: int = 100, max_chunk_size: int = 1000) -> list[Document]:
    """Semantic chunking that groups related sentences."""
    from langchain_experimental.text_splitter import SemanticChunker
    from langchain_community.embeddings import HuggingFaceEmbeddings
    
    embeddings = HuggingFaceEmbeddings()
    text_splitter = SemanticChunker(
        embeddings=embeddings,
        breakpoint_threshold_type="percentile"
    )
    
    chunks = []
    for doc in docs:
        doc_chunks = text_splitter.split_text(doc.page_content)
        for chunk_text in doc_chunks:
            if min_chunk_size <= len(chunk_text) <= max_chunk_size:
                chunks.append(Document(
                    page_content=chunk_text,
                    metadata=doc.metadata
                ))
    
    return chunks
```

```python
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from rank_bm25 import BM25Okapi
from typing import List

class HybridRetriever:
    """Combine semantic and keyword search."""
    
    def __init__(self, documents: list[Document], embedding_model: str = "all-MiniLM-L6-v2"):
        self.documents = documents
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        
        # Semantic retriever
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings
        )
        
        # Keyword retriever (BM25)
        tokenized_docs = [doc.page_content.lower().split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized_docs)
    
    def retrieve(self, query: str, k: int = 5, alpha: float = 0.5) -> list[Document]:
        """Retrieve documents using hybrid search.
        
        Args:
            query: Search query
            k: Number of results
            alpha: Weight for semantic search (1-alpha for keyword)
        """
        # Semantic search
        semantic_results = self.vectorstore.similarity_search_with_score(query, k=k*2)
        semantic_scores = {doc.metadata.get("source", i): score 
                          for i, (doc, score) in enumerate(semantic_results)}
        
        # Keyword search
        tokenized_query = query.lower().split()
        keyword_scores = self.bm25.get_scores(tokenized_query)
        keyword_results = sorted(
            enumerate(keyword_scores),
            key=lambda x: x[1],
            reverse=True
        )[:k*2]
        
        # Normalize scores
        max_semantic = max(semantic_scores.values()) if semantic_scores else 1
        max_keyword = max([s for _, s in keyword_results]) if keyword_results else 1
        
        # Combine scores
        combined_scores = {}
        for i, (doc, score) in enumerate(semantic_results):
            doc_id = doc.metadata.get("source", i)
            normalized_semantic = score / max_semantic if max_semantic > 0 else 0
            combined_scores[doc_id] = alpha * (1 - normalized_semantic)  # Lower is better for distance
        
        for i, score in keyword_results:
            doc_id = self.documents[i].metadata.get("source", i)
            normalized_keyword = score / max_keyword if max_keyword > 0 else 0
            if doc_id in combined_scores:
                combined_scores[doc_id] += (1 - alpha) * normalized_keyword
            else:
                combined_scores[doc_id] = (1 - alpha) * normalized_keyword
        
        # Get top k
        top_doc_ids = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:k]
        
        # Return documents
        results = []
        for doc_id, _ in top_doc_ids:
            # Find document
            for doc in self.documents:
                if doc.metadata.get("source") == doc_id:
                    results.append(doc)
                    break
        
        return results

# Usage
retriever = HybridRetriever(documents)
results = retriever.retrieve("machine learning algorithms", k=5, alpha=0.7)
```

```python
from langchain_community.llms import Cohere
from typing import List, Tuple

class Reranker:
    """Rerank retrieved documents for better relevance."""
    
    def __init__(self, cohere_api_key: str = None):
        if cohere_api_key:
            self.cohere = Cohere(cohere_api_key=cohere_api_key)
        else:
            self.cohere = None
    
    def rerank_cohere(self, query: str, documents: list[Document], top_n: int = 5) -> list[Document]:
        """Rerank using Cohere API."""
        if not self.cohere:
            raise ValueError("Cohere API key required")
        
        doc_texts = [doc.page_content for doc in documents]
        
        # Cohere rerank API
        import cohere
        co = cohere.Client(api_key=self.cohere.cohere_api_key)
        
        results = co.rerank(
            model="rerank-english-v3.0",
            query=query,
            documents=doc_texts,
            top_n=top_n
        )
        
        # Map back to documents
        reranked = []
        for result in results:
            idx = result.index
            reranked.append(documents[idx])
        
        return reranked
    
    def rerank_cross_encoder(self, query: str, documents: list[Document], top_n: int = 5) -> list[Document]:
        """Rerank using cross-encoder model (local)."""
        from sentence_transformers import CrossEncoder
        
        model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        
        # Prepare pairs
        pairs = [[query, doc.page_content] for doc in documents]
        
        # Get scores
        scores = model.predict(pairs)
        
        # Sort by score
        scored_docs = list(zip(documents, scores))
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        return [doc for doc, _ in scored_docs[:top_n]]
    
    def rerank_llm(self, query: str, documents: list[Document], top_n: int = 5, llm=None) -> list[Document]:
        """Rerank using LLM reasoning."""
        if not llm:
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        
        # Create prompt
        doc_texts = "\n\n".join([
            f"Document {i+1}:\n{doc.page_content[:500]}"
            for i, doc in enumerate(documents)
        ])
        
        prompt = f"""Rank these documents by relevance to the query: "{query}"

Documents:
{doc_texts}

Return only the numbers of the top {top_n} most relevant documents, separated by commas."""
        
        response = llm.invoke(prompt)
        
        # Parse response
        try:
            indices = [int(x.strip()) - 1 for x in response.content.split(",")]
            return [documents[i] for i in indices if 0 <= i < len(documents)]
        except:
            return documents[:top_n]  # Fallback
```

```python
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from typing import List, Dict

class CitationRAG:
    """RAG system with citation support."""
    
    def __init__(self, retriever, llm):
        self.retriever = retriever
        self.llm = llm
    
    def answer_with_citations(self, query: str, k: int = 5) -> Dict:
        """Answer query with source citations."""
        # Retrieve documents
        docs = self.retriever.get_relevant_documents(query)
        
        # Format context with citations
        context_parts = []
        for i, doc in enumerate(docs[:k], 1):
            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", "")
            citation = f"[{i}]"
            context_parts.append(f"{citation} {doc.page_content}\nSource: {source}{f', Page {page}' if page else ''}")
        
        context = "\n\n".join(context_parts)
        
        # Create prompt with citation instructions
        prompt = PromptTemplate(
            template="""Answer the question using the provided context. Include citations [1], [2], etc. when referencing information.

Context:
{context}

Question: {question}

Answer with citations:""",
            input_variables=["context", "question"]
        )
        
        # Generate answer
        chain = prompt | self.llm
        answer = chain.invoke({"context": context, "question": query})
        
        # Extract citations
        citations = []
        for i, doc in enumerate(docs[:k], 1):
            citations.append({
                "id": i,
                "text": doc.page_content[:200],
                "source": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", ""),
                "metadata": doc.metadata
            })
        
        return {
            "answer": answer.content if hasattr(answer, "content") else str(answer),
            "citations": citations,
            "sources": [c["source"] for c in citations]
        }
    
    def answer_with_quote_attribution(self, query: str) -> Dict:
        """Answer with direct quote attribution."""
        docs = self.retriever.get_relevant_documents(query)
        
        # Build context
        context_parts = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "Unknown")
            context_parts.append(f"[{i}] {doc.page_content}\n(Source: {source})")
        
        context = "\n\n".join(context_parts)
        
        prompt = PromptTemplate(
            template="""Answer the question using quotes from the provided sources. Format quotes as: "quote text" [source number].

Context:
{context}

Question: {question}

Answer with quoted evidence:""",
            input_variables=["context", "question"]
        )
        
        chain = prompt | self.llm
        answer = chain.invoke({"context": context, "question": query})
        
        return {
            "answer": answer.content if hasattr(answer, "content") else str(answer),
            "sources": [
                {
                    "id": i+1,
                    "source": doc.metadata.get("source", "Unknown"),
                    "excerpt": doc.page_content[:300]
                }
                for i, doc in enumerate(docs)
            ]
        }
```

```python
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

class CompleteRAGPipeline:
    """Complete RAG pipeline with chunking, retrieval, reranking, and citation."""
    
    def __init__(self, documents: list[Document], embedding_model: str = "all-MiniLM-L6-v2"):
        # Chunk documents
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.chunks = text_splitter.split_documents(documents)
        
        # Create embeddings and vector store
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        self.vectorstore = Chroma.from_documents(
            documents=self.chunks,
            embedding=self.embeddings
        )
        
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        
        # Create retriever
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": 10, "score_threshold": 0.5}
        )
    
    def query(self, question: str, use_reranking: bool = True, use_citations: bool = True) -> Dict:
        """Query the RAG system."""
        # Retrieve
        docs = self.retriever.get_relevant_documents(question)
        
        # Rerank if enabled
        if use_reranking and len(docs) > 5:
            reranker = Reranker()
            docs = reranker.rerank_cross_encoder(question, docs, top_n=5)
        
        # Build context
        if use_citations:
            context_parts = []
            for i, doc in enumerate(docs, 1):
                source = doc.metadata.get("source", "Unknown")
                context_parts.append(f"[{i}] {doc.page_content}\nSource: {source}")
            context = "\n\n".join(context_parts)
            citation_note = " Include citations [1], [2], etc. in your answer."
        else:
            context = "\n\n".join([doc.page_content for doc in docs])
            citation_note = ""
        
        # Create prompt
        prompt = PromptTemplate(
            template=f"""Answer the question using the provided context.{citation_note}

Context:
{{context}}

Question: {{question}}

Answer:""",
            input_variables=["context", "question"]
        )
        
        # Generate answer
        chain = prompt | self.llm
        answer = chain.invoke({"context": context, "question": question})
        
        result = {
            "answer": answer.content if hasattr(answer, "content") else str(answer),
            "num_sources": len(docs)
        }
        
        if use_citations:
            result["sources"] = [
                {
                    "id": i+1,
                    "source": doc.metadata.get("source", "Unknown"),
                    "excerpt": doc.page_content[:200]
                }
                for i, doc in enumerate(docs)
            ]
        
        return result
```

## Chunking Strategies Comparison
| Strategy | Best For | Pros | Cons |
|----------|----------|------|------|
| Character-based | Simple text | Fast, predictable | Ignores structure |
| Recursive | General documents | Respects structure | May split sentences |
| Token-based | LLM context | Accurate sizing | Requires tokenizer |
| Semantic | Related content | Groups concepts | Slower, needs embeddings |
| Header-based | Markdown | Preserves hierarchy | Markdown only |

## Best Practices
- Use recursive chunking for most documents
- Overlap chunks by 10-20% to preserve context
- Chunk size: 500-1000 chars for general use, adjust for model context
- Use semantic chunking for conceptual grouping
- Combine multiple retrieval methods (hybrid search)
- Rerank results for better relevance
- Always include source citations
- Store metadata (source, page, timestamp) with chunks

## Anti-Patterns
| Anti-Pattern | Fix |
|--------------|-----|
| No chunk overlap | Use 10-20% overlap |
| Too large chunks | Keep under model context limit |
| Ignoring document structure | Use header-aware chunking |
| Single retrieval method | Use hybrid search |
| No reranking | Add reranking step |
| Missing citations | Always include source metadata |
| No metadata preservation | Pass metadata through pipeline |

## Related
- Skill: `advanced-retrieval`
- Skill: `knowledge-graphs`
- Skill: `memory-management`

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Packages: langchain, langchain-core, langchain-community, chromadb, faiss-cpu, sentence-transformers, rank-bm25, cohere

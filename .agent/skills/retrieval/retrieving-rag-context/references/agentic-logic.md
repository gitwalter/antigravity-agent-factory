# Agentic RAG Logic Flow

The `retrieving-rag-context` skill utilizes an agentic loop to ensure high-quality retrieval.

## Flow Diagram
1.  **Input**: User Question
2.  **Retrieve**: Semantic search against Qdrant `ebook_library`.
3.  **Grade**:
    *   Normalize text (umlauts, case, special chars).
    *   Verify keyword presence from question in retrieved snippets.
4.  **Decide**:
    *   If Grade >= Threshold -> **Generate** response from local context.
    *   If Grade < Threshold -> **Web Search** (Tavily) -> **Generate** from combined context.

## Heuristic Grading
The grading logic is purposely heuristic for speed:
- It focuses on **keyword overlap** after normalization.
- This avoids unnecessary LLM calls for relevance checking, keeping the latency low (<200ms).

## Adaptive Fallback
The fallback to Tavily ensures that the agent doesn't "hallucinate" an answer when the local library is silent on a topic.

"""
Local Embedding Service for Memory System

Provides semantic embeddings using sentence-transformers, running entirely locally
without any API keys required. Downloads the model on first run (~80MB).

Features:
    - Local inference with no API dependencies
    - Automatic model caching in data/models/
    - Similarity scoring for memory retrieval
    - Batch embedding for efficiency

Usage:
    from scripts.memory.embedding_service import EmbeddingService
    
    service = EmbeddingService()
    
    # Embed texts
    vectors = service.embed(["Hello world", "Test sentence"])
    
    # Find similarity
    scores = service.similarity("Python testing", ["pytest", "unittest", "cooking"])
"""

import os
import logging
from pathlib import Path
from typing import List, Union, Optional

import numpy as np

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Local embedding service using sentence-transformers.
    
    Downloads and caches the embedding model on first use.
    All inference runs locally with no API keys required.
    
    Attributes:
        model_name: Name of the sentence-transformers model
        cache_dir: Directory for model cache
        model: Loaded SentenceTransformer model
        
    Example:
        >>> service = EmbeddingService()
        >>> vectors = service.embed(["test sentence"])
        >>> print(vectors.shape)
        (1, 384)
    """
    
    # Default model - good balance of speed and quality
    DEFAULT_MODEL = "all-MiniLM-L6-v2"
    
    # Model dimensions for validation
    MODEL_DIMENSIONS = {
        "all-MiniLM-L6-v2": 384,
        "all-mpnet-base-v2": 768,
        "paraphrase-MiniLM-L6-v2": 384,
    }
    
    def __init__(
        self, 
        model_name: str = DEFAULT_MODEL,
        cache_dir: str = "data/models",
        lazy_load: bool = False
    ):
        """
        Initialize the embedding service.
        
        Args:
            model_name: Name of the sentence-transformers model to use.
                        Default: "all-MiniLM-L6-v2" (384 dimensions, ~80MB)
            cache_dir: Directory to cache downloaded models.
                       Default: "data/models"
            lazy_load: If True, delay model loading until first use.
                       Default: False (load immediately)
        """
        self.model_name = model_name
        self.cache_dir = Path(cache_dir)
        self._model = None
        self._dimension = self.MODEL_DIMENSIONS.get(model_name, 384)
        
        # Create cache directory
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Set environment variable for sentence-transformers cache
        os.environ["SENTENCE_TRANSFORMERS_HOME"] = str(self.cache_dir.absolute())
        
        if not lazy_load:
            self._load_model()
    
    def _load_model(self) -> None:
        """Load the sentence-transformers model."""
        if self._model is not None:
            return
            
        try:
            # Import here to allow graceful failure if not installed
            from sentence_transformers import SentenceTransformer
            
            logger.info(f"Loading embedding model: {self.model_name}")
            logger.info(f"Model cache directory: {self.cache_dir.absolute()}")
            
            # This will download on first run (~80MB for MiniLM)
            self._model = SentenceTransformer(self.model_name)
            
            # Update dimension from loaded model
            self._dimension = self._model.get_sentence_embedding_dimension()
            
            logger.info(f"Embedding model ready (dimension: {self._dimension})")
            
        except ImportError:
            raise ImportError(
                "sentence-transformers is required for the embedding service. "
                "Install with: pip install sentence-transformers"
            )
    
    @property
    def model(self):
        """Lazy-load and return the model."""
        if self._model is None:
            self._load_model()
        return self._model
    
    @property
    def dimension(self) -> int:
        """Return the embedding dimension."""
        return self._dimension
    
    @property
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self._model is not None
    
    def embed(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Generate embeddings for text(s).
        
        Args:
            texts: Single string or list of strings to embed.
            
        Returns:
            numpy array of shape (n_texts, dimension)
            
        Example:
            >>> vectors = service.embed(["Hello", "World"])
            >>> print(vectors.shape)
            (2, 384)
        """
        if isinstance(texts, str):
            texts = [texts]
        
        if not texts:
            return np.array([]).reshape(0, self._dimension)
        
        # Generate embeddings
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False,
            normalize_embeddings=True  # For cosine similarity
        )
        
        return embeddings
    
    def embed_single(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.
        
        Args:
            text: String to embed.
            
        Returns:
            numpy array of shape (dimension,)
        """
        return self.embed([text])[0]
    
    def similarity(
        self, 
        query: str, 
        candidates: List[str],
        return_sorted: bool = False
    ) -> Union[List[float], List[tuple]]:
        """
        Calculate similarity between query and candidate texts.
        
        Uses cosine similarity (embeddings are normalized).
        
        Args:
            query: Query text to compare against.
            candidates: List of candidate texts.
            return_sorted: If True, return (text, score) tuples sorted by score.
            
        Returns:
            If return_sorted=False: List of similarity scores (0.0 to 1.0)
            If return_sorted=True: List of (text, score) tuples, highest first
            
        Example:
            >>> scores = service.similarity("Python testing", ["pytest", "cooking"])
            >>> print(scores)
            [0.85, 0.12]
        """
        if not candidates:
            return [] if not return_sorted else []
        
        # Embed query and candidates
        query_embedding = self.embed_single(query)
        candidate_embeddings = self.embed(candidates)
        
        # Cosine similarity (embeddings are already normalized)
        scores = np.dot(candidate_embeddings, query_embedding).tolist()
        
        if return_sorted:
            pairs = list(zip(candidates, scores))
            pairs.sort(key=lambda x: x[1], reverse=True)
            return pairs
        
        return scores
    
    def most_similar(
        self, 
        query: str, 
        candidates: List[str], 
        k: int = 5,
        threshold: float = 0.0
    ) -> List[tuple]:
        """
        Find the k most similar candidates to the query.
        
        Args:
            query: Query text to compare against.
            candidates: List of candidate texts.
            k: Maximum number of results to return.
            threshold: Minimum similarity score to include.
            
        Returns:
            List of (text, score) tuples, highest first, limited to k results.
            
        Example:
            >>> results = service.most_similar("Python testing", candidates, k=3)
            >>> for text, score in results:
            ...     print(f"{text}: {score:.2f}")
        """
        sorted_pairs = self.similarity(query, candidates, return_sorted=True)
        
        # Filter by threshold and limit to k
        filtered = [(text, score) for text, score in sorted_pairs if score >= threshold]
        return filtered[:k]
    
    def batch_similarity(
        self, 
        queries: List[str], 
        candidates: List[str]
    ) -> np.ndarray:
        """
        Calculate similarity matrix between queries and candidates.
        
        Args:
            queries: List of query texts.
            candidates: List of candidate texts.
            
        Returns:
            numpy array of shape (n_queries, n_candidates) with similarity scores.
        """
        if not queries or not candidates:
            return np.array([]).reshape(len(queries), len(candidates))
        
        query_embeddings = self.embed(queries)
        candidate_embeddings = self.embed(candidates)
        
        # Similarity matrix
        return np.dot(query_embeddings, candidate_embeddings.T)
    
    def is_similar(self, text1: str, text2: str, threshold: float = 0.8) -> bool:
        """
        Check if two texts are semantically similar.
        
        Args:
            text1: First text.
            text2: Second text.
            threshold: Similarity threshold (0.0 to 1.0).
            
        Returns:
            True if similarity >= threshold, False otherwise.
        """
        scores = self.similarity(text1, [text2])
        return scores[0] >= threshold
    
    def get_status(self) -> dict:
        """
        Get status information about the embedding service.
        
        Returns:
            Dictionary with status information.
        """
        return {
            "model_name": self.model_name,
            "dimension": self._dimension,
            "is_loaded": self.is_loaded,
            "cache_dir": str(self.cache_dir.absolute()),
            "model_cached": self._is_model_cached(),
        }
    
    def _is_model_cached(self) -> bool:
        """Check if model is already cached locally."""
        # sentence-transformers uses a specific naming convention
        model_path = self.cache_dir / f"sentence-transformers_{self.model_name}"
        return model_path.exists()


# Singleton instance for convenience
_default_service: Optional[EmbeddingService] = None


def get_embedding_service(
    model_name: str = EmbeddingService.DEFAULT_MODEL,
    cache_dir: str = "data/models"
) -> EmbeddingService:
    """
    Get or create the default embedding service instance.
    
    Uses a singleton pattern to avoid loading the model multiple times.
    
    Args:
        model_name: Model to use (only applies on first call).
        cache_dir: Cache directory (only applies on first call).
        
    Returns:
        EmbeddingService instance.
    """
    global _default_service
    
    if _default_service is None:
        _default_service = EmbeddingService(
            model_name=model_name,
            cache_dir=cache_dir,
            lazy_load=True  # Load on first use
        )
    
    return _default_service

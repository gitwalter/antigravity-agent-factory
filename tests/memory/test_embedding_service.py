"""
Tests for the Embedding Service.

Tests local embedding functionality using sentence-transformers.
"""

import pytest

# Check if dependencies are available
try:
    import numpy as np
    from sentence_transformers import SentenceTransformer

    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False
    np = None  # For type hints

pytestmark = pytest.mark.skipif(
    not HAS_SENTENCE_TRANSFORMERS, reason="sentence-transformers not installed"
)


class TestEmbeddingService:
    """Tests for EmbeddingService class."""

    @pytest.fixture
    def lazy_service(self):
        """Create an embedding service instance WITHOUT loading the model.

        Use this fixture for tests that check lazy loading behavior.
        """
        from scripts.memory.embedding_service import EmbeddingService

        return EmbeddingService(lazy_load=True)

    @pytest.fixture
    def service(self):
        """Create an embedding service instance WITH the model pre-loaded.

        Handles network timeout during model download in CI environments
        by skipping the test if the model cannot be loaded.
        """
        from scripts.memory.embedding_service import EmbeddingService

        service = EmbeddingService(lazy_load=True)

        # Pre-load the model to catch network timeouts early
        try:
            # Force model load to detect network issues
            service._load_model()
        except Exception as e:
            error_str = str(e).lower()
            error_type = type(e).__name__.lower()
            # Check for network-related errors
            network_indicators = [
                "timeout",
                "connection",
                "network",
                "readtimeout",
                "httpx",
            ]
            if any(
                indicator in error_str or indicator in error_type
                for indicator in network_indicators
            ):
                pytest.skip(
                    f"Skipping due to network issue during model download: {type(e).__name__}: {e}"
                )
            raise  # Re-raise if it's a different error

        return service

    def test_service_initialization(self, lazy_service):
        """Test that service initializes correctly with lazy loading."""
        assert lazy_service.model_name == "all-MiniLM-L6-v2"
        assert lazy_service.dimension == 384
        assert not lazy_service.is_loaded  # Lazy load - model not yet loaded

    def test_embedding_produces_vectors(self, service):
        """Verify embeddings are generated correctly."""
        result = service.embed(["test sentence"])

        assert isinstance(result, np.ndarray)
        assert result.shape == (1, 384)  # MiniLM dimension

    def test_embedding_multiple_texts(self, service):
        """Test embedding multiple texts at once."""
        texts = ["Hello world", "Test sentence", "Another example"]
        result = service.embed(texts)

        assert result.shape == (3, 384)

    def test_embedding_single_text(self, service):
        """Test embed_single method."""
        result = service.embed_single("test sentence")

        assert isinstance(result, np.ndarray)
        assert result.shape == (384,)

    def test_similar_texts_have_high_similarity(self, service):
        """Verify semantic similarity works for similar texts."""
        score = service.similarity(
            "Python testing with pytest", ["Testing Python code with pytest framework"]
        )

        assert len(score) == 1
        assert score[0] > 0.8  # High similarity

    def test_dissimilar_texts_have_low_similarity(self, service):
        """Verify dissimilar content is distinguished."""
        score = service.similarity("Python testing", ["Cooking Italian pasta recipes"])

        assert len(score) == 1
        assert score[0] < 0.3  # Low similarity

    def test_similarity_with_multiple_candidates(self, service):
        """Test similarity against multiple candidates."""
        scores = service.similarity(
            "Python programming",
            ["JavaScript coding", "Python development", "Cooking recipes"],
        )

        assert len(scores) == 3
        # Python development should be most similar
        assert scores[1] > scores[0]  # Python > JavaScript
        assert scores[1] > scores[2]  # Python > Cooking

    def test_most_similar_returns_top_k(self, service):
        """Test most_similar method returns correct number of results."""
        candidates = [
            "Python testing",
            "JavaScript frameworks",
            "pytest usage",
            "Cooking recipes",
            "unittest examples",
        ]

        results = service.most_similar("Python pytest testing", candidates, k=3)

        assert len(results) <= 3
        assert all(isinstance(r, tuple) and len(r) == 2 for r in results)
        # First result should be most similar
        if len(results) > 1:
            assert results[0][1] >= results[1][1]

    def test_most_similar_with_threshold(self, service):
        """Test most_similar with threshold filtering."""
        candidates = ["Python testing with pytest", "Cooking pasta recipes"]

        results = service.most_similar(
            "pytest framework", candidates, k=5, threshold=0.5
        )

        # All results should be above threshold
        assert all(score >= 0.5 for _, score in results)

    def test_is_similar_returns_boolean(self, service):
        """Test is_similar method."""
        # Similar texts
        assert service.is_similar(
            "Python testing", "Testing Python code", threshold=0.7
        )

        # Dissimilar texts
        assert not service.is_similar(
            "Python testing", "Cooking recipes", threshold=0.7
        )

    def test_empty_input_handling(self, service):
        """Test handling of empty inputs."""
        # Empty list
        result = service.embed([])
        assert result.shape == (0, 384)

        # Empty similarity
        scores = service.similarity("test", [])
        assert scores == []

    def test_batch_similarity(self, service):
        """Test batch similarity matrix."""
        queries = ["Python", "JavaScript"]
        candidates = ["Python programming", "JS coding", "Cooking"]

        matrix = service.batch_similarity(queries, candidates)

        assert matrix.shape == (2, 3)
        # Python should be more similar to Python programming
        assert matrix[0, 0] > matrix[0, 2]

    def test_get_status(self, service):
        """Test status reporting."""
        status = service.get_status()

        assert "model_name" in status
        assert "dimension" in status
        assert "is_loaded" in status
        assert "cache_dir" in status


class TestEmbeddingServiceSingleton:
    """Tests for the singleton pattern."""

    def test_get_embedding_service_returns_same_instance(self):
        """Test singleton returns same instance."""
        from scripts.memory.embedding_service import get_embedding_service

        # Reset singleton for test
        import scripts.memory.embedding_service as module

        module._default_service = None

        service1 = get_embedding_service()
        service2 = get_embedding_service()

        assert service1 is service2

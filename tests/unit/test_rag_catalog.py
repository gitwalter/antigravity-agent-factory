"""
TDD Tests for RAG Catalog / Library Info (AGENT-40).

Tests the NEW get_library_info() method in OptimizedRAG.
Written BEFORE implementation (Red phase).
"""

import tempfile
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_rag():
    """Create an OptimizedRAG with all heavy dependencies mocked."""
    with patch("scripts.ai.rag.rag_optimized.OptimizedRAG.__init__", return_value=None):
        from scripts.ai.rag.rag_optimized import OptimizedRAG

        rag = OptimizedRAG.__new__(OptimizedRAG)
        rag.parent_store_path = tempfile.mkdtemp()
        rag._embeddings = MagicMock()
        rag._client = MagicMock()
        rag._vectorstore = MagicMock()
        rag._store = MagicMock()
        rag._retriever = MagicMock()
        rag._parent_splitter = None
        rag._child_splitter = None
        return rag


# ---------------------------------------------------------------------------
# get_library_info tests
# ---------------------------------------------------------------------------


class TestGetLibraryInfo:
    """Tests for get_library_info()."""

    def test_structure_has_required_keys(self, mock_rag):
        """get_library_info returns dict with expected top-level keys."""
        mock_doc = MagicMock()
        mock_doc.metadata = {
            "source": "/path/to/book.pdf",
            "file_hash": "abc123",
        }
        mock_rag.store.yield_keys = MagicMock(return_value=["k1"])
        mock_rag.store.mget = MagicMock(return_value=[mock_doc])

        info = mock_rag.get_library_info()
        assert isinstance(info, dict)
        assert "total_documents" in info
        assert "total_chunks" in info
        assert "sources" in info

    def test_empty_library(self, mock_rag):
        """get_library_info handles empty library gracefully."""
        mock_rag.store.yield_keys = MagicMock(return_value=[])

        info = mock_rag.get_library_info()
        assert info["total_documents"] == 0
        assert info["total_chunks"] == 0
        assert info["sources"] == []

    def test_counts_match_reality(self, mock_rag):
        """Counts in get_library_info match actual store contents."""
        # Two docs from the same source, one from another
        doc_a1 = MagicMock()
        doc_a1.metadata = {"source": "/path/a.pdf", "file_hash": "hash_a"}
        doc_a2 = MagicMock()
        doc_a2.metadata = {"source": "/path/a.pdf", "file_hash": "hash_a"}
        doc_b = MagicMock()
        doc_b.metadata = {"source": "/path/b.pdf", "file_hash": "hash_b"}

        mock_rag.store.yield_keys = MagicMock(return_value=["k1", "k2", "k3"])
        # list_sources calls store.mget([key]) one key at a time
        mock_rag.store.mget = MagicMock(side_effect=[[doc_a1], [doc_a2], [doc_b]])

        info = mock_rag.get_library_info()
        assert info["total_documents"] == 2  # unique sources
        assert info["total_chunks"] == 3  # total chunks

    def test_sources_include_metadata(self, mock_rag):
        """Each source entry includes path, hash, and chunk count."""
        doc = MagicMock()
        doc.metadata = {"source": "/path/to/book.pdf", "file_hash": "abc123"}
        mock_rag.store.yield_keys = MagicMock(return_value=["k1", "k2"])
        mock_rag.store.mget = MagicMock(return_value=[doc, doc])

        info = mock_rag.get_library_info()
        assert len(info["sources"]) == 1
        src = info["sources"][0]
        assert "source" in src
        assert "chunk_count" in src
        assert src["chunk_count"] == 2

    def test_toc_availability_tracked(self, mock_rag):
        """Sources indicate whether a TOC chunk exists."""
        doc_regular = MagicMock()
        doc_regular.metadata = {"source": "/path/to/book.pdf", "file_hash": "abc"}
        doc_toc = MagicMock()
        doc_toc.metadata = {
            "source": "/path/to/book.pdf",
            "file_hash": "abc",
            "is_toc": True,
        }

        mock_rag.store.yield_keys = MagicMock(return_value=["k1", "k2"])
        # list_sources calls store.mget([key]) one key at a time
        mock_rag.store.mget = MagicMock(side_effect=[[doc_regular], [doc_toc]])

        info = mock_rag.get_library_info()
        src = info["sources"][0]
        assert "has_toc" in src
        assert src["has_toc"] is True

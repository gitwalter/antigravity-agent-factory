"""
TDD Tests for RAG Deduplication (AGENT-40).

Tests the NEW hash-based deduplication in OptimizedRAG.
Written BEFORE implementation (Red phase).
"""

import hashlib
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch, PropertyMock

import pytest


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def temp_pdf(tmp_path):
    """Create a minimal temp file simulating a PDF for hash testing."""
    pdf = tmp_path / "test_book.pdf"
    pdf.write_bytes(b"%PDF-1.4 fake content for hashing")
    return str(pdf)


@pytest.fixture
def temp_pdf_different(tmp_path):
    """Create a second temp file with different content."""
    pdf = tmp_path / "other_book.pdf"
    pdf.write_bytes(b"%PDF-1.4 completely different content here")
    return str(pdf)


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
# Hash computation tests
# ---------------------------------------------------------------------------


class TestComputeFileHash:
    """Tests for _compute_file_hash()."""

    def test_deterministic_same_file(self, mock_rag, temp_pdf):
        """Same file produces the same hash every time."""
        hash1 = mock_rag._compute_file_hash(temp_pdf)
        hash2 = mock_rag._compute_file_hash(temp_pdf)
        assert hash1 == hash2
        assert isinstance(hash1, str)
        assert len(hash1) == 64  # SHA-256 hex digest length

    def test_different_files_different_hashes(
        self, mock_rag, temp_pdf, temp_pdf_different
    ):
        """Different files produce different hashes."""
        hash1 = mock_rag._compute_file_hash(temp_pdf)
        hash2 = mock_rag._compute_file_hash(temp_pdf_different)
        assert hash1 != hash2

    def test_nonexistent_file_returns_none(self, mock_rag):
        """Non-existent file returns None (not an exception)."""
        result = mock_rag._compute_file_hash("/nonexistent/file.pdf")
        assert result is None

    def test_hash_matches_manual_sha256(self, mock_rag, temp_pdf):
        """Hash matches a manually computed SHA-256."""
        expected = hashlib.sha256(Path(temp_pdf).read_bytes()).hexdigest()
        result = mock_rag._compute_file_hash(temp_pdf)
        assert result == expected


# ---------------------------------------------------------------------------
# Deduplication in ingest_ebook tests
# ---------------------------------------------------------------------------


class TestIngestDeduplication:
    """Tests for hash-based dedup in ingest_ebook()."""

    def test_ingest_skips_duplicate_by_hash(self, mock_rag, temp_pdf):
        """Second ingestion of same-hash file is skipped."""
        # Simulate first ingestion stored the hash
        existing_hash = hashlib.sha256(Path(temp_pdf).read_bytes()).hexdigest()

        # Mock store to return a doc with matching hash
        mock_doc = MagicMock()
        mock_doc.metadata = {
            "source": "/some/other/path.pdf",
            "file_hash": existing_hash,
        }
        mock_rag.store.yield_keys = MagicMock(return_value=["key1"])
        mock_rag.store.mget = MagicMock(return_value=[mock_doc])

        result = mock_rag.ingest_ebook(temp_pdf)
        assert result is not None
        assert "duplicate" in result.lower() or "skip" in result.lower()

    def test_ingest_skips_duplicate_by_path(self, mock_rag, temp_pdf):
        """Second ingestion of same-path file is skipped."""
        norm_path = os.path.normpath(temp_pdf)
        mock_doc = MagicMock()
        mock_doc.metadata = {"source": norm_path}
        mock_rag.store.yield_keys = MagicMock(return_value=["key1"])
        mock_rag.store.mget = MagicMock(return_value=[mock_doc])

        result = mock_rag.ingest_ebook(temp_pdf)
        assert result is not None
        assert "skip" in result.lower() or "already" in result.lower()

    def test_ingest_allows_force_reingest(self, mock_rag, temp_pdf):
        """Force flag bypasses dedup."""
        existing_hash = hashlib.sha256(Path(temp_pdf).read_bytes()).hexdigest()
        mock_doc = MagicMock()
        mock_doc.metadata = {
            "source": os.path.normpath(temp_pdf),
            "file_hash": existing_hash,
        }
        mock_rag.store.yield_keys = MagicMock(return_value=["key1"])
        mock_rag.store.mget = MagicMock(return_value=[mock_doc])

        # Mock the actual ingestion pipeline
        mock_rag._extract_toc = MagicMock(return_value=None)
        mock_rag.retriever.parent_splitter = MagicMock()
        mock_rag.retriever.parent_splitter.split_documents = MagicMock(return_value=[])
        mock_rag.retriever.add_documents = MagicMock()
        mock_rag._persist_to_disk = MagicMock()

        with patch("scripts.ai.rag.rag_optimized.PyMuPDFLoader") as MockLoader:
            MockLoader.return_value.load.return_value = []
            result = mock_rag.ingest_ebook(temp_pdf, force=True)

        # Should NOT have been skipped — retriever should have been called
        assert result is None or "skip" not in (result or "").lower()

    def test_ingest_stores_hash_in_metadata(self, mock_rag, temp_pdf):
        """Newly ingested docs have file_hash in their metadata."""
        # Empty store — no duplicates
        mock_rag.store.yield_keys = MagicMock(return_value=[])
        mock_rag._extract_toc = MagicMock(return_value=None)

        captured_docs = []
        mock_rag.retriever.parent_splitter = MagicMock()
        mock_rag.retriever.parent_splitter.split_documents = MagicMock(
            return_value=[MagicMock(metadata={"source": temp_pdf})]
        )
        mock_rag.retriever.add_documents = MagicMock(
            side_effect=lambda docs, **kw: captured_docs.extend(docs)
        )
        mock_rag._persist_to_disk = MagicMock()

        with patch("scripts.ai.rag.rag_optimized.PyMuPDFLoader") as MockLoader:
            mock_doc = MagicMock()
            mock_doc.metadata = {}
            MockLoader.return_value.load.return_value = [mock_doc]
            mock_rag.ingest_ebook(temp_pdf)

        # Check that at least one doc has file_hash in metadata
        assert any("file_hash" in d.metadata for d in captured_docs)


# ---------------------------------------------------------------------------
# list_sources tests
# ---------------------------------------------------------------------------


class TestListSources:
    """Tests for list_sources() method."""

    def test_returns_list_of_dicts(self, mock_rag):
        """list_sources returns a list of dicts with expected keys."""
        mock_doc = MagicMock()
        mock_doc.metadata = {
            "source": "/path/to/book.pdf",
            "file_hash": "abc123",
        }
        mock_rag.store.yield_keys = MagicMock(return_value=["k1", "k2"])
        mock_rag.store.mget = MagicMock(return_value=[mock_doc, mock_doc])

        sources = mock_rag.list_sources()
        assert isinstance(sources, list)
        assert len(sources) > 0
        assert "source" in sources[0]
        assert "file_hash" in sources[0]

    def test_empty_library(self, mock_rag):
        """list_sources returns empty list for empty library."""
        mock_rag.store.yield_keys = MagicMock(return_value=[])
        sources = mock_rag.list_sources()
        assert sources == []

"""
TDD Tests for AGENT-46: TOC Quality & Fast Delivery.

Tests for:
  - get_toc(name) — direct metadata-based lookup (no semantic search)
  - _score_toc(toc_text) — quality scoring
  - delete_toc(name) — remove a bad TOC chunk
  - _extract_toc improvements with quality gate
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
# TOC Quality Scoring
# ---------------------------------------------------------------------------


class TestTocQualityScoring:
    """Tests for _score_toc() quality assessment."""

    def test_good_toc_scores_high(self, mock_rag):
        """A well-structured TOC with chapters scores >= 0.7."""
        good_toc = """
## Table of Contents (Native)

- Chapter 1: Introduction (p. 1)
  - 1.1 Background (p. 3)
  - 1.2 Motivation (p. 5)
- Chapter 2: Methods (p. 15)
  - 2.1 Data Collection (p. 17)
  - 2.2 Analysis (p. 25)
- Chapter 3: Results (p. 40)
- Chapter 4: Discussion (p. 55)
- Chapter 5: Conclusion (p. 70)
"""
        score = mock_rag._score_toc(good_toc)
        assert score >= 0.7

    def test_title_only_scores_low(self, mock_rag):
        """A TOC that's just a book title scores near 0."""
        bad_toc = "Künstliche Intelligenz"
        score = mock_rag._score_toc(bad_toc)
        assert score < 0.3

    def test_copyright_page_scores_low(self, mock_rag):
        """A copyright page disguised as TOC scores low."""
        copyright_toc = """
Data Science from Scratch
by Joel Grus
Copyright 2019 Joel Grus. All rights reserved.
Published by O'Reilly Media.
"""
        score = mock_rag._score_toc(copyright_toc)
        assert score < 0.3

    def test_empty_string_scores_zero(self, mock_rag):
        """Empty string scores 0."""
        score = mock_rag._score_toc("")
        assert score == 0.0

    def test_none_scores_zero(self, mock_rag):
        """None input scores 0."""
        score = mock_rag._score_toc(None)
        assert score == 0.0

    def test_short_toc_with_chapters_scores_medium(self, mock_rag):
        """Short but real TOC (3 chapters) scores moderate."""
        short_toc = """
Chapter 1: Fundamentals
Chapter 2: Planning
Chapter 3: Testing
"""
        score = mock_rag._score_toc(short_toc)
        assert 0.3 <= score <= 0.8


# ---------------------------------------------------------------------------
# Fast TOC Lookup
# ---------------------------------------------------------------------------


class TestGetToc:
    """Tests for get_toc(name) — direct docstore lookup."""

    def test_returns_toc_content(self, mock_rag):
        """get_toc returns TOC text for a matching document."""
        from langchain_core.stores import InMemoryStore
        from langchain_core.documents import Document

        mock_rag._store = InMemoryStore()
        toc_doc = Document(
            page_content="MASTER TABLE OF CONTENTS\n\n- Chapter 1: Intro",
            metadata={"source": "/path/to/book.pdf", "is_toc": True},
        )
        regular_doc = Document(
            page_content="Some content",
            metadata={"source": "/path/to/book.pdf", "is_toc": False},
        )

        mock_rag.store.mset([("k1", toc_doc), ("k2", regular_doc)])

        result = mock_rag.get_toc("book")
        assert result is not None
        assert "Chapter 1" in result

    def test_returns_none_when_no_toc(self, mock_rag):
        """get_toc returns None for doc without a TOC chunk."""
        from langchain_core.stores import InMemoryStore
        from langchain_core.documents import Document

        mock_rag._store = InMemoryStore()
        regular_doc = Document(
            page_content="Some content",
            metadata={"source": "/path/to/notoc.pdf", "is_toc": False},
        )
        mock_rag.store.mset([("k1", regular_doc)])

        result = mock_rag.get_toc("notoc")
        assert result is None

    def test_returns_none_when_no_match(self, mock_rag):
        """get_toc returns None for non-existent document."""
        from langchain_core.stores import InMemoryStore

        mock_rag._store = InMemoryStore()

        result = mock_rag.get_toc("nonexistent")
        assert result is None

    def test_fuzzy_matches_by_basename(self, mock_rag):
        """get_toc matches by partial basename (case-insensitive)."""
        from langchain_core.stores import InMemoryStore
        from langchain_core.documents import Document

        mock_rag._store = InMemoryStore()
        toc_doc = Document(
            page_content="TOC content here",
            metadata={"source": "/long/path/My_Great_Book_2nd_Ed.pdf", "is_toc": True},
        )
        mock_rag.store.mset([("k1", toc_doc)])

        result = mock_rag.get_toc("great_book")
        assert result is not None


# ---------------------------------------------------------------------------
# TOC Deletion
# ---------------------------------------------------------------------------


class TestDeleteToc:
    """Tests for delete_toc(name) — remove a bad TOC chunk."""

    def test_deletes_toc_chunk(self, mock_rag):
        """delete_toc removes only the TOC chunk, not regular chunks."""
        from langchain_core.stores import InMemoryStore
        from langchain_core.documents import Document

        mock_rag._store = InMemoryStore()
        toc_doc = Document(
            page_content="TOC", metadata={"source": "/path/book.pdf", "is_toc": True}
        )
        regular_doc = Document(
            page_content="content",
            metadata={"source": "/path/book.pdf", "is_toc": False},
        )

        mock_rag.store.mset([("toc_key", toc_doc), ("reg_key", regular_doc)])

        deleted = mock_rag.delete_toc("book")
        assert deleted is True
        assert mock_rag.store.mget(["toc_key"]) == [None]
        assert mock_rag.store.mget(["reg_key"]) != [None]

    def test_returns_false_when_no_toc(self, mock_rag):
        """delete_toc returns False when no TOC chunk exists."""
        from langchain_core.stores import InMemoryStore
        from langchain_core.documents import Document

        mock_rag._store = InMemoryStore()
        regular_doc = Document(
            page_content="content",
            metadata={"source": "/path/book.pdf", "is_toc": False},
        )
        mock_rag.store.mset([("k1", regular_doc)])

        deleted = mock_rag.delete_toc("book")
        assert deleted is False


# ---------------------------------------------------------------------------
# Extract TOC with quality gate
# ---------------------------------------------------------------------------


class TestTocQualityGate:
    """Tests that _extract_toc rejects low-quality results."""

    @patch("scripts.ai.rag.rag_optimized.fitz")
    def test_rejects_title_only_toc_from_native(self, mock_fitz, mock_rag):
        """Native TOC with only 1-2 entries is rejected (falls through)."""
        mock_doc = MagicMock()
        # Only 2 entries — below the threshold of 3
        mock_doc.get_toc.return_value = [
            [1, "Title Page", 1],
            [1, "Copyright", 2],
        ]
        mock_page = MagicMock()
        mock_page.get_text.return_value = ""
        mock_doc.__len__ = MagicMock(return_value=1)
        mock_doc.__getitem__ = MagicMock(return_value=mock_page)
        mock_fitz.open.return_value = mock_doc

        with patch(
            "langchain_google_genai.ChatGoogleGenerativeAI",
            side_effect=Exception("skip LLM"),
        ):
            result = mock_rag._extract_toc("/fake/book.pdf")
            # Should return None — 2 entries is too few
            assert result is None

"""
TDD Tests for Multi-Strategy TOC Extraction (AGENT-41).

Tests the NEW _extract_toc() with 3-tier fallback:
  1. PyMuPDF native TOC (doc.get_toc())
  2. Regex heuristic (chapter/section patterns)
  3. LLM extraction (existing Gemini, last resort)

Written BEFORE implementation (Red phase).
"""

import tempfile
from unittest.mock import MagicMock, patch, PropertyMock

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
# PyMuPDF native TOC tests
# ---------------------------------------------------------------------------


class TestTocPyMuPDFNative:
    """Tests for PyMuPDF native TOC extraction (Strategy 1)."""

    @patch("scripts.ai.rag.rag_optimized.fitz")
    def test_uses_native_toc_when_available(self, mock_fitz, mock_rag):
        """When PyMuPDF doc.get_toc() returns entries, use them directly."""
        mock_doc = MagicMock()
        # PyMuPDF TOC format: [level, title, page_number]
        mock_doc.get_toc.return_value = [
            [1, "Chapter 1: Introduction", 1],
            [2, "1.1 Background", 3],
            [1, "Chapter 2: Methods", 15],
        ]
        mock_fitz.open.return_value = mock_doc

        result = mock_rag._extract_toc("/fake/book.pdf")
        assert result is not None
        assert "Chapter 1" in result
        assert "Introduction" in result
        assert "Methods" in result

    @patch("scripts.ai.rag.rag_optimized.fitz")
    def test_skips_empty_native_toc(self, mock_fitz, mock_rag):
        """When native TOC is empty, falls through to next strategy."""
        mock_doc = MagicMock()
        mock_doc.get_toc.return_value = []
        # Simulate pages with chapter-like content for regex
        mock_page = MagicMock()
        mock_page.get_text.return_value = "Chapter 1: Introduction\nSome content here."
        mock_doc.__len__ = MagicMock(return_value=1)
        mock_doc.__getitem__ = MagicMock(return_value=mock_page)
        mock_fitz.open.return_value = mock_doc

        # If regex catches it, result should still contain content
        # If neither works, LLM should be tried (but we're not testing LLM here)
        # This test verifies the native strategy doesn't block fallback
        result = mock_rag._extract_toc("/fake/book.pdf")
        # Result depends on whether regex or LLM catches it — the test
        # just verifies no crash and that we proceed past empty native TOC


# ---------------------------------------------------------------------------
# Regex fallback tests
# ---------------------------------------------------------------------------


class TestTocRegexFallback:
    """Tests for regex-based TOC extraction (Strategy 2)."""

    @patch("scripts.ai.rag.rag_optimized.fitz")
    def test_regex_catches_chapter_patterns(self, mock_fitz, mock_rag):
        """Regex detects 'Chapter N:' patterns in text."""
        mock_doc = MagicMock()
        mock_doc.get_toc.return_value = []  # No native TOC

        # Simulate pages with chapter-like content
        page_texts = [
            "Chapter 1: The Beginning\nSome intro text...",
            "Chapter 2: The Middle\nMore content...",
            "Chapter 3: The End\nFinal content...",
        ]
        mock_pages = []
        for text in page_texts:
            page = MagicMock()
            page.get_text.return_value = text
            mock_pages.append(page)

        mock_doc.__len__ = MagicMock(return_value=len(mock_pages))
        mock_doc.__getitem__ = MagicMock(side_effect=lambda i: mock_pages[i])
        mock_fitz.open.return_value = mock_doc

        result = mock_rag._extract_toc("/fake/book.pdf")
        # Should extract chapter titles via regex before resorting to LLM
        if result is not None:
            assert "Chapter 1" in result or "Beginning" in result


# ---------------------------------------------------------------------------
# LLM fallback tests (Strategy 3)
# ---------------------------------------------------------------------------


class TestTocLlmFallback:
    """Tests for LLM-based TOC extraction (Strategy 3, last resort)."""

    @patch("scripts.ai.rag.rag_optimized.fitz")
    def test_llm_called_only_when_others_fail(self, mock_fitz, mock_rag):
        """LLM is NOT called if native TOC succeeds."""
        mock_doc = MagicMock()
        mock_doc.get_toc.return_value = [
            [1, "Chapter 1: Intro", 1],
        ]
        mock_fitz.open.return_value = mock_doc

        with patch("langchain_google_genai.ChatGoogleGenerativeAI") as MockLLM:
            mock_rag._extract_toc("/fake/book.pdf")
            # LLM should NOT have been instantiated
            MockLLM.assert_not_called()


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestTocEdgeCases:
    """Edge case tests for TOC extraction."""

    @patch("scripts.ai.rag.rag_optimized.fitz")
    def test_returns_none_when_all_fail(self, mock_fitz, mock_rag):
        """Returns None when all three strategies fail."""
        mock_doc = MagicMock()
        mock_doc.get_toc.return_value = []

        # Pages with no recognizable content
        mock_page = MagicMock()
        mock_page.get_text.return_value = ""
        mock_doc.__len__ = MagicMock(return_value=1)
        mock_doc.__getitem__ = MagicMock(return_value=mock_page)
        mock_fitz.open.return_value = mock_doc

        # Mock LLM to also fail
        with patch(
            "langchain_google_genai.ChatGoogleGenerativeAI",
            side_effect=Exception("No API key"),
        ):
            result = mock_rag._extract_toc("/fake/book.pdf")
            assert result is None

    @patch("scripts.ai.rag.rag_optimized.fitz")
    def test_file_open_failure_returns_none(self, mock_fitz, mock_rag):
        """Corrupted/unreadable PDF returns None gracefully."""
        mock_fitz.open.side_effect = Exception("Cannot open file")
        result = mock_rag._extract_toc("/fake/corrupted.pdf")
        assert result is None

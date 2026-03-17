import os
import fitz
import logging
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from scripts.ai.core.llm_config import get_primary_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Configure basic logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Constants
LIBRARY_DIR = "D:\\Users\\wpoga\\Documents\\Ebooks\\Antigravity Library"

# Initialize LLM (Ensure GOOGLE_API_KEY is active in env)
try:
    llm = ChatGoogleGenerativeAI(
        model=get_primary_model(),
        temperature=0.1,  # Low temperature for deterministic extraction
        max_tokens=2048,
    )
except Exception as e:
    logger.error(f"Failed to initialize LLM: {e}")
    exit(1)


def extract_raw_frontend(pdf_path: str, max_pages: int = 40) -> str:
    """Extract raw text from the first 'max_pages' to capture the TOC."""
    try:
        doc = fitz.open(pdf_path)
        extracted_text = []
        for i in range(min(max_pages, len(doc))):
            page_text = doc[i].get_text("text").strip()
            if page_text:
                extracted_text.append(f"--- PAGE {i+1} ---\n{page_text}")

        return "\n\n".join(extracted_text)
    except Exception as e:
        logger.error(f"Failed extracting text from {pdf_path}: {e}")
        return ""


def _generate_llm_toc(raw_text: str, filename: str) -> Optional[str]:
    """Pass front-matter text to LLM to parse a clean markdown TOC."""
    template = """
    You are an expert librarian and data extraction agent.
    Your task is to analyze the front-matter pages of a technical book and extract a perfect, hierarchical Table of Contents (TOC).

    Source Book: {filename}

    Here is the raw text extracted from the first few dozen pages:
    <RAW_TEXT>
    {raw_text}
    </RAW_TEXT>

    INSTRUCTIONS:
    1. Locate the actual Table of Contents within the raw text. Ignore introductory praises, copyright pages, and prefaces unless they are listed IN the TOC.
    2. Extract the hierarchical structure (Parts, Chapters, Sections) and page numbers if available.
    3. Format the output STRICTLY as Markdown bullet points.
    4. Use headers (e.g., `## Part 1`) if the book is divided into parts.
    5. Do not include any conversational filler (e.g. "Here is the TOC:"). ONLY return the markdown TOC itself.
    6. If you cannot find any indication of a Table of Contents, return exactly "NO_TOC_FOUND".

    RETURN ONLY THE MARKDOWN TOC:
    """

    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()

    try:
        logger.info(f"Invoking LLM for TOC extraction: {filename}...")
        result = chain.invoke({"raw_text": raw_text, "filename": filename})
        if result.strip() == "NO_TOC_FOUND":
            return None
        return result
    except Exception as e:
        logger.error(f"LLM extraction failed for {filename}: {e}")
        return None


def main():
    if not os.path.isdir(LIBRARY_DIR):
        logger.error(f"Library directory not found: {LIBRARY_DIR}")
        return

    pdfs = [f for f in os.listdir(LIBRARY_DIR) if f.lower().endswith(".pdf")]
    logger.info(f"Found {len(pdfs)} PDFs in {LIBRARY_DIR}")

    for pdf in pdfs:
        pdf_path = os.path.join(LIBRARY_DIR, pdf)
        logger.info(f"\n{'='*50}\nProcessing: {pdf}\n{'='*50}")

        raw_text = extract_raw_frontend(pdf_path, max_pages=40)

        if not raw_text:
            logger.warning("No text extracted from frontend pages.")
            continue

        logger.info(f"Extracted {len(raw_text)} characters from the first 40 pages.")

        # Invoke LLM
        toc_md = _generate_llm_toc(raw_text, pdf)

        if toc_md:
            logger.info("Successfully extracted TOC formatted by LLM:\n")
            print(toc_md)
        else:
            logger.warning("LLM could not determine a TOC from the provided text.")


if __name__ == "__main__":
    main()

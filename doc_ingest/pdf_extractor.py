"""PDF text extraction using pdfplumber.

Provides two entry points:
- extract_pdf_text: whole-document text, normalized and whitespace-cleaned,
  ready to hand to a text splitter before embedding.
- extract_pdf_pages: per-page text, useful when the caller wants to keep
  page-number metadata attached to each chunk (e.g. for citing "page 3"
  in a RAG answer).

Design note: this module intentionally exposes a narrow, typed surface
(list[str] / list[PageText]) rather than leaking pdfplumber's internal
Page objects, so the rest of the ingestion pipeline does not depend on
which PDF library is used underneath.
"""

from dataclasses import dataclass
import re

import pdfplumber


class PdfExtractionError(Exception):
    """Raised when a PDF cannot be opened or contains no extractable text."""


@dataclass
class PageText:
    page_number: int  # 1-indexed, matches how a human would cite the page
    text: str


def _normalize_whitespace(text: str) -> str:
    # Collapse repeated blank lines and trailing spaces left behind by
    # column-based PDF layouts, without destroying paragraph breaks.
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf_pages(path: str) -> list[PageText]:
    """Return one PageText entry per page, in document order.

    Pages with no extractable text (e.g. a scanned image page with no
    OCR layer) are still returned, with text="" — callers decide whether
    to skip them, rather than this function silently dropping pages and
    shifting page numbers.
    """
    pages: list[PageText] = []
    try:
        with pdfplumber.open(path) as pdf:
            if len(pdf.pages) == 0:
                raise PdfExtractionError(f"{path}: PDF has zero pages")
            for i, page in enumerate(pdf.pages, start=1):
                raw = page.extract_text() or ""
                pages.append(PageText(page_number=i, text=_normalize_whitespace(raw)))
    except PdfExtractionError:
        raise
    except Exception as exc:  # pdfplumber/pdfminer raise several exception types
        raise PdfExtractionError(f"{path}: could not open or parse PDF ({exc})") from exc

    return pages


def extract_pdf_text(path: str) -> str:
    """Return the whole document as a single normalized text blob."""
    pages = extract_pdf_pages(path)
    non_empty = [p.text for p in pages if p.text]
    if not non_empty:
        raise PdfExtractionError(f"{path}: no extractable text on any page")
    return "\n\n".join(non_empty)

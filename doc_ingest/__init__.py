"""Document preprocessing utilities for the RAG agent ingestion pipeline.

Extracts clean, chunk-ready text from heterogeneous source documents
(PDF reports, HTML pages) before they are embedded and indexed in FAISS.
"""

from .pdf_extractor import extract_pdf_text, extract_pdf_pages
from .html_extractor import extract_html_text, extract_html_links

__all__ = [
    "extract_pdf_text",
    "extract_pdf_pages",
    "extract_html_text",
    "extract_html_links",
]

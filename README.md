# rag-document-preprocessing

Document preprocessing utilities for a RAG ingestion pipeline: extracts
clean, chunk-ready text from PDF and HTML source documents before they are
embedded and indexed (e.g. into the FAISS index used by
[rag-tool-agent-demo](https://github.com/SantoshpHiremath/rag-tool-agent-demo)).

## Why

Real source documents are messy before they're useful to a RAG agent:
PDFs need per-page text extraction (with page numbers preserved so the
agent can cite "page 3"), and HTML pages carry nav bars, footers, and
`<script>` tags that pollute embeddings if you don't strip them first.
This module is the preprocessing step that sits before the text splitter
and embedder.

## What's here

- `doc_ingest/pdf_extractor.py` — `extract_pdf_pages()` (per-page text with
  page numbers) and `extract_pdf_text()` (whole-document text), built on
  [pdfplumber](https://github.com/jsvine/pdfplumber). Whitespace is
  normalized; pages with no extractable text (e.g. scanned images with no
  OCR layer) are returned as empty rather than silently dropped, so page
  numbers never shift.
- `doc_ingest/html_extractor.py` — `extract_html_text()` (visible article
  text, with `<script>`/`<style>`/`<nav>`/`<footer>`/`<aside>` stripped)
  and `extract_html_links()` (all content links, with relative URLs
  resolved against a base URL), built on BeautifulSoup.
- `tests/` — 18 tests run against real fixture files (a generated
  multi-page PDF, a realistic HTML knowledge-base article), not mocks.
- `sample_data/` — the fixtures themselves, plus the generator script used
  to build the sample PDF.
- `ingest_demo.py` — a small end-to-end script that runs both extractors
  against the sample files and prints what a downstream splitter/embedder
  would receive.

## Why pdfplumber instead of PyMuPDF

This was originally scoped against PyMuPDF (`fitz`), but the build
environment used to develop this had no PyPI access, so PyMuPDF couldn't
be installed or tested. pdfplumber was already available and is a
comparable, widely-used PDF text-extraction library, so it's used here
instead — named accurately rather than claiming a library that was never
actually run. Swapping the PDF backend later would only touch
`pdf_extractor.py`; the rest of the pipeline is unaffected.

## Setup

```bash
pip install -r requirements.txt
```

## Running the tests

```bash
pytest tests/ -v
```

All 18 tests pass against the real sample fixtures in `sample_data/`.

## Running the demo

```bash
python3 ingest_demo.py
```

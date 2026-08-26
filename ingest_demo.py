"""Small end-to-end demo: run the real extractors against the real sample
files and print what a RAG ingestion pipeline would hand to its text
splitter / embedder next.

Usage:
    python3 ingest_demo.py
"""

from doc_ingest import extract_pdf_pages, extract_html_text, extract_html_links

PDF_PATH = "sample_data/sample_report.pdf"
HTML_PATH = "sample_data/sample_kb_page.html"


def main() -> None:
    print("=== PDF ingestion ===")
    pages = extract_pdf_pages(PDF_PATH)
    print(f"{PDF_PATH}: {len(pages)} pages extracted")
    for page in pages:
        preview = page.text.splitlines()[0] if page.text else "(empty)"
        print(f"  page {page.page_number}: {len(page.text)} chars — \"{preview}\"")

    print("\n=== HTML ingestion ===")
    with open(HTML_PATH, encoding="utf-8") as f:
        html = f.read()
    text = extract_html_text(html)
    links = extract_html_links(html, base_url="https://internal.example.com/kb/articles/sf-codes")
    print(f"{HTML_PATH}: {len(text)} chars of clean text, {len(links)} content links found")
    for link in links:
        print(f"  -> {link.text}: {link.url}")


if __name__ == "__main__":
    main()

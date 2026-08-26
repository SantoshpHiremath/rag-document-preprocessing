"""HTML text and link extraction using BeautifulSoup.

Used for ingesting web-published documentation (e.g. a knowledge-base
article or internal wiki export) into the same pipeline that feeds the
RAG agent's FAISS index.
"""

import re
from dataclasses import dataclass
from urllib.parse import urljoin

from bs4 import BeautifulSoup

# Tags whose content is not human-readable article text and should never
# be embedded into the index (script/style are the obvious ones; nav/
# footer/aside are stripped too so boilerplate site chrome doesn't pollute
# retrieval results).
_NON_CONTENT_TAGS = ["script", "style", "nav", "footer", "aside", "noscript"]


class HtmlExtractionError(Exception):
    """Raised when the given HTML has no parseable content."""


@dataclass
class Link:
    text: str
    url: str


def _clean_soup(html: str) -> BeautifulSoup:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(_NON_CONTENT_TAGS):
        tag.decompose()
    return soup


def extract_html_text(html: str) -> str:
    """Return the visible text content of an HTML document, whitespace-normalized."""
    if not html or not html.strip():
        raise HtmlExtractionError("empty HTML input")

    soup = _clean_soup(html)
    text = soup.get_text(separator="\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    text = text.strip()

    if not text:
        raise HtmlExtractionError("no visible text found in HTML")
    return text


def extract_html_links(html: str, base_url: str | None = None) -> list[Link]:
    """Return all <a href> links, with anchor text, in document order.

    If base_url is given, relative hrefs (e.g. "/docs/page2") are resolved
    to absolute URLs so downstream crawling/citation logic doesn't have to
    special-case relative links.
    """
    soup = _clean_soup(html)
    links: list[Link] = []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href or href.startswith("#"):
            continue
        if base_url:
            href = urljoin(base_url, href)
        anchor_text = a.get_text(strip=True)
        links.append(Link(text=anchor_text, url=href))
    return links

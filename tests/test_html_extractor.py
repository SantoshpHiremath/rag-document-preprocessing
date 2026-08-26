import os

import pytest

from doc_ingest.html_extractor import extract_html_text, extract_html_links, HtmlExtractionError

SAMPLE_HTML_PATH = os.path.join(os.path.dirname(__file__), "..", "sample_data", "sample_kb_page.html")


def _load_sample_html() -> str:
    with open(SAMPLE_HTML_PATH, encoding="utf-8") as f:
        return f.read()


class TestExtractHtmlText:
    def test_extracts_visible_article_text(self):
        text = extract_html_text(_load_sample_html())
        assert "Signal Fault Codes" in text
        assert "Loss of Communication" in text
        assert "Battery Voltage Low" in text

    def test_strips_script_content(self):
        text = extract_html_text(_load_sample_html())
        assert "tracking pixel init" not in text

    def test_strips_nav_and_footer_boilerplate(self):
        text = extract_html_text(_load_sample_html())
        assert "Search" not in text  # nav link text
        assert "Internal Knowledge Base" not in text  # footer copyright text

    def test_empty_input_raises(self):
        with pytest.raises(HtmlExtractionError):
            extract_html_text("")

    def test_whitespace_only_input_raises(self):
        with pytest.raises(HtmlExtractionError):
            extract_html_text("   \n   ")


class TestExtractHtmlLinks:
    def test_finds_all_content_links(self):
        links = extract_html_links(_load_sample_html())
        urls = [l.url for l in links]
        assert "/kb/articles/heartbeat-timeout" in urls
        assert "https://kb.example.com/articles/battery-replacement" in urls

    def test_skips_nav_links_since_nav_is_stripped(self):
        links = extract_html_links(_load_sample_html())
        urls = [l.url for l in links]
        assert "/kb/home" not in urls
        assert "/kb/search" not in urls

    def test_anchor_text_captured(self):
        links = extract_html_links(_load_sample_html())
        by_url = {l.url: l.text for l in links}
        assert by_url["/kb/articles/heartbeat-timeout"] == "heartbeat timeout guide"

    def test_relative_links_resolved_against_base_url(self):
        links = extract_html_links(_load_sample_html(), base_url="https://internal.example.com/kb/articles/sf-codes")
        by_text = {l.text: l.url for l in links}
        assert by_text["heartbeat timeout guide"] == "https://internal.example.com/kb/articles/heartbeat-timeout"

    def test_skips_bare_fragment_links(self):
        html = '<html><body><a href="#top">Back to top</a><a href="/real">Real link</a></body></html>'
        links = extract_html_links(html)
        assert len(links) == 1
        assert links[0].url == "/real"

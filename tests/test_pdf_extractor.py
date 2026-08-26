import os

import pytest

from doc_ingest.pdf_extractor import extract_pdf_text, extract_pdf_pages, PdfExtractionError

SAMPLE_PDF = os.path.join(os.path.dirname(__file__), "..", "sample_data", "sample_report.pdf")


class TestExtractPdfPages:
    def test_returns_one_entry_per_page(self):
        pages = extract_pdf_pages(SAMPLE_PDF)
        assert len(pages) == 3

    def test_page_numbers_are_1_indexed_in_order(self):
        pages = extract_pdf_pages(SAMPLE_PDF)
        assert [p.page_number for p in pages] == [1, 2, 3]

    def test_page_content_matches_expected_section(self):
        pages = extract_pdf_pages(SAMPLE_PDF)
        assert "Track Inspection Summary" in pages[0].text
        assert "Sensor Readings" in pages[1].text
        assert "Recommendations" in pages[2].text

    def test_specific_data_point_extracted_correctly(self):
        pages = extract_pdf_pages(SAMPLE_PDF)
        assert "4.7 mm/s" in pages[1].text

    def test_nonexistent_file_raises_extraction_error(self):
        with pytest.raises(PdfExtractionError):
            extract_pdf_pages("/tmp/does_not_exist_at_all.pdf")


class TestExtractPdfText:
    def test_returns_single_string_with_all_pages(self):
        text = extract_pdf_text(SAMPLE_PDF)
        assert "Track Inspection Summary" in text
        assert "Sensor Readings" in text
        assert "Recommendations" in text

    def test_whitespace_is_normalized_no_triple_newlines(self):
        text = extract_pdf_text(SAMPLE_PDF)
        assert "\n\n\n" not in text

    def test_pages_joined_in_correct_order(self):
        text = extract_pdf_text(SAMPLE_PDF)
        # Section 1 content must appear before Section 3 content
        assert text.index("Track Inspection") < text.index("Recommendations")

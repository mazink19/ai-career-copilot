from pathlib import Path

from app.ai.extraction.pdf_extractior import PDFExtractor


def test_extract_pdf_text():
    extractor = PDFExtractor()

    pdf_path = Path("tests/files/test_resume.pdf")

    text = extractor.extract(str(pdf_path))

    assert text
    assert isinstance(text, str)
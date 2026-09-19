from pathlib import Path

from pypdf import PdfWriter

from app.knowledge.loaders import PDFDocumentLoader
from app.knowledge.models import DocumentType


def create_test_pdf(path: Path) -> None:
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)

    with path.open("wb") as file:
        writer.write(file)


def test_pdf_loader(tmp_path: Path):
    pdf_file = tmp_path / "architecture.pdf"
    create_test_pdf(pdf_file)

    loader = PDFDocumentLoader()
    document = loader.load(pdf_file)

    assert document.title == "architecture"
    assert document.document_type == DocumentType.ARCHITECTURE
    assert document.source == str(pdf_file)
    assert document.metadata["page_count"] == 1


def test_pdf_loader_rejects_non_pdf(tmp_path: Path):
    text_file = tmp_path / "test.txt"
    text_file.write_text("hello", encoding="utf-8")

    loader = PDFDocumentLoader()

    try:
        loader.load(text_file)
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "Unsupported file type" in str(exc)
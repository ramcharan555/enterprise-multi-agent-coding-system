from pathlib import Path

from app.knowledge.loaders import TextDocumentLoader
from app.knowledge.models import DocumentType


def test_markdown_document_loading(tmp_path: Path):
    document_file = tmp_path / "README.md"

    document_file.write_text(
        "# API Guide\n\nNew APIs must use versioning.",
        encoding="utf-8",
    )

    loader = TextDocumentLoader()
    document = loader.load(document_file)

    assert document.title == "README"
    assert document.document_type == DocumentType.README
    assert "New APIs must use versioning." in document.content
    assert document.source == str(document_file)


def test_architecture_document_detection(tmp_path: Path):
    document_file = tmp_path / "architecture.md"

    document_file.write_text(
        "# Architecture\n\nUse the API gateway.",
        encoding="utf-8",
    )

    loader = TextDocumentLoader()
    document = loader.load(document_file)

    assert document.document_type == DocumentType.ARCHITECTURE


def test_unsupported_file_type(tmp_path: Path):
    document_file = tmp_path / "image.png"
    document_file.write_bytes(b"fake image")

    loader = TextDocumentLoader()

    try:
        loader.load(document_file)
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "Unsupported file type" in str(exc)
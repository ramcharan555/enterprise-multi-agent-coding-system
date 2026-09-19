from pathlib import Path

import pytest

from app.knowledge.ingestion import DocumentIngestionPipeline
from app.knowledge.models import DocumentType


def test_ingestion_pipeline_loads_markdown(tmp_path: Path):
    file = tmp_path / "README.md"

    file.write_text(
        "# Project Guide\n\nThis is documentation.",
        encoding="utf-8",
    )

    pipeline = DocumentIngestionPipeline()
    document = pipeline.ingest(file)

    assert document.title == "README"
    assert document.document_type == DocumentType.README
    assert "This is documentation." in document.content


def test_ingestion_pipeline_loads_html(tmp_path: Path):
    file = tmp_path / "api.html"

    file.write_text(
        """
        <html>
            <head>
                <title>API Guide</title>
            </head>
            <body>
                <h1>API</h1>
                <p>Use versioning.</p>
            </body>
        </html>
        """,
        encoding="utf-8",
    )

    pipeline = DocumentIngestionPipeline()
    document = pipeline.ingest(file)

    assert document.title == "API Guide"
    assert "Use versioning." in document.content


def test_ingestion_pipeline_rejects_unsupported_file(tmp_path: Path):
    file = tmp_path / "image.png"
    file.write_bytes(b"fake")

    pipeline = DocumentIngestionPipeline()

    with pytest.raises(ValueError, match="Unsupported document type"):
        pipeline.ingest(file)


def test_ingestion_pipeline_rejects_missing_file(tmp_path: Path):
    file = tmp_path / "missing.md"

    pipeline = DocumentIngestionPipeline()

    with pytest.raises(FileNotFoundError):
        pipeline.ingest(file)
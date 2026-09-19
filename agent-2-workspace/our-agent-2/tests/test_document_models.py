from app.knowledge.models import Document, DocumentChunk, DocumentType


def test_document_creation():
    document = Document(
        document_id="doc-001",
        title="API Architecture Guide",
        content="New APIs must use versioning.",
        source="docs/api.md",
        document_type=DocumentType.ARCHITECTURE,
    )

    assert document.document_id == "doc-001"
    assert document.title == "API Architecture Guide"
    assert document.document_type == DocumentType.ARCHITECTURE


def test_document_chunk_creation():
    chunk = DocumentChunk(
        chunk_id="chunk-001",
        document_id="doc-001",
        content="New APIs must use versioning.",
        title="API Architecture Guide",
        section="API Versioning",
        chunk_index=0,
    )

    assert chunk.document_id == "doc-001"
    assert chunk.section == "API Versioning"
    assert chunk.chunk_index == 0
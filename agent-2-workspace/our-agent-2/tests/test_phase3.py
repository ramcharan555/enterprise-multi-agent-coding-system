from app.knowledge.chunking.chunker import DocumentChunker
from app.knowledge.models import Document, DocumentType
from app.knowledge.parsers.section_parser import (
    MarkdownSectionParser,
)
from app.knowledge.relationships.document_relationships import (
    DocumentRelationshipStore,
)
from app.knowledge.retrieval.embeddings import (
    HashEmbeddingProvider,
)
from app.knowledge.retrieval.vector_index import VectorIndex


def create_document() -> Document:
    return Document(
        document_id="doc-001",
        title="API Architecture",
        content=(
            "# API Architecture\n\n"
            "## Authentication\n\n"
            "Use OAuth2 for authentication.\n\n"
            "## Versioning\n\n"
            "All public APIs must be versioned."
        ),
        source="architecture.md",
        document_type=DocumentType.ARCHITECTURE,
        version="1.0",
        authority="architecture-team",
        scope="public-api",
    )


def test_section_parser():
    document = create_document()

    parser = MarkdownSectionParser()
    sections = parser.parse(document.content)

    assert len(sections) == 3
    assert sections[0].title == "API Architecture"
    assert sections[1].title == "Authentication"
    assert sections[2].title == "Versioning"


def test_chunker_preserves_section_information():
    document = create_document()

    parser = MarkdownSectionParser()
    sections = parser.parse(document.content)

    chunker = DocumentChunker(
        max_characters=100,
        overlap=20,
    )

    chunks = chunker.chunk(
        document,
        sections,
    )

    assert len(chunks) >= 2

    assert any(
        chunk.section == "Authentication"
        for chunk in chunks
    )

    assert any(
        chunk.section == "Versioning"
        for chunk in chunks
    )


def test_chunk_metadata():
    document = create_document()

    parser = MarkdownSectionParser()
    sections = parser.parse(document.content)

    chunker = DocumentChunker()
    chunks = chunker.chunk(
        document,
        sections,
    )

    chunk = chunks[0]

    assert chunk.metadata["source"] == "architecture.md"
    assert (
        chunk.metadata["document_type"]
        == DocumentType.ARCHITECTURE
    )
    assert "section_level" in chunk.metadata


def test_document_relationships():
    store = DocumentRelationshipStore()

    relationship = store.add(
        "doc-001",
        "doc-002",
        "references",
    )

    assert relationship.source_document_id == "doc-001"
    assert relationship.target_document_id == "doc-002"

    related = store.find_related("doc-001")

    assert len(related) == 1
    assert related[0].relationship_type == "references"


def test_embedding_provider():
    provider = HashEmbeddingProvider(
        dimensions=64
    )

    vector = provider.embed(
        "OAuth2 authentication"
    )

    assert len(vector) == 64


def test_vector_index():
    document = create_document()

    parser = MarkdownSectionParser()
    sections = parser.parse(document.content)

    chunker = DocumentChunker()
    chunks = chunker.chunk(
        document,
        sections,
    )

    provider = HashEmbeddingProvider(
        dimensions=64
    )

    index = VectorIndex(provider)
    index.add_many(chunks)

    results = index.search(
        "OAuth2 authentication",
        top_k=2,
    )

    assert len(results) == 2
    assert results[0][0].document_id == "doc-001"


def test_vector_index_empty_query_results():
    provider = HashEmbeddingProvider(
        dimensions=32
    )

    index = VectorIndex(provider)

    assert index.search(
        "anything",
        top_k=5,
    ) == []
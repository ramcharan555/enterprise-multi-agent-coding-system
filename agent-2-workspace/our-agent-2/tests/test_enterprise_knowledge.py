from app.knowledge.enterprise import (
    ConflictDetector,
    EnterpriseMetadata,
    EnterpriseRetriever,
    MetadataFilter,
    authority_score,
    filter_by_scope,
)
from app.knowledge.models import (
    Document,
    DocumentType,
)
from app.knowledge.chunking.chunker import DocumentChunker
from app.knowledge.parsers.section_parser import (
    MarkdownSectionParser,
)
from app.knowledge.retrieval.embeddings import (
    HashEmbeddingProvider,
)


def create_chunks():
    document = Document(
        document_id="enterprise-001",
        title="API Architecture",
        content=(
            "# API Architecture\n\n"
            "## Authentication\n\n"
            "Use OAuth2 for all public APIs.\n\n"
            "## Versioning\n\n"
            "Use semantic versioning."
        ),
        source="architecture.md",
        document_type=DocumentType.ARCHITECTURE,
    )

    parser = MarkdownSectionParser()

    sections = parser.parse(
        document.content
    )

    chunker = DocumentChunker()

    chunks = chunker.chunk(
        document,
        sections,
    )

    for chunk in chunks:
        chunk.metadata["authority"] = (
            "architecture-team"
        )
        chunk.metadata["scope"] = "public-api"
        chunk.metadata["priority"] = 100

    return chunks


def test_enterprise_metadata():
    metadata = EnterpriseMetadata(
        version="2.0",
        authority="architecture-team",
        scope="public-api",
        priority=100,
    )

    assert metadata.version == "2.0"
    assert metadata.authority == "architecture-team"
    assert metadata.is_active() is True


def test_metadata_filter():
    chunks = create_chunks()

    result = MetadataFilter().apply(
        chunks,
        {
            "scope": "public-api",
        },
    )

    assert len(result) == len(chunks)


def test_scope_filter():
    chunks = create_chunks()

    result = filter_by_scope(
        chunks,
        "public-api",
    )

    assert len(result) == len(chunks)


def test_authority_score():
    chunks = create_chunks()

    assert authority_score(
        chunks[0]
    ) == 100


def test_enterprise_retrieval():
    chunks = create_chunks()

    retriever = EnterpriseRetriever(
        HashEmbeddingProvider(
            dimensions=64
        )
    )

    retriever.add_many(chunks)

    results = retriever.search(
        "OAuth2 authentication",
        top_k=2,
        scope="public-api",
    )

    assert len(results) > 0
    assert results[0][0].metadata[
        "scope"
    ] == "public-api"


def test_conflict_detection():
    chunks = create_chunks()

    first = chunks[0]

    from copy import deepcopy

    second = deepcopy(first)
    second.chunk_id = "conflict-001"
    second.content = (
        "Use API keys instead of OAuth2."
    )

    conflicts = ConflictDetector().detect(
        [first, second]
    )

    assert len(conflicts) == 1
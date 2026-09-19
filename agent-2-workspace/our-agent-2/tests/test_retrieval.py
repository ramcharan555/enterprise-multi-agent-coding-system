from app.knowledge.models import Document, DocumentType
from app.knowledge.chunking.chunker import DocumentChunker
from app.knowledge.parsers.section_parser import (
    MarkdownSectionParser,
)
from app.knowledge.retrieval.embeddings import (
    HashEmbeddingProvider,
)
from app.knowledge.retrieval.evidence import (
    create_evidence,
)
from app.knowledge.retrieval.hybrid import HybridRetriever
from app.knowledge.retrieval.keyword import KeywordRetriever
from app.knowledge.retrieval.query import SearchQuery


def create_chunks():
    document = Document(
        document_id="doc-001",
        title="API Architecture",
        content=(
            "# API Architecture\n\n"
            "## Authentication\n\n"
            "APIs use OAuth2 authentication.\n\n"
            "## Versioning\n\n"
            "All APIs require semantic versioning."
        ),
        source="architecture.md",
        document_type=DocumentType.ARCHITECTURE,
    )

    parser = MarkdownSectionParser()
    sections = parser.parse(document.content)

    chunker = DocumentChunker(
        max_characters=500,
        overlap=50,
    )

    return chunker.chunk(
        document,
        sections,
    )


def test_query_parsing():
    query = SearchQuery.parse(
        "How should API authentication use OAuth2?"
    )

    assert "api" in query.terms
    assert "authentication" in query.terms
    assert "oauth2" in query.terms


def test_keyword_retrieval():
    chunks = create_chunks()

    retriever = KeywordRetriever()

    results = retriever.search(
        SearchQuery.parse("OAuth2 authentication"),
        chunks,
        top_k=2,
    )

    assert len(results) >= 1
    assert "OAuth2" in results[0][0].content


def test_hybrid_retrieval():
    chunks = create_chunks()

    provider = HashEmbeddingProvider(
        dimensions=64
    )

    retriever = HybridRetriever(provider)

    retriever.add_many(chunks)

    results = retriever.search(
        "OAuth2 authentication",
        top_k=2,
    )

    assert len(results) == 2
    assert all(
        score >= 0
        for _, score in results
    )


def test_evidence_creation():
    chunks = create_chunks()

    evidence = create_evidence(
        chunks[0],
        0.95,
    )

    assert evidence.chunk_id == chunks[0].chunk_id
    assert evidence.document_id == "doc-001"
    assert evidence.source == "architecture.md"
    assert evidence.score == 0.95
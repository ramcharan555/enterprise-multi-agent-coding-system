from app.knowledge.agent import KnowledgeAgent
from app.knowledge.chunking.chunker import DocumentChunker
from app.knowledge.models import (
    Document,
    DocumentType,
)
from app.knowledge.parsers.section_parser import (
    MarkdownSectionParser,
)
from app.knowledge.retrieval.embeddings import (
    HashEmbeddingProvider,
)


def create_chunks():
    document = Document(
        document_id="architecture-001",
        title="API Architecture",
        content=(
            "# API Architecture\n\n"
            "## Authentication\n\n"
            "All APIs must use OAuth2 authentication.\n\n"
            "## Versioning\n\n"
            "Public APIs must use semantic versioning."
        ),
        source="architecture.md",
        document_type=DocumentType.ARCHITECTURE,
    )

    parser = MarkdownSectionParser()

    sections = parser.parse(
        document.content
    )

    chunker = DocumentChunker(
        max_characters=500,
        overlap=50,
    )

    return chunker.chunk(
        document,
        sections,
    )


def test_knowledge_agent_end_to_end():
    agent = KnowledgeAgent(
        HashEmbeddingProvider(
            dimensions=64
        )
    )

    chunks = create_chunks()

    agent.add_document_chunks(chunks)

    response = agent.ask(
        "How should API authentication work?",
        top_k=2,
    )

    assert response.answer.grounded is True
    assert response.answer.confidence >= 0.0
    assert len(response.evidence) > 0
    assert len(response.citations) > 0


def test_knowledge_agent_returns_grounded_answer():
    agent = KnowledgeAgent(
        HashEmbeddingProvider(
            dimensions=64
        )
    )

    agent.add_document_chunks(
        create_chunks()
    )

    response = agent.ask(
        "OAuth2 authentication",
        top_k=1,
    )

    assert "OAuth2" in response.answer.answer
    assert "architecture.md" in response.answer.citations[0]


def test_empty_knowledge_base():
    agent = KnowledgeAgent(
        HashEmbeddingProvider(
            dimensions=64
        )
    )

    response = agent.ask(
        "How should authentication work?"
    )

    assert response.answer.grounded is False
    assert response.answer.confidence == 0.0
    assert response.citations == []
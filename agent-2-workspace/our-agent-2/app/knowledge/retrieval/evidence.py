from dataclasses import dataclass

from app.knowledge.models import DocumentChunk


@dataclass
class Evidence:
    chunk_id: str
    document_id: str
    source: str
    title: str
    section: str
    content: str
    score: float


def create_evidence(
    chunk: DocumentChunk,
    score: float,
) -> Evidence:
    return Evidence(
        chunk_id=chunk.chunk_id,
        document_id=chunk.document_id,
        source=chunk.metadata.get(
            "source",
            "",
        ),
        title=chunk.title,
        section=chunk.section,
        content=chunk.content,
        score=score,
    )
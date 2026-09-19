from typing import List

from app.knowledge.models import Document, DocumentChunk
from app.knowledge.parsers.section_parser import DocumentSection


class DocumentChunker:
    """Create retrievable chunks while preserving section context."""

    def __init__(
        self,
        max_characters: int = 1200,
        overlap: int = 150,
    ) -> None:
        if max_characters <= 0:
            raise ValueError("max_characters must be positive")

        if overlap < 0 or overlap >= max_characters:
            raise ValueError(
                "overlap must be >= 0 and smaller than max_characters"
            )

        self.max_characters = max_characters
        self.overlap = overlap

    def chunk(
        self,
        document: Document,
        sections: List[DocumentSection],
    ) -> List[DocumentChunk]:
        chunks: List[DocumentChunk] = []
        chunk_index = 0

        for section in sections:
            text = section.content.strip()

            if not text:
                continue

            start = 0

            while start < len(text):
                end = min(
                    start + self.max_characters,
                    len(text),
                )

                content = text[start:end].strip()

                if content:
                    chunks.append(
                        DocumentChunk(
                            chunk_id=(
                                f"{document.document_id}"
                                f":chunk:{chunk_index}"
                            ),
                            document_id=document.document_id,
                            content=content,
                            title=document.title,
                            section=section.title,
                            chunk_index=chunk_index,
                            metadata={
                                "section_level": section.level,
                                "source": document.source,
                                "document_type": document.document_type,
                            },
                        )
                    )

                    chunk_index += 1

                if end >= len(text):
                    break

                start = end - self.overlap

        return chunks
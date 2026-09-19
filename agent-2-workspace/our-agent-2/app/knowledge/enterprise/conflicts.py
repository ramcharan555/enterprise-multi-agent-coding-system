from dataclasses import dataclass
from typing import List

from app.knowledge.models import DocumentChunk


@dataclass
class DocumentConflict:
    topic: str
    chunks: List[DocumentChunk]


class ConflictDetector:
    """
    Detect potentially conflicting chunks.

    Initial implementation uses shared section/topic names
    and different content. A semantic conflict detector can
    replace this later.
    """

    def detect(
        self,
        chunks: List[DocumentChunk],
    ) -> List[DocumentConflict]:
        grouped = {}

        for chunk in chunks:
            key = (
                chunk.section.lower().strip()
                if chunk.section
                else chunk.title.lower().strip()
            )

            grouped.setdefault(key, []).append(chunk)

        conflicts = []

        for topic, items in grouped.items():
            contents = {
                item.content.strip()
                for item in items
            }

            if len(items) > 1 and len(contents) > 1:
                conflicts.append(
                    DocumentConflict(
                        topic=topic,
                        chunks=items,
                    )
                )

        return conflicts
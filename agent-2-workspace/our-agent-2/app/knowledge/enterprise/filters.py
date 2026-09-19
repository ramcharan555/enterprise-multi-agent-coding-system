from typing import Dict, List

from app.knowledge.models import DocumentChunk


class MetadataFilter:
    """Filter knowledge chunks using enterprise metadata."""

    def apply(
        self,
        chunks: List[DocumentChunk],
        filters: Dict[str, str],
    ) -> List[DocumentChunk]:
        if not filters:
            return chunks

        results = []

        for chunk in chunks:
            metadata = chunk.metadata

            matches = all(
                str(metadata.get(key, "")).lower()
                == str(value).lower()
                for key, value in filters.items()
            )

            if matches:
                results.append(chunk)

        return results
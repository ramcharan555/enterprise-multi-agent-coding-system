from typing import List, Optional

from app.knowledge.models import DocumentChunk


def filter_by_scope(
    chunks: List[DocumentChunk],
    scope: Optional[str],
) -> List[DocumentChunk]:
    if not scope:
        return chunks

    normalized_scope = scope.lower()

    return [
        chunk
        for chunk in chunks
        if str(
            chunk.metadata.get("scope", "")
        ).lower()
        == normalized_scope
    ]
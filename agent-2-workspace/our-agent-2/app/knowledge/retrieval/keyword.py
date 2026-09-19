from typing import List, Tuple

from app.knowledge.models import DocumentChunk
from app.knowledge.retrieval.query import SearchQuery


class KeywordRetriever:
    """Simple lexical retrieval over document chunks."""

    def search(
        self,
        query: SearchQuery,
        chunks: List[DocumentChunk],
        top_k: int = 5,
    ) -> List[Tuple[DocumentChunk, float]]:
        if top_k <= 0:
            return []

        results = []

        for chunk in chunks:
            text = (
                f"{chunk.title} "
                f"{chunk.section} "
                f"{chunk.content}"
            ).lower()

            score = sum(
                text.count(term)
                for term in query.terms
            )

            if score > 0:
                results.append((chunk, float(score)))

        results.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        return results[:top_k]
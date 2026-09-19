import math
from typing import List, Tuple

from app.knowledge.models import DocumentChunk
from app.knowledge.retrieval.embeddings import EmbeddingProvider


class VectorIndex:
    """Simple in-memory vector index."""

    def __init__(self, embedding_provider: EmbeddingProvider) -> None:
        self.embedding_provider = embedding_provider
        self._items: List[
            Tuple[DocumentChunk, List[float]]
        ] = []

    def add(self, chunk: DocumentChunk) -> None:
        vector = self.embedding_provider.embed(
            chunk.content
        )

        self._items.append((chunk, vector))

    def add_many(
        self,
        chunks: List[DocumentChunk],
    ) -> None:
        for chunk in chunks:
            self.add(chunk)

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[Tuple[DocumentChunk, float]]:
        if top_k <= 0:
            return []

        query_vector = self.embedding_provider.embed(query)

        scored = [
            (
                chunk,
                self._cosine_similarity(
                    query_vector,
                    vector,
                ),
            )
            for chunk, vector in self._items
        ]

        scored.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        return scored[:top_k]

    @staticmethod
    def _cosine_similarity(
        left: List[float],
        right: List[float],
    ) -> float:
        if len(left) != len(right):
            raise ValueError(
                "Vectors must have the same dimensions"
            )

        dot_product = sum(
            left_value * right_value
            for left_value, right_value in zip(left, right)
        )

        left_norm = math.sqrt(
            sum(value * value for value in left)
        )

        right_norm = math.sqrt(
            sum(value * value for value in right)
        )

        if left_norm == 0 or right_norm == 0:
            return 0.0

        return dot_product / (left_norm * right_norm)
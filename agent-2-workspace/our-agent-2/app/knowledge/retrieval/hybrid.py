from typing import List, Tuple

from app.knowledge.models import DocumentChunk
from app.knowledge.retrieval.embeddings import EmbeddingProvider
from app.knowledge.retrieval.keyword import KeywordRetriever
from app.knowledge.retrieval.query import SearchQuery
from app.knowledge.retrieval.vector_index import VectorIndex


class HybridRetriever:
    """Combines semantic and lexical retrieval."""

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
    ) -> None:
        self.vector_index = VectorIndex(
            embedding_provider
        )
        self.keyword_retriever = KeywordRetriever()
        self._chunks: List[DocumentChunk] = []

    def add(self, chunk: DocumentChunk) -> None:
        self._chunks.append(chunk)
        self.vector_index.add(chunk)

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
        parsed = SearchQuery.parse(query)

        semantic_results = self.vector_index.search(
            query,
            top_k=max(top_k * 2, 10),
        )

        keyword_results = self.keyword_retriever.search(
            parsed,
            self._chunks,
            top_k=max(top_k * 2, 10),
        )

        scores = {}

        for rank, (chunk, _) in enumerate(
            semantic_results,
            start=1,
        ):
            scores.setdefault(chunk.chunk_id, {
                "chunk": chunk,
                "score": 0.0,
            })
            scores[chunk.chunk_id]["score"] += 1.0 / rank

        for rank, (chunk, _) in enumerate(
            keyword_results,
            start=1,
        ):
            scores.setdefault(chunk.chunk_id, {
                "chunk": chunk,
                "score": 0.0,
            })
            scores[chunk.chunk_id]["score"] += 1.0 / rank

        ranked = sorted(
            scores.values(),
            key=lambda item: item["score"],
            reverse=True,
        )

        return [
            (item["chunk"], item["score"])
            for item in ranked[:top_k]
        ]
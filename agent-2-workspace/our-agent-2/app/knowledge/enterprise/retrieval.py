from typing import Dict, List, Optional, Tuple

from app.knowledge.enterprise.authority import (
    authority_score,
    priority_score,
)
from app.knowledge.enterprise.filters import MetadataFilter
from app.knowledge.enterprise.scope import filter_by_scope
from app.knowledge.models import DocumentChunk
from app.knowledge.retrieval.embeddings import EmbeddingProvider
from app.knowledge.retrieval.hybrid import HybridRetriever


class EnterpriseRetriever:
    """Enterprise-aware retrieval layer."""

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
    ) -> None:
        self.retriever = HybridRetriever(
            embedding_provider
        )
        self.filter = MetadataFilter()
        self._chunks: List[DocumentChunk] = []

    def add_many(
        self,
        chunks: List[DocumentChunk],
    ) -> None:
        self._chunks.extend(chunks)
        self.retriever.add_many(chunks)

    def search(
        self,
        query: str,
        top_k: int = 5,
        metadata_filters: Optional[
            Dict[str, str]
        ] = None,
        scope: Optional[str] = None,
    ) -> List[Tuple[DocumentChunk, float]]:
        candidates = self.filter.apply(
            self._chunks,
            metadata_filters or {},
        )

        candidates = filter_by_scope(
            candidates,
            scope,
        )

        if not candidates:
            return []

        # Build a temporary retriever for the filtered set.
        filtered_retriever = HybridRetriever(
            self.retriever.vector_index.embedding_provider
        )

        filtered_retriever.add_many(candidates)

        results = filtered_retriever.search(
            query,
            top_k=max(top_k * 3, 10),
        )

        ranked = []

        for chunk, retrieval_score in results:
            enterprise_bonus = (
                authority_score(chunk) / 1000.0
                + priority_score(chunk) / 1000.0
            )

            final_score = (
                retrieval_score
                + enterprise_bonus
            )

            ranked.append(
                (chunk, final_score)
            )

        ranked.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        return ranked[:top_k]
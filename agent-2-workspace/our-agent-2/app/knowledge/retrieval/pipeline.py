from dataclasses import dataclass
from typing import Any, List, Optional

from app.knowledge.retrieval.reranker import RetrievalReranker


@dataclass
class RetrievalPipelineResult:
    query: str
    results: List[Any]
    expanded_query: str
    total_candidates: int


class RetrievalPipeline:
    """
    Phase 11 orchestration layer.

    Pipeline:
        query
          -> query expansion
          -> retrieval
          -> reranking
          -> diversification
          -> final results
    """

    def __init__(
        self,
        retriever: Any,
        reranker: Optional[RetrievalReranker] = None,
        top_k: int = 5,
        max_per_document: int = 2,
    ):
        self.retriever = retriever
        self.reranker = reranker or RetrievalReranker()
        self.top_k = top_k
        self.max_per_document = max_per_document

    def _expand_query(self, query: str) -> str:
        """
        Use the existing query expansion implementation when available.
        Falls back to the original query.
        """
        try:
            from app.knowledge.retrieval.query_expansion import QueryExpander

            return QueryExpander().expand(query)
        except (ImportError, AttributeError, TypeError):
            return query

    def _retrieve(self, query: str) -> List[Any]:
        """
        Support the retrieval interfaces already used by the project.
        """
        if hasattr(self.retriever, "retrieve"):
            result = self.retriever.retrieve(query)
        elif hasattr(self.retriever, "search"):
            result = self.retriever.search(query)
        else:
            raise TypeError(
                "Retriever must provide either retrieve() or search()."
            )

        if result is None:
            return []

        return list(result)

    def _rerank(self, query: str, candidates: List[Any]) -> List[Any]:
        if not candidates:
            return []

        if hasattr(self.reranker, "rerank"):
            return list(self.reranker.rerank(query, candidates))

        return candidates

    def _document_id(self, item: Any) -> Optional[str]:
        if isinstance(item, dict):
            metadata = item.get("metadata", {}) or {}
            return (
                item.get("document_id")
                or metadata.get("document_id")
                or metadata.get("source")
            )

        metadata = getattr(item, "metadata", {}) or {}

        return (
            getattr(item, "document_id", None)
            or metadata.get("document_id")
            or metadata.get("source")
        )

    def _diversify(self, candidates: List[Any]) -> List[Any]:
        """
        Limit duplicate results from the same document.
        """
        selected = []
        counts = {}

        for candidate in candidates:
            document_id = self._document_id(candidate)

            if document_id is None:
                selected.append(candidate)
                continue

            count = counts.get(document_id, 0)

            if count >= self.max_per_document:
                continue

            selected.append(candidate)
            counts[document_id] = count + 1

            if len(selected) >= self.top_k:
                break

        return selected

    def run(self, query: str) -> RetrievalPipelineResult:
        if not query or not query.strip():
            raise ValueError("query must not be empty")

        query = query.strip()
        expanded_query = self._expand_query(query)

        candidates = self._retrieve(expanded_query)
        reranked = self._rerank(expanded_query, candidates)
        final_results = self._diversify(reranked)

        return RetrievalPipelineResult(
            query=query,
            results=final_results,
            expanded_query=expanded_query,
            total_candidates=len(candidates),
        )

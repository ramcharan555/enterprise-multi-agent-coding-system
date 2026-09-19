from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Sequence


@dataclass
class RetrievalEvaluationCase:
    query: str
    relevant_document_ids: Sequence[str]


@dataclass
class RetrievalEvaluationResult:
    query: str
    retrieved_document_ids: List[str]
    relevant_document_ids: List[str]
    hit: bool
    precision_at_k: float
    recall_at_k: float
    reciprocal_rank: float


class RetrievalEvaluator:
    """Evaluate a retrieval pipeline using standard retrieval metrics."""

    def __init__(self, pipeline: Any):
        self.pipeline = pipeline

    @staticmethod
    def _document_id(item: Any):
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

    @classmethod
    def _ids(cls, results: Iterable[Any]) -> List[str]:
        ids = []

        for item in results:
            document_id = cls._document_id(item)

            if document_id is not None:
                ids.append(str(document_id))

        return ids

    @staticmethod
    def _precision_at_k(
        retrieved: Sequence[str],
        relevant: Sequence[str],
    ) -> float:
        if not retrieved:
            return 0.0

        relevant_set = set(relevant)
        hits = sum(
            1 for item in retrieved
            if item in relevant_set
        )

        return hits / len(retrieved)

    @staticmethod
    def _recall_at_k(
        retrieved: Sequence[str],
        relevant: Sequence[str],
    ) -> float:
        relevant_set = set(relevant)

        if not relevant_set:
            return 1.0

        hits = sum(
            1 for item in retrieved
            if item in relevant_set
        )

        return hits / len(relevant_set)

    @staticmethod
    def _reciprocal_rank(
        retrieved: Sequence[str],
        relevant: Sequence[str],
    ) -> float:
        relevant_set = set(relevant)

        for index, item in enumerate(retrieved, start=1):
            if item in relevant_set:
                return 1.0 / index

        return 0.0

    def evaluate_case(
        self,
        case: RetrievalEvaluationCase,
    ) -> RetrievalEvaluationResult:
        result = self.pipeline.run(case.query)

        retrieved_ids = self._ids(result.results)
        relevant_ids = [str(x) for x in case.relevant_document_ids]

        hit = bool(
            set(retrieved_ids) &
            set(relevant_ids)
        )

        return RetrievalEvaluationResult(
            query=case.query,
            retrieved_document_ids=retrieved_ids,
            relevant_document_ids=relevant_ids,
            hit=hit,
            precision_at_k=self._precision_at_k(
                retrieved_ids,
                relevant_ids,
            ),
            recall_at_k=self._recall_at_k(
                retrieved_ids,
                relevant_ids,
            ),
            reciprocal_rank=self._reciprocal_rank(
                retrieved_ids,
                relevant_ids,
            ),
        )

    def evaluate(
        self,
        cases: Sequence[RetrievalEvaluationCase],
    ) -> Dict[str, Any]:
        results = [
            self.evaluate_case(case)
            for case in cases
        ]

        if not results:
            return {
                "cases": [],
                "count": 0,
                "hit_rate": 0.0,
                "mean_precision_at_k": 0.0,
                "mean_recall_at_k": 0.0,
                "mean_reciprocal_rank": 0.0,
            }

        count = len(results)

        return {
            "cases": results,
            "count": count,
            "hit_rate": (
                sum(result.hit for result in results)
                / count
            ),
            "mean_precision_at_k": (
                sum(
                    result.precision_at_k
                    for result in results
                )
                / count
            ),
            "mean_recall_at_k": (
                sum(
                    result.recall_at_k
                    for result in results
                )
                / count
            ),
            "mean_reciprocal_rank": (
                sum(
                    result.reciprocal_rank
                    for result in results
                )
                / count
            ),
        }

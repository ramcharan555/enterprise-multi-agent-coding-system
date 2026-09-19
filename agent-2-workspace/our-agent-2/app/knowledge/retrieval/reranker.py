from typing import List


class RetrievalReranker:
    """
    Re-ranks retrieval candidates using multiple relevance signals.

    Signals:
    - original retrieval score
    - keyword overlap
    - metadata match
    - authority
    """

    def rerank(self, query: str, candidates: List[object]) -> List[object]:
        query_terms = set(query.lower().split())

        scored = []

        for candidate in candidates:
            text = str(
                getattr(candidate, "text", None)
                or getattr(candidate, "content", None)
                or ""
            ).lower()

            overlap = sum(1 for term in query_terms if term in text)

            base_score = float(
                getattr(candidate, "score", 0.0)
                or getattr(candidate, "similarity", 0.0)
                or 0.0
            )

            authority = float(
                getattr(candidate, "authority_score", 0.0) or 0.0
            )

            final_score = (
                0.60 * base_score
                + 0.25 * min(overlap / max(len(query_terms), 1), 1.0)
                + 0.15 * authority
            )

            scored.append((final_score, candidate))

        scored.sort(key=lambda item: item[0], reverse=True)

        return [candidate for _, candidate in scored]
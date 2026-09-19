from typing import List

from app.knowledge.retrieval.evidence import Evidence


class CitationFormatter:
    """Format evidence references for grounded answers."""

    def format(
        self,
        evidence: List[Evidence],
    ) -> List[str]:
        citations = []

        for index, item in enumerate(
            evidence,
            start=1,
        ):
            citations.append(
                f"[{index}] {item.source}"
                f" — {item.title}"
                f" — {item.section}"
            )

        return citations
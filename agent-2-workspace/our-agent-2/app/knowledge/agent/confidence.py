from typing import List

from app.knowledge.retrieval.evidence import Evidence


def calculate_confidence(
    evidence: List[Evidence],
) -> float:
    if not evidence:
        return 0.0

    scores = sorted(
        (
            max(0.0, min(1.0, item.score))
            for item in evidence
        ),
        reverse=True,
    )

    # Give greater weight to the strongest evidence.
    weights = [
        0.6,
        0.25,
        0.1,
        0.05,
    ]

    weighted_score = 0.0
    total_weight = 0.0

    for score, weight in zip(
        scores,
        weights,
    ):
        weighted_score += score * weight
        total_weight += weight

    if total_weight == 0:
        return 0.0

    return weighted_score / total_weight
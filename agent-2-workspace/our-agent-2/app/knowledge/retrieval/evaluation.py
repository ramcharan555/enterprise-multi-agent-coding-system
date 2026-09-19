from typing import Iterable, List, Sequence


def hit_rate(
    retrieved: Sequence[str],
    relevant: Iterable[str],
) -> float:
    relevant_set = set(relevant)

    if not relevant_set:
        return 0.0

    return 1.0 if any(item in relevant_set for item in retrieved) else 0.0


def precision_at_k(
    retrieved: Sequence[str],
    relevant: Iterable[str],
    k: int,
) -> float:
    relevant_set = set(relevant)

    if k <= 0:
        return 0.0

    results = list(retrieved[:k])

    if not results:
        return 0.0

    matches = sum(item in relevant_set for item in results)

    return matches / len(results)


def recall_at_k(
    retrieved: Sequence[str],
    relevant: Iterable[str],
    k: int,
) -> float:
    relevant_set = set(relevant)

    if not relevant_set:
        return 0.0

    results = set(retrieved[:k])

    return len(results & relevant_set) / len(relevant_set)


def reciprocal_rank(
    retrieved: Sequence[str],
    relevant: Iterable[str],
) -> float:
    relevant_set = set(relevant)

    for index, item in enumerate(retrieved, start=1):
        if item in relevant_set:
            return 1.0 / index

    return 0.0


def mean_reciprocal_rank(
    rankings: List[Sequence[str]],
    relevant_sets: List[Iterable[str]],
) -> float:
    if not rankings:
        return 0.0

    scores = [
        reciprocal_rank(ranking, relevant)
        for ranking, relevant in zip(rankings, relevant_sets)
    ]

    return sum(scores) / len(scores)
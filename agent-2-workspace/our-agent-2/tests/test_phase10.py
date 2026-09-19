from types import SimpleNamespace

from app.knowledge.retrieval.reranker import RetrievalReranker
from app.knowledge.retrieval.diversity import RetrievalDiversifier
from app.knowledge.retrieval.query_expansion import QueryExpander
from app.knowledge.retrieval.evaluation import (
    hit_rate,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
    mean_reciprocal_rank,
)


def test_reranker_orders_candidates():
    candidates = [
        SimpleNamespace(
            text="database configuration",
            score=0.4,
            authority_score=0.2,
        ),
        SimpleNamespace(
            text="authentication login credentials",
            score=0.9,
            authority_score=0.8,
        ),
    ]

    result = RetrievalReranker().rerank(
        "authentication",
        candidates,
    )

    assert result[0].text == "authentication login credentials"


def test_diversifier_limits_document_duplicates():
    candidates = [
        SimpleNamespace(document_id="doc-a"),
        SimpleNamespace(document_id="doc-a"),
        SimpleNamespace(document_id="doc-a"),
        SimpleNamespace(document_id="doc-b"),
        SimpleNamespace(document_id="doc-c"),
    ]

    result = RetrievalDiversifier().diversify(
        candidates,
        max_results=5,
        max_per_document=2,
    )

    assert len(result) == 4
    assert sum(x.document_id == "doc-a" for x in result) == 2


def test_query_expansion():
    result = QueryExpander().expand(
        "How does authentication work?"
    )

    assert "authentication" in result
    assert "login" in result
    assert "credentials" in result


def test_query_without_known_concept_is_preserved():
    result = QueryExpander().expand(
        "How does the scheduler work?"
    )

    assert result == ["How does the scheduler work?"]


def test_hit_rate():
    assert hit_rate(
        ["a", "b", "c"],
        ["c"],
    ) == 1.0

    assert hit_rate(
        ["a", "b"],
        ["c"],
    ) == 0.0


def test_precision_at_k():
    assert precision_at_k(
        ["a", "b", "c"],
        ["a", "c"],
        3,
    ) == 2 / 3


def test_recall_at_k():
    assert recall_at_k(
        ["a", "b", "c"],
        ["a", "c"],
        3,
    ) == 1.0


def test_reciprocal_rank():
    assert reciprocal_rank(
        ["x", "b", "c"],
        ["b"],
    ) == 0.5


def test_mean_reciprocal_rank():
    score = mean_reciprocal_rank(
        [
            ["a", "b"],
            ["x", "c"],
        ],
        [
            ["a"],
            ["c"],
        ],
    )

    assert score == 0.75
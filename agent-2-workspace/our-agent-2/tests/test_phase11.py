from dataclasses import dataclass

import pytest

from app.knowledge.retrieval.pipeline import RetrievalPipeline


@dataclass
class Candidate:
    document_id: str
    score: float
    text: str


class FakeRetriever:
    def retrieve(self, query):
        return [
            Candidate("doc-a", 0.95, "authentication implementation"),
            Candidate("doc-a", 0.90, "authentication configuration"),
            Candidate("doc-a", 0.85, "authentication tests"),
            Candidate("doc-b", 0.80, "authorization implementation"),
            Candidate("doc-c", 0.75, "security configuration"),
        ]


class FakeReranker:
    def rerank(self, query, candidates):
        return sorted(candidates, key=lambda x: x.score, reverse=True)


def test_pipeline_runs_end_to_end():
    pipeline = RetrievalPipeline(
        retriever=FakeRetriever(),
        reranker=FakeReranker(),
        top_k=5,
        max_per_document=2,
    )

    result = pipeline.run("authentication")

    assert result.query == "authentication"
    assert result.total_candidates == 5
    assert len(result.results) == 4


def test_pipeline_limits_duplicate_documents():
    pipeline = RetrievalPipeline(
        retriever=FakeRetriever(),
        reranker=FakeReranker(),
        top_k=5,
        max_per_document=2,
    )

    result = pipeline.run("authentication")

    counts = {}

    for item in result.results:
        counts[item.document_id] = counts.get(item.document_id, 0) + 1

    assert counts["doc-a"] == 2
    assert counts["doc-b"] == 1
    assert counts["doc-c"] == 1


def test_pipeline_preserves_ranking():
    pipeline = RetrievalPipeline(
        retriever=FakeRetriever(),
        reranker=FakeReranker(),
        top_k=3,
        max_per_document=1,
    )

    result = pipeline.run("authentication")

    scores = [item.score for item in result.results]

    assert scores == sorted(scores, reverse=True)


def test_pipeline_rejects_empty_query():
    pipeline = RetrievalPipeline(
        retriever=FakeRetriever(),
        reranker=FakeReranker(),
    )

    with pytest.raises(ValueError):
        pipeline.run("")


def test_pipeline_rejects_whitespace_query():
    pipeline = RetrievalPipeline(
        retriever=FakeRetriever(),
        reranker=FakeReranker(),
    )

    with pytest.raises(ValueError):
        pipeline.run("   ")


def test_pipeline_supports_search_interface():
    class SearchRetriever:
        def search(self, query):
            return [
                Candidate("doc-a", 1.0, "result")
            ]

    pipeline = RetrievalPipeline(
        retriever=SearchRetriever(),
        reranker=FakeReranker(),
    )

    result = pipeline.run("test")

    assert len(result.results) == 1


def test_pipeline_handles_empty_retrieval():
    class EmptyRetriever:
        def retrieve(self, query):
            return []

    pipeline = RetrievalPipeline(
        retriever=EmptyRetriever(),
        reranker=FakeReranker(),
    )

    result = pipeline.run("missing")

    assert result.total_candidates == 0
    assert result.results == []


def test_pipeline_requires_retrieval_interface():
    class InvalidRetriever:
        pass

    pipeline = RetrievalPipeline(
        retriever=InvalidRetriever(),
        reranker=FakeReranker(),
    )

    with pytest.raises(TypeError):
        pipeline.run("test")

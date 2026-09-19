from dataclasses import dataclass

from app.knowledge.retrieval.evaluator import (
    RetrievalEvaluationCase,
    RetrievalEvaluator,
)


@dataclass
class Candidate:
    document_id: str
    score: float


class FakePipeline:
    def __init__(self, mapping):
        self.mapping = mapping

    def run(self, query):
        class Result:
            def __init__(self, results):
                self.results = results

        return Result(self.mapping.get(query, []))


def test_evaluator_detects_hit():
    pipeline = FakePipeline({
        "authentication": [
            Candidate("auth.py", 1.0),
            Candidate("other.py", 0.5),
        ]
    })

    evaluator = RetrievalEvaluator(pipeline)

    result = evaluator.evaluate_case(
        RetrievalEvaluationCase(
            query="authentication",
            relevant_document_ids=["auth.py"],
        )
    )

    assert result.hit is True


def test_evaluator_detects_miss():
    pipeline = FakePipeline({
        "authentication": [
            Candidate("other.py", 1.0),
        ]
    })

    evaluator = RetrievalEvaluator(pipeline)

    result = evaluator.evaluate_case(
        RetrievalEvaluationCase(
            query="authentication",
            relevant_document_ids=["auth.py"],
        )
    )

    assert result.hit is False
    assert result.reciprocal_rank == 0.0


def test_precision_at_k():
    pipeline = FakePipeline({
        "q": [
            Candidate("a", 1.0),
            Candidate("b", 0.9),
            Candidate("c", 0.8),
            Candidate("d", 0.7),
        ]
    })

    evaluator = RetrievalEvaluator(pipeline)

    result = evaluator.evaluate_case(
        RetrievalEvaluationCase(
            query="q",
            relevant_document_ids=["a", "c"],
        )
    )

    assert result.precision_at_k == 0.5


def test_recall_at_k():
    pipeline = FakePipeline({
        "q": [
            Candidate("a", 1.0),
            Candidate("b", 0.9),
            Candidate("c", 0.8),
        ]
    })

    evaluator = RetrievalEvaluator(pipeline)

    result = evaluator.evaluate_case(
        RetrievalEvaluationCase(
            query="q",
            relevant_document_ids=["a", "c"],
        )
    )

    assert result.recall_at_k == 1.0


def test_reciprocal_rank():
    pipeline = FakePipeline({
        "q": [
            Candidate("wrong", 1.0),
            Candidate("target", 0.9),
        ]
    })

    evaluator = RetrievalEvaluator(pipeline)

    result = evaluator.evaluate_case(
        RetrievalEvaluationCase(
            query="q",
            relevant_document_ids=["target"],
        )
    )

    assert result.reciprocal_rank == 0.5


def test_evaluate_dataset():
    pipeline = FakePipeline({
        "q1": [
            Candidate("a", 1.0),
        ],
        "q2": [
            Candidate("b", 1.0),
        ],
    })

    evaluator = RetrievalEvaluator(pipeline)

    report = evaluator.evaluate([
        RetrievalEvaluationCase(
            query="q1",
            relevant_document_ids=["a"],
        ),
        RetrievalEvaluationCase(
            query="q2",
            relevant_document_ids=["b"],
        ),
    ])

    assert report["count"] == 2
    assert report["hit_rate"] == 1.0
    assert report["mean_precision_at_k"] == 1.0
    assert report["mean_recall_at_k"] == 1.0
    assert report["mean_reciprocal_rank"] == 1.0


def test_empty_dataset():
    pipeline = FakePipeline({})

    evaluator = RetrievalEvaluator(pipeline)

    report = evaluator.evaluate([])

    assert report["count"] == 0
    assert report["hit_rate"] == 0.0


def test_multiple_relevant_documents():
    pipeline = FakePipeline({
        "q": [
            Candidate("a", 1.0),
            Candidate("b", 0.9),
        ]
    })

    evaluator = RetrievalEvaluator(pipeline)

    result = evaluator.evaluate_case(
        RetrievalEvaluationCase(
            query="q",
            relevant_document_ids=["a", "b"],
        )
    )

    assert result.hit is True
    assert result.recall_at_k == 1.0


def test_dataset_is_available():
    from app.knowledge.evaluation.dataset import (
        DEFAULT_RETRIEVAL_DATASET,
    )

    assert len(DEFAULT_RETRIEVAL_DATASET) >= 3

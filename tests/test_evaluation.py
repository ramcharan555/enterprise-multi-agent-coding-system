from evaluation.dataset import (
    EVALUATION_DATASET,
    EvaluationCase,
)
from evaluation.runner import EvaluationRunner


def test_evaluation_dataset_is_not_empty():
    assert EVALUATION_DATASET


def test_evaluation_cases_have_required_fields():
    for case in EVALUATION_DATASET:
        assert isinstance(case, EvaluationCase)
        assert case.query
        assert case.expected_symbols
        assert case.expected_files
        assert case.expected_intent


class FakeContextItem:
    def __init__(self, name, file_path):
        self.name = name
        self.file_path = file_path


class FakeService:
    def answer(self, question):
        query = question.query
        query_lower = query.lower()

        # Symbol detection
        if "send" in query_lower or "sent" in query_lower:
            symbol = "send"
        elif "post" in query_lower:
            symbol = "post"
        elif "session" in query_lower:
            symbol = "Session"
        else:
            symbol = "send"

        # Intent detection
        if any(
            phrase in query_lower
            for phrase in [
                "where is",
                "where can i find",
                "where can i",
                "where does",
                "which file",
                "which source file",
                "what file",
                "implementation of",
                "implementation for",
            ]
        ):
            intent = "location"

        elif any(
            phrase in query_lower
            for phrase in [
                "what calls",
                "who calls",
                "which code calls",
                "which functions call",
                "called by",
                "depends on",
                "what depends",
                "which code depends",
                "which functions depend",
                "which code uses",
                "which functions use",
                "what code uses",
                "what uses",
                "who uses",
            ]
        ):
            intent = "dependency"

        else:
            intent = "explanation"

        return type(
            "FakeResponse",
            (),
            {
                "answer": "The send function handles the request. [E1]",
                "intent": intent,
                "context": [
                    FakeContextItem(
                        symbol,
                        "src/requests/sessions.py",
                    )
                ],
                "citation_validation": {
                    "is_valid": True,
                    "has_citations": True,
                    "missing_citations": False,
                },
            },
        )()

def test_evaluation_runner_evaluates_case():
    runner = EvaluationRunner(FakeService())
    case = EVALUATION_DATASET[0]

    result = runner.evaluate_case(case)

    assert result.symbol_hit is True
    assert result.file_hit is True
    assert result.intent_hit is True


def test_evaluation_runner_runs_dataset():
    runner = EvaluationRunner(FakeService())

    results = runner.run()

    assert len(results) == len(EVALUATION_DATASET)


def test_evaluation_runner_reports_retrieval_results():
    runner = EvaluationRunner(FakeService())
    case = EVALUATION_DATASET[0]

    result = runner.evaluate_retrieval(case)

    assert result["query"] == case.query
    assert result["symbol_hit"] is True
    assert result["file_hit"] is True
    assert "send" in result["retrieved_symbols"]
    assert "src/requests/sessions.py" in result["retrieved_files"]


def test_retrieval_metrics():
    runner = EvaluationRunner(FakeService())

    metrics = runner.retrieval_metrics()

    assert metrics["total_cases"] == len(EVALUATION_DATASET)
    assert metrics["symbol_hit_rate"] == 1.0
    assert metrics["file_hit_rate"] == 1.0


def test_evaluation_runner_evaluates_answer():
    runner = EvaluationRunner(FakeService())
    case = EVALUATION_DATASET[0]

    result = runner.evaluate_answer(case)

    assert result["query"] == case.query
    assert "answer" in result
    assert result["has_citations"] is True
    assert result["citations_valid"] is True
    assert result["missing_citations"] is False


def test_answer_metrics():
    runner = EvaluationRunner(FakeService())

    metrics = runner.answer_metrics()

    assert metrics["total_cases"] == len(EVALUATION_DATASET)
    assert metrics["citation_validity_rate"] == 1.0
    assert metrics["citation_presence_rate"] == 1.0
    assert metrics["missing_citation_rate"] == 0.0


def test_real_evaluation_runs():
    from app.api import create_repository_qa_service

    service = create_repository_qa_service()
    runner = EvaluationRunner(service)

    results = runner.run()

    assert len(results) == len(EVALUATION_DATASET)

    for result in results:
        assert result.case.query
        assert result.retrieved_symbols
        assert result.retrieved_files


def test_benchmark_report():
    runner = EvaluationRunner(FakeService())

    report = runner.benchmark()

    assert report["total_cases"] == len(EVALUATION_DATASET)
    assert "retrieval" in report
    assert "answer" in report
    assert report["retrieval"]["symbol_hit_rate"] == 1.0
    assert report["retrieval"]["file_hit_rate"] == 1.0
    assert report["answer"]["citation_validity_rate"] == 1.0


def test_real_benchmark_report():
    from app.api import create_repository_qa_service

    service = create_repository_qa_service()
    runner = EvaluationRunner(service)

    report = runner.benchmark()

    assert report["total_cases"] == len(EVALUATION_DATASET)

    assert 0.0 <= report["retrieval"]["symbol_hit_rate"] <= 1.0
    assert 0.0 <= report["retrieval"]["file_hit_rate"] <= 1.0

    assert 0.0 <= report["answer"]["citation_validity_rate"] <= 1.0
    assert 0.0 <= report["answer"]["citation_presence_rate"] <= 1.0
    assert 0.0 <= report["answer"]["missing_citation_rate"] <= 1.0


def test_intent_metrics():
    runner = EvaluationRunner(FakeService())

    metrics = runner.intent_metrics()

    assert metrics["total_cases"] == len(EVALUATION_DATASET)
    assert metrics["intent_accuracy"] == 1.0
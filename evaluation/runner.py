from dataclasses import dataclass

from evaluation.dataset import (
    EVALUATION_DATASET,
    EvaluationCase,
)


@dataclass
class EvaluationResult:
    case: EvaluationCase
    retrieved_symbols: list[str]
    retrieved_files: list[str]
    intent: str
    symbol_hit: bool
    file_hit: bool
    intent_hit: bool


class EvaluationRunner:
    def __init__(self, service):
        self.service = service

    def evaluate_case(self, case: EvaluationCase) -> EvaluationResult:
        result = self.service.answer(
            self._build_question(case)
        )

        context = result.context

        retrieved_symbols = [
            item.name
            for item in context
        ]

        retrieved_files = [
            item.file_path
            for item in context
        ]

        symbol_hit = any(
            symbol in retrieved_symbols
            for symbol in case.expected_symbols
        )

        file_hit = any(
            file_path in retrieved_files
            for file_path in case.expected_files
        )

        intent_hit = (
            result.intent == case.expected_intent
        )

        return EvaluationResult(
            case=case,
            retrieved_symbols=retrieved_symbols,
            retrieved_files=retrieved_files,
            intent=result.intent,
            symbol_hit=symbol_hit,
            file_hit=file_hit,
            intent_hit=intent_hit,
        )

    def retrieval_metrics(self):
        results = self.run()

        total = len(results)

        if total == 0:
            return {
            "total_cases": 0,
            "symbol_hit_rate": 0.0,
            "file_hit_rate": 0.0,
            }

        symbol_hits = sum(
        result.symbol_hit
        for result in results
        )

        file_hits = sum(
        result.file_hit
        for result in results
        )

        return {
            "total_cases": total,
            "symbol_hit_rate": symbol_hits / total,
            "file_hit_rate": file_hits / total,
            }

    def evaluate_retrieval(self, case: EvaluationCase):
        result = self.evaluate_case(case)

        return {
            "query": case.query,
            "symbol_hit": result.symbol_hit,
            "file_hit": result.file_hit,
            "retrieved_symbols": result.retrieved_symbols,
            "retrieved_files": result.retrieved_files,
            }
    
    def run(self):
        return [
            self.evaluate_case(case)
            for case in EVALUATION_DATASET
        ]

    @staticmethod
    def _build_question(case):
        from app.api import RepositoryQuestion

        return RepositoryQuestion(
            query=case.query,
            top_k=5,
            max_context_chunks=12,
        )

    def evaluate_answer(
        self,
        case: EvaluationCase,
):
        result = self.service.answer(
            self._build_question(case)
        )

        citation_validation = getattr(
            result,
            "citation_validation",
            None,
        )

        if citation_validation is None:
            has_citations = False
            citations_valid = False
            missing_citations = False

        elif isinstance(citation_validation, dict):
            has_citations = citation_validation.get(
                "has_citations",
                False,
            )
            citations_valid = citation_validation.get(
                "is_valid",
                False,
            )
            missing_citations = citation_validation.get(
                "missing_citations",
                False,
            )

        else:
            has_citations = getattr(
                citation_validation,
                "has_citations",
                False,
            )
            citations_valid = getattr(
                citation_validation,
                "is_valid",
                False,
            )
            missing_citations = getattr(
                citation_validation,
                "missing_citations",
                False,
            )

        return {
            "query": case.query,
            "answer": result.answer,
            "has_citations": has_citations,
            "citations_valid": citations_valid,
            "missing_citations": missing_citations,
        }

    def answer_metrics(self):
        results = [
            self.evaluate_answer(case)
            for case in EVALUATION_DATASET
        ]

        total = len(results)

        if total == 0:
            return {
                "total_cases": 0,
                "citation_validity_rate": 0.0,
                "citation_presence_rate": 0.0,
                "missing_citation_rate": 0.0,
            }

        citation_valid = sum(
            result["citations_valid"]
            for result in results
        )

        citation_present = sum(
            result["has_citations"]
            for result in results
        )

        missing_citations = sum(
            result["missing_citations"]
            for result in results
        )

        return {
            "total_cases": total,
            "citation_validity_rate": citation_valid / total,
            "citation_presence_rate": citation_present / total,
            "missing_citation_rate": missing_citations / total,
        }

    def run_real(self):
        from app.api import create_repository_qa_service

        service = create_repository_qa_service()

        original_service = self.service
        self.service = service

        try:
            return self.run()
        finally:
            self.service = original_service

    def benchmark(self):
        retrieval = self.retrieval_metrics()
        intent = self.intent_metrics()
        answer = self.answer_metrics()

        return {
            "total_cases": retrieval["total_cases"],
            "retrieval": retrieval,
            "intent": intent,
            "answer": answer,
        }

    def intent_metrics(self):
        results = self.run()

        total = len(results)

        if total == 0:
            return {
                "total_cases": 0,
                "intent_accuracy": 0.0,
            }

        intent_hits = sum(
            result.intent_hit
            for result in results
        )

        return {
        "total_cases": total,
        "intent_accuracy": intent_hits / total,
        }
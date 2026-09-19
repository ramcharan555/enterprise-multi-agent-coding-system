from evaluation.runner import EvaluationRunner
from app.api import create_repository_qa_service


def main():
    service = create_repository_qa_service()
    runner = EvaluationRunner(service)

    results = runner.run()

    print("\n========== DETAILED BENCHMARK ==========\n")

    for i, result in enumerate(results, start=1):
        print(f"Case {i}: {result.case.query}")
        print(f"  Expected symbols: {result.case.expected_symbols}")
        print(f"  Retrieved symbols: {result.retrieved_symbols}")
        print(f"  Symbol hit: {result.symbol_hit}")
        print(f"  Expected files: {result.case.expected_files}")
        print(f"  Retrieved files: {result.retrieved_files}")
        print(f"  File hit: {result.file_hit}")
        print(f"  Expected intent: {result.case.expected_intent}")
        print(f"  Actual intent: {result.intent}")
        print(f"  Intent hit: {result.intent_hit}")
        print()

    report = runner.benchmark()

    print("========== SUMMARY ==========\n")
    print(f"Total cases: {report['total_cases']}")
    print(
        f"Symbol hit rate: "
        f"{report['retrieval']['symbol_hit_rate']:.3f}"
    )
    print(
        f"File hit rate: "
        f"{report['retrieval']['file_hit_rate']:.3f}"
    )
    print("\n--- Intent ---")
    print(
        f"Intent accuracy: "
        f"{report['intent']['intent_accuracy']:.3f}"
    )
    print(
        f"Citation validity rate: "
        f"{report['answer']['citation_validity_rate']:.3f}"
    )
    print(
        f"Citation presence rate: "
        f"{report['answer']['citation_presence_rate']:.3f}"
    )
    print(
        f"Missing citation rate: "
        f"{report['answer']['missing_citation_rate']:.3f}"
    )


if __name__ == "__main__":
    main()
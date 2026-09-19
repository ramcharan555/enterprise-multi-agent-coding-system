import pytest

from app.orchestrator.synthesizer import ResponseSynthesizer


def test_synthesizes_code_result():
    synthesizer = ResponseSynthesizer()

    result = synthesizer.synthesize(
        "Fix the authentication function",
        {
            "route": "code",
            "code": {
                "agent": "code",
                "answer": "Authentication is implemented in auth.py.",
                "evidence": ["auth.py"],
            },
            "knowledge": None,
        },
    )

    assert result["query"] == "Fix the authentication function"
    assert "Code Agent" in result["answer"]
    assert "Authentication is implemented in auth.py." in result["answer"]
    assert "auth.py" in result["sources"]


def test_synthesizes_knowledge_result():
    synthesizer = ResponseSynthesizer()

    result = synthesizer.synthesize(
        "What does the architecture document say?",
        {
            "route": "knowledge",
            "code": None,
            "knowledge": {
                "agent": "knowledge",
                "answer": "APIs must use versioning.",
                "evidence": ["architecture.md"],
            },
        },
    )

    assert "Knowledge Agent" in result["answer"]
    assert "APIs must use versioning." in result["answer"]
    assert "architecture.md" in result["sources"]


def test_synthesizes_both_agents():
    synthesizer = ResponseSynthesizer()

    result = synthesizer.synthesize(
        "Modify the authentication API according to architecture guidelines",
        {
            "route": "both",
            "code": {
                "agent": "code",
                "answer": "Authentication is implemented in auth.py.",
                "evidence": ["auth.py"],
            },
            "knowledge": {
                "agent": "knowledge",
                "answer": "OAuth2 is required.",
                "evidence": ["security.md"],
            },
        },
    )

    assert "Code Agent" in result["answer"]
    assert "Knowledge Agent" in result["answer"]
    assert "auth.py" in result["sources"]
    assert "security.md" in result["sources"]


def test_duplicate_sources_are_removed():
    synthesizer = ResponseSynthesizer()

    result = synthesizer.synthesize(
        "Check authentication",
        {
            "route": "both",
            "code": {
                "agent": "code",
                "answer": "Code result",
                "evidence": ["auth.py"],
            },
            "knowledge": {
                "agent": "knowledge",
                "answer": "Knowledge result",
                "evidence": ["auth.py"],
            },
        },
    )

    assert result["sources"] == ["auth.py"]


def test_empty_query_rejected():
    synthesizer = ResponseSynthesizer()

    with pytest.raises(ValueError):
        synthesizer.synthesize(
            "",
            {
                "route": "code",
                "code": None,
                "knowledge": None,
            },
        )


def test_empty_results_are_handled():
    synthesizer = ResponseSynthesizer()

    result = synthesizer.synthesize(
        "Some query",
        {
            "route": "knowledge",
            "code": None,
            "knowledge": None,
        },
    )

    assert result["sources"] == []
    assert "No agent produced a result." in result["answer"]
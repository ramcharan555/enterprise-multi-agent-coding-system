import pytest

from app.orchestrator.orchestrator import Orchestrator, QueryRoute


def test_code_query_routes_to_code():
    orchestrator = Orchestrator()

    result = orchestrator.route("Fix this Python function")

    assert result == QueryRoute.CODE


def test_knowledge_query_routes_to_knowledge():
    orchestrator = Orchestrator()

    result = orchestrator.route(
        "What does our architecture documentation say?"
    )

    assert result == QueryRoute.KNOWLEDGE


def test_combined_query_routes_to_both():
    orchestrator = Orchestrator()

    result = orchestrator.route(
        "Modify the authentication API according to our architecture guidelines"
    )

    assert result == QueryRoute.BOTH


def test_empty_query_rejected():
    orchestrator = Orchestrator()

    with pytest.raises(ValueError):
        orchestrator.route("")


def test_whitespace_query_rejected():
    orchestrator = Orchestrator()

    with pytest.raises(ValueError):
        orchestrator.route("   ")
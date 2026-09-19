import pytest

from app.orchestrator.service import MultiAgentService


class FakeCodeAgent:
    def query(self, query):
        return {
            "agent": "code",
            "answer": "Found implementation in auth.py.",
            "evidence": ["auth.py"],
        }


class FakeKnowledgeAgent:
    def query(self, query):
        return {
            "agent": "knowledge",
            "answer": "OAuth2 is required by the architecture.",
            "evidence": ["architecture.md"],
        }


def test_code_query_end_to_end():
    service = MultiAgentService(
        code_agent=FakeCodeAgent(),
        knowledge_agent=FakeKnowledgeAgent(),
    )

    result = service.query("Fix the authentication function")

    assert result["route"] == "code"
    assert "Code Agent" in result["answer"]
    assert "auth.py" in result["sources"]


def test_knowledge_query_end_to_end():
    service = MultiAgentService(
        code_agent=FakeCodeAgent(),
        knowledge_agent=FakeKnowledgeAgent(),
    )

    result = service.query(
        "What does the architecture documentation say?"
    )

    assert result["route"] == "knowledge"
    assert "Knowledge Agent" in result["answer"]
    assert "architecture.md" in result["sources"]


def test_combined_query_end_to_end():
    service = MultiAgentService(
        code_agent=FakeCodeAgent(),
        knowledge_agent=FakeKnowledgeAgent(),
    )

    result = service.query(
        "Modify the authentication API according to architecture guidelines"
    )

    assert result["route"] == "both"
    assert "Code Agent" in result["answer"]
    assert "Knowledge Agent" in result["answer"]
    assert "auth.py" in result["sources"]
    assert "architecture.md" in result["sources"]


def test_empty_query_rejected():
    service = MultiAgentService(
        code_agent=FakeCodeAgent(),
        knowledge_agent=FakeKnowledgeAgent(),
    )

    with pytest.raises(ValueError):
        service.query("")
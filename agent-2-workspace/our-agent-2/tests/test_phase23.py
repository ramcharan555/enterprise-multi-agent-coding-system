from app.orchestrator.service import MultiAgentService


class CodeAgent:
    def query(self, query):
        return {
            "agent": "code",
            "answer": "The authentication implementation is in auth.py.",
            "evidence": ["auth.py"],
        }


class KnowledgeAgent:
    def query(self, query):
        return {
            "agent": "knowledge",
            "answer": "The architecture requires OAuth2 authentication.",
            "evidence": ["architecture.md"],
        }


def test_full_multi_agent_flow():
    service = MultiAgentService(
        code_agent=CodeAgent(),
        knowledge_agent=KnowledgeAgent(),
    )

    result = service.query(
        "Modify the authentication API according to architecture guidelines"
    )

    assert result["route"] == "both"

    assert "Code Agent" in result["answer"]
    assert "Knowledge Agent" in result["answer"]

    assert "auth.py" in result["sources"]
    assert "architecture.md" in result["sources"]


def test_code_only_flow():
    service = MultiAgentService(
        code_agent=CodeAgent(),
        knowledge_agent=KnowledgeAgent(),
    )

    result = service.query("Fix the authentication function")

    assert result["route"] == "code"
    assert "auth.py" in result["sources"]


def test_knowledge_only_flow():
    service = MultiAgentService(
        code_agent=CodeAgent(),
        knowledge_agent=KnowledgeAgent(),
    )

    result = service.query(
        "What does the architecture documentation say?"
    )

    assert result["route"] == "knowledge"
    assert "architecture.md" in result["sources"]


def test_sources_are_deduplicated():
    service = MultiAgentService(
        code_agent=CodeAgent(),
        knowledge_agent=KnowledgeAgent(),
    )

    result = service.query(
        "Modify the authentication API according to architecture guidelines"
    )

    assert len(result["sources"]) == len(set(result["sources"]))
from app.orchestrator.orchestrator import Orchestrator, QueryRoute


class FakeCodeAgent:
    def query(self, query):
        return {
            "agent": "code",
            "answer": "Code evidence",
            "evidence": ["code.py"],
        }


class FakeKnowledgeAgent:
    def query(self, query):
        return {
            "agent": "knowledge",
            "answer": "Knowledge evidence",
            "evidence": ["architecture.md"],
        }


def test_code_query_calls_code_agent():
    orchestrator = Orchestrator()

    result = orchestrator.execute(
        "Fix this Python function",
        code_agent=FakeCodeAgent(),
        knowledge_agent=FakeKnowledgeAgent(),
    )

    assert result["route"] == QueryRoute.CODE
    assert result["code"] is not None
    assert result["knowledge"] is None


def test_knowledge_query_calls_knowledge_agent():
    orchestrator = Orchestrator()

    result = orchestrator.execute(
        "What does the architecture documentation say?",
        code_agent=FakeCodeAgent(),
        knowledge_agent=FakeKnowledgeAgent(),
    )

    assert result["route"] == QueryRoute.KNOWLEDGE
    assert result["knowledge"] is not None
    assert result["code"] is None


def test_combined_query_calls_both_agents():
    orchestrator = Orchestrator()

    result = orchestrator.execute(
        "Modify the authentication API according to architecture guidelines",
        code_agent=FakeCodeAgent(),
        knowledge_agent=FakeKnowledgeAgent(),
    )

    assert result["route"] == QueryRoute.BOTH
    assert result["code"] is not None
    assert result["knowledge"] is not None


def test_empty_query_rejected():
    orchestrator = Orchestrator()

    try:
        orchestrator.execute(
            "",
            code_agent=FakeCodeAgent(),
            knowledge_agent=FakeKnowledgeAgent(),
        )
        assert False
    except ValueError:
        assert True
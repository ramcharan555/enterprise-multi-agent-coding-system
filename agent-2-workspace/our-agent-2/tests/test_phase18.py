from app.integration.agent_context import AgentContext
from app.integration.multi_agent_context import MultiAgentContextBuilder


def test_context_combines_agent_results():
    builder = MultiAgentContextBuilder()

    context = builder.build(
        "How should authentication be implemented?",
        code_results=["code-result"],
        knowledge_results=["architecture-result"],
    )

    assert context.query == "How should authentication be implemented?"
    assert context.code_results == ["code-result"]
    assert context.knowledge_results == ["architecture-result"]
    assert context.combined_results() == [
        "code-result",
        "architecture-result",
    ]


def test_context_supports_empty_agent_results():
    context = MultiAgentContextBuilder().build("test")

    assert context.code_results == []
    assert context.knowledge_results == []
    assert context.combined_results() == []


def test_context_rejects_empty_query():
    builder = MultiAgentContextBuilder()

    try:
        builder.build("   ")
        assert False
    except ValueError as exc:
        assert "query" in str(exc)


def test_context_preserves_agent_separation():
    context = AgentContext(
        query="test",
        code_results=["code"],
        knowledge_results=["knowledge"],
    )

    assert context.code_results != context.knowledge_results
    assert context.combined_results() == ["code", "knowledge"]

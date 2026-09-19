from app.knowledge.agent.context import (
    ContextBuilder,
)
from app.knowledge.llm import (
    GroundedPromptBuilder,
    LLMAnswerGenerator,
    MockLLMProvider,
)
from app.knowledge.models import (
    Document,
    DocumentType,
)
from app.knowledge.retrieval.evidence import (
    Evidence,
)


def create_evidence():
    return [
        Evidence(
            chunk_id="chunk-001",
            document_id="doc-001",
            source="architecture.md",
            title="API Architecture",
            section="Authentication",
            content=(
                "All public APIs must use OAuth2."
            ),
            score=0.9,
        )
    ]


def test_prompt_contains_question_and_evidence():
    evidence = create_evidence()

    context = ContextBuilder().build(
        "How should authentication work?",
        evidence,
    )

    prompt = GroundedPromptBuilder().build(
        context
    )

    assert "How should authentication work?" in prompt
    assert "All public APIs must use OAuth2." in prompt
    assert "Do not invent facts." in prompt


def test_mock_llm_provider():
    provider = MockLLMProvider()

    response = provider.generate(
        "test prompt"
    )

    assert response.model == "mock-llm"
    assert response.text


def test_llm_answer_generation():
    evidence = create_evidence()

    context = ContextBuilder().build(
        "How should authentication work?",
        evidence,
    )

    generator = LLMAnswerGenerator(
        MockLLMProvider()
    )

    answer = generator.generate(context)

    assert answer.grounded is True
    assert answer.answer
    assert "architecture.md" in answer.citations
    assert answer.confidence > 0


def test_llm_rejects_empty_evidence():
    context = ContextBuilder().build(
        "How should authentication work?",
        [],
    )

    generator = LLMAnswerGenerator(
        MockLLMProvider()
    )

    answer = generator.generate(context)

    assert answer.grounded is False
    assert answer.confidence == 0.0
    assert answer.citations == []
    assert "insufficient" in answer.answer.lower()
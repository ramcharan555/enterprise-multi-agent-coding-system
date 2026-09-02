from app.llm.answerer import CodeAnswerer
from app.llm.client import MockLLMClient
from app.llm.prompts import build_prompt


def sample_context():
    return [
        {
            "name": "send",
            "chunk_type": "method",
            "file_path": "src/requests/adapters.py",
            "start_line": 634,
            "end_line": 748,
            "source": "def send(self):\n    pass",
        },
        {
            "name": "add_headers",
            "chunk_type": "method",
            "file_path": "src/requests/adapters.py",
            "start_line": 599,
            "end_line": 611,
            "source": "def add_headers(self):\n    pass",
        },
    ]


def test_prompt_contains_query():
    prompt = build_prompt(
        "How does send work?",
        sample_context(),
    )

    assert "How does send work?" in prompt
    assert "src/requests/adapters.py" in prompt
    assert "def send" in prompt


def test_answerer_uses_llm():
    answerer = CodeAnswerer(
        MockLLMClient()
    )

    result = answerer.answer(
        "How does send work?",
        sample_context(),
    )

    assert result["answer"]
    assert "Mock LLM response" in result["answer"]


def test_answer_contains_sources():
    answerer = CodeAnswerer(
        MockLLMClient()
    )

    result = answerer.answer(
        "How does send work?",
        sample_context(),
    )

    assert len(result["sources"]) == 2

    assert result["sources"][0]["file_path"] == (
        "src/requests/adapters.py"
    )

    assert result["sources"][0]["start_line"] == 634


def test_sources_are_deduplicated():
    context = sample_context()

    context.append(context[0].copy())

    answerer = CodeAnswerer(
        MockLLMClient()
    )

    result = answerer.answer(
        "How does send work?",
        context,
    )

    assert len(result["sources"]) == 2


def test_answerer_handles_empty_context():
    answerer = CodeAnswerer(
        MockLLMClient()
    )

    result = answerer.answer(
        "Where is authentication?",
        [],
    )

    assert "not find enough" in result["answer"]
    assert result["sources"] == []
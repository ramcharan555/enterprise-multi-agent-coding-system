from app.llm.answerer import CodeAnswerer
from app.llm.client import MockLLMClient
from app.llm.evidence import build_evidence, validate_citations
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

def test_answer_contains_evidence_metadata():
    context = [
        {
            "chunk_id": "src/requests/adapters.py:634:send",
            "name": "send",
            "chunk_type": "method",
            "file_path": "src/requests/adapters.py",
            "start_line": 634,
            "end_line": 748,
            "source": "def send(self):\n    pass",
            "relationship": "CALLS",
            "score": 0.91,
        }
    ]

    answerer = CodeAnswerer(
        MockLLMClient()
    )

    result = answerer.answer(
        "How does send work?",
        context,
    )

    source = result["sources"][0]

    assert source["chunk_id"] == (
        "src/requests/adapters.py:634:send"
    )
    assert source["file_path"] == (
        "src/requests/adapters.py"
    )
    assert source["start_line"] == 634
    assert source["end_line"] == 748
    assert source["name"] == "send"
    assert source["chunk_type"] == "method"
    assert source["relationship"] == "CALLS"
    assert source["score"] == 0.91


class CitationLLMClient:
    def __init__(self, answer):
        self.answer = answer
        self.system_prompt = None
        self.user_prompt = None

    def generate(self, system_prompt, user_prompt):
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        return self.answer


def test_evidence_ids_are_deterministic_and_map_to_context():
    evidence = build_evidence(sample_context())

    assert [item["evidence_id"] for item in evidence] == ["E1", "E2"]
    assert evidence[0]["file_path"] == "src/requests/adapters.py"
    assert evidence[0]["name"] == "send"
    assert evidence[0]["chunk_id"] == "src/requests/adapters.py:634:send"


def test_duplicate_context_records_share_one_evidence_item():
    context = sample_context()
    context.append(context[0].copy())

    evidence = build_evidence(context)

    assert [item["evidence_id"] for item in evidence] == ["E1", "E2"]


def test_prompt_includes_only_generated_evidence_ids():
    client = CitationLLMClient("send sends a request [E1].")
    result = CodeAnswerer(client).answer("How does send work?", sample_context())

    assert "EVIDENCE ID: [E1]" in client.user_prompt
    assert "EVIDENCE ID: [E2]" in client.user_prompt
    assert "Only use evidence IDs supplied" in client.system_prompt
    assert result["citation_validation"]["valid_evidence_ids"] == ["E1"]
    assert result["citations"][0]["name"] == "send"


def test_citation_validation_detects_fabricated_evidence_ids():
    validation = validate_citations(
        "Observed behavior [E1], [E99], and [Einvented].",
        build_evidence(sample_context()),
    )

    assert validation["is_valid"] is False
    assert validation["valid_evidence_ids"] == ["E1"]
    assert validation["invalid_evidence_ids"] == ["E99", "Einvented"]


def test_answerer_reports_missing_citations_without_failing_answer():
    result = CodeAnswerer(MockLLMClient()).answer("How does send work?", sample_context())

    assert result["citation_validation"]["is_valid"] is True
    assert result["citation_validation"]["missing_citations"] is False
    assert result["citation_validation"]["has_citations"] is True
    assert len(result["citations"]) > 0
    assert result["citations"][0]["evidence_id"] == "E1"


def test_legacy_context_without_chunk_id_preserves_citation_metadata():
    client = CitationLLMClient("The method is shown here [E1].")
    result = CodeAnswerer(client).answer("How does send work?", sample_context())

    evidence = result["evidence"][0]
    assert evidence["chunk_id"] == "src/requests/adapters.py:634:send"
    assert evidence["start_line"] == 634
    assert evidence["end_line"] == 748
    assert evidence["relationship"] is None
    assert evidence["score"] is None

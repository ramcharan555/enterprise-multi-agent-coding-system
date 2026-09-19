from fastapi.testclient import TestClient

from app.api import RepositoryQuestion, RepositoryQAService, create_app


class FakeOrchestrator:
    def __init__(self):
        self.queries = []

    def run(self, query):
        self.queries.append(query)
        return {
            "intent": "explanation",
            "agent": "explainer",
            "result": {
                "context": [
                    {
                        "chunk_id": "adapter:1:send",
                        "name": "send",
                        "chunk_type": "method",
                        "file_path": "src/adapters.py",
                        "start_line": 1,
                        "end_line": 4,
                        "score": 0.9,
                    }
                ]
            },
        }


class FakeRetriever:
    def __init__(self):
        self.queries = []

    def search(self, query, top_k=5):
        self.queries.append((query, top_k))
        return []


class FakeContextBuilder:
    def __init__(self):
        self.calls = []

    def build(self, results, max_chunks=12):
        self.calls.append((results, max_chunks))
        return [
            {
                "chunk_id": "adapter:1:send",
                "name": "send",
                "chunk_type": "method",
                "file_path": "src/adapters.py",
                "start_line": 1,
                "end_line": 4,
                "relationship": "CALLS",
                "score": 0.93,
                "source": "def send(): pass",
            }
        ]


class FakeAnswerer:
    def __init__(self):
        self.calls = []

    def answer(self, query, context):
        self.calls.append((query, context))
        return {
            "answer": "send performs the request.",
            "sources": [
                {
                    "file_path": "src/adapters.py",
                    "start_line": 1,
                    "end_line": 4,
                    "name": "send",
                }
            ],
        }


def build_client():
    orchestrator = FakeOrchestrator()
    retriever = FakeRetriever()
    builder = FakeContextBuilder()
    answerer = FakeAnswerer()
    service = RepositoryQAService(
        orchestrator,
        retriever,
        builder,
        answerer,
    )
    return TestClient(create_app(service)), orchestrator, retriever, builder, answerer


def test_questions_endpoint_runs_the_repository_qa_pipeline():
    client, orchestrator, retriever, builder, answerer = build_client()

    response = client.post(
        "/api/v1/questions",
        json={
            "query": "How does send work?",
            "top_k": 1,
            "max_context_chunks": 3,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["query"] == "How does send work?"
    assert body["intent"] == "explanation"
    assert body["agent"] == "explainer"
    assert body["answer"] == "send performs the request."
    assert body["sources"][0]["name"] == "send"
    assert body["context"][0]["relationship"] == "CALLS"
    assert orchestrator.queries == ["How does send work?"]
    assert retriever.queries == []
    assert builder.calls[0][1] == 3
    assert answerer.calls[0][0] == "How does send work?"


def test_questions_endpoint_uses_retriever_when_orchestration_has_no_results():
    _, _, retriever, builder, _ = build_client()

    # Use a service whose router result has no agent/context, as coding and
    # general questions do in the current orchestrator.
    class EmptyOrchestrator:
        def run(self, query):
            return {"intent": "general", "agent": None, "result": None}

    service = RepositoryQAService(
        EmptyOrchestrator(),
        retriever,
        builder,
        FakeAnswerer(),
    )
    client = TestClient(create_app(service))

    response = client.post(
        "/api/v1/questions",
        json={"query": "Explain adapters", "top_k": 2},
    )

    assert response.status_code == 200
    assert retriever.queries == [("Explain adapters", 2)]


def test_questions_endpoint_validates_request_body():
    client, *_ = build_client()

    response = client.post("/api/v1/questions", json={"query": "  "})

    assert response.status_code == 422
    assert client.post(
        "/api/v1/questions",
        json={"query": "How?", "top_k": 0},
    ).status_code == 422


def test_repository_question_strips_whitespace():
    question = RepositoryQuestion(query="  Where is send?  ")

    assert question.query == "Where is send?"


def test_questions_endpoint_exposes_evidence_and_citation_validation():
    class CitationAnswerer:
        def answer(self, query, context):
            return {
                "answer": "send performs the request [E1].",
                "sources": [],
                "evidence": [
                    {
                        "evidence_id": "E1",
                        "chunk_id": "adapter:1:send",
                        "name": "send",
                        "chunk_type": "method",
                        "file_path": "src/adapters.py",
                        "start_line": 1,
                        "end_line": 4,
                        "relationship": "CALLS",
                        "score": 0.93,
                    }
                ],
                "citations": [
                    {
                        "evidence_id": "E1",
                        "chunk_id": "adapter:1:send",
                        "name": "send",
                        "chunk_type": "method",
                        "file_path": "src/adapters.py",
                        "start_line": 1,
                        "end_line": 4,
                        "relationship": "CALLS",
                        "score": 0.93,
                    }
                ],
                "citation_validation": {
                    "is_valid": True,
                    "has_citations": True,
                    "missing_citations": False,
                    "valid_evidence_ids": ["E1"],
                    "invalid_evidence_ids": [],
                },
            }

    _, orchestrator, retriever, builder, _ = build_client()
    service = RepositoryQAService(orchestrator, retriever, builder, CitationAnswerer())
    response = TestClient(create_app(service)).post(
        "/api/v1/questions", json={"query": "How does send work?"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["evidence"][0]["evidence_id"] == "E1"
    assert body["citations"][0]["chunk_id"] == "adapter:1:send"
    assert body["citation_validation"]["valid_evidence_ids"] == ["E1"]

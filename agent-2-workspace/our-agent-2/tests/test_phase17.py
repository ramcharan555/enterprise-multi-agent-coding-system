from fastapi.testclient import TestClient

from app.knowledge.api.app import create_app


def test_health():
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_knowledge_query_endpoint():
    client = TestClient(create_app())

    response = client.post(
        "/knowledge/query",
        json={"query": "What is the architecture?"},
    )

    assert response.status_code == 200

    body = response.json()

    assert "answer" in body
    assert "evidence" in body
    assert "citations" in body


def test_empty_query_is_rejected():
    client = TestClient(create_app())

    response = client.post(
        "/knowledge/query",
        json={"query": "   "},
    )

    assert response.status_code == 400

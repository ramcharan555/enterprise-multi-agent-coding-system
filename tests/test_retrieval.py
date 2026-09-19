import json

import numpy as np

from app.retrieval.searcher import CodeRetriever
from app.retrieval.context import GraphContextExpander


def test_embedding_dimensions():
    with open(
        "data/embeddings.json",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    assert data["count"] == len(data["chunk_ids"])
    assert data["count"] == len(data["embeddings"])
    assert data["dimension"] == len(data["embeddings"][0])


def test_vectors_are_valid():
    with open(
        "data/embeddings.json",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    vectors = np.asarray(
        data["embeddings"],
        dtype=np.float32,
    )

    assert vectors.shape == (
        data["count"],
        data["dimension"],
    )

    assert np.isfinite(vectors).all()


def test_retriever_returns_results():
    retriever = CodeRetriever()

    results = retriever.search(
        "HTTP adapter",
        top_k=3,
    )

    assert len(results) == 3

    for result in results:
        assert "score" in result
        assert "chunk_id" in result
        assert "file_path" in result
        assert "source" in result


def test_retriever_resolves_type_definitions():

    retriever = CodeRetriever()

    result = retriever._resolve_type_definitions(
        {
            "parameter_types": [
                "HTTPAdapter"
            ],
            "return_type": None,
        }
    )

    names = {
        item["name"]
        for item in result
    }

    assert "HTTPAdapter" in names


def test_graph_context_resolves_tests(tmp_path):

    graph_path = tmp_path / "graph.json"
    chunks_path = tmp_path / "chunks.json"

    chunks = [
        {
            "chunk_id": "a.py:1:foo",
            "chunk_type": "function",
            "name": "foo",
            "file_path": "a.py",
            "start_line": 1,
            "end_line": 3,
            "parent": None,
            "imports": [],
            "inherits_from": [],
            "calls": [],
            "tests": [],
        },
        {
            "chunk_id": "test_a.py:1:test_foo",
            "chunk_type": "function",
            "name": "test_foo",
            "file_path": "test_a.py",
            "start_line": 1,
            "end_line": 3,
            "parent": None,
            "imports": [],
            "inherits_from": [],
            "calls": [],
            "tests": ["foo"],
        },
    ]

    graph = {
        "nodes": [
            {
                "id": "a.py:1:foo",
                "node_type": "function",
                "name": "foo",
            },
            {
                "id": "test_a.py:1:test_foo",
                "node_type": "function",
                "name": "test_foo",
            },
        ],
        "edges": [
            {
                "source": "test_a.py:1:test_foo",
                "target": "foo",
                "relationship": "TESTS",
            }
        ],
    }

    chunks_path.write_text(
        json.dumps(chunks),
        encoding="utf-8",
    )

    graph_path.write_text(
        json.dumps(graph),
        encoding="utf-8",
    )

    expander = GraphContextExpander(
        graph_path=graph_path,
        chunks_path=chunks_path,
    )

    result = expander.expand(
        "a.py:1:foo"
    )

    test_names = {
        item["name"]
        for item in result
        if item["relationship"] == "TESTS"
    }

    assert "test_foo" in test_names

def test_find_related_tests(tmp_path):

    graph_path = tmp_path / "graph.json"
    chunks_path = tmp_path / "chunks.json"

    chunks = [
        {
            "chunk_id": "a.py:1:foo",
            "chunk_type": "function",
            "name": "foo",
            "file_path": "a.py",
            "start_line": 1,
            "end_line": 3,
            "parent": None,
            "imports": [],
            "inherits_from": [],
            "calls": [],
            "tests": [],
        },
        {
            "chunk_id": "test_a.py:1:test_foo",
            "chunk_type": "function",
            "name": "test_foo",
            "file_path": "test_a.py",
            "start_line": 1,
            "end_line": 3,
            "parent": None,
            "imports": [],
            "inherits_from": [],
            "calls": [],
            "tests": ["foo"],
        },
    ]

    graph = {
        "nodes": [
            {
                "id": "a.py:1:foo",
                "node_type": "function",
                "name": "foo",
            },
            {
                "id": "test_a.py:1:test_foo",
                "node_type": "function",
                "name": "test_foo",
            },
        ],
        "edges": [
            {
                "source": "test_a.py:1:test_foo",
                "target": "foo",
                "relationship": "TESTS",
            }
        ],
    }

    chunks_path.write_text(
        json.dumps(chunks),
        encoding="utf-8",
    )

    graph_path.write_text(
        json.dumps(graph),
        encoding="utf-8",
    )

    expander = GraphContextExpander(
        graph_path=graph_path,
        chunks_path=chunks_path,
    )

    results = expander.find_related_tests(
        "a.py:1:foo"
    )

    names = {
        result["name"]
        for result in results
    }

    assert "test_foo" in names
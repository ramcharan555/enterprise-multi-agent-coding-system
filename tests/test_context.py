from app.retrieval.context import GraphContextExpander


def test_graph_context_expansion():
    expander = GraphContextExpander()

    chunk_id = "src/requests/adapters.py:634:send"

    results = expander.expand(
        chunk_id,
        max_neighbors=20,
    )

    assert results

    relationships = {
        result["relationship"]
        for result in results
    }

    assert "DEFINED_IN" in relationships
    assert "CALLS" in relationships


def test_graph_context_contains_parent():
    expander = GraphContextExpander()

    results = expander.expand(
        "src/requests/adapters.py:634:send",
        max_neighbors=20,
    )

    names = {
        result["name"]
        for result in results
    }

    assert "HTTPAdapter" in names


def test_graph_context_contains_called_methods():
    expander = GraphContextExpander()

    results = expander.expand(
        "src/requests/adapters.py:634:send",
        max_neighbors=30,
    )

    names = {
        result["name"]
        for result in results
    }

    assert "add_headers" in names
    assert "request_url" in names
    assert "build_response" in names

def test_graph_context_resolves_parameter_types(tmp_path):
    import json

    graph = {
        "nodes": [
            {"id": "function_1"},
            {"id": "type_1"},
        ],
        "edges": [],
    }

    chunks = [
        {
            "chunk_id": "function_1",
            "name": "create_order",
            "chunk_type": "function",
            "file_path": "orders.py",
            "start_line": 1,
            "end_line": 5,
            "source": "def create_order(order: OrderRequest):",
            "parameter_types": ["OrderRequest"],
            "return_type": None,
        },
        {
            "chunk_id": "type_1",
            "name": "OrderRequest",
            "chunk_type": "class",
            "file_path": "models.py",
            "start_line": 1,
            "end_line": 5,
            "source": "class OrderRequest:",
            "parameter_types": [],
            "return_type": None,
        },
    ]

    graph_path = tmp_path / "graph.json"
    chunks_path = tmp_path / "chunks.json"

    graph_path.write_text(
        json.dumps(graph)
    )

    chunks_path.write_text(
        json.dumps(chunks)
    )

    from app.retrieval.context import GraphContextExpander

    expander = GraphContextExpander(
        graph_path=graph_path,
        chunks_path=chunks_path,
    )

    results = expander.expand(
        "function_1"
    )

    type_results = [
        result
        for result in results
        if result["relationship"] == "USES_TYPE"
    ]

    assert len(type_results) == 1
    assert type_results[0]["name"] == "OrderRequest"

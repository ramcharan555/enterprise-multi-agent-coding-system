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

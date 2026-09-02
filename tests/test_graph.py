from app.graph.builder import CodeGraphBuilder


def test_graph_creates_nodes():
    chunks = [
        {
            "chunk_id": "a.py:1:A",
            "chunk_type": "class",
            "name": "A",
            "file_path": "a.py",
            "start_line": 1,
            "end_line": 5,
            "parent": None,
            "imports": [],
            "inherits_from": [],
            "calls": [],
        }
    ]

    graph = CodeGraphBuilder().build(chunks)

    assert "a.py:1:A" in graph.nodes
    assert graph.nodes["a.py:1:A"]["name"] == "A"


def test_graph_creates_relationships():
    chunks = [
        {
            "chunk_id": "a.py:1:A",
            "chunk_type": "class",
            "name": "A",
            "file_path": "a.py",
            "start_line": 1,
            "end_line": 5,
            "parent": None,
            "imports": [],
            "inherits_from": ["Base"],
            "calls": ["helper"],
        }
    ]

    graph = CodeGraphBuilder().build(chunks)

    assert graph.has_edge("a.py:1:A", "Base")
    assert graph["a.py:1:A"]["Base"]["relationship"] == "INHERITS_FROM"

    assert graph.has_edge("a.py:1:A", "helper")
    assert graph["a.py:1:A"]["helper"]["relationship"] == "CALLS"


def test_parent_relationship():
    chunks = [
        {
            "chunk_id": "a.py:1:A",
            "chunk_type": "class",
            "name": "A",
            "file_path": "a.py",
            "start_line": 1,
            "end_line": 5,
            "parent": None,
            "imports": [],
            "inherits_from": [],
            "calls": [],
        },
        {
            "chunk_id": "a.py:2:foo",
            "chunk_type": "method",
            "name": "foo",
            "file_path": "a.py",
            "start_line": 2,
            "end_line": 4,
            "parent": "a.py:1:A",
            "imports": [],
            "inherits_from": [],
            "calls": [],
        },
    ]

    graph = CodeGraphBuilder().build(chunks)

    assert graph.has_edge(
        "a.py:2:foo",
        "a.py:1:A",
    )

    assert (
        graph["a.py:2:foo"]["a.py:1:A"]["relationship"]
        == "DEFINED_IN"
    )
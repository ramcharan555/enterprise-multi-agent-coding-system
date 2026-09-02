from app.agents.tools.repository_search import RepositorySearchTool
from app.agents.tools.symbol_lookup import SymbolLookupTool
from app.agents.tools.graph_traversal import GraphTraversalTool


def test_repository_search_tool():
    class FakeRetriever:
        def search(self, query, top_k=5):
            return [{"query": query, "top_k": top_k}]

    tool = RepositorySearchTool(FakeRetriever())

    result = tool.run("HTTPAdapter", top_k=3)

    assert result[0]["query"] == "HTTPAdapter"
    assert result[0]["top_k"] == 3


def test_symbol_lookup_tool():
    chunks = [
        {"name": "HTTPAdapter"},
        {"name": "send"},
        {"name": "request"},
    ]

    tool = SymbolLookupTool(chunks)

    result = tool.run("send")

    assert len(result) == 1
    assert result[0]["name"] == "send"


def test_graph_traversal_tool():
    class FakeExpander:
        def expand(self, chunk_id, max_neighbors=20):
            return [
                {
                    "chunk_id": chunk_id,
                    "max_neighbors": max_neighbors,
                }
            ]

    tool = GraphTraversalTool(FakeExpander())

    result = tool.run("abc", max_neighbors=10)

    assert result[0]["chunk_id"] == "abc"
    assert result[0]["max_neighbors"] == 10

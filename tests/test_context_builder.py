from app.retrieval.context_builder import ContextBuilder
from app.agents.tools.context_retrieval import ContextRetrievalTool


class FakeAssembler:
    def assemble(self, results, max_chunks=12):
        return list(results)[:max_chunks]

    def format_context(self, context):
        return "\n".join(item["chunk"]["name"] for item in context)


class FakeExpander:
    def __init__(self):
        self.chunks = {
            "root": self._chunk("root", "function"),
            "parent": self._chunk("parent", "class"),
            "type": self._chunk("Request", "class"),
            "test": self._chunk("test_root", "function"),
        }

    @staticmethod
    def _chunk(name, chunk_type):
        return {
            "name": name,
            "chunk_type": chunk_type,
            "file_path": "example.py",
            "start_line": 1,
            "end_line": 2,
        }

    def expand(self, chunk_id, max_neighbors=5):
        assert chunk_id == "root"
        assert max_neighbors == 5
        return [
            self._result("root", "CALLS"),
            self._result("parent", "DEFINED_IN"),
            self._result("type", "USES_TYPE"),
            self._result("test", "TESTS"),
        ]

    def find_related_tests(self, chunk_id):
        assert chunk_id == "root"
        return [self._result("test", "TESTS")]

    def _result(self, chunk_id, relationship):
        return {
            "chunk_id": chunk_id,
            "chunk": self.chunks[chunk_id],
            "relationship": relationship,
        }


def test_context_builder_combines_and_deduplicates_all_context_sources():
    builder = ContextBuilder(FakeAssembler(), FakeExpander())

    results = builder.rank(
        [
            {
                "chunk_id": "root",
                "score": 0.9,
                "chunk": FakeExpander().chunks["root"],
                "type_definitions": [
                    {
                        "chunk_id": "type",
                        "name": "Request",
                        "chunk_type": "class",
                        "file_path": "types.py",
                        "start_line": 1,
                        "end_line": 3,
                    }
                ],
            }
        ]
    )

    by_id = {result["chunk_id"]: result for result in results}

    assert set(by_id) == {"root", "parent", "type", "test"}
    assert by_id["root"]["context_sources"] == ["graph", "semantic"]
    assert by_id["type"]["context_sources"] == ["graph", "type"]
    assert by_id["test"]["context_sources"] == ["graph", "test"]
    assert results[0]["chunk_id"] == "root"


def test_context_builder_can_exclude_type_and_test_context():
    builder = ContextBuilder(FakeAssembler(), FakeExpander())

    results = builder.rank(
        [{"chunk_id": "root", "score": 0.9}],
        include_types=False,
        include_tests=False,
    )

    assert {result["chunk_id"] for result in results} == {"root", "parent"}


def test_context_builder_builds_llm_formatted_context():
    builder = ContextBuilder(FakeAssembler(), FakeExpander())

    formatted = builder.build_formatted(
        [{"chunk_id": "root", "score": 0.9}],
        max_chunks=2,
    )

    assert formatted.splitlines() == ["root", "parent"]


def test_context_retrieval_tool_supports_formatted_builder_output():
    tool = ContextRetrievalTool(FakeAssembler(), FakeExpander())

    formatted = tool.run(
        [{"chunk_id": "root", "score": 0.9}],
        format_context=True,
        max_chunks=1,
    )

    assert formatted == "root"

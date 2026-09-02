from app.retrieval.assembler import ContextAssembler


def test_context_assembler():
    assembler = ContextAssembler()

    results = [
        {
            "chunk_id": "src/requests/adapters.py:599:add_headers",
            "final_score": 0.8,
            "chunk": {
                "name": "add_headers",
                "chunk_type": "method",
                "file_path": "src/requests/adapters.py",
                "start_line": 599,
                "end_line": 611,
            },
        }
    ]

    context = assembler.assemble(results)

    assert len(context) == 1
    assert context[0]["name"] == "add_headers"
    assert context[0]["source"]


def test_context_formatting():
    assembler = ContextAssembler()

    context = [
        {
            "name": "send",
            "file_path": "src/requests/adapters.py",
            "start_line": 634,
            "end_line": 748,
            "source": "def send(self):\n    pass",
        }
    ]

    formatted = assembler.format_context(context)

    assert "send" in formatted
    assert "adapters.py" in formatted
    assert "def send" in formatted
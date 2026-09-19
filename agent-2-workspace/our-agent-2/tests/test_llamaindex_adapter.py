def test_llamaindex_adapter_builds_index():
    adapter = LlamaIndexAdapter()

    adapter.build_index(
        [
            "Authentication must use OAuth2.",
            "All public APIs must be versioned.",
        ]
    )

    assert adapter.index is not None


def test_llamaindex_adapter_queries():
    adapter = LlamaIndexAdapter()

    adapter.build_index(
        [
            "Authentication must use OAuth2.",
            "All public APIs must be versioned.",
        ]
    )

    results = adapter.query(
        "How should authentication work?"
    )

    assert results is not None
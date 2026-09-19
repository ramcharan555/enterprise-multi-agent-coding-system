from app.knowledge.integrations.llamaindex.adapter import LlamaIndexAdapter


def test_llamaindex_index_can_be_persisted(tmp_path):
    adapter = LlamaIndexAdapter()

    adapter.build_index(
        [
            "Authentication must use OAuth2.",
            "All public APIs must be versioned.",
        ]
    )

    persist_dir = tmp_path / "index"

    adapter.save(str(persist_dir))

    assert persist_dir.exists()
    assert any(persist_dir.iterdir())


def test_llamaindex_index_can_be_loaded(tmp_path):
    adapter = LlamaIndexAdapter()

    adapter.build_index(
        [
            "Authentication must use OAuth2.",
            "All public APIs must be versioned.",
        ]
    )

    persist_dir = tmp_path / "index"

    adapter.save(str(persist_dir))

    restored = LlamaIndexAdapter()
    restored.load(str(persist_dir))

    response = restored.query(
        "How should authentication work?"
    )

    assert response is not None


def test_llamaindex_load_missing_index_fails(tmp_path):
    adapter = LlamaIndexAdapter()

    missing_dir = tmp_path / "missing"

    try:
        adapter.load(str(missing_dir))
        assert False
    except FileNotFoundError:
        assert True

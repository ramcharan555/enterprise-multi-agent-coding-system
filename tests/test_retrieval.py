import json

import numpy as np

from app.retrieval.searcher import CodeRetriever


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
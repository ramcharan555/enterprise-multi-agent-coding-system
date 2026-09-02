import json
from pathlib import Path

import numpy as np

from app.embedding.encoder import CodeEmbedder


class CodeRetriever:

    def __init__(
        self,
        embeddings_path: str = "data/embeddings.json",
        chunks_path: str = "data/chunks.json",
    ):
        self.embeddings_path = Path(embeddings_path)
        self.chunks_path = Path(chunks_path)

        with self.embeddings_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        self.chunk_ids = data["chunk_ids"]
        self.vectors = np.asarray(
            data["embeddings"],
            dtype=np.float32,
        )

        with self.chunks_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            chunks = json.load(file)

        self.chunks = {
            chunk["chunk_id"]: chunk
            for chunk in chunks
        }

        self.embedder = CodeEmbedder()

        self._normalize_vectors()

    def _normalize_vectors(self):
        lengths = np.linalg.norm(
            self.vectors,
            axis=1,
            keepdims=True,
        )

        lengths[lengths == 0] = 1

        self.vectors = self.vectors / lengths

    def search(self, query: str, top_k: int = 5):
        query_vector = self.embedder.encode([query])[0]

        query_vector = np.asarray(
            query_vector,
            dtype=np.float32,
        )

        length = np.linalg.norm(query_vector)

        if length != 0:
            query_vector = query_vector / length

        scores = self.vectors @ query_vector

        top_k = min(top_k, len(scores))

        indices = np.argsort(scores)[::-1][:top_k]

        results = []

        for index in indices:
            chunk_id = self.chunk_ids[index]
            chunk = self.chunks.get(chunk_id)

            if chunk is None:
                continue

            results.append(
                {
                    "score": float(scores[index]),
                    "chunk_id": chunk_id,
                    "chunk_type": chunk["chunk_type"],
                    "name": chunk["name"],
                    "file_path": chunk["file_path"],
                    "start_line": chunk["start_line"],
                    "end_line": chunk["end_line"],
                    "source": chunk["source"],
                }
            )

        return results
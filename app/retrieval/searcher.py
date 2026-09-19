import json
from pathlib import Path

import numpy as np

from app.embedding.encoder import CodeEmbedder
from app.retrieval.search import HybridRetriever

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

    def _build_result(
        self,
        score,
        chunk_id,
        chunk,
    ):
        return {
            "score": float(score),
            "chunk_id": chunk_id,
            "chunk_type": chunk["chunk_type"],
            "name": chunk["name"],
            "file_path": chunk["file_path"],
            "start_line": chunk["start_line"],
            "end_line": chunk["end_line"],
            "source": chunk["source"],
            "parameter_types": chunk.get(
                "parameter_types",
                [],
            ),
            "return_type": chunk.get(
                "return_type",
            ),
        }

    def _resolve_type_definitions(self, result):
        type_names = set(
            result.get("parameter_types", [])
        )

        return_type = result.get("return_type")

        if return_type:
            type_names.add(return_type)

        type_names = {
            type_name.split("[")[0].strip()
            for type_name in type_names
        }

        definitions = []

        for chunk in self.chunks.values():
            if (
                chunk["name"] in type_names
                and chunk["chunk_type"] in {
                    "class",
                    "interface",
                }
            ):
                definitions.append(
                    {
                        "chunk_id": chunk["chunk_id"],
                        "name": chunk["name"],
                        "chunk_type": chunk["chunk_type"],
                        "file_path": chunk["file_path"],
                        "start_line": chunk["start_line"],
                        "end_line": chunk["end_line"],
                        "source": chunk["source"],
                    }
                )

        return definitions

    
    def search(
        self,
        query: str,
        top_k: int = 5,
    ):
        query_vector = self.embedder.encode(
            [query]
        )[0]

        hybrid_retriever = HybridRetriever(
            embeddings_path=str(self.embeddings_path),
            chunks_path=str(self.chunks_path),
            graph_path="data/graph.json",
        )

        results = hybrid_retriever.search(
            query_vector=query_vector,
            query=query,
            vector_top_k=max(top_k * 4, 20),
            top_k=top_k,
        )

        final_results = []

        for item in results:
            chunk = item["chunk"]

            result = self._build_result(
                item["final_score"],
                item["chunk_id"],
                chunk,
            )

            result["vector_score"] = item.get(
                "vector_score",
                0.0,
            )

            result["symbol_score"] = item.get(
                "symbol_score",
                0.0,
            )

            result["retrieval_source"] = item.get(
                "source",
                "vector",
            )

            result["type_definitions"] = (
                self._resolve_type_definitions(
                    result
                )
            )

            final_results.append(result)

        return final_results
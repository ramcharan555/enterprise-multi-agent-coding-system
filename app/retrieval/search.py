import json
from pathlib import Path

import numpy as np


class HybridRetriever:

    def __init__(
        self,
        embeddings_path="data/embeddings.json",
        chunks_path="data/chunks.json",
        graph_path="data/graph.json",
    ):
        self.embeddings_path = Path(embeddings_path)
        self.chunks_path = Path(chunks_path)
        self.graph_path = Path(graph_path)

        # Load embeddings
        with self.embeddings_path.open(
            "r",
            encoding="utf-8",
        ) as f:
            embedding_data = json.load(f)

        self.chunk_ids = embedding_data["chunk_ids"]

        self.vectors = np.asarray(
            embedding_data["embeddings"],
            dtype=np.float32,
        )

        # Normalize vectors once.
        norms = np.linalg.norm(
            self.vectors,
            axis=1,
            keepdims=True,
        )

        self.vectors = self.vectors / np.maximum(
            norms,
            1e-12,
        )

        # Load chunks
        with self.chunks_path.open(
            "r",
            encoding="utf-8",
        ) as f:
            chunks = json.load(f)

        self.chunks = {
            chunk["chunk_id"]: chunk
            for chunk in chunks
        }

        # Load graph
        with self.graph_path.open(
            "r",
            encoding="utf-8",
        ) as f:
            graph = json.load(f)

        self.graph_nodes = {
            node["id"]: node
            for node in graph["nodes"]
        }

        self.graph_edges = graph["edges"]

        # Build adjacency lookup.
        self.neighbors = {}

        for edge in self.graph_edges:
            source = edge["source"]
            target = edge["target"]

            self.neighbors.setdefault(
                source,
                set(),
            ).add(target)

            self.neighbors.setdefault(
                target,
                set(),
            ).add(source)

    def vector_search(
        self,
        query_vector,
        top_k=10,
    ):
        query = np.asarray(
            query_vector,
            dtype=np.float32,
        )

        query_norm = np.linalg.norm(query)

        if query_norm == 0:
            return []

        query = query / query_norm

        scores = self.vectors @ query

        count = min(
            top_k,
            len(scores),
        )

        indexes = np.argsort(
            scores
        )[::-1][:count]

        results = []

        for index in indexes:
            chunk_id = self.chunk_ids[index]

            chunk = self.chunks.get(chunk_id)

            if chunk is None:
                continue

            results.append(
                {
                    "chunk_id": chunk_id,
                    "score": float(scores[index]),
                    "chunk": chunk,
                }
            )

        return results

    def expand_graph(
        self,
        results,
        max_neighbors=5,
    ):
        expanded = {}

        for result in results:
            chunk_id = result["chunk_id"]

            expanded[chunk_id] = {
                "chunk_id": chunk_id,
                "score": result["score"],
                "chunk": result["chunk"],
                "source": "vector",
            }

            neighbors = self.neighbors.get(
                chunk_id,
                set(),
            )

            for neighbor_id in list(neighbors)[
                :max_neighbors
            ]:
                if neighbor_id in self.chunks:
                    if neighbor_id not in expanded:
                        expanded[neighbor_id] = {
                            "chunk_id": neighbor_id,
                            "score": 0.0,
                            "chunk": self.chunks[
                                neighbor_id
                            ],
                            "source": "graph",
                        }

        return list(expanded.values())

    def symbol_score(self, query, chunk):
        query_words = {
            word.lower()
            for word in query.replace("_", " ").split()
        }

        name = chunk["name"].lower()

        score = 0.0

        # Exact symbol mention.
        if name in query.lower():
            score += 0.15

        # Individual words from the symbol.
        name_words = set(
            name.replace("_", " ").split()
        )

        overlap = query_words & name_words

        score += 0.05 * len(overlap)

        return score

    def rank_hybrid(
        self,
        results,
        query,
        top_k=5,
    ):
        ranked = []

        for result in results:
            chunk = result["chunk"]

            vector_score = result["score"]

            symbol_score = self.symbol_score(
                query,
                chunk,
            )

            # Prefer actual source code over tests.
            source_bonus = 0.0

            if chunk["file_path"].startswith("tests/"):
                source_bonus = -0.15
            else:
                source_bonus = 0.05

            # Prefer structural code chunks.
            type_bonus = {
                "class": 0.04,
                "method": 0.03,
                "function": 0.02,
            }.get(
                chunk["chunk_type"],
                0.0,
            )

            # Graph-discovered nodes get a smaller score.
            graph_bonus = (
                0.02
                if result["source"] == "graph"
                else 0.0
            )

            final_score = (
                vector_score
                + source_bonus
                + type_bonus
                + graph_bonus
                + symbol_score
            )

            ranked.append(
                {
                    **result,
                    "vector_score": vector_score,
                    "symbol_score": symbol_score,
                    "final_score": final_score,
                }
            )

        ranked.sort(
            key=lambda x: x["final_score"],
            reverse=True,
        )

        return ranked[:top_k]

    def search(
        self,
        query_vector,
        query,
        vector_top_k=10,
        top_k=5,
    ):
        vector_results = self.vector_search(
            query_vector,
            top_k=vector_top_k,
        )

        expanded_results = self.expand_graph(
            vector_results,
        )

        return self.rank_hybrid(
            expanded_results,
            query=query,
            top_k=top_k,
        )
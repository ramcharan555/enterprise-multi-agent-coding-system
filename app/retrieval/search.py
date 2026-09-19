import json
from pathlib import Path
import re

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
        query_text = query.lower().strip()

        name = chunk["name"].lower().strip()

        if not name:
            return 0.0

    # Exact symbol mention.
        if re.search(
            rf"\b{re.escape(name)}\b",
            query_text,
        ):
            return 0.50
 
        query_words = {
            word.lower()
            for word in re.findall(
                r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
                query_text,
            )
        }

        name_words = {
            word.lower()
            for word in name.replace("_", " ").split()
        }

        overlap = query_words & name_words

        return 0.10 * len(overlap)

    def lexical_symbol_search(self, query, top_k=10):
        query_text = query.lower()

    # Common natural-language variants of code symbols.
        aliases = {
            "send": [
                "send",
                "sent",
                "sending",
                "request flow",
                "http request flow",
                "request move through",
                "sends an http request",
                "sends requests",
            ],
            "post": [
                "post",
                "posted",
                "posting",
            ],
            "get": [
                "get",
                "got",
                "getting",
            ],
            "request": [
                "request",
                "requested",
                "requesting",
            ],
        }

        matches = []

        for chunk in self.chunks.values():
            name = chunk.get("name", "").strip()

            if not name:
                continue

            name_lower = name.lower()

            search_terms = aliases.get(
                name_lower,
                {name_lower},
            )

            found = False

            for term in search_terms:
                pattern = (
                    rf"(?<![a-zA-Z0-9_])"
                    rf"{re.escape(term)}"
                    rf"(?![a-zA-Z0-9_])"
                )

                if re.search(
                    pattern,
                    query_text,
                    re.IGNORECASE,
                ):
                    found = True
                    break

            if found:
                matches.append(
                    {
                        "chunk_id": chunk["chunk_id"],
                        "score": 1.0,
                        "chunk": chunk,
                        "source": "lexical",
                    }
                )

        return matches[:top_k]

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
            lexical_bonus = (
                0.80
                if result["source"] == "lexical"
                else 0.0
            )

            final_score = (
                vector_score
                + source_bonus
                + type_bonus
                + graph_bonus
                + symbol_score
                + lexical_bonus
            )

            if symbol_score >= 0.50:
                final_score += 0.25

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

        lexical_results = self.lexical_symbol_search(
            query,
            top_k=top_k * 2,
        )

        combined = {}

        for result in vector_results:
            combined[result["chunk_id"]] = result

        for result in lexical_results:
            chunk_id = result["chunk_id"]

            if chunk_id in combined:
             combined[chunk_id]["source"] = "lexical"
             combined[chunk_id]["score"] = max(
                   combined[chunk_id]["score"],
                  result["score"],
             )
            else:
                combined[chunk_id] = result

        combined_results = list(combined.values())

        expanded_results = self.expand_graph(
            combined_results,
        )

        return self.rank_hybrid(
            expanded_results,
            query=query,
            top_k=top_k,
        )
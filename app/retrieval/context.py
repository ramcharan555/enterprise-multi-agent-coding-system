import json
from pathlib import Path


class GraphContextExpander:

    def __init__(
        self,
        graph_path="data/graph.json",
        chunks_path="data/chunks.json",
    ):
        self.graph_path = Path(graph_path)
        self.chunks_path = Path(chunks_path)

        with self.graph_path.open("r", encoding="utf-8") as f:
            graph = json.load(f)

        with self.chunks_path.open("r", encoding="utf-8") as f:
            chunks = json.load(f)

        self.nodes = {
            node["id"]: node
            for node in graph["nodes"]
        }

        self.chunks = {
            chunk["chunk_id"]: chunk
            for chunk in chunks
        }

        self.symbol_index = {}

        for chunk_id, chunk in self.chunks.items():
            name = chunk["name"]

            self.symbol_index.setdefault(
                name,
                []
            ).append(chunk_id)

        self.outgoing = {}
        self.incoming = {}

        for edge in graph["edges"]:
            source = edge["source"]
            target = edge["target"]
            relationship = edge["relationship"]

            self.outgoing.setdefault(
                source,
                []
            ).append(
                {
                    "relationship": relationship,
                    "target": target,
                }
            )

            self.incoming.setdefault(
                target,
                []
            ).append(
                {
                    "relationship": relationship,
                    "source": source,
                }
            )

    def expand(
        self,
        chunk_id,
        max_neighbors=10,
    ):
        results = []

        # Outgoing relationships
        for edge in self.outgoing.get(chunk_id, []):
            target = edge["target"]

            resolved_ids = self._resolve_symbol(
                target,
                current_chunk_id=chunk_id,
            )

            for resolved_id in resolved_ids:
                if resolved_id in self.chunks:
                    results.append(
                        self._make_result(
                            resolved_id,
                            edge["relationship"],
                        )
                    )

        # Incoming relationships
        for edge in self.incoming.get(chunk_id, []):
            source = edge["source"]

            if source in self.chunks:
                resolved_ids = [source]
            else:
                resolved_ids = self._resolve_symbol(
                    source,
                    current_chunk_id=chunk_id,
                )

            for resolved_id in resolved_ids:
                if resolved_id in self.chunks:
                    results.append(
                        self._make_result(
                            resolved_id,
                            edge["relationship"],
                        )
                    )

        # Resolve symbolic TESTS targets
        for target, edges in self.incoming.items():
            resolved_targets = self._resolve_symbol(
                target,
                current_chunk_id=chunk_id,
            )

            if chunk_id not in resolved_targets:
                continue

            for edge in edges:
                if edge["relationship"] != "TESTS":
                    continue

                source = edge["source"]

                if source in self.chunks:
                    results.append(
                        self._make_result(
                            source,
                            "TESTS",
                        )
                    )

        # Type relationships
        results.extend(
            self._resolve_types(chunk_id)
        )

        # Test metadata relationships
        results.extend(
            self._resolve_tests(chunk_id)
        )

        # Deduplicate
        unique = {}

        for result in results:
            key = (
                result["chunk_id"],
                result["relationship"],
            )

            unique[key] = result

        return list(
            unique.values()
        )[:max_neighbors]

    def _resolve_tests(self, chunk_id):
        results = []

        chunk = self.chunks.get(chunk_id)

        if chunk is None:
            return results

        # Tests written by this chunk
        for test_name in chunk.get(
            "tests",
            [],
        ):
            candidates = self.symbol_index.get(
                test_name,
                [],
            )

            for candidate in candidates:
                candidate_chunk = self.chunks[
                    candidate
                ]

                if candidate_chunk["name"].startswith(
                    "test_"
                ):
                    results.append(
                        self._make_result(
                            candidate,
                            "TESTS",
                        )
                    )

        # Tests covering this chunk
        for edge in self.incoming.get(
            chunk_id,
            [],
        ):
            if edge["relationship"] != "TESTS":
                continue

            source = edge["source"]

            if source in self.chunks:
                results.append(
                    self._make_result(
                        source,
                        "TESTS",
                    )
                )

        return results

    def find_related_tests(
    self,
    chunk_id,
    max_tests=20,
    ):
        results = []

        for edge in self.incoming.get(
            chunk_id,
            [],
        ):
            if edge["relationship"] != "TESTS":
                continue

            source = edge["source"]

            if source in self.chunks:
                results.append(
                    self._make_result(
                        source,
                        "TESTS",
                    )
                )

    # Resolve symbolic TESTS targets
        for target, edges in self.incoming.items():
            resolved_targets = self._resolve_symbol(
                target,
                current_chunk_id=chunk_id,
            )

            if chunk_id not in resolved_targets:
                continue

            for edge in edges:
                if edge["relationship"] != "TESTS":
                    continue

                source = edge["source"]

                if source in self.chunks:
                    results.append(
                        self._make_result(
                            source,
                            "TESTS",
                        )
                    )

        unique = {}

        for result in results:
            unique[result["chunk_id"]] = result

        return list(
            unique.values()
        )[:max_tests]

    def _resolve_types(self, chunk_id):
        chunk = self.chunks.get(chunk_id)

        if chunk is None:
            return []

        type_names = set(
            chunk.get(
                "parameter_types",
                [],
            )
        )

        return_type = chunk.get(
            "return_type"
        )

        if return_type:
            type_names.add(return_type)

        type_names = {
            type_name.split("[")[0].strip()
            for type_name in type_names
        }

        results = []

        for type_name in type_names:
            candidates = self.symbol_index.get(
                type_name,
                [],
            )

            for candidate in candidates:
                candidate_chunk = self.chunks[
                    candidate
                ]

                if candidate_chunk["chunk_type"] in {
                    "class",
                    "interface",
                }:
                    results.append(
                        self._make_result(
                            candidate,
                            "USES_TYPE",
                        )
                    )

        return results

    def _resolve_symbol(
        self,
        symbol,
        current_chunk_id=None,
    ):
        if symbol in self.chunks:
            return [symbol]

        name = symbol.split(".")[-1]

        candidates = self.symbol_index.get(
            name,
            [],
        )

        if not candidates:
            return []

        if current_chunk_id in self.chunks:
            current_file = self.chunks[
                current_chunk_id
            ]["file_path"]

            same_file = [
                candidate
                for candidate in candidates
                if self.chunks[candidate]["file_path"]
                == current_file
            ]

            if same_file:
                return same_file

        return candidates

    def _make_result(
        self,
        chunk_id,
        relationship,
    ):
        chunk = self.chunks[chunk_id]

        return {
            "chunk_id": chunk_id,
            "name": chunk["name"],
            "chunk_type": chunk["chunk_type"],
            "file_path": chunk["file_path"],
            "start_line": chunk["start_line"],
            "end_line": chunk["end_line"],
            "relationship": relationship,
            "chunk": chunk,
        }
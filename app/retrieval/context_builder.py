"""Compose retrieval results into focused, LLM-ready repository context."""

from collections import OrderedDict


class ContextBuilder:
    """Build ranked context from semantic, graph, type, and test signals.

    The builder deliberately accepts the result shapes returned by both
    ``CodeRetriever`` and ``HybridRetriever``.  It keeps the existing
    retrievers and ``ContextAssembler`` independent, while making their
    output usable as one context pipeline.
    """

    RELATIONSHIP_WEIGHTS = {
        "DEFINED_IN": 0.12,
        "USES_TYPE": 0.11,
        "CALLS": 0.10,
        "INHERITS_FROM": 0.09,
        "IMPORTS": 0.08,
        "TESTS": 0.07,
    }

    def __init__(self, assembler, graph_expander=None):
        self.assembler = assembler
        self.graph_expander = graph_expander

    def build(
        self,
        retrieval_results,
        max_chunks=12,
        max_neighbors=5,
        include_types=True,
        include_tests=True,
    ):
        """Return assembled, deduplicated context records.

        Semantic matches remain the primary ranking signal.  A one-hop graph
        expansion contributes structural context, while type definitions and
        related tests are included when those sources expose them.
        """
        ranked = self.rank(
            retrieval_results,
            max_neighbors=max_neighbors,
            include_types=include_types,
            include_tests=include_tests,
        )
        return self.assembler.assemble(ranked, max_chunks=max_chunks)

    def build_formatted(self, retrieval_results, **kwargs):
        """Return ``build`` output in the assembler's LLM prompt format."""
        return self.assembler.format_context(
            self.build(retrieval_results, **kwargs)
        )

    def rank(
        self,
        retrieval_results,
        max_neighbors=5,
        include_types=True,
        include_tests=True,
    ):
        """Return normalized candidates ordered by combined context priority."""
        candidates = []
        roots = []

        for result in retrieval_results or []:
            candidate = self._candidate(result, origin="semantic")
            if candidate is None:
                continue
            candidates.append(candidate)
            roots.append(candidate)

        if self.graph_expander is not None:
            for root in roots:
                chunk_id = root["chunk_id"]

                for result in self.graph_expander.expand(
                    chunk_id,
                    max_neighbors=max_neighbors,
                ):
                    relationship = result.get("relationship")
                    if relationship == "USES_TYPE" and not include_types:
                        continue
                    if relationship == "TESTS" and not include_tests:
                        continue
                    candidate = self._candidate(result, origin="graph")
                    if candidate is not None:
                        candidates.append(candidate)

                if include_types:
                    for result in root["raw"].get("type_definitions", []):
                        candidate = self._candidate(
                            {**result, "relationship": "USES_TYPE"},
                            origin="type",
                        )
                        if candidate is not None:
                            candidates.append(candidate)

                find_related_tests = getattr(
                    self.graph_expander,
                    "find_related_tests",
                    None,
                )
                if include_tests and find_related_tests is not None:
                    for result in find_related_tests(chunk_id):
                        candidate = self._candidate(result, origin="test")
                        if candidate is not None:
                            candidates.append(candidate)

        merged = self._deduplicate(candidates)
        for result in merged:
            result["final_score"] = self._priority(result)

        return sorted(
            merged,
            key=lambda result: (
                -result["final_score"],
                "semantic" not in result["context_sources"],
                result["chunk_id"],
            ),
        )

    def _candidate(self, result, origin):
        chunk_id = result.get("chunk_id")
        if not chunk_id:
            return None

        chunk = result.get("chunk")
        if chunk is None and self.graph_expander is not None:
            chunk = self.graph_expander.chunks.get(chunk_id)
        if chunk is None:
            chunk = self._chunk_from_result(result)
        if chunk is None:
            return None

        return {
            "chunk_id": chunk_id,
            "chunk": chunk,
            "score": self._score(result),
            "relationship": result.get("relationship"),
            "context_sources": {origin},
            "raw": result,
        }

    @staticmethod
    def _chunk_from_result(result):
        required = (
            "name",
            "chunk_type",
            "file_path",
            "start_line",
            "end_line",
        )
        if not all(key in result for key in required):
            return None
        return {key: result[key] for key in required}

    @staticmethod
    def _score(result):
        return float(result.get("final_score", result.get("score", 0.0)))

    def _deduplicate(self, candidates):
        unique = OrderedDict()
        for candidate in candidates:
            existing = unique.get(candidate["chunk_id"])
            if existing is None:
                candidate["relationships"] = set()
                if candidate["relationship"]:
                    candidate["relationships"].add(candidate["relationship"])
                unique[candidate["chunk_id"]] = candidate
                continue

            existing["score"] = max(existing["score"], candidate["score"])
            existing["context_sources"].update(candidate["context_sources"])
            if candidate["relationship"]:
                existing["relationships"].add(candidate["relationship"])

        for candidate in unique.values():
            relationships = sorted(candidate["relationships"])
            candidate["relationships"] = relationships
            candidate["relationship"] = relationships[0] if relationships else None
            candidate["context_sources"] = sorted(candidate["context_sources"])
        return list(unique.values())

    def _priority(self, result):
        relationship_bonus = max(
            (
                self.RELATIONSHIP_WEIGHTS.get(relationship, 0.05)
                for relationship in result["relationships"]
            ),
            default=0.0,
        )
        structural_bonus = {
            "class": 0.03,
            "interface": 0.03,
            "method": 0.02,
            "function": 0.02,
        }.get(result["chunk"].get("chunk_type"), 0.0)
        return result["score"] + relationship_bonus + structural_bonus

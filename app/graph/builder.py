import json
from pathlib import Path

import networkx as nx


class CodeGraphBuilder:

    def __init__(self):
        self.graph = nx.DiGraph()

    def build(self, chunks):
        self.graph.clear()

        for chunk in chunks:
            self.graph.add_node(
                chunk["chunk_id"],
                node_type=chunk["chunk_type"],
                name=chunk["name"],
                file_path=chunk["file_path"],
                start_line=chunk["start_line"],
                end_line=chunk["end_line"],
            )

        for chunk in chunks:
            source = chunk["chunk_id"]

            if chunk.get("parent"):
                self._edge(
                    source,
                    chunk["parent"],
                    "DEFINED_IN",
                )

            for target in chunk.get("imports", []):
                self._edge(source, target, "IMPORTS")

            for target in chunk.get("inherits_from", []):
                self._edge(source, target, "INHERITS_FROM")

            for target in chunk.get("calls", []):
                self._edge(source, target, "CALLS")

        return self.graph

    def _edge(self, source, target, relationship):
        self.graph.add_edge(
            source,
            target,
            relationship=relationship,
        )

    def save(self, output_path):
        output_path = Path(output_path)
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        data = nx.node_link_data(
            self.graph,
            edges="edges",
        )

        output_path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )
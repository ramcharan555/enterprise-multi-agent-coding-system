class ContextRetrievalTool:

    name = "context_retrieval"

    description = (
        "Retrieve and assemble relevant repository context for a query."
    )

    def __init__(self, assembler, graph_expander=None):
        self.assembler = assembler
        self.graph_expander = graph_expander

    def run(self, results, expand_graph=True):
        if not results:
            return []

        if expand_graph and self.graph_expander:
            expanded = []

            for result in results:
                expanded.append(result)

                chunk_id = result.get("chunk_id")

                if chunk_id:
                    neighbors = self.graph_expander.expand(
                        chunk_id,
                        max_neighbors=5,
                    )

                    expanded.extend(neighbors)

            results = self._deduplicate(expanded)

        return self.assembler.assemble(results)

    def _deduplicate(self, results):
        unique = []
        seen = set()

        for result in results:
            chunk_id = result.get("chunk_id")

            if chunk_id in seen:
                continue

            seen.add(chunk_id)
            unique.append(result)

        return unique
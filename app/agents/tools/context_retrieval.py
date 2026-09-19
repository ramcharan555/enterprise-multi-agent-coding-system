from app.retrieval.context_builder import ContextBuilder


class ContextRetrievalTool:

    name = "context_retrieval"

    description = (
        "Retrieve and assemble relevant repository context for a query."
    )

    def __init__(self, assembler, graph_expander=None, context_builder=None):
        self.assembler = assembler
        self.graph_expander = graph_expander
        self.context_builder = context_builder or ContextBuilder(
            assembler,
            graph_expander,
        )

    def run(
        self,
        results,
        expand_graph=True,
        max_chunks=12,
        format_context=False,
    ):
        if not results:
            return "" if format_context else []

        if expand_graph:
            context = self.context_builder.build(
                results,
                max_chunks=max_chunks,
            )
        else:
            context = self.assembler.assemble(
                self._with_chunks(results),
                max_chunks=max_chunks,
            )

        if format_context:
            return self.assembler.format_context(context)
        return context

    def _with_chunks(self, results):
        return [
            candidate
            for candidate in (
                self.context_builder._candidate(result, origin="semantic")
                for result in results
            )
            if candidate is not None
        ]

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

class GraphTraversalTool:

    name = "graph_traversal"

    description = (
        "Find relationships connected to a repository symbol."
    )

    def __init__(self, context_expander):
        self.context_expander = context_expander

    def run(self, chunk_id, max_neighbors=20):
        return self.context_expander.expand(
            chunk_id,
            max_neighbors=max_neighbors,
        )

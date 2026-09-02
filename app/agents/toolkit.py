class AgentToolkit:

    def __init__(
        self,
        repository_search,
        symbol_lookup,
        graph_traversal,
    ):
        self.repository_search = repository_search
        self.symbol_lookup = symbol_lookup
        self.graph_traversal = graph_traversal

    def search_repository(self, query, top_k=5):
        return self.repository_search.run(
            query,
            top_k=top_k,
        )

    def lookup_symbol(self, name):
        return self.symbol_lookup.run(name)

    def traverse_graph(self, symbol, relationship=None):
        return self.graph_traversal.run(
            symbol,
            relationship=relationship,
        )
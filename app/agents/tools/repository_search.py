class RepositorySearchTool:

    name = "repository_search"

    description = (
        "Search the repository for code relevant to a query."
    )

    def __init__(self, retriever):
        self.retriever = retriever

    def run(self, query, top_k=5):
        return self.retriever.search(
            query=query,
            top_k=top_k,
        )

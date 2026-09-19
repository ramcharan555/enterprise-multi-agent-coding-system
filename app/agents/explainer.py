from app.agents.base import BaseAgent


class ExplainerAgent(BaseAgent):

    name = "explainer"

    def run(self, query, context=None):
        if context is None and self.toolkit is not None:
            context = self.toolkit.search_repository(
                query,
                top_k=5,
            )

        return {
            "agent": self.name,
            "query": query,
            "task": "explain",
            "context": context or [],
        }
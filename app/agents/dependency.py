from app.agents.base import BaseAgent


class DependencyAgent(BaseAgent):

    name = "dependency"

    def run(self, query, context=None):
        if context is None and self.toolkit is not None:
            context = self.toolkit.search_repository(
                query,
                top_k=5,
            )

        return {
            "agent": self.name,
            "query": query,
            "task": "dependency",
            "context": context or [],
        }
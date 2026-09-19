from app.agents.base import BaseAgent


class LocatorAgent(BaseAgent):

    name = "locator"

    def run(self, query, context=None):
        results = self.toolkit.search_repository(
            query,
            top_k=5,
        )

        return {
            "agent": self.name,
            "query": query,
            "task": "locate",
            "results": results,
            "context": context or [],
        }
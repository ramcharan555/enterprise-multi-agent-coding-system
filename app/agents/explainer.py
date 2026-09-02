from app.agents.base import BaseAgent


class ExplainerAgent(BaseAgent):

    name = "explainer"

    def run(self, query, context=None):
        return {
            "agent": self.name,
            "query": query,
            "task": "explain",
            "context": context or [],
        }
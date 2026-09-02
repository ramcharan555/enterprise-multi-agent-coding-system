from app.agents.base import BaseAgent


class DependencyAgent(BaseAgent):

    name = "dependency"

    def run(self, query, context=None):
        return {
            "agent": self.name,
            "query": query,
            "task": "dependency",
            "context": context or [],
        }
from app.agents.base import BaseAgent


class DebuggerAgent(BaseAgent):

    name = "debugger"

    def run(self, query, context=None):
        return {
            "agent": self.name,
            "query": query,
            "task": "debug",
            "context": context or [],
        }
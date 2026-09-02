from app.agents.locator import LocatorAgent
from app.agents.explainer import ExplainerAgent
from app.agents.debugger import DebuggerAgent
from app.agents.dependency import DependencyAgent


class AgentOrchestrator:

    def __init__(self, router, repository_search=None):
        self.router = router

        self.agents = {
            "location": LocatorAgent(repository_search),
            "explanation": ExplainerAgent(),
            "debugging": DebuggerAgent(),
            "dependency": DependencyAgent(),
        }

    def run(self, query, context=None):
        route = self.router.route(query)

        intent = route.intent

        agent = self.agents.get(intent)

        if agent is None:
            return {
                "agent": None,
                "intent": intent,
                "query": query,
                "context": context or [],
                "result": None,
            }

        # Location agent needs repository_search.
        # Tests can run without it.
        if intent == "location" and getattr(agent, "repository_search", None) is None:
            result = {
                "agent": agent.name,
                "query": query,
                "task": "locate",
                "results": [],
                "context": context or [],
            }
        else:
            result = agent.run(
                query,
                context=context,
            )

        return {
            "agent": agent.name,
            "intent": intent,
            "query": query,
            "context": context or [],
            "result": result,
        }
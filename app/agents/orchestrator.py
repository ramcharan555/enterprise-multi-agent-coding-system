from app.agents.locator import LocatorAgent
from app.agents.explainer import ExplainerAgent
from app.agents.debugger import DebuggerAgent
from app.agents.dependency import DependencyAgent


class AgentOrchestrator:

    def __init__(self, router, toolkit=None, repository_search=None):
        self.router = router

        if toolkit is None and repository_search is not None:
            toolkit = repository_search

        self.agents = {
            "location": LocatorAgent(toolkit),
            "explanation": ExplainerAgent(toolkit),
            "debugging": DebuggerAgent(toolkit),
            "dependency": DependencyAgent(toolkit),
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

        if intent in {
            "location",
            "explanation",
            "debugging",
            "dependency",
        } and agent.toolkit is None:
            result = {
                "agent": agent.name,
                "query": query,
                "task": agent.name,
                "context": context or [],
            }

            if intent == "location":
                result["results"] = []

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
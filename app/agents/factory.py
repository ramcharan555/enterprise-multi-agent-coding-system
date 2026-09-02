from app.agents.locator import LocatorAgent
from app.agents.explainer import ExplainerAgent
from app.agents.debugger import DebuggerAgent
from app.agents.dependency import DependencyAgent


def create_agents(toolkit):
    return {
        "location": LocatorAgent(toolkit),
        "explanation": ExplainerAgent(toolkit),
        "debugging": DebuggerAgent(toolkit),
        "dependency": DependencyAgent(toolkit),
    }
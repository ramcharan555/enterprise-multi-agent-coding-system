from app.agents.orchestrator import AgentOrchestrator


class FakeRouter:

    def __init__(self, intent):
        self.intent = intent

    def route(self, query):
        class Result:
            pass

        result = Result()
        result.intent = self.intent
        result.confidence = 1.0

        return result


def test_location_agent():
    orchestrator = AgentOrchestrator(
        FakeRouter("location")
    )

    result = orchestrator.run(
        "where is authentication implemented"
    )

    assert result["agent"] == "locator"
    assert result["intent"] == "location"


def test_explanation_agent():
    orchestrator = AgentOrchestrator(
        FakeRouter("explanation")
    )

    result = orchestrator.run(
        "how does HTTPAdapter work"
    )

    assert result["agent"] == "explainer"


def test_debugger_agent():
    orchestrator = AgentOrchestrator(
        FakeRouter("debugging")
    )

    result = orchestrator.run(
        "why does this request fail"
    )

    assert result["agent"] == "debugger"


def test_unknown_agent():
    orchestrator = AgentOrchestrator(
        FakeRouter("unknown")
    )

    result = orchestrator.run(
        "something unknown"
    )

    assert result["agent"] is None
    assert result["result"] is None

def test_dependency_agent():
    orchestrator = AgentOrchestrator(
        FakeRouter("dependency")
    )

    result = orchestrator.run(
        "what calls HTTPAdapter"
    )

    assert result["agent"] == "dependency"
    assert result["intent"] == "dependency"
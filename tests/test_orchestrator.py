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

def test_location_agent_uses_toolkit():

    class FakeToolkit:

        def search_repository(self, query, top_k=5):
            return [
                {
                    "chunk_id": "chunk_1",
                    "name": "HTTPAdapter",
                    "file_path": "requests/adapters.py",
                }
            ]

    orchestrator = AgentOrchestrator(
        FakeRouter("location"),
        repository_search=FakeToolkit(),
    )

    result = orchestrator.run(
        "where is HTTPAdapter implemented"
    )

    assert result["result"]["results"][0]["name"] == "HTTPAdapter"

def test_explanation_agent_uses_toolkit():

    class FakeToolkit:

        def search_repository(self, query, top_k=5):
            return [
                {
                    "chunk_id": "chunk_1",
                    "name": "HTTPAdapter",
                    "file_path": "requests/adapters.py",
                }
            ]

    orchestrator = AgentOrchestrator(
        FakeRouter("explanation"),
        repository_search=FakeToolkit(),
    )

    result = orchestrator.run(
        "how does HTTPAdapter work"
    )

    assert result["result"]["context"][0]["name"] == "HTTPAdapter"

def test_dependency_agent_uses_toolkit():

    class FakeToolkit:

        def search_repository(self, query, top_k=5):
            return [
                {
                    "chunk_id": "chunk_1",
                    "name": "HTTPAdapter",
                    "file_path": "requests/adapters.py",
                }
            ]

    orchestrator = AgentOrchestrator(
        FakeRouter("dependency"),
        repository_search=FakeToolkit(),
    )

    result = orchestrator.run(
        "what calls HTTPAdapter"
    )

    assert result["result"]["context"][0]["name"] == "HTTPAdapter"

def test_debugger_agent_uses_toolkit():

    class FakeToolkit:

        def search_repository(self, query, top_k=5):
            return [
                {
                    "chunk_id": "chunk_1",
                    "name": "HTTPAdapter",
                    "file_path": "requests/adapters.py",
                }
            ]

    orchestrator = AgentOrchestrator(
        FakeRouter("debugging"),
        repository_search=FakeToolkit(),
    )

    result = orchestrator.run(
        "why does HTTPAdapter fail"
    )

    assert result["result"]["context"][0]["name"] == "HTTPAdapter"

def test_end_to_end_location_flow():

    class FakeToolkit:

        def search_repository(self, query, top_k=5):
            return [
                {
                    "chunk_id": "chunk_1",
                    "name": "HTTPAdapter",
                    "file_path": "requests/adapters.py",
                }
            ]

    orchestrator = AgentOrchestrator(
        FakeRouter("location"),
        toolkit=FakeToolkit(),
    )

    result = orchestrator.run(
        "where is HTTPAdapter implemented"
    )

    assert result["agent"] == "locator"
    assert result["intent"] == "location"
    assert result["result"]["results"][0]["name"] == "HTTPAdapter"


def test_end_to_end_explanation_flow():

    class FakeToolkit:

        def search_repository(self, query, top_k=5):
            return [
                {
                    "chunk_id": "chunk_2",
                    "name": "Session",
                    "file_path": "requests/sessions.py",
                }
            ]

    orchestrator = AgentOrchestrator(
        FakeRouter("explanation"),
        toolkit=FakeToolkit(),
    )

    result = orchestrator.run(
        "how does Session work"
    )

    assert result["agent"] == "explainer"
    assert result["intent"] == "explanation"
    assert result["result"]["context"][0]["name"] == "Session"


def test_end_to_end_debugging_flow():

    class FakeToolkit:

        def search_repository(self, query, top_k=5):
            return [
                {
                    "chunk_id": "chunk_3",
                    "name": "HTTPAdapter",
                    "file_path": "requests/adapters.py",
                }
            ]

    orchestrator = AgentOrchestrator(
        FakeRouter("debugging"),
        toolkit=FakeToolkit(),
    )

    result = orchestrator.run(
        "why does HTTPAdapter fail"
    )

    assert result["agent"] == "debugger"
    assert result["intent"] == "debugging"
    assert result["result"]["context"][0]["name"] == "HTTPAdapter"


def test_end_to_end_dependency_flow():

    class FakeToolkit:

        def search_repository(self, query, top_k=5):
            return [
                {
                    "chunk_id": "chunk_4",
                    "name": "HTTPAdapter",
                    "file_path": "requests/adapters.py",
                }
            ]

    orchestrator = AgentOrchestrator(
        FakeRouter("dependency"),
        toolkit=FakeToolkit(),
    )

    result = orchestrator.run(
        "what calls HTTPAdapter"
    )

    assert result["agent"] == "dependency"
    assert result["intent"] == "dependency"
    assert result["result"]["context"][0]["name"] == "HTTPAdapter"
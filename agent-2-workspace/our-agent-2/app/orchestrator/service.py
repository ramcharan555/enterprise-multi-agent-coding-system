from app.orchestrator.orchestrator import Orchestrator
from app.orchestrator.synthesizer import ResponseSynthesizer


class MultiAgentService:
    def __init__(self, code_agent=None, knowledge_agent=None):
        self.orchestrator = Orchestrator()
        self.synthesizer = ResponseSynthesizer()
        self.code_agent = code_agent
        self.knowledge_agent = knowledge_agent

    def query(self, query: str):
        if not query or not query.strip():
            raise ValueError("query must not be empty")

        orchestration_result = self.orchestrator.execute(
            query,
            code_agent=self.code_agent,
            knowledge_agent=self.knowledge_agent,
        )

        return self.synthesizer.synthesize(
            query,
            orchestration_result,
        )
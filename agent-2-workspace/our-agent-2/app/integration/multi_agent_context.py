from app.integration.agent_context import AgentContext


class MultiAgentContextBuilder:
    """Combines independent Agent 1 and Agent 2 results."""

    def build(
        self,
        query: str,
        code_results=None,
        knowledge_results=None,
    ) -> AgentContext:
        if not query or not query.strip():
            raise ValueError("query must not be empty")

        return AgentContext(
            query=query.strip(),
            code_results=list(code_results or []),
            knowledge_results=list(knowledge_results or []),
        )

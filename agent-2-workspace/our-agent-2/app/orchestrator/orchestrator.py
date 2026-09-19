class QueryRoute:
    CODE = "code"
    KNOWLEDGE = "knowledge"
    BOTH = "both"


class Orchestrator:
    def route(self, query: str) -> str:
        if not query or not query.strip():
            raise ValueError("query must not be empty")

        q = query.lower()

        code_terms = (
            "code",
            "function",
            "class",
            "bug",
            "error",
            "implement",
            "modify",
            "fix",
            "python",
            "api",
        )

        knowledge_terms = (
            "architecture",
            "documentation",
            "document",
            "adr",
            "guideline",
            "policy",
            "requirement",
            "standard",
        )

        has_code = any(term in q for term in code_terms)
        has_knowledge = any(term in q for term in knowledge_terms)

        if has_code and has_knowledge:
            return QueryRoute.BOTH

        if has_code:
            return QueryRoute.CODE

        if has_knowledge:
            return QueryRoute.KNOWLEDGE

        return QueryRoute.KNOWLEDGE

    def execute(
        self,
        query,
        code_agent=None,
        knowledge_agent=None,
    ):
        route = self.route(query)

        result = {
            "query": query,
            "route": route,
            "code": None,
            "knowledge": None,
        }

        if route in (QueryRoute.CODE, QueryRoute.BOTH):
            if code_agent is None:
                raise ValueError("code_agent is required")

            result["code"] = code_agent.query(query)

        if route in (QueryRoute.KNOWLEDGE, QueryRoute.BOTH):
            if knowledge_agent is None:
                raise ValueError("knowledge_agent is required")

            result["knowledge"] = knowledge_agent.query(query)

        return result
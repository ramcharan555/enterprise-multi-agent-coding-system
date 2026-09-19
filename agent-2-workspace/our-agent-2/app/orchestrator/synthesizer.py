class ResponseSynthesizer:
    def synthesize(self, query, orchestration_result):
        if not query or not query.strip():
            raise ValueError("query must not be empty")

        if orchestration_result is None:
            raise ValueError("orchestration_result is required")

        route = orchestration_result.get("route")

        code_result = orchestration_result.get("code")
        knowledge_result = orchestration_result.get("knowledge")

        sections = []

        if code_result is not None:
            sections.append(self._format_agent_result(
                "Code Agent",
                code_result,
            ))

        if knowledge_result is not None:
            sections.append(self._format_agent_result(
                "Knowledge Agent",
                knowledge_result,
            ))

        if not sections:
            return {
                "query": query,
                "answer": "No agent produced a result.",
                "route": route,
                "sources": [],
            }

        answer = (
            f"Query: {query}\n\n"
            + "\n\n".join(sections)
        )

        sources = self._collect_sources(
            code_result,
            knowledge_result,
        )

        return {
            "query": query,
            "answer": answer,
            "route": route,
            "sources": sources,
        }

    def _format_agent_result(self, agent_name, result):
        answer = result.get("answer", "")
        evidence = result.get("evidence", [])

        section = f"{agent_name}:\n{answer}"

        if evidence:
            section += "\nEvidence:\n"
            section += "\n".join(
                f"- {item}" for item in evidence
            )

        return section

    def _collect_sources(self, code_result, knowledge_result):
        sources = []

        for result in (code_result, knowledge_result):
            if result is None:
                continue

            evidence = result.get("evidence", [])

            for item in evidence:
                if item not in sources:
                    sources.append(item)

        return sources
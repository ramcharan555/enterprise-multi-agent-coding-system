from app.llm.prompts import SYSTEM_PROMPT, build_prompt


class CodeAnswerer:

    def __init__(self, llm_client):
        self.llm_client = llm_client

    def answer(self, query, context):
        if not context:
            return {
                "answer": (
                    "I could not find enough repository "
                    "context to answer this question."
                ),
                "sources": [],
            }

        user_prompt = build_prompt(
            query,
            context,
        )

        answer = self.llm_client.generate(
            SYSTEM_PROMPT,
            user_prompt,
        )

        sources = self._build_sources(context)

        return {
            "answer": answer,
            "sources": sources,
        }

    def _build_sources(self, context):
        sources = []

        seen = set()

        for item in context:
            source = {
                "file_path": item["file_path"],
                "start_line": item["start_line"],
                "end_line": item["end_line"],
                "name": item["name"],
            }

            key = (
                source["file_path"],
                source["start_line"],
                source["end_line"],
            )

            if key not in seen:
                sources.append(source)
                seen.add(key)

        return sources
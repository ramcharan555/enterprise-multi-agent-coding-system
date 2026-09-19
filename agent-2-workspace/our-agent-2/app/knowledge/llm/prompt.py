from app.knowledge.agent.context import Context


SYSTEM_INSTRUCTION = """
You are an enterprise documentation assistant.

Answer questions using ONLY the supplied evidence.

Rules:
1. Do not invent facts.
2. Do not use unsupported external knowledge.
3. If the evidence is insufficient, say so clearly.
4. Preserve important technical details.
5. Cite the supplied sources.
""".strip()


class GroundedPromptBuilder:
    """Build prompts that constrain the LLM to retrieved evidence."""

    def build(
        self,
        context: Context,
    ) -> str:
        return (
            f"{SYSTEM_INSTRUCTION}\n\n"
            f"QUESTION:\n{context.question}\n\n"
            f"EVIDENCE:\n{context.text}\n\n"
            "ANSWER:\n"
        )
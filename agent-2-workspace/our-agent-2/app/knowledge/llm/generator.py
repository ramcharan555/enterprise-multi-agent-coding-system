from typing import List

from app.knowledge.agent.answer import Answer
from app.knowledge.agent.context import Context
from app.knowledge.llm.prompt import GroundedPromptBuilder
from app.knowledge.llm.provider import LLMProvider


class LLMAnswerGenerator:
    """Generate answers using a pluggable LLM provider."""

    def __init__(
        self,
        provider: LLMProvider,
    ) -> None:
        self.provider = provider
        self.prompt_builder = GroundedPromptBuilder()

    def generate(
        self,
        context: Context,
    ) -> Answer:
        if not context.evidence:
            return Answer(
                question=context.question,
                answer=(
                   "I could not find insufficient evidence "
                   "to answer this question from the available documentation."
                ),
                citations=[],
                grounded=False,
                confidence=0.0,
            )

        prompt = self.prompt_builder.build(
            context
        )

        response = self.provider.generate(
            prompt
        )

        citations = list(
            dict.fromkeys(
                evidence.source
                for evidence in context.evidence
            )
        )

        scores = [
            evidence.score
            for evidence in context.evidence
        ]

        confidence = (
            min(max(sum(scores) / len(scores), 0.0), 1.0)
            if scores
            else 0.0
        )

        return Answer(
            question=context.question,
            answer=response.text,
            citations=citations,
            grounded=True,
            confidence=confidence,
        )
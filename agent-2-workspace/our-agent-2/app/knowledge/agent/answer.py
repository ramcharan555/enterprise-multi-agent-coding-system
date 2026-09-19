from dataclasses import dataclass
from typing import List

from app.knowledge.agent.context import Context


@dataclass
class Answer:
    question: str
    answer: str
    citations: List[str]
    grounded: bool
    confidence: float


class AnswerGenerator:
    """
    Interface for generating grounded answers.

    The initial implementation is deterministic and does not
    require an external LLM. A real LLM can be plugged in later.
    """

    def generate(self, context: Context) -> Answer:
        if not context.evidence:
            return Answer(
                question=context.question,
                answer=(
                    "I could not find supporting information "
                    "in the available documentation."
                ),
                citations=[],
                grounded=False,
                confidence=0.0,
            )

        citations = [
            evidence.source
            for evidence in context.evidence
        ]

        answer_parts = [
            evidence.content
            for evidence in context.evidence
        ]

        return Answer(
            question=context.question,
            answer="\n\n".join(answer_parts),
            citations=list(dict.fromkeys(citations)),
            grounded=True,
            confidence=self._calculate_confidence(
                context
            ),
        )

    @staticmethod
    def _calculate_confidence(
        context: Context,
    ) -> float:
        if not context.evidence:
            return 0.0

        scores = [
            evidence.score
            for evidence in context.evidence
        ]

        average = sum(scores) / len(scores)

        return min(max(average, 0.0), 1.0)
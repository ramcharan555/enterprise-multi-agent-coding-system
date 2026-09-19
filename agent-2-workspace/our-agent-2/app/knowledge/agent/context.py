from dataclasses import dataclass
from typing import List

from app.knowledge.retrieval.evidence import Evidence


@dataclass
class Context:
    question: str
    evidence: List[Evidence]
    text: str


class ContextBuilder:
    """Build grounded context from retrieved evidence."""

    def build(
        self,
        question: str,
        evidence: List[Evidence],
    ) -> Context:
        sections = []

        for index, item in enumerate(evidence, start=1):
            sections.append(
                f"[Source {index}]\n"
                f"Title: {item.title}\n"
                f"Section: {item.section}\n"
                f"Source: {item.source}\n"
                f"Content:\n{item.content}"
            )

        text = "\n\n".join(sections)

        return Context(
            question=question,
            evidence=evidence,
            text=text,
        )
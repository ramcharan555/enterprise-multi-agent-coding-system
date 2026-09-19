from dataclasses import dataclass
from typing import List, Optional

from app.knowledge.agent.answer import (
    Answer,
    AnswerGenerator,
)
from app.knowledge.agent.citations import (
    CitationFormatter,
)
from app.knowledge.agent.confidence import (
    calculate_confidence,
)
from app.knowledge.agent.context import ContextBuilder
from app.knowledge.llm.generator import (
    LLMAnswerGenerator,
)
from app.knowledge.llm.provider import LLMProvider
from app.knowledge.models import DocumentChunk
from app.knowledge.retrieval.embeddings import (
    EmbeddingProvider,
)
from app.knowledge.retrieval.evidence import (
    create_evidence,
)
from app.knowledge.retrieval.hybrid import (
    HybridRetriever,
)


@dataclass
class KnowledgeAgentResponse:
    answer: Answer
    evidence: List
    citations: List[str]


class KnowledgeAgent:
    """End-to-end documentation knowledge agent."""

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        llm_provider: Optional[LLMProvider] = None,
    ) -> None:
        self.retriever = HybridRetriever(
            embedding_provider
        )

        self.context_builder = ContextBuilder()
        self.citation_formatter = CitationFormatter()

        if llm_provider is None:
            self.answer_generator = AnswerGenerator()
        else:
            self.answer_generator = LLMAnswerGenerator(
                llm_provider
            )

    def add_document_chunks(
        self,
        chunks: List[DocumentChunk],
    ) -> None:
        self.retriever.add_many(chunks)

    def ask(
        self,
        question: str,
        top_k: int = 5,
    ) -> KnowledgeAgentResponse:
        results = self.retriever.search(
            question,
            top_k=top_k,
        )

        evidence = [
            create_evidence(chunk, score)
            for chunk, score in results
        ]

        context = self.context_builder.build(
            question,
            evidence,
        )

        answer = self.answer_generator.generate(
            context
        )

        answer.confidence = calculate_confidence(
            evidence
        )

        citations = self.citation_formatter.format(
            evidence
        )

        return KnowledgeAgentResponse(
            answer=answer,
            evidence=evidence,
            citations=citations,
        )
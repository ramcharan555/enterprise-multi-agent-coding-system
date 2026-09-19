"""FastAPI entry point for repository question answering."""

from functools import lru_cache
from typing import Annotated

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

from app.agents.orchestrator import AgentOrchestrator
from app.agents.toolkit import AgentToolkit
from app.agents.tools.graph_traversal import GraphTraversalTool
from app.agents.tools.repository_search import RepositorySearchTool
from app.agents.tools.symbol_lookup import SymbolLookupTool
from app.llm.answerer import CodeAnswerer
from app.llm.client import MockLLMClient
from app.query.router import QueryRouter
from app.retrieval.assembler import ContextAssembler
from app.retrieval.context import GraphContextExpander
from app.retrieval.context_builder import ContextBuilder
from app.retrieval.searcher import CodeRetriever


class RepositoryQuestion(BaseModel):
    """Validated input for a repository question."""

    model_config = ConfigDict(str_strip_whitespace=True)

    query: Annotated[str, Field(min_length=1, max_length=4_000)]
    top_k: Annotated[int, Field(ge=1, le=20)] = 5
    max_context_chunks: Annotated[int, Field(ge=1, le=50)] = 12


class SourceMetadata(BaseModel):
    file_path: str
    start_line: int
    end_line: int
    name: str


class ContextMetadata(SourceMetadata):
    chunk_id: str
    chunk_type: str
    relationship: str | None = None
    score: float | None = None


class EvidenceMetadata(ContextMetadata):
    evidence_id: str


class CitationValidation(BaseModel):
    is_valid: bool
    has_citations: bool
    missing_citations: bool
    valid_evidence_ids: list[str]
    invalid_evidence_ids: list[str]


class RepositoryAnswer(BaseModel):
    query: str
    intent: str
    agent: str | None
    answer: str
    sources: list[SourceMetadata]
    context: list[ContextMetadata]
    evidence: list[EvidenceMetadata] = Field(default_factory=list)
    citations: list[EvidenceMetadata] = Field(default_factory=list)
    citation_validation: CitationValidation = Field(
        default_factory=lambda: CitationValidation(
            is_valid=True,
            has_citations=False,
            missing_citations=True,
            valid_evidence_ids=[],
            invalid_evidence_ids=[],
        )
    )


class RepositoryQAService:
    """Coordinate the existing routing, retrieval, context, and LLM layers."""

    def __init__(self, orchestrator, retriever, context_builder, answerer):
        self.orchestrator = orchestrator
        self.retriever = retriever
        self.context_builder = context_builder
        self.answerer = answerer

    def answer(self, question: RepositoryQuestion) -> RepositoryAnswer:
        orchestration = self.orchestrator.run(question.query)
        retrieval_results = self._retrieval_results(orchestration)

        if not retrieval_results:
            retrieval_results = self.retriever.search(
                question.query,
                top_k=question.top_k,
            )
        else:
            retrieval_results = retrieval_results[:question.top_k]

        context = self.context_builder.build(
            retrieval_results,
            max_chunks=question.max_context_chunks,
        )
        answer = self.answerer.answer(question.query, context)

        return RepositoryAnswer(
            query=question.query,
            intent=orchestration["intent"],
            agent=orchestration["agent"],
            answer=answer["answer"],
            sources=answer["sources"],
            context=[self._context_metadata(item) for item in context],
            evidence=answer.get("evidence", []),
            citations=answer.get("citations", []),
            citation_validation=answer.get("citation_validation")
            or CitationValidation(
                is_valid=True,
                has_citations=False,
                missing_citations=True,
                valid_evidence_ids=[],
                invalid_evidence_ids=[],
            ),
        )

    @staticmethod
    def _retrieval_results(orchestration):
        result = orchestration.get("result") or {}
        return result.get("results") or result.get("context") or []

    @staticmethod
    def _context_metadata(item):
        return {
            "chunk_id": item.get(
                "chunk_id",
                f'{item["file_path"]}:{item["start_line"]}:{item["name"]}',
            ),
            "name": item["name"],
            "chunk_type": item["chunk_type"],
            "file_path": item["file_path"],
            "start_line": item["start_line"],
            "end_line": item["end_line"],
            "relationship": item.get("relationship"),
            "score": item.get("score", 0.0),
        }


def create_repository_qa_service(llm_client=None):
    """Create the production pipeline using the repository's components."""
    retriever = CodeRetriever()
    graph_expander = GraphContextExpander()
    assembler = ContextAssembler()
    context_builder = ContextBuilder(assembler, graph_expander)

    toolkit = AgentToolkit(
        repository_search=RepositorySearchTool(retriever),
        symbol_lookup=SymbolLookupTool(list(retriever.chunks.values())),
        graph_traversal=GraphTraversalTool(graph_expander),
    )
    orchestrator = AgentOrchestrator(QueryRouter(), toolkit=toolkit)
    answerer = CodeAnswerer(llm_client or MockLLMClient())

    return RepositoryQAService(
        orchestrator=orchestrator,
        retriever=retriever,
        context_builder=context_builder,
        answerer=answerer,
    )


@lru_cache
def get_repository_qa_service():
    """Lazily initialize the embedding-backed production service once."""
    return create_repository_qa_service()


def create_app(service=None):
    app = FastAPI(title="Enterprise Repository Q&A API", version="1.0.0")

    @app.post("/api/v1/questions", response_model=RepositoryAnswer)
    def answer_repository_question(question: RepositoryQuestion):
        active_service = service or get_repository_qa_service()
        return active_service.answer(question)

    return app


app = create_app()

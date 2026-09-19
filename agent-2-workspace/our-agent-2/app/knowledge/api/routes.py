from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.knowledge.agent.knowledge_agent import KnowledgeAgent
from app.knowledge.retrieval.embeddings import EmbeddingProvider, HashEmbeddingProvider


router = APIRouter(prefix="/knowledge", tags=["knowledge"])


class KnowledgeQueryRequest(BaseModel):
    query: str = Field(..., min_length=1)


class KnowledgeQueryResponse(BaseModel):
    answer: str
    evidence: list = Field(default_factory=list)
    citations: list = Field(default_factory=list)


def create_agent() -> KnowledgeAgent:
    embedding_provider = HashEmbeddingProvider()
    return KnowledgeAgent(embedding_provider)


@router.post("/query", response_model=KnowledgeQueryResponse)
def query_knowledge(request: KnowledgeQueryRequest):
    query = request.query.strip()

    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    agent = create_agent()
    result = agent.ask(query)

    if isinstance(result, dict):
        return KnowledgeQueryResponse(
            answer=result.get("answer", ""),
            evidence=result.get("evidence", []),
            citations=result.get("citations", []),
        )

    return KnowledgeQueryResponse(answer=str(result))

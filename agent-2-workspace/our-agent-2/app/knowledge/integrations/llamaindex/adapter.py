from typing import List

from llama_index.core import (
    Document,
    VectorStoreIndex,
    Settings,
)

from llama_index.core.embeddings import MockEmbedding
from llama_index.core.llms import MockLLM

from app.knowledge.persistence.index_store import PersistentIndexStore


class LlamaIndexAdapter:
    """Adapter around LlamaIndex for repository knowledge retrieval."""

    def __init__(self):
        self.index = None

        # Offline deterministic configuration.
        Settings.embed_model = MockEmbedding(embed_dim=8)
        Settings.llm = MockLLM()

    def build_index(self, texts: List[str]) -> None:
        documents = [
            Document(
                text=text,
                metadata={
                    "source": "enterprise-coding-agent",
                },
            )
            for text in texts
        ]

        self.index = VectorStoreIndex.from_documents(
            documents,
            embed_model=Settings.embed_model,
        )

    def save(self, persist_dir: str) -> None:
        if self.index is None:
            raise RuntimeError("Index has not been built.")

        store = PersistentIndexStore(persist_dir)
        store.save(self.index)

    def load(self, persist_dir: str) -> None:
        store = PersistentIndexStore(persist_dir)
        self.index = store.load()

    def query(self, question: str):
        if self.index is None:
            raise RuntimeError("Index has not been built.")

        query_engine = self.index.as_query_engine(
            llm=Settings.llm,
        )

        return query_engine.query(question)

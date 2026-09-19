from pathlib import Path

from llama_index.core import (
    StorageContext,
    load_index_from_storage,
)


class PersistentIndexStore:
    """Persist and reload a LlamaIndex index from local disk."""

    def __init__(self, persist_dir: str):
        self.persist_dir = Path(persist_dir)

    def save(self, index) -> None:
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        index.storage_context.persist(
            persist_dir=str(self.persist_dir)
        )

    def load(self):
        if not self.persist_dir.exists():
            raise FileNotFoundError(
                f"Persisted index not found: {self.persist_dir}"
            )

        storage_context = StorageContext.from_defaults(
            persist_dir=str(self.persist_dir)
        )

        return load_index_from_storage(storage_context)

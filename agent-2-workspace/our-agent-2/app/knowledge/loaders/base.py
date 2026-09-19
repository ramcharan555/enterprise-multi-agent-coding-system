from abc import ABC, abstractmethod
from pathlib import Path

from app.knowledge.models import Document


class DocumentLoader(ABC):
    """Base interface for all document loaders."""

    @abstractmethod
    def load(self, path: Path) -> Document:
        """Load a file and convert it into a Document."""
        raise NotImplementedError
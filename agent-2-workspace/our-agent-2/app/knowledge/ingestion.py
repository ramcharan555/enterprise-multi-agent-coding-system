from pathlib import Path

from app.knowledge.loaders import (
    DOCXDocumentLoader,
    DocumentLoader,
    HTMLDocumentLoader,
    PDFDocumentLoader,
    TextDocumentLoader,
)
from app.knowledge.models import Document


class DocumentIngestionPipeline:
    """Selects the appropriate loader and ingests documents."""

    def __init__(self) -> None:
        self._loaders: dict[str, DocumentLoader] = {
            ".md": TextDocumentLoader(),
            ".markdown": TextDocumentLoader(),
            ".txt": TextDocumentLoader(),
            ".rst": TextDocumentLoader(),
            ".pdf": PDFDocumentLoader(),
            ".docx": DOCXDocumentLoader(),
            ".html": HTMLDocumentLoader(),
            ".htm": HTMLDocumentLoader(),
        }

    def ingest(self, path: Path) -> Document:
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(
                f"Document does not exist: {path}"
            )

        if not path.is_file():
            raise ValueError(
                f"Expected a file, got: {path}"
            )

        extension = path.suffix.lower()

        loader = self._loaders.get(extension)

        if loader is None:
            raise ValueError(
                f"Unsupported document type: {extension}"
            )

        return loader.load(path)
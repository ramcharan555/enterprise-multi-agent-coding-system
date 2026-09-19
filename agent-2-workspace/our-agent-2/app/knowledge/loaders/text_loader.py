from pathlib import Path

from app.knowledge.loaders.base import DocumentLoader
from app.knowledge.models import Document, DocumentType


class TextDocumentLoader(DocumentLoader):
    """Loader for Markdown, README, RST, and plain-text documents."""

    SUPPORTED_EXTENSIONS = {".md", ".markdown", ".txt", ".rst"}

    def load(self, path: Path) -> Document:
        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {path.suffix}"
            )

        content = path.read_text(encoding="utf-8")

        document_type = self._detect_document_type(path)

        return Document(
            document_id=str(path.resolve()),
            title=path.stem,
            content=content,
            source=str(path),
            document_type=document_type,
        )

    @staticmethod
    def _detect_document_type(path: Path) -> DocumentType:
        name = path.name.lower()

        if name in {"readme.md", "readme.rst", "readme.txt"}:
            return DocumentType.README

        if "architecture" in name:
            return DocumentType.ARCHITECTURE

        if "adr" in name:
            return DocumentType.ADR

        if "api" in name:
            return DocumentType.API_DOCUMENTATION

        if "guide" in name or "guideline" in name:
            return DocumentType.DEVELOPER_GUIDELINE

        return DocumentType.GENERAL
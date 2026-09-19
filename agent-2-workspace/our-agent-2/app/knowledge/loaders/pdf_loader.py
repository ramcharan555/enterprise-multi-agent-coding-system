from pathlib import Path

from pypdf import PdfReader

from app.knowledge.loaders.base import DocumentLoader
from app.knowledge.models import Document, DocumentType


class PDFDocumentLoader(DocumentLoader):
    """Loader for PDF documents."""

    SUPPORTED_EXTENSIONS = {".pdf"}

    def load(self, path: Path) -> Document:
        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {path.suffix}"
            )

        reader = PdfReader(str(path))

        pages = []
        for page in reader.pages:
            text = page.extract_text() or ""
            pages.append(text)

        content = "\n\n".join(pages)

        return Document(
            document_id=str(path.resolve()),
            title=path.stem,
            content=content,
            source=str(path),
            document_type=self._detect_document_type(path),
            metadata={
                "page_count": len(reader.pages),
            },
        )

    @staticmethod
    def _detect_document_type(path: Path) -> DocumentType:
        name = path.name.lower()

        if "architecture" in name:
            return DocumentType.ARCHITECTURE

        if "adr" in name:
            return DocumentType.ADR

        if "api" in name:
            return DocumentType.API_DOCUMENTATION

        if "guide" in name or "guideline" in name:
            return DocumentType.DEVELOPER_GUIDELINE

        return DocumentType.GENERAL
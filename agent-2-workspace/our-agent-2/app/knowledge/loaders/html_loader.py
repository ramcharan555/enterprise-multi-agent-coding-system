from pathlib import Path

from bs4 import BeautifulSoup

from app.knowledge.loaders.base import DocumentLoader
from app.knowledge.models import Document, DocumentType


class HTMLDocumentLoader(DocumentLoader):
    """Loader for HTML documents."""

    SUPPORTED_EXTENSIONS = {".html", ".htm"}

    def load(self, path: Path) -> Document:
        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {path.suffix}"
            )

        html = path.read_text(encoding="utf-8")

        soup = BeautifulSoup(html, "html.parser")

        # Remove elements that do not contain useful document content.
        for element in soup(["script", "style", "noscript"]):
            element.decompose()

        content = soup.get_text(
            separator="\n",
            strip=True,
        )

        return Document(
            document_id=str(path.resolve()),
            title=self._extract_title(soup, path),
            content=content,
            source=str(path),
            document_type=self._detect_document_type(path),
            metadata={
                "html": True,
            },
        )

    @staticmethod
    def _extract_title(soup: BeautifulSoup, path: Path) -> str:
        if soup.title and soup.title.string:
            return soup.title.string.strip()

        heading = soup.find(["h1", "h2"])

        if heading:
            return heading.get_text(strip=True)

        return path.stem

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
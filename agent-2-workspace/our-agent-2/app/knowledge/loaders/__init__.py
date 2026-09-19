from .base import DocumentLoader
from .docx_loader import DOCXDocumentLoader
from .html_loader import HTMLDocumentLoader
from .pdf_loader import PDFDocumentLoader
from .text_loader import TextDocumentLoader

__all__ = [
    "DocumentLoader",
    "DOCXDocumentLoader",
    "HTMLDocumentLoader",
    "PDFDocumentLoader",
    "TextDocumentLoader",
]
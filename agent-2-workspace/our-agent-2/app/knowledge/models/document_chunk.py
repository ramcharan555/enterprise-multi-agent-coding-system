from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class DocumentChunk:
    """A retrievable section of a document."""

    chunk_id: str
    document_id: str

    content: str

    title: str
    section: str

    chunk_index: int

    metadata: Dict[str, Any] = field(default_factory=dict)
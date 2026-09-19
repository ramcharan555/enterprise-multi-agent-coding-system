from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class Document:
    """Represents a source document in the enterprise knowledge base."""

    document_id: str
    title: str
    content: str

    source: str
    document_type: str

    version: Optional[str] = None
    authority: Optional[str] = None
    scope: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    metadata: Dict[str, Any] = field(default_factory=dict)
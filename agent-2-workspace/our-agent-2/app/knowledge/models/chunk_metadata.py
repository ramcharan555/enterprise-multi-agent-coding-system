from dataclasses import dataclass
from typing import Optional


@dataclass
class ChunkMetadata:
    source: str
    document_type: str
    section: str
    section_level: int

    version: Optional[str] = None
    authority: Optional[str] = None
    scope: Optional[str] = None
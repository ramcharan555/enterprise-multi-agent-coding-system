from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class FileInfo:
    path: Path
    relative_path: str
    language: Optional[str]
    size_bytes: int

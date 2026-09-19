from dataclasses import dataclass
from typing import Optional


@dataclass
class EnterpriseMetadata:
    version: Optional[str] = None
    authority: Optional[str] = None
    scope: Optional[str] = None
    status: str = "active"
    priority: int = 0

    def is_active(self) -> bool:
        return self.status.lower() == "active"
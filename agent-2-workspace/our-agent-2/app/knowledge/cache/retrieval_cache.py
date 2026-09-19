from dataclasses import dataclass
from typing import Any, Dict, Optional
import hashlib
import json
import time


@dataclass
class CacheEntry:
    key: str
    value: Any
    created_at: float
    ttl_seconds: Optional[float] = None

    def is_expired(self, now: Optional[float] = None) -> bool:
        if self.ttl_seconds is None:
            return False

        current = time.time() if now is None else now
        return current >= self.created_at + self.ttl_seconds


class RetrievalCache:
    def __init__(self, default_ttl_seconds: Optional[float] = None):
        self.default_ttl_seconds = default_ttl_seconds
        self._entries: Dict[str, CacheEntry] = {}

    @staticmethod
    def make_key(query: str, filters: Optional[dict] = None) -> str:
        payload = {
            "query": query.strip(),
            "filters": filters or {},
        }

        encoded = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

        return hashlib.sha256(encoded).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        entry = self._entries.get(key)

        if entry is None:
            return None

        if entry.is_expired():
            del self._entries[key]
            return None

        return entry.value

    def set(
        self,
        key: str,
        value: Any,
        ttl_seconds: Optional[float] = None,
    ) -> None:
        self._entries[key] = CacheEntry(
            key=key,
            value=value,
            created_at=time.time(),
            ttl_seconds=(
                self.default_ttl_seconds
                if ttl_seconds is None
                else ttl_seconds
            ),
        )

    def delete(self, key: str) -> bool:
        return self._entries.pop(key, None) is not None

    def clear(self) -> None:
        self._entries.clear()

    def __len__(self) -> int:
        return len(self._entries)

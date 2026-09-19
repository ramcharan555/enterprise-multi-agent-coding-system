from typing import Dict

from app.knowledge.models import DocumentChunk


DEFAULT_AUTHORITY_PRIORITY: Dict[str, int] = {
    "architecture-team": 100,
    "security-team": 90,
    "platform-team": 80,
    "engineering-team": 70,
    "developer": 50,
    "unknown": 0,
}


def authority_score(chunk: DocumentChunk) -> int:
    authority = chunk.metadata.get(
        "authority",
        "unknown",
    )

    return DEFAULT_AUTHORITY_PRIORITY.get(
        str(authority).lower(),
        0,
    )


def priority_score(chunk: DocumentChunk) -> int:
    value = chunk.metadata.get(
        "priority",
        0,
    )

    try:
        return int(value)
    except (TypeError, ValueError):
        return 0
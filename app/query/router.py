import re
from dataclasses import dataclass


@dataclass
class QueryIntent:
    intent: str
    query: str
    confidence: float


class QueryRouter:

    def route(self, query: str) -> QueryIntent:
        text = query.lower().strip()

        if not text:
            return QueryIntent(
                intent="unknown",
                query=query,
                confidence=0.0,
            )

        if self._matches(
            text,
            [
                r"\bwhere\b",
                r"\blocated\b",
                r"\bimplemented\b",
                r"\bdefined\b",
            ],
        ):
            return QueryIntent(
                intent="location",
                query=query,
                confidence=0.9,
            )

        if self._matches(
            text,
            [
                r"\bhow\b",
                r"\bflow\b",
                r"\bworks\b",
                r"\barchitecture\b",
            ],
        ):
            return QueryIntent(
                intent="explanation",
                query=query,
                confidence=0.9,
            )

        if self._matches(
            text,
            [
                r"\bcaller",
                r"\bcallers",
                r"\bcalled by\b",
                r"\bdepends on\b",
                r"\bdependency\b",
            ],
        ):
            return QueryIntent(
                intent="dependency",
                query=query,
                confidence=0.9,
            )

        if self._matches(
            text,
            [
                r"\bwhy\b",
                r"\bfail",
                r"\berror\b",
                r"\bbug\b",
                r"\bissue\b",
            ],
        ):
            return QueryIntent(
                intent="debugging",
                query=query,
                confidence=0.85,
            )

        if self._matches(
            text,
            [
                r"\badd\b",
                r"\bchange\b",
                r"\bmodify\b",
                r"\bimplement\b",
                r"\bfix\b",
                r"\brefactor\b",
            ],
        ):
            return QueryIntent(
                intent="coding",
                query=query,
                confidence=0.85,
            )

        return QueryIntent(
            intent="general",
            query=query,
            confidence=0.5,
        )

    @staticmethod
    def _matches(text, patterns):
        return any(
            re.search(pattern, text)
            for pattern in patterns
        )
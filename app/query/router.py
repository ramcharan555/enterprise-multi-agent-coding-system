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

        # -------------------------
        # LOCATION
        # -------------------------
        if self._matches(
            text,
            [
                r"\bwhere\b",
                r"\blocated\b",
                r"\bimplemented\b",
                r"\bdefined\b",
                r"\bwhich file\b",
                r"\bwhat file\b",
                r"\bfile is\b",
                r"\bsource file\b",
            ],
        ):
            return QueryIntent(
                intent="location",
                query=query,
                confidence=0.95,
            )

        # -------------------------
        # DEPENDENCY
        # -------------------------
        if self._matches(
            text,
            [
                r"\bwhat calls\b",
                r"\bwho calls\b",
                r"\bwhich code calls\b",
                r"\bcaller\b",
                r"\bcallers\b",
                r"\bcalled by\b",
                r"\bdepends on\b",
                r"\bdepend on\b",
                r"\bdependency\b",
                r"\bdependencies\b",
                r"\bwhat depends\b",
                r"\bwhich code depends\b",
                r"\buses\b",
                r"\bused by\b",
                r"\bwhich functions call\b",
                r"\bwhich functions use\b",
            ],
        ):
            return QueryIntent(
                intent="dependency",
                query=query,
                confidence=0.95,
            )

        # -------------------------
        # DEBUGGING
        # -------------------------
        if self._matches(
            text,
            [
                r"\bwhy\b",
                r"\bfail\b",
                r"\bfailed\b",
                r"\berror\b",
                r"\bbug\b",
                r"\bissue\b",
                r"\bexception\b",
                r"\bcrash\b",
            ],
        ):
            return QueryIntent(
                intent="debugging",
                query=query,
                confidence=0.9,
            )

        # -------------------------
        # CODING
        # -------------------------
        if self._matches(
            text,
            [
                r"\badd\b",
                r"\bchange\b",
                r"\bmodify\b",
                r"\bimplement\b",
                r"\bfix\b",
                r"\brefactor\b",
                r"\bwrite\b",
                r"\bcreate\b",
                r"\bupdate\b",
            ],
        ):
            return QueryIntent(
                intent="coding",
                query=query,
                confidence=0.9,
            )

        # -------------------------
        # EXPLANATION
        # -------------------------
        if self._matches(
            text,
            [
                r"\bhow\b",
                r"\bflow\b",
                r"\bworks\b",
                r"\bexplain\b",
                r"\bexplanation\b",
                r"\bwhat does\b",
                r"\bwhat is\b",
                r"\bpurpose\b",
                r"\bdescribe\b",
                r"\bwhy does\b",
                r"\bperforms\b",
                r"\bperform\b",
                r"\bresponsible for\b",
                r"\bwhat happens\b",
                r"\bwhich component\b",
                r"\bwhich class\b",
                r"\bwhat part of the code\b",
                r"\bwhat code manages\b",
            ],
        ):
            return QueryIntent(
                intent="explanation",
                query=query,
                confidence=0.9,
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
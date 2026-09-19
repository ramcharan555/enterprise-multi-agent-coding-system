import re
from dataclasses import dataclass
from typing import List


@dataclass
class SearchQuery:
    original: str
    terms: List[str]

    @classmethod
    def parse(cls, query: str) -> "SearchQuery":
        terms = re.findall(
            r"\b[a-zA-Z0-9_/-]+\b",
            query.lower(),
        )

        return cls(
            original=query,
            terms=list(dict.fromkeys(terms)),
        )
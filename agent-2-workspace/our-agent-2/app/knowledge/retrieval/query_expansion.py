from typing import List


DEFAULT_SYNONYMS = {
    "authentication": [
        "authentication",
        "auth",
        "login",
        "identity",
        "credentials",
    ],
    "authorization": [
        "authorization",
        "permissions",
        "access control",
        "roles",
    ],
    "database": [
        "database",
        "db",
        "storage",
        "persistence",
    ],
    "api": [
        "api",
        "endpoint",
        "service",
        "interface",
    ],
    "security": [
        "security",
        "secure",
        "encryption",
        "credentials",
    ],
}


class QueryExpander:
    """
    Expands important enterprise/software queries with related concepts.
    """

    def expand(self, query: str) -> List[str]:
        query_lower = query.lower()

        expanded = [query]

        for key, synonyms in DEFAULT_SYNONYMS.items():
            if key in query_lower:
                expanded.extend(synonyms)

        return list(dict.fromkeys(expanded))
from dataclasses import dataclass
from typing import List


@dataclass
class DocumentRelationship:
    source_document_id: str
    target_document_id: str
    relationship_type: str


class DocumentRelationshipStore:
    """Simple in-memory document relationship store."""

    def __init__(self) -> None:
        self._relationships: List[DocumentRelationship] = []

    def add(
        self,
        source_document_id: str,
        target_document_id: str,
        relationship_type: str,
    ) -> DocumentRelationship:
        relationship = DocumentRelationship(
            source_document_id=source_document_id,
            target_document_id=target_document_id,
            relationship_type=relationship_type,
        )

        self._relationships.append(relationship)

        return relationship

    def find_related(
        self,
        document_id: str,
    ) -> List[DocumentRelationship]:
        return [
            relationship
            for relationship in self._relationships
            if (
                relationship.source_document_id == document_id
                or relationship.target_document_id == document_id
            )
        ]
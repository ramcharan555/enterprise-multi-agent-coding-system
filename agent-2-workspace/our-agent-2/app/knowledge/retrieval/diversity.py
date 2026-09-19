from typing import List


class RetrievalDiversifier:
    """
    Prevents retrieval results from being dominated by one document.
    """

    def diversify(
        self,
        candidates: List[object],
        max_results: int = 5,
        max_per_document: int = 2,
    ) -> List[object]:

        selected = []
        document_counts = {}

        for candidate in candidates:
            document_id = (
                getattr(candidate, "document_id", None)
                or getattr(candidate, "source", None)
                or getattr(candidate, "file_path", None)
                or "unknown"
            )

            count = document_counts.get(document_id, 0)

            if count >= max_per_document:
                continue

            selected.append(candidate)
            document_counts[document_id] = count + 1

            if len(selected) >= max_results:
                break

        return selected
from app.llm.prompts import SYSTEM_PROMPT, build_prompt
from app.llm.evidence import build_evidence, source_metadata, validate_citations


class CodeAnswerer:

    def __init__(self, llm_client):
        self.llm_client = llm_client

    def answer(self, query, context):
        if not context:
            return {
                "answer": (
                    "I could not find enough repository "
                    "context to answer this question."
                ),
                "sources": [],
                "evidence": [],
                "citations": [],
                "citation_validation": {
                    "is_valid": True,
                    "has_citations": False,
                    "missing_citations": True,
                    "valid_evidence_ids": [],
                    "invalid_evidence_ids": [],
                },
            }

        evidence = build_evidence(context)
        user_prompt = build_prompt(
            query,
            context,
            evidence,
        )

        answer = self.llm_client.generate(
            SYSTEM_PROMPT,
            user_prompt,
        )

        sources = self._build_sources(context)
        citation_validation = validate_citations(answer, evidence)
        evidence_by_id = {item["evidence_id"]: item for item in evidence}

        return {
            "answer": answer,
            "sources": sources,
            "evidence": evidence,
            "citations": [
                evidence_by_id[evidence_id]
                for evidence_id in citation_validation["valid_evidence_ids"]
            ],
            "citation_validation": citation_validation,
        }

    def _build_sources(self, context):
        sources = []

        seen = set()

        for item in context:
            source = source_metadata(item)

            key = (
            source["chunk_id"],
            source["start_line"],
            source["end_line"],
            )

            if key not in seen:
                sources.append(source)
                seen.add(key)

        return sources

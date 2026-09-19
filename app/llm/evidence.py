"""Deterministic evidence and citation helpers for repository answers."""

import re


_CITATION_PATTERN = re.compile(r"\[([Ee][^\]\s]*)\]")


def evidence_identity(item):
    """Return the stable identity used to merge equivalent context records."""
    chunk_id = item.get("chunk_id")
    if chunk_id:
        return ("chunk_id", str(chunk_id))
    return (
        "location",
        str(item.get("file_path", "")),
        item.get("start_line"),
        item.get("end_line"),
        str(item.get("name", "")),
        str(item.get("chunk_type", "")),
    )


def source_metadata(item):
    """Normalize a context record without discarding retrieval metadata."""
    fallback_chunk_id = "{file_path}:{start_line}:{name}".format(
        file_path=item["file_path"],
        start_line=item["start_line"],
        name=item["name"],
    )
    return {
        "chunk_id": item.get("chunk_id") or fallback_chunk_id,
        "file_path": item["file_path"],
        "start_line": item["start_line"],
        "end_line": item["end_line"],
        "name": item["name"],
        "chunk_type": item["chunk_type"],
        "relationship": item.get("relationship"),
        "score": item.get("score"),
    }


def build_evidence(context):
    """Assign E1, E2, ... in first-seen context order and deduplicate records."""
    evidence = []
    seen = set()
    for item in context or []:
        identity = evidence_identity(item)
        if identity in seen:
            continue
        seen.add(identity)
        evidence.append({"evidence_id": f"E{len(evidence) + 1}", **source_metadata(item)})
    return evidence


def validate_citations(answer, evidence):
    """Validate all ``[E<number>]`` references without modifying model output."""
    known_ids = {item["evidence_id"] for item in evidence}
    cited_ids = []
    for evidence_id in _CITATION_PATTERN.findall(answer or ""):
        if evidence_id not in cited_ids:
            cited_ids.append(evidence_id)

    valid_ids = [evidence_id for evidence_id in cited_ids if evidence_id in known_ids]
    invalid_ids = [evidence_id for evidence_id in cited_ids if evidence_id not in known_ids]
    return {
        "is_valid": not invalid_ids,
        "has_citations": bool(cited_ids),
        "missing_citations": not cited_ids,
        "valid_evidence_ids": valid_ids,
        "invalid_evidence_ids": invalid_ids,
    }

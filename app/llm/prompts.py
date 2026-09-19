from app.llm.evidence import build_evidence, evidence_identity


SYSTEM_PROMPT = """You are an expert software engineer.

Answer questions about a code repository using ONLY the provided repository context.

Rules:
1. Do not invent files, functions, classes, or behavior.
2. Explain the actual execution flow when possible.
3. Cite every repository claim with one or more supplied evidence IDs in the exact form [E1].
4. Only use evidence IDs supplied in the repository context; never invent evidence IDs.
5. Do not invent files, symbols, line numbers, or behavior.
6. Distinguish directly observed code from reasonable inference.
7. If the context is insufficient, say so.
8. Keep the answer focused on the user's question.
"""


def build_prompt(query, context, evidence=None):
    evidence = evidence if evidence is not None else build_evidence(context)
    ids_by_identity = {}
    for item in context:
        identity = evidence_identity(item)
        if identity not in ids_by_identity:
            ids_by_identity[identity] = evidence[len(ids_by_identity)]["evidence_id"]
    sections = []

    for item in context:
        sections.append(
            f"""EVIDENCE ID: [{ids_by_identity[evidence_identity(item)]}]
CHUNK ID: {item.get('chunk_id', f"{item['file_path']}:{item['start_line']}:{item['name']}")}
FILE: {item['file_path']}
LINES: {item['start_line']}-{item['end_line']}
SYMBOL: {item['name']}
TYPE: {item['chunk_type']}

```python
{item['source']}
```"""
        )

    repository_context = "\n\n".join(sections)

    return f"""User question:

{query}

Repository context:

{repository_context}

Answer the user's question using the repository context above. Cite repository
claims only with the supplied evidence IDs, such as [E1].
"""

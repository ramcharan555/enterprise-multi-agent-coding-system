SYSTEM_PROMPT = """You are an expert software engineer.

Answer questions about a code repository using ONLY the provided repository context.

Rules:
1. Do not invent files, functions, classes, or behavior.
2. Explain the actual execution flow when possible.
3. Mention relevant file paths and line numbers.
4. Distinguish directly observed code from reasonable inference.
5. If the context is insufficient, say so.
6. Keep the answer focused on the user's question.
"""


def build_prompt(query, context):
    sections = []

    for item in context:
        sections.append(
            f"""FILE: {item['file_path']}
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

Answer the user's question using the repository context above.
"""
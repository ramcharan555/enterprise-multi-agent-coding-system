from pathlib import Path


class ContextAssembler:

    def __init__(self, repository_root="repositories/requests"):
        self.repository_root = Path(repository_root)

    def load_source(self, chunk):
        file_path = self.repository_root / chunk["file_path"]

        if not file_path.exists():
            return ""

        try:
            lines = file_path.read_text(
                encoding="utf-8"
            ).splitlines()

            start = max(chunk["start_line"] - 1, 0)
            end = chunk["end_line"]

            return "\n".join(lines[start:end])

        except (OSError, UnicodeDecodeError):
            return ""

    def assemble(
        self,
        results,
        max_chunks=12,
    ):
        context = []

        seen = set()

        for result in results:
            chunk = result["chunk"]
            chunk_id = result["chunk_id"]

            if chunk_id in seen:
                continue

            seen.add(chunk_id)

            context.append(
                {
                    "chunk_id": chunk_id,
                    "name": chunk["name"],
                    "chunk_type": chunk["chunk_type"],
                    "file_path": chunk["file_path"],
                    "start_line": chunk["start_line"],
                    "end_line": chunk["end_line"],
                    "relationship": result.get(
                        "relationship"
                    ),
                    "source": self.load_source(chunk),
                    "score": result.get(
                        "final_score",
                        result.get("score", 0.0),
                    ),
                }
            )

            if len(context) >= max_chunks:
                break

        return context

    def format_context(self, context):
        sections = []

        for item in context:
            header = (
                f"{item['file_path']}:"
                f"{item['start_line']}-"
                f"{item['end_line']} "
                f"{item['name']}"
            )

            sections.append(
                f"### {header}\n"
                f"```python\n"
                f"{item['source']}\n"
                f"```"
            )

        return "\n\n".join(sections)
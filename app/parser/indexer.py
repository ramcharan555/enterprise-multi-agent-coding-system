import json
from pathlib import Path

from app.parser.python_parser import PythonParser


class RepositoryIndexer:

    def __init__(self):
        self.python_parser = PythonParser()

    def index(self, repository_path: str):
        repo = Path(repository_path)
        chunks = []

        for file_path in repo.rglob("*.py"):
            if any(
                part in {
                    ".git",
                    ".venv",
                    "venv",
                    "__pycache__",
                }
                for part in file_path.parts
            ):
                continue

            relative_path = file_path.relative_to(repo).as_posix()

            chunks.extend(
                self.python_parser.parse_file(
                    file_path,
                    relative_path,
                )
            )

        return chunks


def save_chunks(chunks, output_path):
    output = Path(output_path)
    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output.write_text(
        json.dumps(
            [chunk.to_dict() for chunk in chunks],
            indent=2,
        ),
        encoding="utf-8",
    )
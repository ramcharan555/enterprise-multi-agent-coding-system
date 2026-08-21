from pathlib import Path
from typing import Optional

import pathspec

from .models import FileInfo


LANGUAGE_MAP = {
    ".py": "Python",
    ".java": "Java",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".go": "Go",
    ".rs": "Rust",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".c": "C",
    ".h": "C/C++",
    ".hpp": "C++",
    ".cs": "C#",
    ".rb": "Ruby",
    ".php": "PHP",
    ".kt": "Kotlin",
    ".swift": "Swift",
    ".scala": "Scala",
}


IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "dist",
    "build",
    "target",
    "coverage",
}


BINARY_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".ico",
    ".webp",
    ".pdf",
    ".zip",
    ".tar",
    ".gz",
    ".7z",
    ".rar",
    ".exe",
    ".dll",
    ".so",
    ".dylib",
    ".bin",
    ".class",
    ".jar",
    ".pyc",
    ".woff",
    ".woff2",
    ".ttf",
    ".mp3",
    ".mp4",
    ".mov",
}


def detect_language(path: Path) -> Optional[str]:
    return LANGUAGE_MAP.get(path.suffix.lower())


def load_gitignore(repo_path: Path):
    gitignore = repo_path / ".gitignore"

    if not gitignore.exists():
        return None

    lines = gitignore.read_text(
        encoding="utf-8",
        errors="ignore",
    ).splitlines()

    return pathspec.PathSpec.from_lines(
        "gitwildmatch",
        lines,
    )


def should_ignore(path: Path, repo_path: Path, gitignore) -> bool:
    relative = path.relative_to(repo_path)

    if any(part in IGNORED_DIRECTORIES for part in relative.parts):
        return True

    if path.suffix.lower() in BINARY_EXTENSIONS:
        return True

    if gitignore and gitignore.match_file(relative.as_posix()):
        return True

    return False


def scan_repository(repo_path: Path) -> list[FileInfo]:
    gitignore = load_gitignore(repo_path)
    files = []

    for path in repo_path.rglob("*"):
        if not path.is_file():
            continue

        if should_ignore(path, repo_path, gitignore):
            continue

        language = detect_language(path)

        if language is None:
            continue

        content = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        files.append(
            FileInfo(
                path=path.relative_to(repo_path).as_posix(),
                language=language,
                size_bytes=path.stat().st_size,
                line_count=len(content.splitlines()),
            )
        )

    return sorted(files, key=lambda item: item.path)
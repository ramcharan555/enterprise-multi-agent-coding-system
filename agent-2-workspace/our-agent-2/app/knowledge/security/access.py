from dataclasses import dataclass
from typing import Iterable, Set


DEFAULT_ALLOWED_EXTENSIONS: Set[str] = {
    ".md",
    ".txt",
    ".html",
    ".htm",
    ".pdf",
    ".docx",
    ".py",
    ".js",
    ".ts",
    ".java",
    ".go",
    ".rs",
    ".cpp",
    ".c",
    ".h",
}


@dataclass(frozen=True)
class AccessPolicy:
    allowed_extensions: Set[str]
    max_file_size_bytes: int = 10 * 1024 * 1024

    def can_read(self, filename: str, file_size: int) -> bool:
        if file_size < 0 or file_size > self.max_file_size_bytes:
            return False

        name = filename.lower()
        extension = ""

        if "." in name:
            extension = "." + name.rsplit(".", 1)[1]

        return extension in self.allowed_extensions


class RepositoryAccessController:
    def __init__(self, policy: AccessPolicy | None = None):
        self.policy = policy or AccessPolicy(
            allowed_extensions=set(DEFAULT_ALLOWED_EXTENSIONS)
        )

    def validate(self, filename: str, file_size: int) -> None:
        if not self.policy.can_read(filename, file_size):
            raise PermissionError(
                f"Access denied for repository file: {filename}"
            )

    def filter_files(
        self,
        files: Iterable[tuple[str, int]],
    ) -> list[str]:
        return [
            filename
            for filename, size in files
            if self.policy.can_read(filename, size)
        ]

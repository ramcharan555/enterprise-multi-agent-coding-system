from pathlib import Path

from .git import get_git_info
from .models import RepositoryInfo
from .scanner import scan_repository


class RepositoryLoader:

    def load(self, repository_path: str) -> RepositoryInfo:
        repo_path = Path(repository_path).resolve()

        if not repo_path.exists():
            raise ValueError(
                f"Repository path does not exist: {repo_path}"
            )

        if not repo_path.is_dir():
            raise ValueError(
                f"Repository path is not a directory: {repo_path}"
            )

        return RepositoryInfo(
            name=repo_path.name,
            path=str(repo_path),
            git=get_git_info(repo_path),
            files=scan_repository(repo_path),
        )
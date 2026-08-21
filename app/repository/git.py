import subprocess
from pathlib import Path

from .models import GitInfo


def run_git(repo_path: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_git_info(repo_path: Path) -> GitInfo:
    if not (repo_path / ".git").exists():
        return GitInfo(is_git_repository=False)

    return GitInfo(
        is_git_repository=True,
        branch=run_git(repo_path, "branch", "--show-current"),
        commit=run_git(repo_path, "rev-parse", "HEAD"),
        remote_url=run_git(
            repo_path,
            "config",
            "--get",
            "remote.origin.url",
        ),
    )
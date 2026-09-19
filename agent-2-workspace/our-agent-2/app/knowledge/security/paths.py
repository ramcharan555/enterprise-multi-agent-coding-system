from pathlib import Path


def is_safe_repository_path(repository_root: str, candidate: str) -> bool:
    root = Path(repository_root).resolve()
    path = Path(candidate).resolve()

    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def validate_repository_path(repository_root: str, candidate: str) -> Path:
    path = Path(candidate)

    if not is_safe_repository_path(repository_root, candidate):
        raise PermissionError(
            f"Repository path escapes configured root: {candidate}"
        )

    return path.resolve()

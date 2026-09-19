from pathlib import Path

import pytest

from app.knowledge.security import (
    AccessPolicy,
    RepositoryAccessController,
    is_safe_repository_path,
    validate_repository_path,
)


def test_access_policy_allows_supported_files():
    policy = AccessPolicy({".py", ".md"})

    assert policy.can_read("main.py", 100)
    assert policy.can_read("README.md", 100)


def test_access_policy_rejects_unsupported_files():
    policy = AccessPolicy({".py"})

    assert not policy.can_read("secret.key", 100)
    assert not policy.can_read("image.png", 100)


def test_access_policy_rejects_oversized_files():
    policy = AccessPolicy({".py"}, max_file_size_bytes=100)

    assert not policy.can_read("main.py", 101)


def test_access_controller_filters_files():
    controller = RepositoryAccessController(
        AccessPolicy({".py", ".md"})
    )

    files = [
        ("main.py", 100),
        ("README.md", 100),
        ("secret.key", 100),
    ]

    assert controller.filter_files(files) == [
        "main.py",
        "README.md",
    ]


def test_access_controller_rejects_invalid_file():
    controller = RepositoryAccessController(
        AccessPolicy({".py"})
    )

    with pytest.raises(PermissionError):
        controller.validate("secret.key", 100)


def test_repository_path_inside_root_is_safe(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()

    candidate = root / "app" / "main.py"
    candidate.parent.mkdir()

    assert is_safe_repository_path(str(root), str(candidate))


def test_repository_path_outside_root_is_rejected(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()

    outside = tmp_path / "secret.py"

    assert not is_safe_repository_path(str(root), str(outside))

    with pytest.raises(PermissionError):
        validate_repository_path(str(root), str(outside))

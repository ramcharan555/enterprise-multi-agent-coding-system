from pathlib import Path

from app.parser.python_parser import PythonParser


def test_python_parser(tmp_path):
    source = """
import os

class User:

    def login(self, name):
        return name

def helper():
    return True
"""

    file_path = tmp_path / "sample.py"
    file_path.write_text(source)

    chunks = PythonParser().parse_file(
        file_path,
        "sample.py",
    )

    names = {chunk.name for chunk in chunks}

    assert "User" in names
    assert "login" in names
    assert "helper" in names


def test_method_relationship(tmp_path):
    source = """
class Account:

    def save(self):
        return True
"""

    file_path = tmp_path / "account.py"
    file_path.write_text(source)

    chunks = PythonParser().parse_file(
        file_path,
        "account.py",
    )

    account = next(
        chunk for chunk in chunks
        if chunk.name == "Account"
    )

    save = next(
        chunk for chunk in chunks
        if chunk.name == "save"
    )

    assert save.parent == account.chunk_id
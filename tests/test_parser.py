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

def test_parameter_type_extraction(tmp_path):
    source = """
class OrderRequest:
    pass

def create_order(order: OrderRequest):
    return order
"""

    file_path = tmp_path / "orders.py"
    file_path.write_text(source)

    chunks = PythonParser().parse_file(
        file_path,
        "orders.py",
    )

    function = next(
        chunk
        for chunk in chunks
        if chunk.name == "create_order"
    )

    assert "OrderRequest" in function.parameter_types


def test_return_type_extraction(tmp_path):
    source = """
class OrderResponse:
    pass

def create_order() -> OrderResponse:
    return OrderResponse()
"""

    file_path = tmp_path / "orders.py"
    file_path.write_text(source)

    chunks = PythonParser().parse_file(
        file_path,
        "orders.py",
    )

    function = next(
        chunk
        for chunk in chunks
        if chunk.name == "create_order"
    )

    assert function.return_type == "OrderResponse"
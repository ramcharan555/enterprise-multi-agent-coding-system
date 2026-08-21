from tree_sitter import Language, Parser
import tree_sitter_python

from app.parser.relationships import RelationshipExtractor


LANGUAGE = Language(tree_sitter_python.language())


def parse(code):
    parser = Parser(LANGUAGE)
    return parser.parse(code.encode("utf-8"))


def test_imports():
    code = """
import os
import requests
from pathlib import Path
from requests.models import Response
"""

    tree = parse(code)
    result = RelationshipExtractor().extract(tree, code)

    assert "os" in result["imports"]
    assert "requests" in result["imports"]
    assert "pathlib" in result["imports"]
    assert "requests.models" in result["imports"]


def test_inheritance():
    code = """
class Child(Base):
    pass

class AnotherChild(package.Parent):
    pass
"""

    tree = parse(code)
    result = RelationshipExtractor().extract(tree, code)

    assert "Base" in result["inherits_from"]
    assert "package.Parent" in result["inherits_from"]


def test_calls():
    code = """
def example():
    print("hello")
    requests.get(url)
    session.send(request)
"""

    tree = parse(code)
    result = RelationshipExtractor().extract(tree, code)

    assert "print" in result["calls"]
    assert "requests.get" in result["calls"]
    assert "session.send" in result["calls"]
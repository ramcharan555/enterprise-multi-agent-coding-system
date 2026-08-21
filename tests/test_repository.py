from pathlib import Path

from app.repository.scanner import detect_language


def test_python_detection():
    assert detect_language(Path("main.py")) == "Python"


def test_java_detection():
    assert detect_language(Path("Main.java")) == "Java"


def test_javascript_detection():
    assert detect_language(Path("app.js")) == "JavaScript"


def test_unknown_file():
    assert detect_language(Path("README.md")) is None
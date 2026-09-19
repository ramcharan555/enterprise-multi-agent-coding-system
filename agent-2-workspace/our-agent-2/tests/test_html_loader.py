from pathlib import Path

from app.knowledge.loaders import HTMLDocumentLoader
from app.knowledge.models import DocumentType


def test_html_loader(tmp_path: Path):
    html_file = tmp_path / "api.html"

    html_file.write_text(
        """
        <html>
            <head>
                <title>API Architecture Guide</title>
                <style>
                    body { color: red; }
                </style>
            </head>
            <body>
                <h1>API Architecture</h1>
                <p>New APIs must use versioning.</p>
                <p>Authentication must use OAuth2.</p>
                <script>
                    console.log("ignore this");
                </script>
            </body>
        </html>
        """,
        encoding="utf-8",
    )

    loader = HTMLDocumentLoader()
    document = loader.load(html_file)

    assert document.title == "API Architecture Guide"
    assert document.document_type == DocumentType.API_DOCUMENTATION

    assert "New APIs must use versioning." in document.content
    assert "Authentication must use OAuth2." in document.content

    assert "console.log" not in document.content
    assert "color: red" not in document.content

    assert document.metadata["html"] is True


def test_html_loader_rejects_non_html(tmp_path: Path):
    text_file = tmp_path / "test.txt"
    text_file.write_text("hello", encoding="utf-8")

    loader = HTMLDocumentLoader()

    try:
        loader.load(text_file)
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "Unsupported file type" in str(exc)
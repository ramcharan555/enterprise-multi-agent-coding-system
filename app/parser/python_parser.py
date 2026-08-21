from pathlib import Path
import re

from tree_sitter import Language, Parser
import tree_sitter_python

from .models import CodeChunk
from .relationships import RelationshipExtractor


PYTHON_LANGUAGE = Language(tree_sitter_python.language())
VALID_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class PythonParser:

    def __init__(self):
        self.parser = Parser(PYTHON_LANGUAGE)
        self.relationships = RelationshipExtractor()

    def parse_file(self, file_path: Path, relative_path: str):
        source = file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        tree = self.parser.parse(source.encode("utf-8"))

        relationship_data = self.relationships.extract(
            tree,
            source,
        )

        chunks = []

        self._walk(
            tree.root_node,
            source,
            relative_path,
            chunks,
            None,
        )

        self._update_children(chunks)

        self._apply_relationships(
            chunks,
            relationship_data,
        )

        return chunks

    def _walk(
        self,
        node,
        source,
        relative_path,
        chunks,
        parent,
    ):
        if node.type == "class_definition":
            name_node = node.child_by_field_name("name")

            if (
                name_node is not None
                and name_node.type == "identifier"
            ):
                name = self._text(name_node, source)

                if not VALID_NAME.fullmatch(name):
                    for child in node.children:
                        self._walk(
                            child,
                            source,
                            relative_path,
                            chunks,
                            parent,
                        )
                    return

                chunk_id = self._make_id(
                    relative_path,
                    node.start_point[0] + 1,
                    name,
                )

                chunk = CodeChunk(
                    chunk_id=chunk_id,
                    chunk_type="class",
                    name=name,
                    file_path=relative_path,
                    start_line=node.start_point[0] + 1,
                    end_line=node.end_point[0] + 1,
                    source=self._text(node, source),
                    parent=parent,
                )

                chunks.append(chunk)

                for child in node.children:
                    self._walk(
                        child,
                        source,
                        relative_path,
                        chunks,
                        chunk_id,
                    )

                return

        if node.type in {
            "function_definition",
            "async_function_definition",
        }:
            name_node = node.child_by_field_name("name")

            if (
                name_node is not None
                and name_node.type == "identifier"
            ):
                name = self._text(name_node, source)

                if not VALID_NAME.fullmatch(name):
                    return

                chunk_id = self._make_id(
                    relative_path,
                    node.start_point[0] + 1,
                    name,
                )

                chunk = CodeChunk(
                    chunk_id=chunk_id,
                    chunk_type="method" if parent else "function",
                    name=name,
                    file_path=relative_path,
                    start_line=node.start_point[0] + 1,
                    end_line=node.end_point[0] + 1,
                    source=self._text(node, source),
                    parent=parent,
                )

                chunks.append(chunk)

                return

        for child in node.children:
            self._walk(
                child,
                source,
                relative_path,
                chunks,
                parent,
            )

    @staticmethod
    def _apply_relationships(chunks, relationships):
        if not chunks:
            return

        imports = relationships.get("imports", [])
        inherits_from = relationships.get("inherits_from", [])
        calls = relationships.get("calls", [])

        chunks[0].imports = imports
        chunks[0].inherits_from = inherits_from
        chunks[0].calls = calls

    @staticmethod
    def _text(node, source):
        return source[node.start_byte:node.end_byte]

    @staticmethod
    def _update_children(chunks):
        by_id = {
            chunk.chunk_id: chunk
            for chunk in chunks
        }

        for chunk in chunks:
            if chunk.parent in by_id:
                parent = by_id[chunk.parent]

                if chunk.chunk_id not in parent.children:
                    parent.children.append(chunk.chunk_id)

    @staticmethod
    def _make_id(file_path, line, name):
        return f"{file_path}:{line}:{name}"

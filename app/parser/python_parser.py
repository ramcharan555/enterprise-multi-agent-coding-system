from pathlib import Path
import re

from tree_sitter import Language, Parser
import tree_sitter_python

from .models import CodeChunk
from .relationships import RelationshipExtractor


PYTHON_LANGUAGE = Language(tree_sitter_python.language())


class PythonParser:

    def __init__(self):
        self.parser = Parser(PYTHON_LANGUAGE)
        self.relationships = RelationshipExtractor()

    def parse_file(self, file_path: Path, relative_path: str):
        source = file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        tree = self.parser.parse(
            source.encode("utf-8")
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

            name_node = node.child_by_field_name(
                "name"
            )

            if (
                name_node is not None
                and name_node.type == "identifier"
            ):
                name = self._text(
                    name_node,
                    source,
                )

                chunk_id = self._make_id(
                    relative_path,
                    node.start_point[0] + 1,
                    name,
                )

                chunk = self._create_chunk(
                    node=node,
                    source=source,
                    relative_path=relative_path,
                    chunk_id=chunk_id,
                    chunk_type="class",
                    name=name,
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

            name_node = node.child_by_field_name(
                "name"
            )

            if (
                name_node is not None
                and name_node.type == "identifier"
            ):
                name = self._text(
                    name_node,
                    source,
                )

                if not re.fullmatch(
                    r"[A-Za-z_][A-Za-z0-9_]*",
                    name,
                ):
                    return

                chunk_id = self._make_id(
                    relative_path,
                    node.start_point[0] + 1,
                    name,
                )

                chunk = self._create_chunk(
                    node=node,
                    source=source,
                    relative_path=relative_path,
                    chunk_id=chunk_id,
                    chunk_type=(
                        "method"
                        if parent
                        else "function"
                    ),
                    name=name,
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

    def _create_chunk(
        self,
        node,
        source,
        relative_path,
        chunk_id,
        chunk_type,
        name,
        parent,
    ):
        chunk_source = self._text(
            node,
            source,
        )

        # Parse relationships INSIDE this
        # structural chunk.
        chunk_tree = self.parser.parse(
            chunk_source.encode("utf-8")
        )

        relationships = self.relationships.extract(
            chunk_tree,
            chunk_source,
        )

        return CodeChunk(
            chunk_id=chunk_id,
            chunk_type=chunk_type,
            name=name,
            file_path=relative_path,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            source=chunk_source,
            parent=parent,
            imports=relationships["imports"],
            inherits_from=relationships[
                "inherits_from"
            ],
            calls=relationships["calls"],
        )

    @staticmethod
    def _text(node, source):
        return source[
            node.start_byte:node.end_byte
        ]

    @staticmethod
    def _update_children(chunks):
        by_id = {
            chunk.chunk_id: chunk
            for chunk in chunks
        }

        for chunk in chunks:

            if chunk.parent in by_id:

                parent = by_id[
                    chunk.parent
                ]

                if (
                    chunk.chunk_id
                    not in parent.children
                ):
                    parent.children.append(
                        chunk.chunk_id
                    )

    @staticmethod
    def _make_id(
        file_path,
        line,
        name,
    ):
        return (
            f"{file_path}:{line}:{name}"
        )
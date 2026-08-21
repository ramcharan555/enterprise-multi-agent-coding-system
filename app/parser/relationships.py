from tree_sitter import Node


class RelationshipExtractor:

    def extract(self, tree, source):
        result = {
            "imports": [],
            "inherits_from": [],
            "calls": [],
        }

        self._walk(tree.root_node, source, result)

        result["imports"] = list(dict.fromkeys(result["imports"]))
        result["inherits_from"] = list(dict.fromkeys(result["inherits_from"]))
        result["calls"] = list(dict.fromkeys(result["calls"]))

        return result

    def _walk(self, node: Node, source: str, result: dict):
        if node.type == "import_statement":
            self._extract_import(node, source, result)

        elif node.type == "import_from_statement":
            self._extract_from_import(node, source, result)

        elif node.type == "class_definition":
            self._extract_inheritance(node, source, result)

        elif node.type == "call":
            self._extract_call(node, source, result)

        for child in node.children:
            self._walk(child, source, result)

    def _extract_import(self, node, source, result):
        for child in node.children:
            if child.type == "dotted_name":
                result["imports"].append(
                    self._text(child, source)
                )

            elif child.type == "aliased_import":
                name_node = child.child_by_field_name("name")

                if name_node is not None:
                    result["imports"].append(
                        self._text(name_node, source)
                    )

    def _extract_from_import(self, node, source, result):
        for child in node.children:
            if child.type == "dotted_name":
                result["imports"].append(
                    self._text(child, source)
                )
                return

    def _extract_inheritance(self, node, source, result):
        superclasses = node.child_by_field_name("superclasses")

        if superclasses is None:
            return

        for child in superclasses.children:
            if child.type in {
                "identifier",
                "attribute",
                "dotted_name",
            }:
                result["inherits_from"].append(
                    self._text(child, source)
                )

    def _extract_call(self, node, source, result):
        function_node = node.child_by_field_name("function")

        if function_node is None:
            return

        name = self._text(function_node, source)

        if name:
            result["calls"].append(name)

    @staticmethod
    def _text(node, source):
        return source[node.start_byte:node.end_byte]

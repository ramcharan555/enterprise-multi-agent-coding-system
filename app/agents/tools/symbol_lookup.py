class SymbolLookupTool:

    name = "symbol_lookup"

    description = (
        "Find a specific class, function, or method in the repository."
    )

    def __init__(self, chunks):
        self.chunks = chunks

    def run(self, symbol):
        symbol = symbol.lower().strip()

        return [
            chunk
            for chunk in self.chunks
            if chunk["name"].lower() == symbol
        ]

    def lookup_types(self, chunk):
        types = []

        for type_name in chunk.get(
            "parameter_types",
            [],
        ):
            types.append(type_name)

        return_type = chunk.get(
            "return_type"
        )

        if return_type:
            types.append(return_type)

        return [
            candidate
            for candidate in self.chunks
            if candidate["name"].lower()
            in {
                type_name.lower()
                for type_name in types
            }
        ]
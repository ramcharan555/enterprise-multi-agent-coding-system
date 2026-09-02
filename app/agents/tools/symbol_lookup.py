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

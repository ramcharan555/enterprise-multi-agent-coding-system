import sys

from .query_encoder import QueryEncoder
from .search import HybridRetriever


def main():

    if len(sys.argv) < 2:
        print(
            'Usage: python -m app.retrieval.main "your query"'
        )
        return

    query = " ".join(sys.argv[1:])

    print()
    print("=" * 65)
    print("       ENTERPRISE CODING AGENT")
    print("             PHASE 6")
    print("        HYBRID RETRIEVAL")
    print("=" * 65)

    print()
    print("Query:", query)
    print()
    print("Loading search system...")

    encoder = QueryEncoder()
    retriever = HybridRetriever()

    print("Searching...")

    query_vector = encoder.encode(query)

    results = retriever.search(
        query_vector,
        query=query,
        vector_top_k=10,
        top_k=5,
    )

    print()
    print("Top results")
    print("-" * 65)

    for i, result in enumerate(
        results,
        1,
    ):
        chunk = result["chunk"]

        print()
        print(
            f"#{i} "
            f"Score: {result['final_score']:.4f}"
        )

        print(
            f"Vector : "
            f"{result['vector_score']:.4f}"
        )

        print(
            f"Symbol : "
            f"{result['symbol_score']:.4f}"
        )

        print(
            f"Source : {result['source']}"
        )

        print(
            f"Name   : {chunk['name']}"
        )

        print(
            f"Type   : {chunk['chunk_type']}"
        )

        print(
            f"File   : {chunk['file_path']}"
        )

        print(
            f"Lines  : "
            f"{chunk['start_line']}-"
            f"{chunk['end_line']}"
        )

        print(
            f"ID     : {result['chunk_id']}"
        )


if __name__ == "__main__":
    main()
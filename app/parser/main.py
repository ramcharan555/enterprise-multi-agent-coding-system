import argparse

from app.parser.indexer import RepositoryIndexer, save_chunks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repository")
    parser.add_argument("--output", default="data/chunks.json")

    args = parser.parse_args()

    chunks = RepositoryIndexer().index(args.repository)
    save_chunks(chunks, args.output)

    print()
    print("=" * 55)
    print("       ENTERPRISE CODING AGENT")
    print("             PHASE 2")
    print("       AST STRUCTURAL PARSER")
    print("=" * 55)
    print()
    print(f"Repository : {args.repository}")
    print(f"Chunks     : {len(chunks)}")
    print(f"Output     : {args.output}")
    print()

    counts = {}

    for chunk in chunks:
        counts[chunk.chunk_type] = counts.get(chunk.chunk_type, 0) + 1

    print("Chunk types")

    for kind, count in sorted(counts.items()):
        print(f"  {kind:<15} {count}")


if __name__ == "__main__":
    main()
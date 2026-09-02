import json
import sys
from pathlib import Path

from .encoder import CodeEmbedder


def build_text(chunk):
    parts = [
        f"File: {chunk['file_path']}",
        f"Type: {chunk['chunk_type']}",
        f"Name: {chunk['name']}",
        f"Lines: {chunk['start_line']}-{chunk['end_line']}",
    ]

    if chunk.get("parent"):
        parts.append(f"Parent: {chunk['parent']}")

    if chunk.get("imports"):
        parts.append(
            "Imports: " + ", ".join(chunk["imports"])
        )

    if chunk.get("inherits_from"):
        parts.append(
            "Inherits: " + ", ".join(chunk["inherits_from"])
        )

    if chunk.get("calls"):
        parts.append(
            "Calls: " + ", ".join(chunk["calls"])
        )

    parts.append("")
    parts.append("Code:")
    parts.append(chunk["source"])

    return "\n".join(parts)


def main():
    if len(sys.argv) != 2:
        print("Usage: python -m app.embedding.main data/chunks.json")
        raise SystemExit(1)

    input_path = Path(sys.argv[1])

    with input_path.open("r", encoding="utf-8") as file:
        chunks = json.load(file)

    print(f"Loading {len(chunks)} chunks...")

    texts = [
        build_text(chunk)
        for chunk in chunks
    ]

    embedder = CodeEmbedder()

    print(f"Device    : {embedder.device}")
    print("Generating embeddings...")

    embeddings = embedder.encode(texts)

    output = {
        "model": "Salesforce/codet5p-110m-embedding",
        "dimension": embedder.dimension(),
        "count": len(chunks),
        "chunk_ids": [
            chunk["chunk_id"]
            for chunk in chunks
        ],
        "embeddings": embeddings,
    }

    output_path = Path("data/embeddings.json")

    output_path.write_text(
        json.dumps(output),
        encoding="utf-8",
    )

    print()
    print("=" * 55)
    print("       ENTERPRISE CODING AGENT")
    print("             PHASE 4")
    print("          CODE EMBEDDINGS")
    print("=" * 55)
    print()
    print(f"Model     : {output['model']}")
    print(f"Chunks    : {output['count']}")
    print(f"Dimension : {output['dimension']}")
    print(f"Vectors   : {len(output['embeddings'])}")
    print(f"Output    : {output_path}")
    print(f"Size      : {output_path.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
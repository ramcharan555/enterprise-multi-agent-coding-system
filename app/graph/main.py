import json
import sys

from .builder import CodeGraphBuilder


def main():
    if len(sys.argv) != 2:
        print("Usage: python -m app.graph.main data/chunks.json")
        raise SystemExit(1)

    input_path = sys.argv[1]

    with open(input_path, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    builder = CodeGraphBuilder()
    graph = builder.build(chunks)

    output_path = "data/graph.json"
    builder.save(output_path)

    relationships = {}

    for _, _, data in graph.edges(data=True):
        relation = data["relationship"]
        relationships[relation] = relationships.get(relation, 0) + 1

    print()
    print("=" * 55)
    print("       ENTERPRISE CODING AGENT")
    print("             PHASE 3")
    print("           CODE GRAPH")
    print("=" * 55)
    print()
    print(f"Nodes : {graph.number_of_nodes()}")
    print(f"Edges : {graph.number_of_edges()}")
    print()
    print("Relationships")

    for relation, count in sorted(relationships.items()):
        print(f"  {relation:<20} {count}")

    print()
    print(f"Output : {output_path}")


if __name__ == "__main__":
    main()
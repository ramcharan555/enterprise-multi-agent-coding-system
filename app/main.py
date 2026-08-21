import argparse
import json
from collections import Counter
from pathlib import Path

from app.repository.loader import RepositoryLoader


def main():
    parser = argparse.ArgumentParser(
        description="Enterprise Coding Agent - Repository Loader"
    )

    parser.add_argument(
        "repository",
        help="Path to the repository",
    )

    parser.add_argument(
        "--output",
        default="data/repository.json",
        help="Output JSON path",
    )

    args = parser.parse_args()

    repository = RepositoryLoader().load(args.repository)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    output.write_text(
        json.dumps(repository.to_dict(), indent=2),
        encoding="utf-8",
    )

    languages = Counter(
        file.language for file in repository.files
    )

    print()
    print("=" * 55)
    print("       ENTERPRISE CODING AGENT")
    print("             PHASE 1")
    print("          REPOSITORY LOADER")
    print("=" * 55)

    print(f"\nRepository : {repository.name}")
    print(f"Path       : {repository.path}")

    print("\nGit information")
    print(f"  Git repository : {repository.git.is_git_repository}")
    print(f"  Branch         : {repository.git.branch}")
    print(f"  Commit         : {repository.git.commit}")
    print(f"  Remote         : {repository.git.remote_url}")

    print(f"\nSource files : {len(repository.files)}")

    print("\nLanguages")
    for language, count in languages.most_common():
        print(f"  {language:<15} {count}")

    print(f"\nMetadata saved to: {output}")
    print()


if __name__ == "__main__":
    main()
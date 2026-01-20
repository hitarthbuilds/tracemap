import sys
import json
from pathlib import Path

from tracemap.api import trace
from tracemap.export.snapshot import export_snapshot


def main():
    if len(sys.argv) != 2:
        print("Usage: python -m tracemap <python_file>", file=sys.stderr)
        sys.exit(1)

    target = Path(sys.argv[1])

    if not target.exists() or not target.suffix == ".py":
        print(f"Error: {target} is not a valid Python file", file=sys.stderr)
        sys.exit(1)

    code = target.read_text()

    graph = trace(code)
    snapshot = export_snapshot(graph)

    print(json.dumps(snapshot, indent=2))


if __name__ == "__main__":
    main()

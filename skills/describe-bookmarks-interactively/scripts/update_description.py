#!/usr/bin/env python3
"""
Atomically update one URL -> description entry in descriptions.json.

Usage:
    python3 update_description.py <descriptions.json> <url>

The description is read from stdin (heredoc-friendly), so descriptions
containing quotes don't have to be shell-escaped. Writes to a tmp file
and renames it into place so a crash mid-write can't corrupt the
descriptions file.
"""

import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__.strip())

    path = Path(sys.argv[1])
    url = sys.argv[2]
    description = sys.stdin.read().strip()

    if path.exists():
        text = path.read_text(encoding="utf-8").strip()
        data = json.loads(text) if text else {}
    else:
        data = {}

    if not isinstance(data, dict):
        sys.exit(f"{path} must contain a JSON object mapping url -> description.")

    data[url] = description

    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    tmp.replace(path)

    preview = description if len(description) <= 60 else description[:57] + "..."
    print(f"OK: {url} -> {preview}")


if __name__ == "__main__":
    main()

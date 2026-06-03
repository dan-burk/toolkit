#!/usr/bin/env python3
"""
Parse a Netscape-format browser bookmarks export and emit:
- bookmarks.jsonl : one bookmark per line, with folder-derived labels
- bookmarks.md   : flat, human/agent-readable index

Per-bookmark descriptions live in a sidecar `descriptions.json` next to
the input HTML — a flat URL -> description map. The script reads it on
each run and merges descriptions into the outputs, so descriptions
survive re-exports of the bookmarks HTML. If the sidecar doesn't exist,
the script creates an empty one.

Usage:
    python build_index.py [input.html] [output_dir]

If input.html is omitted, the script picks the only .html file in the
current directory (and errors if there is more than one).
"""

import sys
import json
import glob
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path


class BookmarkParser(HTMLParser):
    """Walks the Netscape DL/DT tree, tracking the folder ancestry stack."""

    def __init__(self):
        super().__init__()
        self.folder_stack = []      # ancestor folders for the current position
        self.pending_folder = None  # H3 just seen, will be pushed by next <DL>
        self.in_h3 = False
        self.in_a = False
        self.text_buf = []
        self.current_a = None
        self.bookmarks = []
        self.folder_count = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs = dict(attrs)
        if tag == "h3":
            self.in_h3 = True
            self.text_buf = []
        elif tag == "dl":
            self.folder_stack.append(self.pending_folder)
            self.pending_folder = None
        elif tag == "a":
            href = attrs.get("href")
            if href:
                self.in_a = True
                self.text_buf = []
                self.current_a = {
                    "url": href,
                    "add_date": attrs.get("add_date"),
                }

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "h3" and self.in_h3:
            self.in_h3 = False
            self.pending_folder = "".join(self.text_buf).strip()
            self.folder_count += 1
        elif tag == "dl":
            if self.folder_stack:
                self.folder_stack.pop()
        elif tag == "a" and self.in_a:
            self.in_a = False
            title = "".join(self.text_buf).strip()
            labels = [f for f in self.folder_stack if f]
            self.bookmarks.append({
                "title": title,
                "url": self.current_a["url"],
                "labels": labels,
                "description": "",
                "add_date": self.current_a.get("add_date"),
            })
            self.current_a = None

    def handle_data(self, data):
        if self.in_h3 or self.in_a:
            self.text_buf.append(data)


def iso_date(ts):
    if not ts:
        return None
    try:
        return datetime.fromtimestamp(int(ts), tz=timezone.utc).date().isoformat()
    except (ValueError, TypeError):
        return None


DESCRIPTIONS_FILENAME = "descriptions.json"


def load_descriptions(path):
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        sys.exit(f"{path} must contain a JSON object mapping url -> description.")
    return data


def resolve_input():
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    htmls = sorted(p for p in glob.glob("*.html"))
    if len(htmls) != 1:
        sys.exit(
            f"Expected exactly one .html file in cwd; found {len(htmls)}. "
            f"Pass a path explicitly: python build_index.py <file.html>"
        )
    return Path(htmls[0])


def write_jsonl(path, bookmarks):
    with path.open("w", encoding="utf-8") as f:
        for bm in bookmarks:
            f.write(json.dumps(bm, ensure_ascii=False) + "\n")


def write_markdown(path, bookmarks, source_name, folder_count):
    lines = [
        "# Bookmarks Index",
        "",
        f"{len(bookmarks)} bookmarks · {folder_count} folders · source: `{source_name}`",
        "",
        "Each entry shows title (linked), folder-derived labels, and a description "
        "slot (empty until filled in).",
        "",
        "---",
        "",
    ]
    for bm in bookmarks:
        title = bm["title"] or bm["url"]
        labels = ", ".join(f"`{l}`" for l in bm["labels"]) or "_(no labels)_"
        added = iso_date(bm["add_date"])
        added_str = f" · added {added}" if added else ""
        desc = bm["description"] or "_no description yet_"
        lines.append(f"- **[{title}]({bm['url']})** — {labels}{added_str}")
        lines.append(f"  - {desc}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    input_path = resolve_input()
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(".")
    out_dir.mkdir(parents=True, exist_ok=True)

    descriptions_path = input_path.parent / DESCRIPTIONS_FILENAME
    descriptions = load_descriptions(descriptions_path)

    raw = input_path.read_text(encoding="utf-8")
    parser = BookmarkParser()
    parser.feed(raw)

    for bm in parser.bookmarks:
        bm["description"] = descriptions.get(bm["url"], "")

    if not descriptions_path.exists():
        descriptions_path.write_text("{}\n", encoding="utf-8")

    jsonl_path = out_dir / "bookmarks.jsonl"
    md_path = out_dir / "bookmarks.md"
    write_jsonl(jsonl_path, parser.bookmarks)
    write_markdown(md_path, parser.bookmarks, input_path.name, parser.folder_count)

    matched = sum(1 for bm in parser.bookmarks if bm["description"])
    bookmark_urls = {bm["url"] for bm in parser.bookmarks}
    orphans = [u for u in descriptions if u not in bookmark_urls]

    print(f"Parsed {len(parser.bookmarks)} bookmarks across {parser.folder_count} folders.")
    print(f"Merged {matched}/{len(parser.bookmarks)} descriptions from {descriptions_path.name}.")
    if orphans:
        print(f"Note: {len(orphans)} description(s) in sidecar no longer match any bookmark URL (kept, not pruned).")
    print(f"Wrote {jsonl_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()

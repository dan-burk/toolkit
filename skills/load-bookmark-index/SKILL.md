---
name: load-bookmark-index
description: Load the user's bookmark index into context so it can answer 'find the link to X' / 'what bookmarks do I have about Y' lookups for the session, and expose the structured bookmarks.jsonl for programmatic tasks (filtering, deduping, tagging). Use when the user wants to reference, browse, search, or recall their saved bookmarks. Do NOT trigger when they want to write/refresh descriptions (that's describe-bookmarks-interactively).
---

# load-bookmark-index

Loads the user's bookmark index so it can answer lookups for the rest of the session, and points to the structured data file for any programmatic work.

## Data location

All bookmark data lives in a single user-configured directory, referenced here as `$BOOKMARK_DIR` (environment variable `BOOKMARK_DIR`, default `~/.bookmarks/`). Resolve it once; if it is unset and you don't yet know where the user keeps their bookmarks, ask them the first time. This is the same directory that `describe-bookmarks-interactively` writes to — this skill consumes exactly what that one produces.

## Load the human-readable index

Read `$BOOKMARK_DIR/bookmarks.md` now and treat it as the authoritative reference for any "find the link to X", "what bookmarks do I have about Y", or similar lookups during this conversation.

Each entry shows the title (with its URL), folder-derived labels, and a description. Answer human-facing questions about bookmarks directly from this content.

## Companion file for programmatic tasks

A structured version of the same data lives at:

`$BOOKMARK_DIR/bookmarks.jsonl`

Each line is a JSON object representing one bookmark (`{title, url, labels, description, add_date}`). Use this file (not the markdown) whenever the task calls for code — filtering, deduping, tagging, building an index, transforming into another format, feeding a script, etc. Read or process it with whatever file-reading or scripting capability fits the task. Do not paste its full contents into context unless the user asks.

## Rule of thumb

- Human-facing question about a bookmark → answer from `bookmarks.md`.
- Programmatic / bulk operation on bookmarks → operate on `bookmarks.jsonl`.

Keep the dual-file discipline: `.md` is for human lookups, `.jsonl` is for programmatic ops. Don't dump the whole file into context unless the user explicitly asks for it.

---
name: describe-bookmarks-interactively
description: Walk through saved bookmarks one URL at a time as a human-AI collaboration: fetch each page, propose a 1-2 sentence draft, ask the user why they bookmarked it, then synthesize page content with the user's intent into a final description and persist it. Use when the user wants to fill in / write / refresh / go through / describe / index their bookmarks. Do NOT trigger for generic lookups like 'what's in my bookmarks'.
---

# describe-bookmarks-interactively

Populates `descriptions.json` — the sidecar that maps `{url -> description}` and gets merged into the generated bookmark outputs by `build_index.py`.

The flow is **interactive**, one URL at a time: fetch the page, propose a draft, ask the user why they bookmarked it, synthesize their context with the page content into a final 1-2 sentence description, save, advance. The "why I saved this" signal is what the user actually wants captured — page content alone gives generic summaries; user context turns the file into a retrieval-friendly map of curation intent.

Progress is durable: every answer is written to `descriptions.json` immediately via an atomic helper. The user can quit mid-batch and resume next session — undescribed URLs are picked up where they left off.

## Data location

All bookmark data lives in a single user-configured directory, referenced here as `$BOOKMARK_DIR` (environment variable `BOOKMARK_DIR`, default `~/.bookmarks/`). Resolve it once at the start of the session; if it is unset and you don't yet know where the user keeps their bookmarks, ask them the first time and use that path for the rest of the work.

Only the Python scripts are skill assets (shipped in this skill's `scripts/` folder). All generated/data files live in `$BOOKMARK_DIR`.

## Files this skill operates on

All paths below are inside `$BOOKMARK_DIR`:

- `bookmarks.jsonl` — one bookmark per line: `{title, url, labels, description, add_date}`. Generated; supplies the URL list and folder labels that drive the work queue.
- `descriptions.json` — `{url: description}` map. The thing being updated.
- the bookmarks HTML export — the Netscape-format source `build_index.py` parses.
- `bookmarks.md` — generated, human-readable index.

The skill's scripts:

- `${CLAUDE_SKILL_DIR}/scripts/update_description.py` — atomic single-entry writer for `descriptions.json`.
- `${CLAUDE_SKILL_DIR}/scripts/build_index.py` — regenerates `bookmarks.jsonl` and `bookmarks.md` from the HTML export + `descriptions.json`. Run it at the end.

If `bookmarks.jsonl` is missing, generate it first by running `build_index.py` against `$BOOKMARK_DIR` (see "After the queue is done" for the exact invocation pattern).

## Reserved sentinel strings

Four exact strings are reserved as sentinels — they signal a fetch outcome where the page itself can't be summarized. Default flow treats them as "already handled, skip", but `--force` redoes everything and `--only-sentinels` retries just these:

- `URL not found` — server confirmed the page is gone (HTTP 404 / 410), or DNS doesn't resolve.
- `Authentication required` — page is gated behind a login (sign-in form, redirect to SSO/identity provider, "sign in to continue" interstitial with no public content).
- `Unable to index` — page loaded but is client-side rendered with no meaningful content (empty SPA root, "Please enable JavaScript" notice, body text < ~200 chars after script/style stripping).
- `Unreachable` — transient failure: timeout, SSL/TLS error, 5xx, connection refused. Worth retrying later with `--only-sentinels`.

**Sentinels can become real descriptions if the user provides context.** For `Authentication required` and `Unable to index`, the user usually knows exactly what the page is (their own portal, dashboard, etc.) — the skill asks them, and any free-text answer turns into a real description. The sentinel is only saved if the user has nothing to add (says `keep`). Dead URLs (`URL not found` / `Unreachable`) skip the prompt entirely — there's nothing for the user to react to.

Anything in `descriptions.json` that isn't one of these four strings is a real description and must be left alone unless `--force`.

## Argument parsing

Parse arguments from the user's invocation, then use them to filter the work queue:

| Argument | Effect |
|----------|--------|
| (none) | Process every URL whose current description is empty `""`. |
| `<integer>` (e.g. `20`) | Process the next N undescribed URLs only. Useful for a short session. |
| `--force` or `--redo` | Process every URL in `bookmarks.jsonl`, overwriting existing descriptions. Re-collaborates from scratch. |
| `--only-sentinels` | Process only URLs whose current description is one of the four sentinel strings. Use to retry transient failures or revisit auth/JS pages with new context. |

`<integer>` combines with `--only-sentinels` (process next N sentinel entries). It does not combine with `--force` (force already processes everything).

## The per-URL turn

For each URL in the work queue, run this loop:

### 1. Fetch and classify

Retrieve the page with whatever web-fetch capability you have. Pull the bookmark's title and labels from `bookmarks.jsonl` for context — labels disambiguate sparse pages (a thin landing page in `RTutor > CUI` is about Controlled Unclassified Information, not coffee).

Classify the response:

- **Dead URL** (404 / 410 / DNS-not-found / timeout / SSL / 5xx / connection refused) → save the appropriate sentinel (`URL not found` or `Unreachable`) and move on **without prompting**. Show one line: `[N/total] <url> → URL not found (auto-saved)`.
- **Auth-walled** (login form, SSO redirect to `accounts.google.com`, `login.microsoftonline.com`, `okta.com`, `auth0.com`, etc., or "sign in to continue" interstitial with no public content) → AI draft is `(can't see — page is auth-walled)`. Default sentinel if user keeps: `Authentication required`. Continue to step 2.
- **JS-rendered shell** (body < ~200 chars after stripping, "Please enable JavaScript", empty SPA root) → AI draft is `(can't see — page is client-side rendered)`. Default sentinel if user keeps: `Unable to index`. Continue to step 2.
- **Real content** → write a 1-2 sentence factual draft from the page content and labels. Continue to step 2.

When in doubt between auth-walled and real content: a marketing homepage with "Sign in" in the corner *but* substantial public content is real content. Reserve `Authentication required` for pages where login is *the* gate to seeing anything.

### 2. Show the user the draft and ask

Print exactly this shape (one URL per turn):

```
[12/159] https://nist.gov/...
AI draft: <the 1-2 sentence draft, or the "(can't see…)" placeholder>

Why did you bookmark this? (k = keep, s = skip)
```

Then wait for the user's response. Show ONE URL at a time, not a batch.

### 3. Interpret the response

The user's reply maps to one of three actions:

- **`k`, `keep`, or empty** → save the AI's draft as the final description. For auth/JS cases where the draft is `(can't see...)`, save the sentinel string instead (`Authentication required` or `Unable to index`).
- **`s` or `skip`** → leave this URL's description empty in `descriptions.json` (so the next default run revisits it). Print `Skipped (will revisit next run).`
- **Free text** (anything else) → treat as the user's context. Synthesize the AI draft + user context into a polished 1-2 sentence final description. The user's intent is the load-bearing signal; the page content is supporting structure. Examples:

| AI draft | User says | Final |
|----------|-----------|-------|
| "NIST SP 800-171 — federal publication listing security requirements for CUI." | "I use this when scoping research IT controls for compliance" | "NIST SP 800-171 — federal publication listing 110 security requirements for protecting Controlled Unclassified Information; primary reference for scoping research IT controls." |
| "(can't see — auth-walled)" | "Snowflake account console for our prod warehouse" | "Snowflake account console for the production data warehouse — query editor, role/warehouse management, account configuration." |
| "Open-source bookmark parsing library." | "saved while researching how to build this very repo" | "Open-source library for parsing Netscape-format bookmark exports; saved during initial research for this project." |

### 4. Save immediately

Write the result before moving to the next URL using the bundled atomic helper. Pass the path to `descriptions.json` (in `$BOOKMARK_DIR`) and the URL as arguments, and the description on stdin via heredoc (this avoids shell-escaping problems):

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/update_description.py" "$BOOKMARK_DIR/descriptions.json" "<URL>" <<'DESC'
<the final description, sentinel, or empty string>
DESC
```

The helper takes the URL as an argument and the description on stdin. It writes to a tmp file and renames into place, so a crash mid-write can't corrupt `descriptions.json`.

Print one summary line, then advance to the next URL:

```
Saved: <first ~80 chars of the description>...
```

## After the queue is done

Regenerate `bookmarks.jsonl` and `bookmarks.md` with the merged descriptions by running `build_index.py`. It reads the HTML export and `descriptions.json` from the input HTML's directory and writes the outputs to the output directory, so run it against `$BOOKMARK_DIR` for both — e.g. point it at the HTML export in `$BOOKMARK_DIR` and pass `$BOOKMARK_DIR` as the output dir:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/build_index.py" "$BOOKMARK_DIR/<export>.html" "$BOOKMARK_DIR"
```

(If `$BOOKMARK_DIR` holds exactly one `.html`, the script auto-picks it when run with that directory as the working location.)

Then print a summary:

```
collaborated:               X
URL not found (auto):       X
Unreachable (auto):         X
kept AI draft:              X
kept sentinel (auth/JS):    X
skipped (left empty):       X
total this session:         Y
```

If any `Unreachable` entries showed up, mention they can be retried later with `--only-sentinels`. If the user skipped any, remind them those will surface again on the next default run.

## Description style

Whether the description is the AI's draft or a synthesis of user context:

- **Factual, present tense.** What the page *is* + what it's used for.
- **No marketing language.** Not "the world's leading platform for…" but "Cloud-based version control hosting service."
- **Specific over generic.** Not "Documentation page" but "Reference docs for the Anthropic Python SDK's Messages API."
- **User context leads when it exists.** "Used as the primary…" or "Reference for…" beats a neutral page summary, because the user's framing is the signal a future agent will search against.

Avoid naming the user explicitly ("Daniel uses this for…") — it reads weird at scale and the agent already knows whose bookmarks these are. Prefer "Used as the…", "Reference for…", "Saved during…".

## Pacing and fatigue

The user may do all URLs at once or do 10 a night for two weeks. Don't pressure them. If they answer with very short replies (one or two words), that's fine — synthesize on what they gave. If they go quiet or send something off-topic, treat the batch as ended: run `build_index.py`, print the summary for the URLs you did finish, and stop. They can resume next session.

## Why this design

- **The user's "why" is the retrieval signal.** Page content alone gives generic Wikipedia-flavored descriptions. The reason a link is in this user's bookmarks set is what an agent will later search against. Capturing that turns the file from a list of pages into a map of curation intent.
- **Cheap responses respect fatigue.** `k`/`s`/empty cover the common cases in one keystroke; only URLs the user actually has context for need a sentence.
- **No prompts on dead URLs.** There's nothing for the user to react to on a 404, so the skill saves the sentinel and moves on. Auth and JS pages still ask, because those are usually pages the user knows really well.
- **Durable progress.** Atomic writes after every URL mean a long session interrupted near the end doesn't lose work — the next run picks up exactly where it stopped.
- **Sentinels are reserved strings, not booleans.** The `descriptions.json` file alone tells you what happened for each URL — no separate state file — and `bookmarks.md` shows meaningful text for every entry.

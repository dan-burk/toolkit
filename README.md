# daniel-toolkit

My personal, cross-platform skill catalog — one repo, installed on every machine, works in **both Claude Code and OpenAI Codex**.

Everything here is a **skill** (`SKILL.md`), because skills are the one format both tools read. Commands and standalone agents from my old per-repo setups were converted into skills so they travel. User *data* (bookmarks, a workspace's `DOMAIN.md`) never lives here — only the code/templates that operate on it.

## The skills

| Skill | What it does |
|---|---|
| `generate-image-prompt-from-markdown` | Turn a markdown doc section into a structured, self-validated AI image prompt |
| `sketch-to-ascii-diagram` | Photo of a hand-drawn sketch → clean ASCII diagram → paste-ready Gemini infographic prompt |
| `review-r-code-pre-push` | Pre-push review of R changes: bugs, security, performance, test coverage → READY/NEEDS WORK |
| `r-data-science-best-practices` | R data-science coding conventions (auto-applied while writing R) |
| `analyze-data-for-story` | Iterative, story-first data-analysis project workflow |
| `review-data-code-correctness` | Adversarially audit data/stats code for hidden NAs, sentinels, silent row loss |
| `profile-and-catalog-datasets` | Bootstrap a workspace: discover, profile, catalog datasets into DOMAIN.md |
| `save-domain-knowledge-to-catalog` | Append generalizable findings from a finished analysis to DOMAIN.md |
| `save-session-progress` | Compress the session into a "Where Did We Leave Off?" recap + commit message |
| `update-documented-file-tree` | Reconcile a documented file tree with the repo's actual layout |
| `describe-bookmarks-interactively` | Walk bookmarks one URL at a time, capturing why each was saved |
| `load-bookmark-index` | Load the bookmark index into context for lookups |
| `diagnose-and-fix-code-error` | Systematic debug: gather → trace → root-cause → fix → verify |
| `check-network-for-tampering` | Triage the current network for spoofing/hijack/weak-WiFi signs (report-only) |

## Install (Claude Code)

**Local (this machine, for testing now):**
```bash
claude plugin marketplace add "/mnt/c/Users/Daniel Burkhalter/Documents/GitHub/daniel-toolkit"
claude plugin install daniel-toolkit@daniel-toolkit
```

**From GitHub (any machine, once pushed):** first set the `source` in `.claude-plugin/marketplace.json` to the git-subdir form:
```json
"source": { "source": "git-subdir", "url": "https://github.com/<USER>/daniel-toolkit.git", "path": "daniel-toolkit" }
```
then on each machine:
```bash
claude plugin marketplace add <USER>/daniel-toolkit
claude plugin install daniel-toolkit@daniel-toolkit
```
Update later with: `claude plugin marketplace update daniel-toolkit`.

## Use in OpenAI Codex

Codex reads `SKILL.md` from `~/.codex/skills/`. Point it at this repo's skills (symlink, so updates flow with `git pull`):
```bash
for d in "<repo>/daniel-toolkit/skills"/*/; do ln -s "$d" ~/.codex/skills/; done
```

## Maintaining across PCs

This repo is the single source of truth. Edit a skill → `git push`. On another machine → `git pull` (Codex) and/or `claude plugin marketplace update daniel-toolkit` (Claude Code). No account sync is involved; the repo is the sync mechanism.

## Conventions

- **Names** are `verb-noun-qualifier` so a skill's job is obvious at a glance.
- **No Claude-only constructs** in skill bodies (no tool name-drops, subagents, or `.claude/` paths) — instructions are intent-level so any capable agent can follow them.
- **Instruction file** is detected per platform: `CLAUDE.md` (Claude Code) or `AGENTS.md` (Codex).
- **Bundled assets** live in each skill folder and are referenced via `${CLAUDE_SKILL_DIR}/...`.

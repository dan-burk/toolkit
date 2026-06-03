# toolkit

Daniel Burkhalter's cross-platform SKILL catalog — one repo, installable on every machine. Claude Code and Codex compatible.

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

**Local (this machine):**
```bash
claude plugin marketplace add "/mnt/c/Users/Daniel Burkhalter/Documents/GitHub/toolkit"
claude plugin install toolkit@toolkit
```

**From GitHub (any machine, once pushed):**
```bash
claude plugin marketplace add <USER>/toolkit
claude plugin install toolkit@toolkit
```
Update later with: `claude plugin marketplace update toolkit`.

## Use in OpenAI Codex

Codex reads `SKILL.md` from `~/.codex/skills/`. Symlink this repo's skills so updates flow with `git pull`:
```bash
for d in "<repo>/skills"/*/; do ln -s "$d" ~/.codex/skills/; done
```

## Maintaining across PCs

This repo is the single source of truth. Edit a skill → `git push`. On another machine → `git pull` (Codex) and/or `claude plugin marketplace update toolkit` (Claude Code). No account sync involved; the repo is the sync mechanism.

## Conventions

- **Names** are `verb-noun-qualifier` so a skill's job is obvious at a glance.
- **No Claude-only constructs** in skill bodies — instructions are intent-level so either Claude Code or Codex can follow them.
- **Instruction file** is detected per platform: `CLAUDE.md` (Claude Code) or `AGENTS.md` (Codex).
- **Bundled assets** live in each skill folder, referenced via `${CLAUDE_SKILL_DIR}/...`.

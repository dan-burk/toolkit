# toolkit

Daniel Burkhalter's cross-platform SKILL catalog — one repo, installable on every machine. Claude Code and Codex compatible.

## The skills

| Skill | What it does |
|---|---|
| `sketch-to-ascii-diagram` | Sketch photo or markdown section → clean ASCII diagram → paste-ready Gemini infographic prompt |
| `ascii-to-architecture-diagram` | ASCII, markdown, or plain description → presentation-quality 1600x900 architecture diagram with real brand logos (HTML → self-reviewed PNG) |
| `review-r-code-pre-push` | Pre-push review of R changes: bugs, security, performance, test coverage → READY/NEEDS WORK |
| `r-data-science-best-practices` | R data-science coding conventions (auto-applied while writing R) |
| `review-data-code-correctness` | Adversarially audit data/stats code for hidden NAs, sentinels, silent row loss |
| `save-session-progress` | Compress the session into a "Where Did We Leave Off?" recap + commit message |
| `update-documented-file-tree` | Reconcile a documented file tree with the repo's actual layout |
| `describe-bookmarks-interactively` | Walk bookmarks one URL at a time, capturing why each was saved |
| `load-bookmark-index` | Load the bookmark index into context for lookups |
| `check-network-for-tampering` | Triage the current network for spoofing/hijack/weak-WiFi signs (report-only) |
| `record-installed-plugins` | Snapshot installed 3rd-party plugins into the `third-party-plugins.*` manifest |
| `restore-installed-plugins` | Print the `/plugin marketplace add … / install …` commands to reinstall the manifest on a new machine |

Which diagram skill? Sketch/photo → `sketch-to-ascii-diagram`, then its approved ASCII → `ascii-to-architecture-diagram`; text input → `ascii-to-architecture-diagram` directly.

## Agents

Claude Code only — Codex has no subagent equivalent (use the skill directly there).

| Agent | What it does |
|---|---|
| `diagram-designer` | Runs `ascii-to-architecture-diagram` end to end: spec → HTML → PNG, asks when labels/layout are ambiguous, and self-reviews the render before handing it over. Invoke with `@agent-toolkit:diagram-designer` or just ask for a polished architecture diagram. |

## Install (Claude Code)

Register this repo as a Claude Code plugin marketplace by running this in Claude Code:

```
/plugin marketplace add dan-burk/toolkit
```

Then install the plugin, either interactively:

- Select **Browse and install plugins**
- Select **toolkit**
- Select **Install now**

Alternatively, install it directly:

```
/plugin install toolkit@orditus
```

After installing, use a skill by just mentioning it — for instance: "Use the sketch-to-ascii-diagram skill on this photo" or "Review my R changes before I push."

Update later with `/plugin marketplace update orditus`.

## Use in OpenAI Codex

Codex reads `SKILL.md` from `~/.codex/skills/`. Symlink this repo's skills so updates flow with `git pull`:
```bash
for d in "<repo>/skills"/*/; do ln -s "$d" ~/.codex/skills/; done
```

## Maintaining across PCs

This repo is the single source of truth. Edit a skill → `git push`. On another machine → `git pull` (Codex) and/or `/plugin marketplace update orditus` (Claude Code). No account sync involved; the repo is the sync mechanism.

### When you change something — what to run

| You did this | Steps | Marketplace update? |
|---|---|---|
| **Installed a 3rd-party plugin** | Run `record-installed-plugins` (regenerates the manifest) → commit → push | ❌ No — the manifest is just a shopping list, only read by `restore-installed-plugins` on a fresh machine |
| **Added/edited a toolkit skill (to distribute)** | commit → push → `/plugin marketplace update orditus` → `/reload-plugins` | ✅ Yes — `update` pulls the new commit, `reload-plugins` loads it into the session. If it still doesn't show, re-run `/plugin install toolkit@orditus` |
| **Iterating on a skill locally** | `claude --plugin-dir <repo>` then edit + `/reload-plugins` | ❌ No — and no commit needed; changes are live instantly. Commit + push only when ready to distribute |

Don't hand-edit `third-party-plugins.*` — always run the `record-installed-plugins` skill so the manifest stays consistent.

## Conventions

- **Names** are `verb-noun-qualifier` so a skill's job is obvious at a glance.
- **No Claude-only constructs** in skill bodies — instructions are intent-level so either Claude Code or Codex can follow them.
- **Instruction file** is detected per platform: `CLAUDE.md` (Claude Code) or `AGENTS.md` (Codex).
- **Bundled assets** live in each skill folder, referenced via `${CLAUDE_SKILL_DIR}/...`.

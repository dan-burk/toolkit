# next-steps

Running notes for finishing setup and maintaining `toolkit`. Tick items off as you go.

## Outstanding setup

- [ ] **Push to GitHub** — create empty repo `dan-burk/toolkit`, then `git remote add origin https://github.com/dan-burk/toolkit.git && git push -u origin <branch>`. (Private repo recommended for a personal toolkit.)
- [ ] **Install + end-to-end test** — `claude plugin marketplace add dan-burk/toolkit` → `claude plugin install toolkit@toolkit`, then say "restore my installed plugins" and confirm `toolkit:restore-installed-plugins` prints the expected `claude plugin marketplace add … / install …` block.
- [ ] **Codex setup** (if/when using Codex) — symlink skills into `~/.codex/skills/`:
  `for d in "$(pwd)/skills"/*/; do ln -sfn "$d" ~/.codex/skills/; done`
- [ ] **(Optional) Fix this machine's plugins** — the 3 plugins (`document-skills`, `claude-api`, `example-skills`) are currently project-scoped to the DoD project. To make them global here: uninstall the project-scoped copies, then reinstall at user scope. The manifest is already global, so a fresh PC gets this right automatically.
- [ ] **(Optional) Enable marketplace auto-update** so you skip manual refreshes — toggle in `/plugin` (Marketplaces tab) or set `autoUpdate: true` for the marketplace in `~/.claude/settings.json`.

## Maintenance model

**The clone is the source of truth — always edit here, never the installed copy** (Claude keeps its own copy in `~/.claude/plugins/cache/…`; editing that does nothing). Loop: edit → commit → push → refresh other machines.

| Task | Steps |
|---|---|
| Tweak/fix a skill | Edit its `SKILL.md` → commit → push |
| Add a new skill | New `skills/<name>/SKILL.md` → commit → push |
| Record a new 3rd-party plugin | Run `toolkit:record-installed-plugins` → commit → push |
| Pull onto another PC | `git pull`, then refresh (below) |

**Two ways to work:**
- *Iterate fast (one machine):* `claude --plugin-dir ./toolkit` + `/reload-plugins` — see edits instantly, no commit needed.
- *Distribute (all machines):* commit + push, then `claude plugin marketplace update toolkit`. No version bumping — every commit is the latest.

**Refreshing differs by platform:**
- Claude Code: `claude plugin marketplace update toolkit` (or auto-update).
- Codex: `git pull` — symlinks reflect edits to existing skills instantly; a *new* skill needs re-linking (re-run the `ln -sfn` loop above).

**Gotchas:** edit the clone not the cache · Codex new-skill re-link · hand-maintained, no CI (a malformed `SKILL.md` silently won't load — spot-check) · `record` only captures the PC it runs on (run it on each machine where you install things).

## Candidate enhancements (not built yet)

- [ ] **`sync.sh`** — one command per machine: `git pull` + re-link Codex skills (`ln -sfn`) + `claude plugin marketplace update toolkit`. Makes "refresh this PC" a single step.
- [ ] **`new-skill` scaffolder** — script or meta-skill that stamps out `skills/<name>/SKILL.md` with correct frontmatter, so adding skills stays consistent.
- [ ] **Validation check** — a small script that lints every `SKILL.md` (valid frontmatter, has `name` + `description`) before commit, to catch the silent-no-load failure.

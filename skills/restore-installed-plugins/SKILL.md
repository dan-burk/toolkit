---
name: restore-installed-plugins
description: Read the third-party-plugins manifest from the daniel-toolkit repo and produce the exact commands to reinstall all recorded Claude Code marketplaces and plugins on a fresh machine. Use on a new PC after cloning daniel-toolkit, or whenever the user wants to restore, reinstall, or rebuild their installed plugins. Claude Code only.
---

# Restore installed plugins

Turn the manifest written by `record-installed-plugins` back into a working set of Claude Code plugins on a new machine. By default this **prints the commands for the user to review and run** — it does not install anything on its own (installing software is worth a glance first). Only run the commands directly if the user explicitly asks you to.

This skill is **Claude Code-specific**.

## 1. Find and read the manifest

Look for `third-party-plugins.lock.json` at the root of the `daniel-toolkit` checkout (current directory or a parent; if you can't find it, ask the user for the repo path). Fall back to parsing `third-party-plugins.md` only if the lock file is absent.

## 2. Emit the marketplace commands first

For each unique marketplace in the manifest, output:
```
claude plugin marketplace add <owner/repo>
```
(Marketplaces must be added before their plugins can be installed.)

## 3. Then the plugin install commands

For each plugin, output:
```
claude plugin install <plugin>@<marketplace>
```
Install everything **globally** (the default user scope) so it's available in every project — the manifest is a desired-state global list and carries no project pinning.

## 3b. Codex side (if present)

If the manifest lists `codex_skills`, remind the user that Codex consumes skills from `~/.codex/skills/` and give the symlink one-liner to relink this repo's skills there.

## 4. Present, don't execute

Show the full command block in one copy-paste-able fenced section, grouped (marketplaces, then plugins), with a one-line note per plugin saying what it is (from the manifest description) so the user can skip any they no longer want. Finish by telling them to run `claude plugin marketplace update` afterward if they want the latest versions. Offer to run the commands for them only if they ask.

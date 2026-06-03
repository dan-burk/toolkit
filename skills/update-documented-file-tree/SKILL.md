---
name: update-documented-file-tree
description: Reconcile the documented directory/file-structure tree with the repository's actual layout and rewrite it in place. Targets either a README or the agent-instruction file, auto-detecting whichever holds the structure section. Use when the user says 'update paths', 'sync the file tree', the structure section is stale, or after adding, moving, or deleting files.
---

# Update Documented File Tree

Compare the directory structure documented in a project's markdown with the actual directory structure in the repository, then rewrite the documented tree to reflect reality.

## Determine the target

1. **If the user names a file or section**, use that file and that section.
2. **Otherwise, auto-detect** which document holds the structure section. Look for headings such as "Project Structure", "File Organization", or "Repository Structure":
   - Prefer `README.md` if it contains such a section.
   - Else use the project's agent-instruction file — `CLAUDE.md` on Claude Code, `AGENTS.md` on Codex. Detect whichever exists at the repo root; if both exist, prefer the one already containing the structure section, else the one in active use.
3. Always locate the section by its **heading**, never by line number.

## Steps

1. **Read current documentation**: Extract the structure section from the target document.

2. **Scan actual structure**: List the real directory tree, focusing on:
   - All directories
   - Key files (R scripts, data files, markdown files, etc.)
   - Exclude: `.git/`, temporary files, OS files (`.DS_Store`, `Thumbs.db`, etc.)

3. **Identify differences**:
   - Files/folders that exist but aren't documented
   - Files/folders documented but no longer exist
   - Files that could be collapsed into patterns

4. **Apply pattern placeholder rules**:
   - **Preserve existing patterns**: If the document already uses a pattern like `debug<X>.r`, `plot_<metric>_by_<variable>.r`, or `PLAN_<feature>_<date>.md`, keep it.
   - **Search for related instructions**: Check if other sections of the document reference this pattern (e.g., "Debug scripts should live close to the subsystem being debugged"), and cross-reference them so the tree stays consistent.
   - **Multiple similar files**: If 3+ files follow a pattern (debug1.r, debug2.r, debug3.r), use a placeholder like `debug<X>.r`.
   - **Auto-generated directories**: For folders like `baselines/` and `output/` that contain timestamped files, use pattern examples (e.g., `daily_aggregate_<check_id>_<timestamp>.json`).
   - **Archive folders**: For any folder named "Archive", just show the folder exists with a brief comment. Don't list contents.
   - **Person-named folders**: For folders named after people (Daniel, Jenna, etc.), just show the folder exists with a brief comment. Don't list contents.
   - **Project folders**: For `projects/<project-name>/` directories, just show the project folder exists. Don't list internal files.
   - **Otherwise**: List specific filenames.

5. **Update the document**: Replace the structure section with the updated structure, preserving:
   - Comments explaining what directories contain
   - Inline annotations (like `# *** PRIMARY DATA PIPELINE ***`)
   - The ASCII tree structure format
   - Any Quick Reference table that follows the directory tree

6. **Report changes**: Show a concise summary of what was added, removed, or changed.

## Special considerations

- Keep the same level of detail for each directory (don't over-expand some and under-expand others).
- Maintain consistent comment style and formatting.
- Preserve any Quick Reference table that follows the directory tree.
- If unsure whether to use a pattern, err on the side of being specific (listing actual files).

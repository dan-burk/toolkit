---
name: save-domain-knowledge-to-catalog
description: Extract generalizable domain knowledge from a completed analysis project's notes and append it to the workspace DOMAIN.md so future analyses avoid known data pitfalls. Use after finishing an analysis, or when asked to record findings or domain knowledge.
---

# Save Domain Knowledge to Catalog

Extract domain knowledge from a project's notes file and append it to the workspace DOMAIN.md (the workspace data catalog — workspace-local user data, not shipped with the skill).

## Input
The user will specify a project name, or if not specified, use the most recently modified project in `projects/`.

## Workflow

1. **Read the project's notes file** — CLAUDE.md (Claude Code) or AGENTS.md (Codex), whichever exists:
   ```
   projects/<project-name>/<notes-file>
   ```

2. **Identify domain knowledge to extract**
   Look for:
   - Key findings about data structure or relationships
   - Variable meanings or interpretations discovered
   - Data quality issues or quirks found
   - Statistical insights (e.g., distributions, correlations)
   - Anything that would prevent mistakes in future analyses

3. **Format the extraction**
   Create a section like:
   ```markdown
   ### <project-name> (YYYY-MM-DD)
   **Finding:** [One-sentence summary]

   Key facts discovered:
   - [Fact 1]
   - [Fact 2]
   - ...
   ```

4. **Append to DOMAIN.md**
   Add the new section under the "## Project-Specific Findings" heading in the workspace DOMAIN.md.

5. **Confirm with user**
   Show what was added and ask if any edits are needed.

## Example

From `projects/na-column-patterns/` notes file:

**Extracted:**
```markdown
### na-column-patterns (2026-01-05)
**Finding:** The mostly-NA columns populate only for specific events, not random missing data.

Key facts discovered:
- `field_x` documents a specific subset of work
- Geographic concentration: 67% at one location
- Temporal analysis ruled out seasonal effects
```

## Notes

- Don't duplicate facts already in DOMAIN.md
- Focus on GENERALIZABLE knowledge, not project-specific details
- If a finding contradicts existing knowledge, flag it for review
- Keep entries concise - this is a reference, not documentation

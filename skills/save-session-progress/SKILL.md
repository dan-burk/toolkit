---
name: save-session-progress
description: Summarize the current session and write a compressed 1-3 bullet recap into the 'Where Did We Leave Off?' section of the project's agent-instruction file, then propose a Git commit message. Use when the user says 'save', 'save session', 'wrap up', 'log where we left off', or wants progress checkpointed before clearing context.
---

# Save Session Progress

Analyze the current conversation history and update the "Where Did We Leave Off?" section in the project's agent-instruction file with a compressed summary of this session, then generate a Git commit message.

## Target instruction file

This skill writes to the project's agent-instruction file:

- `CLAUDE.md` on Claude Code, `AGENTS.md` on Codex.
- Detect whichever exists at the repo root. If both exist, prefer the one already containing the "Where Did We Leave Off?" section; otherwise prefer the one in active use.
- Always locate the section by its `## Where Did We Leave Off?` heading, never by line number.

## Steps

1. **Analyze conversation history**: Review all messages in this session to identify:
   - Files created, modified, or deleted
   - Features implemented or bugs fixed
   - Key decisions, discoveries, or insights
   - Commands or workflows established
   - Problems solved or blockers encountered

2. **Generate compressed summary**: Create 1-3 concise bullet points that capture the essence of what was accomplished. Focus on:
   - **Concrete actions**: "Created X", "Fixed Y", "Updated Z"
   - **Decisions made**: "Decided to use X approach for Y"
   - **Key findings**: "Discovered that X causes Y"
   - Avoid vague statements like "worked on the codebase"

3. **Update the instruction file**:
   - Locate the section by its `## Where Did We Leave Off?` heading and read its current contents.
   - Replace it with:
     - The new session entry with today's date (format: YYYY-MM-DD)
     - Only ONE previous session (if one exists) to reduce clutter
     - Keep the `DO NOT REMOVE THIS SECTION!` warning
   - Remove any sessions older than the most recent previous session.
   - Always maintain exactly 2 sessions: current + one previous.

4. **Format template** (write this into the instruction file):
   ```markdown
   ## Where Did We Leave Off?

   **DO NOT REMOVE THIS SECTION!**

   **Last Session (YYYY-MM-DD)**:
   - [Bullet point 1]
   - [Bullet point 2]
   - [Bullet point 3]

   **Previous Session (YYYY-MM-DD)**:
   - [Previous bullet 1]
   - [Previous bullet 2]
   ```

5. **Generate commit message**: Create a Git commit message following this format:
   - **Title line**: 50 chars max, imperative mood (e.g., "Add feature" not "Added feature")
   - **Body** (optional): Wrap at 72 chars, explain what and why (not how)
   - Use conventional commit prefixes when appropriate: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`

6. **Report completion**: Show the user:
   - The new summary that was saved to the instruction file
   - The suggested commit message in a code block they can copy

## Output Format

```
Session saved to <instruction file>:

**Last Session (YYYY-MM-DD)**:
- [Bullet 1]
- [Bullet 2]

---

**Suggested commit message:**

```
docs: Update Reports documentation and rename init log

- Clarify file naming conventions and drift detection in READMEs
- Rename daily_aggregate_report to init_log_report for clarity
- Document that drift checks appear as _drift suffix in daily reports
```
```

## Guidelines

- Keep it compressed: 1-3 bullets for the current session.
- Use action verbs: "Created", "Fixed", "Updated", "Implemented", "Discovered".
- Be specific: Include file names, feature names, or key terms.
- Preserve context: Someone reading this weeks later should understand what happened.
- Always maintain exactly 2 sessions: current + one previous.
- Commit messages should be useful for `git log --oneline` scanning.

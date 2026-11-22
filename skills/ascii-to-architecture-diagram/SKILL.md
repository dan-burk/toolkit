---
name: ascii-to-architecture-diagram
description: Turn an ASCII diagram, a markdown description, or a plain description of a system into a presentation-quality, dark-themed architecture diagram with real brand logos — one self-contained 1600x900 HTML file, rendered to PNG and visually self-reviewed before delivery. Use when the user wants an exact, logo-accurate final image of a system/architecture/workflow for a slide, doc, or blog post.
argument-hint: <path-to-ascii-or-markdown[#section] | plain description>
---

# ASCII to Architecture Diagram

**Which skill?**
- Input is a **sketch or photo** → run `sketch-to-ascii-diagram` first, then this skill on its approved ASCII.
- Input is **text** (ASCII, markdown, plain description) → this skill directly.

The user has a system they want drawn — as an ASCII diagram, a markdown section, or just a description — and wants a **polished, exact image** of it: real brand logos, exact labels, nothing garbled. You build it as one self-contained HTML/SVG file, render it to PNG, look at it, fix it, and hand over the PNG.

If nothing was provided, ask for the ASCII, markdown path, or a description before doing anything else.

**This skill vs `sketch-to-ascii-diagram`.** That skill turns a sketch into an approved ASCII diagram plus a Gemini prompt for an illustrated "vibe" image (approximate logos, possibly garbled text). This skill produces the **exact, logo-accurate final image**. Use this one when labels and logos must be right.

**Bundled assets:**
- `${CLAUDE_SKILL_DIR}/templates/style-template.html` — base style: palette, grid, card, arrow, and boundary patterns.
- `${CLAUDE_SKILL_DIR}/examples/little-burky-architecture.png` (+ `.html`) — the gold-standard result. Match its quality bar: spacing, tile/logo treatment, arrow routing, label placement.
- `${CLAUDE_SKILL_DIR}/references/build-brief-template.md` — fill-in brief for Phase 1/2, with the brief that produced the gold-standard example.
- `${CLAUDE_SKILL_DIR}/scripts/embed_icons.py` — inlines Simple Icons logos in one call (Phase 2).

**Speed:** read only this file, the style template, and the example PNG. Open the example HTML or the brief template only if you need them.

(On Codex, `${CLAUDE_SKILL_DIR}` is this skill's folder.)

**Output location.** Save to a user-specified path, or default to the current directory: `./<slug>-architecture.html` and `./<slug>-architecture.png`, where `<slug>` is a short kebab-case name for the system.

---

## Phase 1 — Write the spec

Turn the input into a short written spec, modeled on the brief template:
- **Exact labels in Title Case.** One consistent name per thing, used everywhere (never "GH" in one place and "GitHub" in another).
- **Short subtitles only** — a few words (e.g. "Manager: Plans, Reviews, Ships"). No sentences, no version numbers.
- **Layout, top to bottom / left to right:** which zones/boundaries exist, what sits in each, what's nested.
- **Connections:** every arrow, its direction, and its short label (if any).
- **Logos:** the Simple Icons slug for each brand.

If anything is ambiguous — a label you're guessing at, unclear nesting, a connection whose direction isn't obvious — **ask the user before building.** Show the spec back briefly when the input was loose; skip that when the user handed you an exact brief.

## Phase 2 — Build ONE self-contained HTML file

Canvas exactly **1600x900** (16:9): `html, body` and one `<svg viewBox="0 0 1600 900">` at that size, no page scroll, no header outside the canvas, no summary cards, no footer. Follow the design system below and the gold-standard example.

### Real brand logos (Simple Icons)
1. Write the HTML with a `<!--ICONS-->` placeholder inside `<defs>`, and reference each logo as `<use href="#i-<slug>" ...>`. Don't paste any SVG paths yourself.
2. Run the script **once** with every slug (`python` on Windows):
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/embed_icons.py <file.html> <slug> [<slug> ...]
   ```
   It replaces the placeholder with a `<symbol id="i-<slug>">` per slug, filled with the brand hex, so the file renders offline. It prints `OK <slug> #<hex>` or `MISSING <slug>`. For a MISSING slug, try the nearest official alternative (e.g. `claude` → `anthropic`): put `<!--ICONS-->` back in `<defs>` and rerun with just that slug. Note which slug you used.
3. **No Python?** Fetch one logo per `curl -sfL https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/<slug>.svg` command, with the full URL written out (no loops or `&&` chains), and inline its path in a `<symbol>` with its brand hex.
4. Put every logo on a **light rounded tile** (e.g. 44x44, `rx="10"`, fill `#f8fafc`) so dark marks (GitHub, Ubuntu) stay visible on the dark background. Logo size is consistent everywhere, about **30px** (`<use href="#i-<slug>" width="30" height="30">` centered on the tile).
5. **No Simple Icons mark?** (Removed brands, internal tools, people.) Use a plain neutral glyph (person, terminal, sparkle, lock, database cylinder) in a neutral color — never a fake or hand-drawn brand logo — and tell the user which ones you substituted.

### Hard rules
- Minimal text. No sentences. Labels and short subtitles only.
- Nothing overlapping — cards, labels, tiles, boundaries, arrowheads.
- Arrows are drawn **behind** cards (earlier in the SVG); arrowheads land on card edges.
- Arrow labels sit clear of lines and boxes — never crossing or touching.
- **Every element is connected.** No floating cards: each card is reached by an arrow or is visibly nested inside a connected boundary. If the flow is a loop (e.g. review → back to the user), draw the loop.
- Generous whitespace, consistent spacing, aligned edges.

## Phase 3 — Render to PNG and look at it

**Find a renderer with ONE check — don't search again.**
- **Linux/macOS:** `command -v playwright chromium chromium-browser google-chrome google-chrome-stable microsoft-edge` (on macOS, also `ls "/Applications/Google Chrome.app" "/Applications/Microsoft Edge.app"` if that finds nothing).
- **Windows:** `where playwright chrome msedge`. Edge ships with Windows at `"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"`.

Render with what it found:
- **Chrome / Chromium / Edge** (preferred — 2x, 3200x1800):
  ```
  <browser> --headless --screenshot=out.png --window-size=1600,900 --force-device-scale-factor=2 --virtual-time-budget=5000 file:///abs/path.html
  ```
- **Only Playwright:** `playwright screenshot --viewport-size=1600,900 --wait-for-timeout=1500 file:///abs/path.html out.png` (1x is fine).

Use an absolute path; on Windows write it as `file:///C:/path/to/file.html`.

**Nothing found:** stop. Return the HTML path and tell the user to open it in a browser and screenshot it (or install Playwright). Don't write helper render scripts.

**Leave no helper files behind** — the only outputs are the HTML and the PNG.

**Self-review.** If you can view images, open the PNG and check it against the hard rules: overlaps, clipped text, labels touching lines, floating/disconnected cards, inconsistent logo sizes, invisible dark logos, cramped areas. Fix the HTML, re-render, and look again until it's clean. Never deliver a render you haven't looked at.

## Phase 4 — Deliver

Deliver the **PNG** (and mention the HTML path as the editable source). Never send an extra ASCII or text version of the diagram alongside it. In a short note, list the logo slugs used, any neutral glyphs substituted, and anything you couldn't do.

---

## Design system

### Color palette (semantic)

| Component Type | Fill (rgba) | Stroke (Hex) |
| :--- | :--- | :--- |
| **Frontend / People / Entry** | `rgba(8, 51, 68, 0.4)` | `#22d3ee` (cyan-400) |
| **Backend** | `rgba(6, 78, 59, 0.4)` | `#34d399` (emerald-400) |
| **Database / Core Service** | `rgba(76, 29, 149, 0.4)` | `#a78bfa` (violet-400) |
| **Cloud / Host Boundary** | `rgba(120, 53, 15, 0.3)` | `#fbbf24` (amber-400) |
| **Security / Sandboxed** | `rgba(136, 19, 55, 0.4)` | `#fb7185` (rose-400) |
| **Message Bus** | `rgba(251, 146, 60, 0.3)` | `#fb923c` (orange-400) |
| **External** | `rgba(30, 41, 59, 0.5)` | `#94a3b8` (slate-400) |

Arrows take the color of the flow they belong to; each color gets its own SVG marker.

### Typography and background
- **Labels:** Inter (600–700) for names; **subtitles and arrow labels:** JetBrains Mono, slate (`#94a3b8`) or the card's accent tint. Both from Google Fonts, with system fallbacks.
- **Sizes at 1600x900:** ~22px boundary/section titles, ~17px card names, ~14px chip names, ~13px subtitles and arrow labels.
- **Background:** slate-950 (`#020617`) with a subtle 40px grid, optionally a soft radial vignette.

```svg
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
  <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="0.5"/>
</pattern>
```

### Components
- Cards are rounded rects (`rx` 12–14; chips ~10) with 1.5px strokes. Inner chips use a dark fill (`rgba(15,23,42,0.78)`) with a `#334155` stroke.
- If arrows pass under semi-transparent fills, use a **double rect**: an opaque `#0f172a` rect first, the styled rect on top.

### Connections and boundaries
- **Z-order:** boundaries → arrows → cards → tiles/logos → text.
- Arrowheads via SVG markers; rounded elbows (`Q` curves) for routed lines.
- **Security flows:** dashed rose (`#fb7185`). **Return/feedback loops:** dashed, slightly transparent.
- **Boundaries:** host/region = large dashed (`10,6` or `8,4`) amber, `rx` 12–20; security group = dashed (`4,4`) rose.

### Spacing
- Minimum ~40px between sibling cards; message buses go *in the gap* between services, never overlapping them.
- A legend, if needed at all, goes outside every boundary. Prefer none — color and labels should be self-explanatory.

---

Based on [Cocoon AI's architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator) (MIT). `templates/style-template.html` is Cocoon AI's template, used under the MIT license.

Keep your own prose tight. The deliverable is the PNG.

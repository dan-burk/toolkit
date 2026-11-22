# Build brief template

Fill in the `<...>` placeholders from the Phase 1 spec, delete the optional lines you don't need, and follow the brief yourself (or hand it to a separate build agent). Keep the rules and wording; replace only the content.

---

## Template

```
Build a professional architecture diagram as ONE self-contained HTML file: <output-path>/<slug>-architecture.html

Style reference: <path-to>/style-template.html (dark slate background, subtle grid, rounded component cards, JetBrains Mono / Inter). Follow its design language, but this is a polished, presentation-quality diagram for a human, not a dense infra map. Canvas exactly 1600x900 px (16:9), everything inside one SVG/HTML block sized 1600x900 with no page scroll, no header text outside the canvas, no summary cards, no footer.

REAL LOGOS ARE REQUIRED. Use official brand marks from Simple Icons (https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/<slug>.svg). Download each with curl, verify it is a valid SVG, and INLINE the path data (no external image links at runtime, so it renders offline). Slugs to use (check each exists; if one is missing, try the nearest official alternative and tell me which you used): <slug-1>, <slug-2>, <slug-3>, ... (<slug-n> for <thing>; or use a clean <neutral glyph> icon if none fits). Render each logo in its brand color, at a consistent size (about 28-36 px) on a light rounded tile inside its card.

Content. Use Title Case for every label, and the same names everywhere:
- <Position, e.g. Top-left>: "<Actor / Entry Point>" (<logo or neutral glyph>), with <n> <channels/inputs> feeding into <target>, each with its logo: "<Label A>", "<Label B>", "<Label C>" (<Brand> logo).
- One large boundary box: "<Boundary Name>" with subtitle "<Host · Platform>" (<Brand> + <Brand> logos).
- Inside, <upper/left> card: "<Component Name>" with subtitle "<Role: Verb, Verb, Verb>". Inside it, small logo chips: "<Chip 1>", "<Chip 2>" (<Brand> logo), ...
- <Labeled arrows between cards: <direction> arrow "<Label>", <direction> arrow "<Label>".>
- Inside, <lower/right> card: "<Component Name>" with subtitle "<Short Constraint>". <n> sub-cards: "<Sub-card>" (<Brand> logo) with caption "<Caption>" and ...
- The flow must be CONNECTED: an arrow from <source> to "<Next Card>" (<logo>), then an arrow from that to "<Final Step>", visually closing the loop back toward <start>. No floating, disconnected elements.

Typography/layout rules: minimal text, no sentences, no version numbers, consistent spacing, nothing overlapping, arrows drawn behind cards, arrow labels never colliding with lines or boxes, generous whitespace. Make it look like a diagram from a polished engineering blog.

When done, report: the file path, every logo slug actually used, and anything you couldn't do.
```

---

## Worked example (the brief that produced `examples/little-burky-architecture.html`)

```
Build a professional architecture diagram as ONE self-contained HTML file: ~/work/diagram/architecture.html

Style reference: ./template.html (dark slate background, subtle grid, rounded component cards, JetBrains Mono / Inter). Follow its design language, but this is a polished, presentation-quality diagram for a human, not a dense infra map. Canvas exactly 1600x900 px (16:9), everything inside one SVG/HTML block sized 1600x900 with no page scroll, no header text outside the canvas, no summary cards, no footer.

REAL LOGOS ARE REQUIRED. Use official brand marks from Simple Icons (https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/<slug>.svg). Download each with curl, verify it is a valid SVG, and INLINE the path data (no external image links at runtime, so it renders offline). Slugs to use (check each exists; if one is missing, try the nearest official alternative and tell me which you used): claude (or anthropic), googlegemini, github, telegram, gmail, googledrive, googlecalendar, ubuntu, hostinger, gnubash (for SSH; or use a clean terminal icon if none fits). Render each logo in its brand color, at a consistent size (about 28-36 px) inside its card.

Content. Use Title Case for every label, and the same names everywhere:
- Top-left: "Daniel" (a simple person glyph is fine), with three channels feeding into the server, each with its logo: "SSH", "Telegram", "Email" (Gmail logo).
- One large boundary box: "Cloud Server" with subtitle "Hostinger VPS · Ubuntu" (Hostinger + Ubuntu logos).
- Inside, upper card: "Little Burky" with subtitle "Manager: Plans, Reviews, Ships". Inside it, small logo chips: "Hermes Agent", "Claude Opus" (Claude logo), "GitHub" (GitHub logo), "Gmail", "Google Drive", "Google Calendar" (their logos).
- Two labeled arrows between the cards: down arrow "Tasks", up arrow "Commits".
- Inside, lower card: "Agent Workshop" with subtitle "Locked Down: No Admin, No Keys". Two sub-cards: "Claude Code" (Claude logo) with caption "Coding" and "Antigravity" (Gemini logo) with caption "Research & Images".
- The flow must be CONNECTED: an arrow from the Little Burky card out of the server to a "GitHub Pull Request" card (GitHub logo), then an arrow from that to "Daniel Reviews & Merges", visually closing the loop back toward Daniel. No floating, disconnected elements.

Typography/layout rules: minimal text, no sentences, no version numbers, consistent spacing, nothing overlapping, arrows drawn behind cards, arrow labels never colliding with lines or boxes, generous whitespace. Make it look like a diagram from a polished engineering blog.

When done, report: the file path, every logo slug actually used, and anything you couldn't do. Do NOT push anything. Do not touch any git repo.
```

Note on the result: "Hermes Agent" had no Simple Icons mark, so it got a neutral sparkle glyph; "Daniel" got a neutral person glyph.

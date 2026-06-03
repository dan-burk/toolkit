---
name: sketch-to-ascii-diagram
description: Turn a photo of a hand-drawn sketch into a clean, self-critiqued ASCII/Unicode diagram, then a paste-ready image-generation prompt for a polished infographic. Use when the user has a whiteboard or napkin sketch they want cleaned up into a slide- or web-ready visual for a mixed developer + executive audience.
argument-hint: <path-to-sketch-image>
---

# Sketch to ASCII Diagram

The user has a hand-drawn sketch or rough diagram and wants two things out of it:
1. A clean **ASCII/Unicode diagram** that captures the sketch accurately, and
2. An **image-generation prompt** that turns that diagram into a polished, colorful infographic for a slide deck or webpage.

The sketch image path is provided as the argument. If no path was provided, ask the user for the image path — or to paste/attach the image — before doing anything else.

Work through the phases below. Move at a good pace, but treat this as collaborative: the user expects a couple of back-and-forth iterations, not a one-shot answer.

**Output location.** This run's deliverables get saved to their own folder: `documentation/image-prompts/<slug>/` in the current project (create `documentation/image-prompts/` if it doesn't exist — these are documentation artifacts). `<slug>` is a short kebab-case name for the diagram's subject (e.g. `auth-flow`, `data-pipeline`) — pick it from what the sketch depicts and confirm it with the user before writing files. Each run gets its own `<slug>/` subfolder, holding:
- `diagram.md` — the approved ASCII diagram.
- `gemini-prompt.md` — the image-generation prompt.

---

## Phase 1 — See the sketch

Open and view the image at the given path (any capable agent can view images natively). Then:
- Confirm you can actually see it. If it's unreadable/blurry, say so and ask for a better photo.
- Briefly list back what you see (the boxes, arrows, labels, any legend) so the user can correct any misreading **before** you invest in the diagram. Hand-drawn text is often ambiguous — call out anything you're guessing at.

## Phase 2 — Draft the ASCII diagram

Draw an ASCII/Unicode diagram that captures the sketch. Guiding rules:
- **Least text possible while still followable.** No editorializing labels, no redundant words. Position and arrows should carry meaning.
- One consistent visual vocabulary — pick one box style, one or two arrow styles (reserve a distinct style only for something special like a trust/system boundary).
- One clear flow direction (top-to-bottom or left-to-right); keep a single spine.
- If the system has zones (e.g. local vs cloud, frontend vs backend), draw each zone once with one boundary between them — don't represent the same boundary three different ways.
- Preserve any legend/key or structural call-out from the sketch if it does real teaching work; cut it if it's noise.

## Phase 3 — Self-critique harshly, then revise

Switch into a harsh-reviewer mindset and adversarially critique your own draft on the two axes below **without rewriting it as you go.** Hold in mind: (a) a faithful description of what the source sketch shows, (b) any ground-truth facts you've established, and (c) your draft ASCII. Critique on these TWO axes:
- **Accuracy** — anything wrong, missing, ambiguous, or conflated vs the source.
- **ASCII clarity / minimalism** — broken arrow alignment, dangling arrows that point nowhere, redundant boundary devices, inconsistent node/arrow vocabularies, and what to CUT without losing followability.

Then fold the high-leverage fixes back in and reprint the diagram. Do a second critique round if the diagram is complex or the first pass found a lot. Tell the user what changed and why. Iterate with the user until they're happy with the ASCII.

**On approval:** write the final ASCII to `documentation/image-prompts/<slug>/diagram.md` (wrap it in a fenced code block, with a one-line title above it). Only write this file once the user has explicitly approved the diagram — never before.

## Phase 4 — Build the image prompt

Once the ASCII is approved, write a prompt the user can paste into an image generator (e.g. Gemini) to produce a polished infographic. First, settle these with the user (ask only what you can't sensibly infer):
- **Audience** — default to **both a developer and a curious, non-technical CEO**: the image should be technically faithful enough that an engineer nods along, but framed and labeled so a curious executive can follow what's going on without jargon. This dual framing is the default; only change it if the user asks for a different audience. It sets how much technical detail survives the simplification below.
- **Format / aspect ratio** (16:9 for slides, vertical/square for web).
- **Logos / brand icons** to include (e.g. Node.js, R, Google, Stripe, AWS…).
- **Style** (flat modern, playful, corporate, etc.).

Then **simplify the diagram for the image.** Image models garble dense text and fine arrows, so strip to the legible spine (roughly 6–10 short labels). Keep the detailed ASCII as the source-of-truth; the image is the "vibe" version.

Write the prompt with this structure so the model can't wander:
- Goal + audience + format/aspect in the first lines.
- **LAYOUT**: named zones and what sits in each.
- **Exact short text labels**, quoted verbatim, kept short — explicitly tell the model to use these labels and invent no others (this is the main defense against garbled text).
- **Logos/icons** to place, by name.
- **Arrows** with their short labels.
- **STYLE**: palette, flat/rounded, white space, legible sans-serif.
- A constraint line: beautify layout/color/icons only; do not add, remove, or rename any technical content.

Show the prompt to the user. Once they're happy with it, save it to `documentation/image-prompts/<slug>/gemini-prompt.md` (the raw prompt in a fenced code block so it's easy to copy, with a short title line above it). Then tell the user both file paths (`diagram.md` and `gemini-prompt.md`) so they know where the run landed.

## Phase 5 — Caveats + optional accurate companion

Tell the user plainly:
- AI image models approximate brand logos and may garble dense text — expect 2–3 generations; drop real logo PNGs on top afterward (PowerPoint/Figma/Canva) if exact branding matters.
- Offer a **pixel-accurate companion** (Mermaid or SVG/HTML) if they want every label exact and editable — less illustrated, but diffable and precise. Present this as an explicit yes/no option for the user to take or leave. If they don't respond to the offer (ignore it, or end the conversation), assume **no** and do not build it.

---

Keep your own prose tight throughout. The deliverables are the diagram and the prompt; don't bury them in explanation.

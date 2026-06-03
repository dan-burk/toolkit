---
name: generate-image-prompt-from-markdown
description: Turn a section of a markdown document into a structured, validated AI image-generation prompt (architecture, workflow, comparison, timeline, code, metaphor, or conceptual visualization), ready to paste into any image model. Use when the user wants to visualize or illustrate documentation or spec content.
argument-hint: <path-to-markdown-file> [section name/number | "1,3,5" | "1-3" | all]
---

# Generate Image Prompt from Markdown

Generate structured AI image-generation prompts from markdown documentation sections. Works with ANY markdown file by auto-detecting sections through heading hierarchy. The output is a self-contained prompt the user can paste into any image generator (DALL-E, Midjourney, Stable Diffusion, Gemini, etc.).

## Inputs

You need, at minimum, a path to a markdown file. The user may also provide:
- **A specific section** — by name fragment (e.g. `MCP Servers`) or by number (e.g. `2`).
- **A multi-select** — `1,3,5` (sections 1, 3, and 5) or `1-3` (sections 1 through 3).
- **All sections** — `all` (batch mode: generate one prompt per top-level section).

If no section is specified, present a numbered menu of the detected sections and let the user choose (number, name fragment, `1,3,5`, `1-3`, or `all`).

## Steps

### 1. Resolve and read the source file
- Take the markdown file path from the input.
- Verify the file exists and is markdown (`.md`). If not found or not markdown, show a helpful error with examples (see Error Handling).
- Read the entire file content.

### 2. Detect sections using heading hierarchy
- Scan the file for `##` headings (primary sections) and `###` headings (subsections).
- Build a section index with structure:
  ```
  {
    title: "Chapter 2: MCP Servers",
    level: 2,  # (## = 2, ### = 3)
    line_start: 166,
    line_end: 396,
    parent: null  # (or parent section index)
  }
  ```
- Example detection:
  ```
  Line 29: "## Chapter 1: Claude Code (CLI)"  → Section 1, lines 29-165
  Line 166: "## Chapter 2: MCP Servers"       → Section 2, lines 166-396
  Line 168: "### Question: Where do I..."     → Subsection 2.1, lines 168-179
  ```

### 3. Show a menu (only if no section was specified)
- Display: `"Found {N} sections in {filename}:"`
- List all `##` level sections, numbered 1, 2, 3...
- Show format: `"{number}. {section_title}"`
- Instructions: "Enter number, name fragment, '1,3,5', '1-3', or 'all'"
- If the user already specified a section in the input, skip the menu and jump to step 4.

### 4. Extract the target section content
- From the section heading line to (next same-level heading line - 1).
- Include all subsections (`###` and `####`) under the parent `##`.
- If the user selects a subsection specifically, only extract that subsection.
- Typically 50-300 lines per section.
- Store: section_title, section_content, line_range.

### 5. Analyze content type (7 visualization types)
Scan the section content for keywords to determine the visualization type:

| Type | Detection Keywords | Default Dimensions |
|------|-------------------|-------------------|
| **architecture** | "layer", "component", "server", "system", "container", "architecture" | 1920x1080 |
| **workflow** | "step", "process", "workflow", "then", "next", "flow", "procedure" | 1920x1080 |
| **comparison** | table syntax `\|`, "vs", "versus", "compared to", "difference" | 1920x1200 |
| **timeline** | "level", "stage", "evolution", "progression", "history", "timeline" | 2400x600 |
| **code** | code blocks (```), "function", "class", "implementation", "snippet" | 1920x1200 |
| **metaphor** | "like", "think of", "metaphor", "imagine", "similar to", "analogy" | 1200x1200 |
| **conceptual** | (default if no other keywords match) | 1920x1080 |

Use the **first matching type** from the priority order above.

### 6. Generate the structured prompt

Use the template reference at `${CLAUDE_SKILL_DIR}/template-reference.md` for detailed section structures, color scheme examples, composition guidance, metaphor integration, and target audience specifications.

**Base structure** (all prompts):

```markdown
# Image Generation Prompt: {Section Title}

## Overview
{2-3 sentence description of what to visualize based on section content}

{Extract key concepts, main topic, purpose from section}

**Target Audience**: {Infer from technical complexity: "Technical developers", "Business stakeholders", "General audience"}

## Visual Style
- **Style**: {Clean/Technical/Artistic based on content type}
- **Layout**: {Vertical/Horizontal/Circular based on visualization type}
- **Color Scheme**:
  - Primary: {Hex code} - {Purpose}
  - Secondary: {Hex code} - {Purpose}
  - Accent: {Hex code} - {Purpose}
  - Background: {Hex code}
  - Text: {Hex code}
- **Typography**: {Clear, readable sans-serif / Monospace for code / etc.}
- **Icons**: {Style guidance - friendly, technical, minimalist, etc.}

## {Type-Specific Content Section}

{Insert appropriate section based on visualization type - see type templates below}

## Composition Guidelines
- **Whitespace**: {Generous / Balanced / Compact - based on content density}
- **Fonts**: Large enough to read in presentations (min 16pt for body text)
- **Emphasis**: {What to highlight - key concepts, relationships, critical points}
- **Layout Flow**: {Top-to-bottom / Left-to-right / Center-outward}

## Example Short Prompt for AI Generation
{100-200 word condensed version optimized for quick image generation}

Include:
- Core visualization description
- Key elements to show
- Style and color guidance
- Layout recommendation

## Metadata
- **Source**: {file_path}
- **Section**: {section_title}
- **Visualization Type**: {detected_type}
- **Suggested Dimensions**: {dimensions based on type}
- **Generated**: {current_date YYYY-MM-DD}
- **Content Lines**: {line_start}-{line_end}
```

**Type-specific middle sections:**

#### Architecture Type:
```markdown
## System Architecture

### Layers / Components
{List major components with descriptions}

1. **{Component Name}**
   - Purpose: {What it does}
   - Visual: {Icon / Shape / Color}
   - Position: {Where in diagram}

### Connections
- {Component A} → {Component B}: {Relationship description}
- Flow arrows with labels
- Interaction types (API calls, data flow, etc.)

### Callouts
{2-3 callout boxes explaining key concepts or clarifications}
```

#### Workflow Type:
```markdown
## Process Workflow

### Steps
{Extract sequential steps from content}

1. **Step Name**: {Description}
   - Input: {What's needed}
   - Action: {What happens}
   - Output: {Result}

### Decision Points
- {Decision description}: Yes → {Path A}, No → {Path B}

### Flow Visualization
- Use clear directional arrows
- Color-code different paths
- Show loops or branches explicitly
```

#### Comparison Type:
```markdown
## Comparison Elements

### Dimensions Being Compared
{Extract comparison categories from table or content}

### Side-by-Side Elements
| Aspect | Option A | Option B |
|--------|----------|----------|
| {Dimension 1} | {Value/Description} | {Value/Description} |

### Visual Encoding
- Use split-screen or column layout
- Color-code differences (green = advantage, red = disadvantage)
- Highlight key differentiators
```

#### Timeline Type:
```markdown
## Timeline Stages

### Progression
{Extract stages/levels/phases from content}

1. **Stage Name** ({Time/Level})
   - Key characteristics
   - Visual representation
   - Transition to next stage

### Overall Flow
- Left-to-right or top-to-bottom progression
- Show evolution/growth visually
- Mark key milestones
```

#### Code Type:
```markdown
## Code Visualization

### Code Structure
{Show code with annotations}

```language
{Actual code snippet from section}
```

### Annotations
- Highlight key lines with callout boxes
- Explain important concepts
- Show data flow or logic path

### Visual Elements
- Syntax highlighting
- Line numbers or section markers
- Arrows pointing to explained sections
```

#### Metaphor Type:
```markdown
## Metaphor Illustration

### Central Metaphor
{Extract metaphor from content}

### Visual Mapping
- {Real concept} = {Metaphor element}
- Show parallel structure
- Make connections obvious

### Relatable Elements
{Describe how to visualize the metaphor clearly}
```

#### Conceptual Type (Default):
```markdown
## Conceptual Diagram

### Key Concepts
{Extract main ideas from section}

1. **{Concept Name}**
   - Definition/Description
   - Visual representation (shape, icon, etc.)
   - Relationships to other concepts

### Relationships
- {Concept A} ↔ {Concept B}: {Connection description}
- Show hierarchy, dependencies, or interactions

### Abstract Representations
{Guidance on visualizing non-physical concepts}
```

### 7. Self-review before finalizing (5-dimension validation)

Before finalizing each generated prompt, switch into a Professional AI Image Prompt Expert mindset and review your own draft against the framework below. Read the prompt from beginning to end, score each dimension systematically using the rubrics, determine an overall verdict, then fold concrete improvements back into the prompt before output. This is a self-review pass within the same flow — no separate agent.

You evaluate prompts across 5 critical dimensions:

#### 1. COMPLETENESS Check
**Question**: Does the prompt include all essential sections?

**Required sections**:
- ✅ Title/Overview section
- ✅ Visual Style specifications (style, layout, colors, typography, icons)
- ✅ Type-specific content (layers, steps, comparisons, etc. - varies by type)
- ✅ Composition Guidelines (whitespace, fonts, emphasis)
- ✅ Example Short Prompt (condensed 100-200 word version)
- ✅ Metadata (source, section, type, dimensions, date)

**What to check**:
- Count sections present vs required (target: 6/6)
- Flag missing sections explicitly
- Note if sections exist but are empty or placeholder text

**Scoring**:
- 6/6 sections = COMPLETE ✓
- 5/6 sections = MINOR GAP ⚠
- ≤4/6 sections = MAJOR GAP ✗

#### 2. CLARITY Check
**Question**: Are descriptions concrete and specific vs vague?

**Red flags** (vague language):
- "Nice colors" → Should specify hex codes
- "Big elements" → Should specify relative sizes
- "Some connections" → Should enumerate and describe
- "Good layout" → Should specify arrangement (vertical, horizontal, grid, etc.)
- "Professional look" → Should define what makes it professional

**Green flags** (concrete language):
- "Primary: #2C3E50 (dark blue) for trust and stability"
- "24pt sans-serif bold headers, 16pt body text"
- "3 horizontal layers with 20px spacing between"
- "Arrows flow left-to-right connecting each component"

**What to check**:
- Are colors specified with hex codes?
- Are sizes given in relative or absolute terms?
- Are positions and layouts explicitly defined?
- Are relationships and connections described clearly?

**Scoring**:
- Mostly concrete, specific details = HIGH CLARITY ✓
- Mix of concrete and vague = MEDIUM CLARITY ⚠
- Mostly vague, general descriptions = LOW CLARITY ✗

#### 3. VISUAL CONSISTENCY Check
**Question**: Do all visual elements form a coherent design system?

**Color palette coherence**:
- Are 3-5 colors defined?
- Do colors have complementary relationships?
- Are colors assigned clear semantic meanings? (e.g., blue = system components, green = data flow)
- Are background and text colors readable (sufficient contrast)?

**Typography consistency**:
- Are font families specified (serif/sans-serif/monospace)?
- Are size hierarchies clear (headers, subheaders, body)?
- Do font choices match the content type? (monospace for code, sans-serif for technical, etc.)

**Style unity**:
- Do icon styles match? (all flat, all line art, all 3D, etc.)
- Does layout match content? (workflow = left-to-right, hierarchy = top-to-bottom)
- Are metaphors consistent if used?

**What to check**:
- Color palette is defined and complementary
- Typography system is specified
- Visual style is internally consistent
- No contradictory guidance (e.g., "minimalist" but also "highly detailed")

**Scoring**:
- Cohesive visual system throughout = PASS ✓
- Some inconsistencies but workable = MINOR ISSUES ⚠
- Contradictory or incoherent elements = FAIL ✗

#### 4. TARGET AUDIENCE Alignment Check
**Question**: Is the technical complexity appropriate for the intended audience?

**Audience indicators**:
- **Technical developers**: Code snippets, technical terms, detailed architectures
- **Business stakeholders**: High-level concepts, metaphors, simplified flows
- **General audience**: Minimal jargon, heavy use of metaphors and icons

**What to check**:
- Is target audience explicitly stated?
- Does visual complexity match audience? (developers = detailed OK, general = simplified)
- Does terminology match audience? (technical = APIs, schemas; general = simpler terms)
- Are explanations at appropriate depth?

**Red flags**:
- High technical detail for "general audience"
- Oversimplified diagrams for "advanced developers"
- No target audience specified at all

**Scoring**:
- Clear audience, appropriate complexity = ALIGNED ✓
- Audience unclear or minor mismatches = MINOR MISALIGNMENT ⚠
- Wrong complexity level for audience = MISALIGNED ✗

#### 5. ACTIONABILITY Check
**Question**: Can an AI image generator execute this prompt successfully?

**Executable criteria**:
- Spatial relationships are clear ("top left", "center", "bottom right", "arranged horizontally")
- Element counts are specific ("3 boxes", "5 arrows", "4 layers")
- Visual attributes are described ("blue rectangle", "dashed line", "bold text")
- Relationships are explicit ("A connects to B with arrow", "X sits above Y")

**What to check**:
- Could you sketch this based on the prompt? If yes → actionable
- Are there ambiguous instructions? ("arrange nicely" = BAD, "arrange in 2x2 grid" = GOOD)
- Are all visual elements accounted for?
- Is there enough detail without being overconstrained?

**Red flags**:
- Vague spatial descriptions
- "Figure it out" type instructions
- Missing critical details (what are the components?)
- Conflicting instructions

**Scoring**:
- Clear, executable instructions = HIGH ACTIONABILITY ✓
- Mostly clear with minor ambiguities = MEDIUM ACTIONABILITY ⚠
- Too vague to execute reliably = LOW ACTIONABILITY ✗

#### Self-review report format

Produce a short report in this structure:

```
IMAGE PROMPT VALIDATION REPORT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 PROMPT DETAILS
Source: {file_path}
Section: {section_title}
Visualization Type: {type}
Target Audience: {audience}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ VALIDATION SCORES

1. COMPLETENESS:        {6/6 ✓ | 5/6 ⚠ | ≤4/6 ✗}
   {If not 6/6: "Missing: [list missing sections]"}

2. CLARITY:             {HIGH ✓ | MEDIUM ⚠ | LOW ✗}
   {If not HIGH: Brief explanation of vague areas}

3. VISUAL CONSISTENCY:  {PASS ✓ | MINOR ISSUES ⚠ | FAIL ✗}
   {If not PASS: Brief explanation of inconsistencies}

4. TARGET AUDIENCE:     {ALIGNED ✓ | MINOR MISALIGNMENT ⚠ | MISALIGNED ✗}
   {If not ALIGNED: Brief explanation}

5. ACTIONABILITY:       {HIGH ✓ | MEDIUM ⚠ | LOW ✗}
   {If not HIGH: Brief explanation of ambiguities}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 OVERALL ASSESSMENT

{Count checkmarks: 5✓ = APPROVED, 3-4✓ = MINOR REVISIONS, ≤2✓ = MAJOR REVISIONS}

VERDICT: {APPROVED ✓ | MINOR REVISIONS NEEDED ⚠ | MAJOR REVISIONS NEEDED ✗}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 RECOMMENDED IMPROVEMENTS

{If APPROVED: "Prompt is ready for image generation!"}

{If MINOR REVISIONS: List 2-4 specific improvements}
1. {Concrete fix with example}
2. {Concrete fix with example}

{If MAJOR REVISIONS: List all critical issues}
1. {Critical fix needed}
2. {Critical fix needed}
3. {Critical fix needed}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Verdict thresholds** (count the ✓ across the 5 dimensions):
- 5 ✓ = APPROVED (ready to use)
- 3-4 ✓ = MINOR REVISIONS (usable but improvable)
- ≤2 ✓ = MAJOR REVISIONS (needs significant work)

**Apply the fixes.** Be specific ("Add hex code for accent color: #E74C3C" not "improve colors"), give examples of what good looks like, prioritize most critical issues first, and acknowledge what's working. For mechanical gaps (missing hex codes, dimensions, target audience), fill them in directly. Fold the improvements into the prompt so the finalized output reflects an APPROVED state wherever possible.

### 8. Determine output location
- Extract the base filename from the source path (e.g., `my-doc.md` → `my-doc`).
- Use a subdirectory `image-prompts/{base_filename}/` (relative to the project/working root). Create it if it doesn't exist.

**Filename generation** — sanitize the section title:
- Convert to lowercase
- Replace spaces with hyphens
- Remove special characters (keep only a-z, 0-9, hyphens)
- Truncate to 50 chars if needed
- Format: `{sanitized_section_title}_{YYYY-MM-DD}.md`
- Examples:
  - `"Chapter 2: Overview"` → `chapter-2-overview_{YYYY-MM-DD}.md`
  - `"Section III.A"` → `section-iii-a_{YYYY-MM-DD}.md`

**File existence check** — if a file with the same date already exists, ask the user whether to regenerate, or suggest using a different section or trying again tomorrow.

### 9. Write the output file
Write the complete structured prompt to:
`image-prompts/{base_filename}/{sanitized_section_title}_{YYYY-MM-DD}.md`

### 10. Display a summary

**For a single section**:
```
Image Prompt Generated Successfully! 🎨

Source: {file_path}
Section: {section_title}
Visualization Type: {type}
Output File: {relative_path_to_output_file}

Validation Result: {APPROVED / MINOR REVISIONS / MAJOR REVISIONS} {✓ or ⚠}

Quick Stats:
- Prompt length: {line_count} lines
- Suggested dimensions: {dimensions}
- Color palette: {color_count} colors defined
- {Additional relevant stats based on type}

{If validation found issues}:
Validation Notes:
- {Issue 1}
- {Issue 2}

Next Steps:
1. Review full prompt: {output_file_path}
2. Copy "Example Short Prompt" section for quick generation
3. Generate another section by re-running with a different section
```

**For batch processing** (multi-select or `all`):
```
Batch Image Prompts Generated Successfully! 🎨📦

Source: {file_path}
Sections Processed: {count}
Output Directory: image-prompts/{base_filename}/

Files Created:
✓ {filename1} ({type1})
✓ {filename2} ({type2})
✓ {filename3} ({type3})
...

Validation Results:
- Approved: {approved_count}
- Minor revisions: {minor_count}
- Major revisions: {major_count}

{If any failures}:
Failed Sections:
✗ {section_name}: {error_reason}

Next Steps:
1. Review all prompts: image-prompts/{base_filename}/
2. Address revisions for flagged prompts
3. Begin image generation with your preferred tool
```

## Error Handling

**File not found**:
```
Error: File not found: {file_path}

Please check the path and try again.

Examples:
  path/to/your-file.md
  README.md
```

**Not a markdown file**:
```
Error: File must be a markdown file (.md extension)

Received: {file_path}
Expected: *.md file
```

**No sections detected**:
```
Error: No ## headings found in {file_path}

This requires markdown files with ## (h2) headings.

Current file structure: {brief summary}
```

**Section not found**:
```
Error: Section "{section_query}" not found in {file_path}

Available sections:
1. {section1_title}
2. {section2_title}
3. {section3_title}

Try:
- Entering a number (1, 2, 3...)
- Using part of the title: "MCP" instead of full title
- Running without a section argument for the interactive menu
```

## Guidelines

- **Content Extraction**: Focus on extracting the ESSENCE of the section, not just copying text.
- **Visual Thinking**: Think about how concepts translate to visual elements.
- **Color Psychology**: Choose colors that reinforce the message (blue = trust, green = growth, orange = energy).
- **Hierarchy**: Most important elements should be largest/most prominent.
- **Simplicity**: Don't overcrowd - aim for clarity over comprehensiveness.
- **Metaphors**: When content has metaphors, make them central to the visualization.
- **Context**: Include enough context that the image stands alone.
- **Actionability**: Prompts should be specific enough that an AI can execute them.
- **Flexibility**: Generated prompts should work across different AI image generators (DALL-E, Midjourney, etc.).

## Special Behaviors

**Batch processing** (`all`):
- Process ALL `##` sections in sequence.
- Generate a separate prompt file for each.
- Show an aggregate summary at the end.
- Continue on errors (don't stop the entire batch).

**Multi-select** (in the menu):
- `1,3,5` → process sections 1, 3, and 5.
- `1-4` → process sections 1 through 4.
- `all` → process all sections.

**Fuzzy matching** (section selection):
- The user can type a partial section title.
- Match against all section titles.
- If multiple matches, show options.
- If a single match, proceed automatically.

## Template Reference

The comprehensive example template is at `${CLAUDE_SKILL_DIR}/template-reference.md`. Use it as reference for detailed section structures, color scheme examples, composition guidance, metaphor integration, and target audience specifications.

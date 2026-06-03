---
name: analyze-data-for-story
description: Run an iterative, story-first data-analysis project to discover WHY a pattern exists. Use when exploring a dataset or question, continuing an existing analysis, or building a documented, reproducible analysis project with scripted outputs and figures.
---

# Data Analysis Workflow

Create or continue an analysis project in `projects/` to explore a data question, using iterative analysis to discover the underlying story.

---

## Quick Checklist (DO THIS FIRST)

**For NEW projects:**
1. [ ] Read domain knowledge: the workspace DOMAIN.md
2. [ ] **CREATE PROJECT FOLDER IMMEDIATELY** - `projects/<name>/` with a project notes file, scripts/, output/, figures/
3. [ ] Write ALL analysis in scripts using `start_output()`/`end_output()`
4. [ ] Document findings in the project notes file

**NO AD-HOC EXPLORATION.** All analysis happens inside project scripts. No exceptions.

**For EXISTING projects:**
1. [ ] Read domain knowledge (may have new insights)
2. [ ] Read the project's notes file
3. [ ] Continue from where you left off

---

## Input
The user will provide either:
- A new topic/question: "Explore columns X, Y, Z which are mostly NA"
- A project to continue: "Continue the clustering project"
- An implicit continuation: "Let's pick up where we left off on repair times"

## Philosophy

**Story-first, not report-first.** The goal is to uncover *why* patterns exist, not just document *that* they exist. Numbers without narrative are not useful.

Key principles:
1. **Start broad, narrow dynamically** - Begin with multiple hypotheses, but abandon unproductive lines quickly
2. **Ask "so what?" after every analysis** - If a finding doesn't advance the story, move on
3. **The plan is a living document** - Update it as you learn what matters
4. **Concentration reveals causation** - When data clusters (e.g., 6 entities account for 80% of events), that IS the story
5. **Show actual values, not just counts** - If <=15 unique values, list them all; otherwise show top 5
6. **ELI5 test** - Before finalizing, ask "what's the obvious answer?" Often clusters that look different are the same thing with one field filled vs not filled. If you can't explain it simply, you don't understand it yet.

## Domain Knowledge

**Location:** the workspace DOMAIN.md (workspace-local user data, not shipped with the skill).

See `${CLAUDE_SKILL_DIR}/domain-example.md` for what a mature DOMAIN.md looks like.

This file contains the data catalog and accumulated facts about the data that prevent common mistakes. Read it before creating a project folder because:
- It may contain insights from previous analyses
- Reading it does NOT count as "exploration" - it's preparation

## Workflow

### Phase 0: Determine Mode

**Always do this first:**

1. **Read domain knowledge:** Read the workspace DOMAIN.md for the data catalog, variable meanings, and known data quality issues.
2. **Check if project exists:** Look for `projects/<project-name>/`

**If project EXISTS (Continue Mode):**
1. Read the project's notes file — CLAUDE.md (Claude Code) or AGENTS.md (Codex); detect whichever exists — to understand:
   - The story so far (what's been discovered)
   - Current hypotheses
   - What's been ruled out
2. Scan `scripts/` to see what analyses exist
3. Scan `output/` to review previous results
4. Resume from the current state - don't repeat completed work
5. Skip to Phase 3 (Iterative Analysis Loop)

**If project is NEW (Create Mode):**
1. Proceed to Phase 1 below

---

### Phase 1: Create Project Structure (FIRST - before any analysis)

**DO NOT RUN ANY EXPLORATORY QUERIES BEFORE THIS STEP.**

Create the project folder IMMEDIATELY:

```
projects/<project-name>/
├── <notes-file>           # CLAUDE.md or AGENTS.md — document hypotheses and findings (can embed figures)
├── scripts/
│   ├── 01_verify.r        # First script: confirm the anomaly/pattern exists
│   └── [analysis scripts] # Add as needed based on findings
├── output/                # Script text output (markdown)
└── figures/               # Saved plots (.png) and interactive widgets (.html) - created as needed
```

**Verify the folder exists before ANY analysis:**
```bash
ls projects/<project-name>/   # The project notes file must exist before running any R code
```

### Phase 2: Script Output (Text and Figures)

All project scripts should output to markdown files (not the R terminal) for easy comparison and review. Use the output utilities:

```r
# At top of script (after loading data)
source(paste0(getwd(), "/scripts/output_utils.r"))
start_output("projects/<project-name>/output/<script-name>.md")

# ... script content with cat(), print(), etc. ...

# At end of script
end_output()
```

This:
- Writes output to a `.md` file with code fence formatting
- Sets print width to 200 (prevents "squished" data frames)

### Generating Figures

Create figures when visualization helps reveal patterns that tables obscure (distributions, outliers, time series, comparisons across groups).

**Default to interactive `.html` figures** using `plotly` or `leaflet` rather than static `.png`. Interactive figures let the user explore the data (hover for details, zoom, filter). Only use static `.png` when interactivity adds no value (e.g., simple bar charts with few categories).

**When to create interactive figures (.html):**
- **Maps** - Geographic data (e.g., bus stops, incident locations) should be plotted on an interactive `leaflet` map with markers, popups, and tile layers so users can pan/zoom a real street map
- **Scatter plots** - Hover to identify individual points, zoom into clusters
- **Distributions** - Interactive histograms/density plots with hover details
- **Time series** - Zoom into date ranges, hover for exact values
- **Comparisons across many groups** - Filter/highlight specific groups

**When static `.png` is fine:**
- Simple bar charts with <10 categories
- Publication-ready figures where exact formatting matters
- Figures embedded in markdown reports where interactivity isn't needed

**When tables are sufficient:**
- Frequency counts with <10 categories
- Summary statistics (mean, median, percentiles)
- Exact values matter more than shape

**Figure workflow (interactive — preferred):**

```r
library(plotly)
library(leaflet)
source(paste0(getwd(), "/scripts/output_utils.r"))

my_data <- readr::read_csv("data/my_dataset.csv")

project_path <- "projects/<project-name>"
dir.create(file.path(project_path, "figures"), showWarnings = FALSE)

# 1. Interactive plotly figure (preferred for most plots)
p1 <- plot_ly(my_data, x = ~log(value), type = "histogram") %>%
  layout(title = "Value Distribution (Log Scale)")
htmlwidgets::saveWidget(p1, file.path(project_path, "figures/01_distribution.html"),
                        selfcontained = TRUE)

# 2. Interactive leaflet map (for geographic data like bus stops, incidents, locations)
map <- leaflet(bus_stops) %>%
  addTiles() %>%
  addCircleMarkers(~longitude, ~latitude,
    popup = ~paste0("<b>", stop_name, "</b><br>Route: ", route),
    radius = 5)
htmlwidgets::saveWidget(map, file.path(project_path, "figures/01_bus_stops_map.html"),
                        selfcontained = TRUE)

# 3. Capture text output
start_output(file.path(project_path, "output/01_verify.md"))
cat("Summary Statistics\n==================\n")
summary(my_data$value)
end_output()

# 4. Append figure reference to output file
cat("\n\n## Figures\n\nSee [Value Distribution](../figures/01_distribution.html)\n",
    "See [Bus Stops Map](../figures/01_bus_stops_map.html)\n",
    file = file.path(project_path, "output/01_verify.md"), append = TRUE)
```

**Static fallback (when interactivity adds no value):**

```r
p1 <- ggplot(my_data, aes(x = category)) + geom_bar()
ggsave(file.path(project_path, "figures/01_categories.png"), p1,
       width = 8, height = 5, dpi = 150)
```

**Naming convention:** Prefix figures with script number (e.g., `01_distribution.html`, `01_categories.png`). Re-running a script overwrites its figures.

**Viewing figures:** After running a script, inspect `.png` files directly to review plots. For `.html` files, note that they were saved successfully — the user will open them in a browser.

### Phase 3: Iterative Analysis Loop (all exploration happens here)

For each analysis:

1. **Run the analysis**
2. **Interpret immediately** - What does this mean? Does it tell a story?
3. **Decision point:**
   - If finding is meaningful -> Document it, explore deeper
   - If finding is noise -> Note it, move on
   - If finding reveals concentration -> THIS IS LIKELY THE STORY

4. **Update the plan** based on what you learned:
   - Remove planned analyses that are now irrelevant
   - Add new analyses suggested by findings
   - Refine hypotheses

### Phase 4: Synthesize the Story

Once a coherent narrative emerges:

1. **Write a clear summary** in the project's notes file
2. **State the conclusion plainly**: "These columns are populated for X, not Y"
3. **Explain what the NA values mean**: Missing data? Expected behavior? Data entry practice?

## Example: NA Column Patterns

**Initial plan:** Analyze temporal, geographic, entity, category patterns

**After iteration:**
- Entity analysis showed only 6 items -> THIS IS THE PRIMARY STORY
- Digging into those 6 items revealed: all related to a specific activity
- Geographic analysis showed concentration at 4 locations -> SUPPORTING CONTEXT (where the work happened)
- Temporal analysis showed no patterns -> RULED OUT (not relevant)
- **Conclusion:** Not missing data - these columns only populate for specific events

**Key distinction:**
- "Ruled out as cause" != "irrelevant to writeup"
- Geographic wasn't THE cause, but tells us WHERE it happened
- This adds value: "6 entities did the work, **primarily at location X**"

**Final writeup structure:**
1. The Story (primary finding)
2. Supporting Context (secondary findings that enrich the story)
3. What We Ruled Out (things that didn't matter)

## Writing Style: Data First, No Fluff

**CRITICAL: Write like a data analyst, not a storyteller. Let the data speak.**

**Good example:**
> "Location X has 7.14x the expected rate - this is a localized problem, not a system-wide issue."

**Bad examples:**
- "This is HIGHLY unusual" - Let the numbers show it's unusual
- "They fail visibly (good news for safety!)" - Unnecessary editorialization
- "Most likely candidates: ..." - Don't speculate beyond the data
- "Based on the evidence..." - Just state the finding

**Rules:**
1. **Lead with the finding, not setup** - Start with "X has Y" not "Based on our analysis of X..."
2. **Use numbers, not adjectives** - Say "7.14x the expected rate" not "extremely high"
3. **No safety cushions** - Don't add "(good news!)" or "(this is normal)" - state facts only
4. **Minimal speculation** - Only speculate when listing possible causes, and keep it brief
5. **No emphatic formatting** - Avoid "HIGHLY", "VERY", excessive bold/italics
6. **Skip obvious explanations** - Don't explain what a code means unless it's critical to the finding

**Compare:**
- Bad: "The 'F' discovery code is the smoking gun. Code F means these components are **visible during walk-around** and they're likely **external or easily accessible**. They **fail visibly** (good news for safety!)"
- Good: "89% discovered via 'F' code (visual inspection, not operationally discovered)"

## Anti-patterns to Avoid

1. **Ad-hoc terminal exploration** - NEVER run R queries outside of project scripts. "Quick checks" spiral into undocumented analysis. If you're tempted to run "just one query" before creating the project, STOP and create the project first.
2. **Report dumping** - Don't generate 5 scripts of numbers without interpretation
3. **Static planning** - Don't execute a fixed plan regardless of findings
4. **Ignoring concentration** - When a small group explains the majority of records, STOP and investigate that group
5. **Treating NA as "missing"** - NA often means "not applicable", not "data quality issue"
6. **Adding fluff** - No editorializing, speculation beyond data, or emphatic language
7. **Visualization without purpose** - Don't create figures just because you can. If a table tells the story, use a table. Figures should reveal patterns that numbers obscure.

## Output Checklist

Before considering the project complete:
- [ ] The story is clear and can be stated in 1-2 sentences
- [ ] We know WHY the pattern exists, not just THAT it exists
- [ ] NA values are explained (missing? expected? data entry practice?)
- [ ] The project notes file has three sections:
  - **The Story** - Primary finding (what explains the pattern)
  - **Supporting Context** - Secondary findings that enrich the story (where, when, who)
  - **What We Ruled Out** - Analyses that didn't contribute
- [ ] Scripts that produced useful context are kept; truly irrelevant ones noted
- [ ] Key figures referenced in the notes file where they strengthen the narrative
- [ ] Unreferenced figures in `figures/` can be deleted or kept for reference

## After Project Completion

Update domain knowledge: invoke the save-domain-knowledge-to-catalog capability to extract findings from the project's notes file and add them to the workspace DOMAIN.md for future projects. (Note: in some deployments DOMAIN.md is read-only at runtime — there, domain updates happen in the development environment and are baked into the next build.)

## Update Projects Index

Add the new project to the projects index notes file (`projects/CLAUDE.md` or `projects/AGENTS.md`):

```markdown
| [project-name](project-name/) | Brief description of the FINDING | Active |
```

Note: The description should state what was FOUND, not what was ANALYZED.

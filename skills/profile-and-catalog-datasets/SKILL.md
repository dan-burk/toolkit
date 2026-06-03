---
name: profile-and-catalog-datasets
description: Bootstrap a new data workspace: discover local and cloud (e.g. Azure blob) datasets, profile every dataset, and write a DOMAIN.md data catalog with quality flags and analysis recommendations. Use on the first analysis in a fresh workspace, or when DOMAIN.md is missing or empty.
---

# Onboarding - Workspace Bootstrap

**Do NOT ask the user any questions during onboarding. This process is fully autonomous.**

Execute the steps below **in order**. Do not skip steps. Do not proceed past a GATE until its condition is met.

DOMAIN.md is the workspace data catalog (workspace-local user data, not shipped with the skill).

---

## Step 1: Discover Data Sources

### 1a. Check Azure configuration

Read the workspace `.env`.

Look for these variables (ignore lines that are commented out or have placeholder values like `<your-key-here>`):
- `AZURE_STORAGE_ACCOUNT`
- `AZURE_STORAGE_CONTAINER`
- `AZURE_SAS_TOKEN` (optional — only needed for private containers)

Record whether Azure is configured: both ACCOUNT and CONTAINER must have real values.

### 1b. If Azure is configured, read the dataset catalog

Extract a summary from `data/metadata.json` (this file can be very large — do NOT read it in full into context). Run the following R snippet:

```bash
Rscript -e '
library(jsonlite)
meta <- fromJSON("data/metadata.json")
cat(sprintf("Total datasets: %d\n\n", nrow(meta)))

# Summary table sorted by row_count descending
meta <- meta[order(-meta$row_count), ]
cat(sprintf("%-50s %10s %5s %8s %s\n", "Title", "Rows", "Cols", "Size_MB", "First Tag"))
cat(paste(rep("-", 85), collapse = ""), "\n")
for (i in seq_len(nrow(meta))) {
  tag <- if (!is.null(meta$tags[[i]]) && length(meta$tags[[i]]) > 0) meta$tags[[i]][1] else ""
  cat(sprintf("%-50s %10s %5s %8.1f %s\n",
    substr(meta$title[i], 1, 50),
    format(meta$row_count[i], big.mark = ","),
    meta$column_count[i],
    meta$file_size_mb[i],
    tag))
}
'
```

Record:
- Total dataset count
- The blob URL pattern: `https://{account}.blob.core.windows.net/{container}/{title}.{ext}`
- Extension rule: `has_spatial_data = true` → `.geoparquet`, otherwise → `.parquet`
- For private containers, append `?{sas_token}` to the URL
- All formats use `arrow::read_parquet()` as the reader

### 1c. List local data files

List files in `data/` (pattern `data/*.*`).

Keep only files with supported extensions: `.csv`, `.tsv`, `.parquet`, `.geoparquet`, `.fst`, `.rds`, `.xlsx`

Skip these (not datasets): `data_dictionary.csv`, `metadata.json`, `README.md`, `.gitkeep`

### 1d. Read data dictionary (if it exists)

Look for `data/data_dictionary.csv`.

If found, read it. Expected columns: `column_name`, `definition` (and optional: `type`, `role`, `dataset`). These go into the Key Variable Meanings section of DOMAIN.md in Step 3.

### GATE 1

You must have **at least one** data source:
- Local data files from 1c, OR
- Azure datasets from 1b

**If NEITHER exists:** Tell the user "No data sources found. Place data files in `data/` or configure Azure credentials in `.env`." Then **STOP. Do not continue.**

---

## Step 2: Profile Local Datasets

Profile **every local dataset** found in Step 1c. If no local files exist (Azure-only), skip to Step 3.

Azure-only datasets get a catalog entry from metadata.json dimensions but **no column-level profile** — they are profiled on-demand later.

For each local dataset, run the following R profiling snippet. Replace `{reader}` and `{filepath}` with the correct values (see Reference: Readers at the bottom of this file):

```bash
Rscript -e '
df <- {reader}("{filepath}")

# Filter out unsupported column types (blob, raw, list)
supported <- sapply(df, function(x) !inherits(x, c("blob", "raw")) && !is.list(x))
df <- df[, supported, drop = FALSE]

cat(sprintf("Dimensions: %d rows x %d columns\n", nrow(df), ncol(df)))

# Column types and NA rates
na_rates <- colMeans(is.na(df)) * 100
cat("\nNA rates (columns with >0%% NA):\n")
if (any(na_rates > 0)) print(round(na_rates[na_rates > 0], 1)) else cat("  None\n")

# Numeric summaries
nums <- df[, sapply(df, is.numeric), drop = FALSE]
if (ncol(nums) > 0) { cat("\nNumeric summary:\n"); print(summary(nums)) }

# Categorical frequencies (columns with <= 20 unique values)
chars <- df[, sapply(df, is.character), drop = FALSE]
for (col in names(chars)) {
  n_unique <- length(unique(chars[[col]]))
  if (n_unique <= 20) {
    cat(sprintf("\n%s (%d unique):\n", col, n_unique))
    print(sort(table(chars[[col]]), decreasing = TRUE))
  }
}
'
```

From the output, note these for DOMAIN.md:
- High NA columns (>90%) — conditionally populated or truly missing?
- Skewed numerics — log-transform candidates
- Low/no variance columns (1 unique value) — uninformative
- High cardinality (>100 unique) — needs grouping for modeling
- Potential identifiers — every value unique
- Date/time columns — note range and gaps

### GATE 2

You have profiling output for every local dataset, OR all data is Azure-only (in which case you have the metadata.json summary from Step 1b). Proceed to Step 3.

---

## Step 3: Write DOMAIN.md

Create the workspace DOMAIN.md file.

Fill in the template below with findings from Steps 1–2. Remove sections that don't apply (e.g., Azure section if not configured). Replace all `{placeholders}` with real values.

```markdown
# Domain Knowledge

Accumulated facts about the dataset that prevent common analysis mistakes.

## Azure Blob Storage
<!-- REMOVE this section if Azure is not configured -->

{N} datasets available in Azure blob storage ({account}/{container}).

**Loading a dataset:**
\```r
df <- arrow::read_parquet("https://{account}.blob.core.windows.net/{container}/{title}.parquet")
# Spatial datasets use .geoparquet extension
# Private containers: append ?{sas_token} to URL
\```

See `data/metadata.json` for the full catalog (titles, column samples, row counts).

## Data Catalog

### {dataset_name}

- **Path:** `data/{filename}` or Azure blob URL
- **Format:** CSV / Parquet / GeoParquet / etc.
- **Reader:** `{reader}("data/{filename}")`
- **Dimensions:** {rows} rows x {cols} columns

| Column | Type | NA% | Notes |
|--------|------|-----|-------|
| col1   | numeric | 0.0 | Identifier (all unique) |
| col2   | character | 12.3 | 15 unique values |

<!-- For unprofiled Azure datasets: catalog entry with dimensions only, no column table.
     Add a note: "Column-level profile pending — run on-demand when needed." -->

## Key Variable Meanings

<!-- From data_dictionary.csv. If no dictionary exists, leave as "No data dictionary provided." -->
- **column_name**: definition

## Data Quality Issues

<!-- Group by type: high NA, skewed, low variance, etc. If none found, write "None identified during initial profiling." -->
- {issue description}

## Analysis Recommendations

<!-- Log-transform candidates, grouping suggestions, identifier columns to exclude, etc. -->

## Project-Specific Findings

<!-- Empty at bootstrap. Updated after each completed project via the save-domain-knowledge-to-catalog capability. -->

---

*This file is updated via the save-domain-knowledge-to-catalog capability after completing projects.*
```

### GATE 3

Read the workspace DOMAIN.md. Verify:
1. The file is not empty
2. The Data Catalog section has at least one dataset entry
3. Dimensions (rows x cols) are populated with real numbers

**If any check fails:** The write did not work. Debug and rewrite before proceeding.

---

## Step 4: Create `projects/onboarding/`

This marks bootstrap as complete.

### 4a. Create directories

Create the directories: `projects/onboarding/output` and `projects/onboarding/scripts`.

### 4b. Write the project notes file

Create `projects/onboarding/`'s notes file — CLAUDE.md (Claude Code) or AGENTS.md (Codex); detect whichever the workspace uses — with:

- **Data source**: local files, Azure, or both
- **Datasets found**: list each with dimensions
- **Key findings**: notable issues from profiling (not an exhaustive list — just what matters)
- **Pointer**: "See the workspace DOMAIN.md for the full data catalog."

### GATE 4

Confirm `projects/onboarding/`'s notes file exists.

**If the file does not exist:** Something went wrong. Create it before proceeding.

---

## Step 5: Display the Data Catalog

Present the data catalog to the user. Show:
- Total number of data sources (local + Azure)
- A summary table of all datasets (title, rows, cols, format)
- Where to find the full catalog: the workspace DOMAIN.md

This is the user's first view of what data is available. Make it clear and complete.

---

## Done

Bootstrap is complete. Return to the calling capability (data analysis), which will:
1. Read the freshly written DOMAIN.md
2. Proceed with the user's original analysis question

---

## Reference

### Readers by Format

| Extension | Reader | Package |
|-----------|--------|---------|
| `.csv` | `readr::read_csv()` | readr |
| `.tsv` | `readr::read_tsv()` | readr |
| `.parquet` | `arrow::read_parquet()` | arrow |
| `.geoparquet` | `arrow::read_parquet()` | arrow |
| `.fst` | `fst::read_fst()` | fst |
| `.rds` | `readRDS()` | base |
| `.xlsx` | `readxl::read_excel()` | readxl |

Full spec: `${CLAUDE_SKILL_DIR}/scripts/supported-files.json`

### Profiler Thresholds

| What | Threshold | Action |
|------|-----------|--------|
| High NA | >90% | Flag as conditionally populated |
| Skewness | >2 | Log-transform candidate |
| High cardinality | >100 unique | Needs grouping for modeling |
| Categorical display | <=20 unique | Show all values; otherwise show top 10 |

### On-Demand Profiling (Post-Bootstrap)

When a user later asks about an unprofiled Azure dataset:
1. Load it: `arrow::read_parquet("{blob_url}")`
2. Profile using the Step 2 approach
3. Append the column table to that dataset's entry in DOMAIN.md
4. The entry goes from "catalog-only" to "fully profiled"

### DOMAIN.md Example

See `${CLAUDE_SKILL_DIR}/domain-example.md` for what a mature DOMAIN.md looks like after several completed projects.

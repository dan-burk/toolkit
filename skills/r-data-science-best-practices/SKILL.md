---
name: r-data-science-best-practices
description: R data-science coding conventions and best practices — library loading, `package::function()` namespacing, reproducible seeds, train/test splits, portable file paths, code style, and commenting. Apply when writing or reviewing R scripts for data-analysis work.
user-invocable: false
---

# Data Science Best Practices

When performing data analysis or writing R code for data science tasks, adhere to these best practices:

## Library Loading
- Load ALL required libraries at the beginning of the script
- Group library calls together at the top
- Consider adding brief comments to indicate what each library is used for

## Function References
- For functions from tidyverse core packages (dplyr, ggplot2, tidyr, readr, purrr, tibble, stringr, forcats), use them directly
- For ALL other packages, use explicit double-colon notation: `package::function()`
  - Examples: `lubridate::ymd()`, `fst::write_fst()`, `janitor::clean_names()`
  - This makes dependencies clear and avoids namespace conflicts

## Random Seeds
- ALWAYS set a seed when using random operations or train/test splits
- Use meaningful seed values derived from today's date (e.g., 20251128 for 2025-11-28)
- NEVER use trivial seeds like 123 or 42
- Place `set.seed()` immediately before the random operation

## Train/Test Splits
- Use 80/20 train/test split as the default for model building
- Adjust only if sample size is too small (e.g., < 100 observations)
- Document any deviation from 80/20 with a comment explaining why
- Use appropriate splitting methods (e.g., `rsample::initial_split()` or similar)

## File Paths
- Use paths relative to the project root (e.g. `"data/input.csv"`), with the project root as the working directory (RStudio Project / `.Rproj`)
- For scripts run from subfolders (or Quarto/R Markdown, which knit from the file's folder), use `here::here("data", "input.csv")`
- Never use absolute paths, `setwd()`, or hardcoded machine-specific paths
- Example:
  ```r
  # Reading data
  df <- readr::read_csv("data/input.csv")

  # Writing data (from a script in a subfolder)
  readr::write_csv(df, here::here("output", "results.csv"))
  ```

## Code Style
- Use consistent indentation (2 spaces per level is R standard)
- Use meaningful variable names (snake_case preferred)
- Keep line length reasonable (< 80-100 characters when possible)
- Use spaces around operators: `x <- 5 + 3`, not `x<-5+3`
- Add blank lines to separate logical sections of code

## Comments
- Write clear, concise comments that explain WHY, not WHAT
- Comment complex operations, but don't over-comment obvious code
- Add section headers for major code blocks using `# Section Name ----`
- Include brief descriptions of custom functions
- Document assumptions and important decisions

## Example Template
```r
# Load libraries ----
library(dplyr)
library(ggplot2)
library(readr)

# Read data ----
raw_data <- read_csv("data/raw_data.csv")

# Data cleaning ----
clean_data <- raw_data |>
  janitor::clean_names() |>  # Clean column names
  filter(!is.na(target_variable))

# Train/test split ----
set.seed(20251128)  # Using today's date

split_data <- rsample::initial_split(clean_data, prop = 0.8)
train_data <- rsample::training(split_data)
test_data <- rsample::testing(split_data)

# Model building ----
# Build your model here

# Save results ----
write_csv(predictions, "output/predictions.csv")
```

## Additional Guidelines
- Check for and handle missing values appropriately
- Validate data types after import
- Use the native pipe (`|>`, R >= 4.1) for readable data transformations
- Prefer vectorized operations over loops when possible
- Test code on small subsets before running on full datasets

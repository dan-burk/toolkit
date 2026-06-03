# KC-135 Domain Knowledge

Accumulated facts about the KC-135 dataset that prevent common analysis mistakes.

## Dataset Scope (2022 Data)

- **415 aircraft** (428 total minus 13 incomplete)
- **149,446 hourly observations** after cleaning
- **25,983 maintenance issues** (Definition 1) or **8,728 issues** (Definition 2)
- **1,822 unique Work Unit Codes**
- **Date range**: Full year 2022 (aircraft should have 302 days of data)

## Geographic Hierarchy

**CRITICAL: Command → Base → Organization is NESTED, not independent.**

```
Command (8) → Base (33) → Organization (34)
```

**Structure**:
- Bases per command: 4Z (17), 0M (6), 1L (3), 1M (3), 0D (1), 0J (1), 0R (1), 1C (1)
- Base → Organization is 1:1 except CTGC (2 organizations)
- Commands are Major Commands (MAJCOM) with operational/administrative control

**Analysis implications**:
- **DON'T**: Use chi-square tests to compare base vs command (violates independence assumption)
- **DON'T**: Treat command and base as independent factors in ANOVA
- **DO**: Compare WITHIN-command variation vs BETWEEN-command variation (nested ANOVA)
- **DO**: Use "Russian Doll" drill-down: Start at Command level, then drill into Bases within each Command
- **DO**: If using mixed models, specify base nested within command: `(1|command/base)`

## Key Variable Meanings

### WUC (Work Unit Code)

**CRITICAL: `WUC = "NA"` means FULLY FUNCTIONING aircraft, NOT missing data.**

- WUC is a hierarchical code: **first 2 chars = system level** (~37 groups)
- Full WUC can be up to 6 characters (system → subsystem → component)
- Only specific WUC codes get `wuc_desc` populated (component-level work)
- **1,822 unique WUCs** in 2022 data (too many for modeling without grouping)

**WUC System Codes with confirmed descriptions (from data):**
- **27**: Engine (ENGINE ASSEMBLY, COWL ASSY FAN, ENGINE MOUNT SYSTEM)
- **61**: HF Communications (HF COMM SET AN/ARC, ANTENNA, HF MAST LONG WIRE)
- **62**: VHF/UHF Radio (AN/ARC-210(V) VHF/UHF RADIO)
- **72**: Unknown - only one description exists: "CONTROL DISPLAY UNIT DCU-900B" (729B0)
  - 729Q*: Problematic subsystem (729QB, 729QC, 729QF) - **system function unconfirmed**
- **23**: Autopilot (no description in data - assumed from standard conventions)
- **42**: Electrical (no description in data - assumed from standard conventions)
- **91**: Powerplant/Engine (no description in data - assumed from standard conventions)

**Note**: Only 47 of 1,822 WUC codes have descriptions populated. Do not assume system meanings without verification.

**Analysis implications**:
- **DON'T**: Filter out WUC = "NA" records thinking they're bad data—they represent FMC status
- **DO**: Use `wuc_system` (first 2 chars) for system-level analysis (~37 groups), not the full 1,822 codes
- **DO**: Expect WUC = "NA" to correlate perfectly with Status = "FMC"

### Status (Mission Capability)

**Three levels**: FMC (Fully Mission Capable) → PMC (Partially Mission Capable) → NMC (Non-Mission Capable)

**Status variants**:
- `status` or `condition_overall`: High-level status (FMC/PMC/NMC)
- `condition_detail`: Granular breakdown (NMC-M, NMC-S, NMC-MU, PMC-S, etc.)
- `condition_summary`: Snapshot status with additional context

**Key subcodes**:
- **NMC-M**: Non-Mission Capable due to Maintenance
- **NMC-S**: Non-Mission Capable due to Supply (waiting for parts)
- **NMC-MU**: Non-Mission Capable, Maintenance, Unscheduled
- **PMC-S**: Partially Mission Capable due to Supply

**Analysis implications**:
- **DO**: Use `condition_detail` for root cause analysis (maintenance vs supply)
- **DO**: Separate scheduled from unscheduled NMC events (different durations)
- **NOTE**: Supply delays (NMC-S) have different repair time distributions than maintenance issues (NMC-M)

### JCN (Job Control Number)

**Unique identifier** for each maintenance action.

**CRITICAL: JCN existence is logically linked to other fields.**

**Logical rules**:
1. If `Status = PMC or NMC`, then `JCN` must exist (not NA)
2. If `WUC` exists, then `JCN` must exist
3. If `JCN` exists, then `WUC` must exist
4. If `WUC` exists, then `when_discovered` must exist

**Analysis implications**:
- **DO**: Use these rules to validate data integrity
- **DO**: Expect ~8 records in 2022 data to violate JCN rules (were forward-filled)
- **NOTE**: JCN is the true "unique maintenance event" identifier—use it for counting distinct issues

### When Discovered Codes

**21 original codes** indicating when/where a discrepancy was found.

**Flight phase codes** (most common):
- **A, B**: Before flight (A = mission aborted by aircrew, B = no abort)
- **C, D**: In-flight (C = mission aborted, D = no abort)
- **E**: After flight / between flights (discovered by aircrew)
- **H**: Between flights (discovered by ground crew)

**Inspection codes**:
- **J**: Daily inspection
- **K**: Turnaround inspection
- **M**: Major or phase inspection
- **L**: Special inspection
- **F**: Pilot/NFO inspection (not flight-related)
- **G**: Acceptance or transfer inspection

**Grouped for modeling**: 21 codes → **5 categories**:
- Before-flight (A, B)
- In-flight (C, D)
- After/Between-flights (E, H)
- Inspection (J, K, L, M)
- Other (F, G, etc.)

**Analysis implications**:
- **DO**: Use `when_discovered_group` (5 levels) instead of raw codes (21 levels)
- **DO**: Expect in-flight aborts (C) to correlate with higher severity/longer repairs
- **NOTE**: "Before flight" discoveries prevent mission failures—track separately from in-flight

## Scheduled vs. Unscheduled Maintenance

**CRITICAL: `condition_scheduled` is the strongest predictor of repair duration.**

**Values**:
- **Scheduled**: Planned inspections, phase maintenance, preventive work
- **Unscheduled**: Unexpected failures, discovered during operations
- Multiple unscheduled variants (collapsed to "Unscheduled" in modeling)

**Distribution** (approximate):
- Unscheduled: ~60-70% of maintenance events
- Scheduled: ~30-40% of events

**Analysis implications**:
- **DO**: Always stratify analysis by scheduled vs. unscheduled (different repair time distributions)
- **DO**: Expect unscheduled repairs to be 2-3x longer on average
- **DO**: Use `condition_scheduled_general` (collapsed categories) for modeling
- **NOTE**: Scheduled maintenance still has variability—don't assume constant duration

## Repair Time Distributions

**CRITICAL: Repair times are HEAVILY right-skewed. You MUST log-transform.**

**Raw repair times** (`cum_status_hours` or `total_cum_hrs`):
- **Range**: 0.1 to 7,248 hours
- **Median**: ~17 hours
- **Mean**: ~40-50 hours (much higher due to outliers)
- **Distribution**: Extremely right-skewed (most repairs are quick, few are very long)

**Analysis implications**:
- **DON'T**: Use raw repair times in linear models (violates normality assumption)
- **DON'T**: Use mean repair time (heavily influenced by outliers—median is ~17 hrs but mean is ~45 hrs)
- **DO**: Use `log(cum_status_hours)` as response variable
- **DO**: Use Median Absolute Error (MAE) instead of RMSE for model evaluation
- **NOTE**: Extended repairs (>100 hrs) are <5% of events but dominate mean calculations

**Class imbalance**:
- Quick repairs (<24 hrs): ~60-70%
- Standard repairs (24-100 hrs): ~25-30%
- Extended repairs (>100 hrs): ~5-10%

**For classification tasks**:
- **DO**: Use SMOTE or other balancing techniques for extended repair prediction
- **DO**: Focus on binary classification (Extended vs Not-Extended) rather than 3-class
- **NOTE**: Even with balancing, extended repair prediction is difficult (AUC ~0.70-0.75 at best)

## Issue Definition (Definition 1 vs Definition 2)

**CRITICAL: There are TWO definitions of "unique maintenance issue".**

### Definition 1: Disjoint WUC
- **Logic**: Any change in WUC = new issue
- **Identifier**: `status_change_id`
- **Result**: **25,983 issues** in 2022
- **Use case**: Conservative—treats each WUC change as separate issue

### Definition 2: 72-hour Lookback
- **Logic**: Same WUC within 72 hours = same issue
- **Identifier**: `wuc_session_full`
- **Result**: **8,728 issues** in 2022
- **Use case**: Realistic—consolidates repeat failures of same system

**Analysis implications**:
- **DO**: Use Definition 2 (`wuc_session_full`) for most analyses (more realistic)
- **DO**: Use Definition 1 if you want to count every distinct WUC entry
- **NOTE**: Definition 2 reduces issue count by ~66% compared to Definition 1
- **NOTE**: Both definitions filter out WUC = "NA" (fully functioning aircraft)

**Files**:
- Definition 1: `data/issue_level_data_def1.fst` (25,983 rows)
- Definition 2: `data/issue_level_data_def2.fst` (8,728 rows)

## Data Quality Issues

### 13 Incomplete Aircraft

**CRITICAL: 13 aircraft are excluded from all analysis due to incomplete data.**

- **Issue**: These aircraft have < 302 days of data in 2022
- **List**: Stored in `data/latest_incomplete_df.csv`
- **Impact**: 428 total aircraft → 415 aircraft in cleaned data

**Analysis implications**:
- **DO**: Verify your dataset has 415 aircraft (not 428)
- **DO**: Check `data/latest_incomplete_df.csv` if you find references to excluded aircraft
- **NOTE**: Incomplete aircraft are filtered out in `src/pipeline/filter_incomplete_aircraft.r`

### JCN Forward-Filling

**8 records** had missing JCN values that violated logical rules. These were forward-filled from subsequent records.

**Analysis implications**:
- **NOTE**: This is a data quality fix applied in `src/pipeline/forward_fill_JCN.r`
- **NOTE**: Affects <0.01% of records—negligible impact on analysis

### Timestamp Artifacts

The 13 incomplete aircraft have timestamp irregularities (gaps, duplicates, out-of-order entries). These are the same 13 excluded above.

**Analysis implications**:
- **NOTE**: See `src/pipeline/Debug/debug1.r` for investigation of specific cases
- **DO**: Validate timestamp ordering if doing time-series analysis

## Categorical Variable Cardinality

**CRITICAL: Many categorical variables have too many levels for direct modeling.**

| Variable | Raw Levels | Grouped Levels | Grouping Variable |
|----------|-----------|---------------|------------------|
| `work_unit_code` | 1,822 | ~37 | `wuc_system` (first 2 chars) |
| `when_discovered` | 21 | 5 | `when_disc_group` |
| `possessing_organization` | 34 | 9 | `poss_org_group` (chars 5-9) |
| `condition_scheduled` | Multiple variants | 2 | `condition_scheduled_general` |

**Analysis implications**:
- **DO**: Use pre-grouped variables (`*_group` or `*_general` suffix) for modeling instead of raw high-cardinality variables
- **NOTE**: Grouping variables are created in `src/pipeline/data_pipeline.r`

## Key Predictors of Repair Duration

**Ranked by importance** (from Random Forest models, R² ~0.45-0.50):

1. **`condition_scheduled_general`** - Scheduled vs. unscheduled (strongest predictor)
2. **`condition_summary_group`** - PMC vs NMC variants
3. **`aircraft_repair_count`** - Historical frequency of repairs (chronic issues)
4. **`when_discovered_group`** - Flight phase when issue was found
5. **`possessing_command_group`** - Which MAJCOM is responsible (operational tempo)
6. **`ppc_type_flag_group`** - Possession purpose (training vs operational)

**Analysis implications**:
- **DO**: Start with these 6 predictors for any repair time model
- **NOTE**: Even with these predictors, R² ~0.50 on log-scale (challenging prediction problem)

## Aircraft Serial Numbers

**Format**: `YY-NNNN`
- **YY** = Fiscal year of procurement (e.g., "85" = 1985)
- **NNNN** = Sequence number (e.g., "0123" = 123rd aircraft ordered that year)

**Example**: `85-0123` = 123rd aircraft ordered in Fiscal Year 1985

**Analysis implications**:
- **DO**: Use `aircraft_serial_number` as unique aircraft identifier
- **DO**: Use `key` (aircraft_serial_number + begin_date) as unique record identifier
- **NOTE**: Serial numbers are painted on aircraft tails (called "tail numbers")

## Mission Design Series (MDS)

**Dataset focus**: KC-135 Stratotanker (aerial refueling aircraft)

**KC-135 variants in data**:
- **KC-135R**: Most common (upgraded CFM56 engines)
- **KC-135T**: Modified R-model with additional fuel capacity

**Other aircraft** (minority of data):
- **C-130 Hercules**: Tactical airlift (C-130H, C-130J, MC-130J, etc.)
- **KC-46 Pegasus**: Modern refueling (based on Boeing 767)

**Analysis implications**:
- **NOTE**: Most analysis focuses on KC-135 only
- **NOTE**: If comparing across MDS, control for aircraft age and mission type

## Quick Reference: Files

| What you need | File path |
|---------------|-----------|
| Hourly-level data | `data/timestamp_level_data.fst` (149,446 rows) |
| Issue-level (Def 1) | `data/issue_level_data_def1.fst` (25,983 rows) |
| Issue-level (Def 2) | `data/issue_level_data_def2.fst` (8,728 rows) |
| Model-ready data | `data/model_issue_level_data_def1.fst` |
| Incomplete aircraft | `data/latest_incomplete_df.csv` (13 aircraft) |
| Variable definitions | `data/Data Definitions.csv` |
| Data quality notes | `notebooks/daniel/data_integrity.md` |
| Load all data | `source("scripts/load_data.r")` |

---

## Project-Specific Findings

### na-column-patterns (2026-01-06)
**Finding:** The mostly-NA columns populate for component-level work. `wuc_desc` = working on a component. `corrective_action` = someone wrote a note. The "two clusters" are the same work.

Key facts discovered:
- **wuc_desc** populates when working on specific components (antennas, boom assembly, etc.)
- **corrective_action** only populates if someone writes what they did — it's optional documentation
- **The clusters are the same work**: Both dominated by HF antenna work. Cluster 1 (800 records) has notes; Cluster 2 (5,833 records) doesn't.
- **Hierarchical relationship**: corrective_action → wuc_desc → discrepancy_* (can't have outer without inner)
- Only 8.2% of records with WUC codes have wuc_desc populated

**Seasonal maintenance cycles**:
- Cold-weather work (entry door, nose gear, bulkhead) concentrates in Q4
- Warm-weather work (thermal curtains, food warmers) only appears Q1-Q3
- Year-round work (antennas) shows no seasonal pattern

**Data quirks**:
- **Midnight hour artifact**: 89% of wuc_desc records show hour 0 — this is data entry timing, not work timing
- **Base non-NA % misleads**: FBNX ranks #1 (56.6%) but has zero corrective_action (all APU work on 1 aircraft)

---

## Anomaly Detection Methodology

### What Actually Gets Flagged? (Two-Stage Filtering)

The anomaly report uses a two-stage filter. A record must pass **both** stages to appear in the report.

**Stage 1: Identify "slow" base/WUC combinations**

For each WUC with sufficient data (≥10 records, ≥3 bases):
1. Calculate median repair hours per base
2. Compute baseline = median of those medians (fleet norm)
3. Compute threshold = 90th percentile of those medians
4. Flag any base where `median > threshold` as "slow"

A record at an "efficient" base is **never** flagged, even if it's a statistical outlier. The system only drills into slow bases.

**Stage 2: Find outlier records within slow groups**

For each slow base/WUC combination, flag individual records that meet **either** criterion:

| Method | Criterion | Rationale |
|--------|-----------|-----------|
| IQR | `value > Q3 + 1.5×IQR` | Statistical outlier within the group |
| Baseline | `value > 1.5× baseline` | Significantly above fleet norm |

The final outlier set is the **union** of both methods.

**Example:**
- WUC "24DF0" has baseline of 18.9 hours across the fleet
- Base "PCZP" has median of 89.5 hours for this WUC (slow, above 90th percentile)
- Within PCZP's 24DF0 records, a 1637-hour repair is flagged because:
  - It exceeds the IQR upper fence for that group, **and**
  - It exceeds 1.5× the 18.9-hour baseline (28.4 hours)

This two-stage approach focuses investigation on bases that are systematically slow, then surfaces their most extreme individual cases.

---

*This file is updated via `/save-domain-knowledge-to-skill` after completing projects.*

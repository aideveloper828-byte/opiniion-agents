---
name: pipeline-intelligence
description: >-
  Analyze HubSpot pipeline for velocity, conversion, deal aging, and coverage.
  Use when the user asks for pipeline analysis, GTM funnel metrics, deal aging,
  pipeline velocity, win rate, forecast categories, quota attainment, or says
  "pull the pipeline" or "run the pipeline report." Outputs a formatted Excel
  workbook with Opiniion branding.
---

# Pipeline Intelligence

Pulls deal data from HubSpot and computes pipeline velocity, stage conversion rates, deal aging, and coverage ratios. Supports Jessica's RevOps mandate and Phase 1 priorities: "Re-create KPIs & pipeline velocity metrics" and "Map full GTM funnel."

## When to Use

- "Pull the pipeline" / "Run the pipeline report"
- "What's our pipeline velocity?"
- "Show me conversion rates by stage"
- "Which deals are stale?"
- "What's our pipeline coverage?"
- "Build a weekly pipeline report"
- Any request about GTM funnel, forecast categories, or quota coverage

## Architecture

```
HubSpot (Deals API + stage history)
    ↓
connectors/hubspot_connect.py (auth + pagination)
    ↓
pull_pipeline.py (pandas: stage funnel, velocity, aging)
    ↓
openpyxl (formatted Excel with Opiniion branding)
    ↓
~/Desktop/ or configured output path
```

## Before Running: Clarify Scope

1. **Pipeline**: Which pipeline? (default: primary/default pipeline)
2. **Period**: Current open pipeline, or closed deals for a specific period?
3. **Quota**: What's the quota number for coverage calculation? (manual input until comp plan is built)

## Metrics Computed

### Pipeline Velocity
```
Velocity = (# Deals in Pipeline × Win Rate × Avg Deal Size) / Avg Sales Cycle (days)
```
Measures revenue throughput — how much ARR flows through the pipeline per day.

### Stage Conversion Rates
For each pipeline stage pair (e.g., Discovery → Proposal):
```
Conversion Rate = Deals that moved to Stage N+1 / Deals that entered Stage N
```

### Deal Aging
For each open deal:
```
Days in Current Stage = today - date_entered_current_stage
Stale Flag = Days in Current Stage > 2× median for that stage
```

### Pipeline Coverage
```
Coverage Ratio = Total Weighted Pipeline / Quota
```
Where weighted pipeline = SUM(deal_amount × stage_probability).

### Forecast Categories
- **Commit**: Deals in final stages with >80% probability
- **Best Case**: Deals with 50-80% probability
- **Pipeline**: Deals with <50% probability
- **Closed Won**: Already closed in period

### Win Rate (by period)
```
Win Rate = Closed Won / (Closed Won + Closed Lost)
```

### Rep Performance
Per sales rep: deals in pipeline, weighted value, win rate, avg cycle time.

## Output Workbook

`Opiniion_Pipeline_Report_[YYYY-MM-DD].xlsx` with these tabs:

### Tab 1: Pipeline Summary
- Key metrics: total pipeline, weighted pipeline, velocity, coverage ratio
- Forecast categories (commit / best case / pipeline / closed won)
- Period-over-period comparison

### Tab 2: Stage Funnel
- Stage-by-stage deal counts and values
- Conversion rates between stages
- Median days in each stage

### Tab 3: Deal Aging
- All open deals sorted by days in current stage (descending)
- Stale deal flags (red highlight)
- Owner, amount, stage, days in stage, next step

### Tab 4: Rep Performance
- Per-rep: deal count, pipeline value, win rate, avg days to close
- Sorted by weighted pipeline value

### Tab 5: Deal Detail
- Full deal-level export with all key properties
- Sorted by close date (soonest first)

## Formatting

Follows Opiniion standards from chief-of-staff:
- `A1`: "opiniion" in teal, bold 22pt
- Stale deals: red fill
- Totals: teal fill, white font
- Conditional formatting: green for above-target, red for below

## Running

```bash
cd skills/pipeline-intelligence/scripts
python3 pull_pipeline.py                                    # Current pipeline
python3 pull_pipeline.py --closed-period 2026-Q1            # Closed deal analysis
python3 pull_pipeline.py --quota 500000                     # With quota for coverage
python3 pull_pipeline.py --output ~/Desktop/weekly_pipeline.xlsx
```

## Dependencies

- `connectors/hubspot_connect.py` — for data pulls
- `opiniion-chief-of-staff` — formatting standards
- `saas-metrics-engine/metrics-definitions.md` — Win Rate, Avg Days to Close, Avg Deal Size definitions

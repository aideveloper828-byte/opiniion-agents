---
name: operating-rhythm
description: >-
  Manage the monthly operating cycle — close checklist, BvA variance,
  Finance Flash exec summary, and mid-month re-forecast. Use when Jessica
  asks about the close, variance analysis, BvA, Finance Flash, board prep,
  or says "run the close" or "where are we on the month." Combines close
  management, variance monitoring, and executive briefing into one agent.
---

# Monthly Operating Rhythm — Opiniion

Orchestrates the full monthly finance cycle: close → variance → reporting → re-forecast. This is the "operating system" for Jessica's monthly rhythm as a one-person finance function.

## When to Use

- "Run the close checklist" / "Where are we on the close?"
- "Generate the BvA" / "Pull variance report"
- "Build the Finance Flash" / "Prep the exec summary"
- "Mid-month forecast check" / "Pipeline snapshot for re-forecast"
- "Board prep" / "Quarterly reporting"
- Beginning of each month (close window)
- Mid-month (re-forecast window)

## Monthly Cycle

```
Day 1-5: CLOSE WINDOW
    ├── Pull close checklist → track RAG status
    ├── Pull NetSuite trial balance (soft close)
    ├── Flag open items & unreconciled accounts
    └── Status email/message to COO

Day 5-10: POST-CLOSE
    ├── BvA variance report (actuals vs. budget/forecast)
    ├── Auto-flag material variances (>10% or >$5K)
    ├── Run SaaS Metrics Engine for closed month
    ├── Generate Finance Flash (1-page exec summary)
    └── Distribute to CEO/COO

Day 15-20: MID-MONTH RE-FORECAST
    ├── Pipeline snapshot (call Pipeline Intelligence)
    ├── Updated full-year forecast based on actuals + pipeline
    ├── Board reporting prep (if quarter-end)
    └── Prep materials for any strategic meetings
```

## Architecture

```
NetSuite (SuiteQL: trial balance, actuals)
HubSpot (deals: pipeline snapshot)
    ↓
connectors/ (netsuite_connect, hubspot_connect)
    ↓
run_close_cycle.py
    ├── Calls saas-metrics-engine (SaaS metrics)
    ├── Calls pipeline-intelligence (pipeline snapshot)
    ├── Calls financial-statement-builder (actuals pull)
    └── Generates close-specific deliverables
    ↓
Excel outputs + Finance Flash summary
```

## Close Checklist

See [close-checklist.md](close-checklist.md) for the configurable checklist template. Each item has:
- Task description
- Owner (Jessica or delegated)
- Status: Not Started / In Progress / Complete / Blocked
- RAG: Red (behind) / Amber (at risk) / Green (on track)
- Due date (relative to month-end)
- Notes

## Output Deliverables

### 1. Close Status Tracker (Excel)
`Opiniion_Close_Status_[YYYY-MM].xlsx`
- Tab 1: Checklist with RAG status
- Tab 2: Open items and blockers
- Tab 3: Timeline (Gantt-style visual of close progress)

### 2. BvA Variance Report (Excel)
`Opiniion_BvA_[YYYY-MM].xlsx`
- Tab 1: P&L with Actuals, Budget, Variance ($), Variance (%)
- Tab 2: Material variances detail (>10% or >$5K)
- Tab 3: Department-level detail
- Auto-commentary: flags for "over budget" or "under budget" with magnitude

### 3. Finance Flash (1-page Excel or PDF)
`Opiniion_Finance_Flash_[YYYY-MM].xlsx`
- Header: Month, Opiniion branding
- Section 1: Key Financial Metrics (Revenue, GM%, OpEx, EBITDA, Cash)
- Section 2: SaaS Metrics (ARR, NRR, GRR, Magic Number)
- Section 3: Pipeline Summary (total pipeline, weighted, coverage)
- Section 4: Key Callouts (2-3 bullet points: what changed, why, what to do)
- Designed to be consumed in <2 minutes by CEO/COO

### 4. Re-Forecast Update (Excel)
`Opiniion_Reforecast_[YYYY-MM].xlsx`
- Updated full-year P&L with actual months locked + remaining forecast
- Pipeline-informed revenue forecast
- Variance from original budget

## Formatting

Follows Opiniion standards from chief-of-staff:
- RAG colors: Red `FF6B6B`, Amber `FFD93D`, Green `6BCB77`
- Variance flags: Red fill for unfavorable >10%, Green fill for favorable >10%
- Finance Flash: clean, minimal, exec-ready

## Running

```bash
cd skills/operating-rhythm/scripts

# Close window (day 1-5)
python3 run_close_cycle.py --phase close --month 2026-04

# Post-close (day 5-10)
python3 run_close_cycle.py --phase post-close --month 2026-04

# Mid-month re-forecast (day 15-20)
python3 run_close_cycle.py --phase reforecast --month 2026-04

# Full cycle (all phases)
python3 run_close_cycle.py --phase all --month 2026-04
```

## Configuration

### Variance Thresholds
- **Material variance**: >10% AND >$5,000 (both conditions must be met)
- **Significant variance**: >5% AND >$2,500
- Thresholds are configurable in the script

### Budget Source
Until Pigment/Rillet is implemented:
- Budget data is manually input via the Assumptions tab in the Financial Statement Builder
- Or loaded from a separate budget Excel file: `~/Desktop/Opiniion_Budget_2026.xlsx`

## Dependencies

- `connectors/netsuite_connect.py` — trial balance, GL actuals
- `connectors/hubspot_connect.py` — pipeline snapshot (via pipeline-intelligence)
- `saas-metrics-engine` — SaaS metrics for closed month
- `pipeline-intelligence` — pipeline data for re-forecast
- `financial-statement-builder` — P&L actuals for BvA
- `close-checklist.md` — checklist configuration
- `opiniion-chief-of-staff` — formatting standards, stakeholder context

## Future Enhancements (Post-90 Days)

- **AR Aging & Collections**: Add AR aging pull from NetSuite, generate graduated collection email drafts
- **Vendor & Contract Tracker**: Add contract renewal calendar, spend analysis
- **Automated distribution**: Email/Slack delivery of Finance Flash and BvA once communication tools are confirmed
- **Board package automation**: Quarterly slide generation from monthly data

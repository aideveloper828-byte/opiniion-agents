---
name: saas-metrics-engine
description: >-
  Compute SaaS metrics from NetSuite billing data — ARR waterfall, NRR, GRR,
  Magic Number, LTV/CAC, Win Rate, Days to Close, Avg Deal Size, ARPU.
  Use when the user asks for SaaS metrics, ARR analysis, retention metrics,
  unit economics, or says "run the metrics" or "update the dashboard."
  Outputs a formatted Excel workbook with Opiniion branding.
---

# SaaS Metrics Engine

Computes all standard SaaS metrics from NetSuite billing/revenue data and outputs a formatted Excel workbook. This is the "single source of truth" for how Opiniion measures SaaS performance.

## When to Use

- "Run the SaaS metrics" / "Update the metrics dashboard"
- "What's our ARR?" / "What's our NRR?"
- "Pull retention metrics for [period]"
- "Compute LTV/CAC"
- Any request for SaaS KPIs or unit economics

## Architecture

```
NetSuite (SuiteQL: invoices, transactions, customers)
    ↓
connectors/netsuite_connect.py (auth + query)
    ↓
compute_metrics.py (pandas: clean, aggregate, compute)
    ↓
openpyxl (formatted Excel with Opiniion branding)
    ↓
~/Desktop/ or configured output path
```

## Before Running: Clarify Scope

1. **Period**: TTM (default), specific quarter, specific month, or custom range?
2. **Segment**: All customers, specific industry, specific cohort?
3. **Compare**: Period-over-period comparison? (default: yes, vs. prior period)

## Metrics Computed

All definitions are canonical and documented in [metrics-definitions.md](metrics-definitions.md). Do NOT deviate from these definitions without explicit approval.

### Revenue Metrics
- **Ending ARR**: Current annualized recurring revenue
- **Beginning ARR**: ARR at start of period
- **ARR Waterfall**: Beginning → New → Expansion → Contraction → Churn → Ending
- **MRR**: Monthly recurring revenue (ARR / 12)

### Retention Metrics
- **Gross Retention Rate (GRR)**: Revenue retained excluding expansion
- **Net Retention Rate (NRR)**: Revenue retained including expansion

### Efficiency Metrics
- **Magic Number**: Net new ARR / prior-period S&M spend
- **LTV/CAC**: Customer lifetime value / customer acquisition cost
- **CAC Payback**: Months to recover acquisition cost

### Sales Velocity Metrics
- **Win Rate**: Closed Won / (Closed Won + Closed Lost)
- **Avg Days to Close**: Mean days from opportunity creation to close
- **Avg Deal Size**: Total new ARR / number of new deals

### Unit Economics
- **ARPU**: Average revenue per customer (ARR / active customers)

## Output Workbook

The Excel output (`Opiniion_SaaS_Metrics_[YYYY-MM].xlsx`) has these tabs:

### Tab 1: Summary Dashboard
- All key metrics in a single view
- Period-over-period comparison (current vs. prior)
- Color-coded: green = improved, red = declined
- Mini sparkline area for 6-month trend (if data available)

### Tab 2: ARR Waterfall
- Monthly ARR bridge: Beginning + New + Expansion - Contraction - Churn = Ending
- Both dollar amounts and as % of Beginning ARR
- 12-month rolling view

### Tab 3: Cohort Analysis
- Retention curves by sign-up quarter
- $ retention and logo retention
- Heatmap formatting (darker = better retention)

### Tab 4: Definitions
- Every metric with its exact formula
- Data source for each component
- Links back to metrics-definitions.md

## Formatting

Follows Opiniion standards from chief-of-staff:
- `A1`: "opiniion" in teal (`4FCBC5`), bold 22pt
- Totals: teal fill, white font
- Section headers: gray fill `F3F3F3`
- Currency: `"$"#,##0`
- Percentages: `0.0%`
- Gridlines hidden, panes frozen

## SuiteQL Queries

The script uses these core queries against NetSuite. Adjust table/column names based on Opiniion's NetSuite configuration (use System Discovery output to confirm).

### Revenue by Customer by Month
```sql
SELECT
    t.entity AS customer_id,
    c.companyname AS customer_name,
    TO_CHAR(t.trandate, 'YYYY-MM-01') AS month,
    SUM(tl.amount) AS revenue
FROM transaction t
JOIN transactionline tl ON t.id = tl.transaction
JOIN customer c ON t.entity = c.id
WHERE t.type = 'CustInvc'
  AND tl.mainline = 'F'
  AND t.trandate >= '2024-01-01'
GROUP BY t.entity, c.companyname, TO_CHAR(t.trandate, 'YYYY-MM-01')
ORDER BY month, customer_name
```

### Customer First Invoice Date
```sql
SELECT
    entity AS customer_id,
    MIN(trandate) AS first_invoice_date
FROM transaction
WHERE type = 'CustInvc'
GROUP BY entity
```

These queries will need adjustment once you discover Opiniion's actual NetSuite schema via the System Discovery agent. The column names above use standard NetSuite record types.

## Running the Script

```bash
cd skills/saas-metrics-engine/scripts
python3 compute_metrics.py                          # TTM, all customers
python3 compute_metrics.py --period 2026-Q1         # Specific quarter
python3 compute_metrics.py --period 2025-01:2025-12 # Custom range
python3 compute_metrics.py --output ~/Desktop/my_metrics.xlsx
```

## Iteration Pattern

After generating the workbook:
1. Verify totals against NetSuite reports (cross-check)
2. Offer: "Want me to add a sensitivity analysis?" / "Break down by segment?"
3. If metrics don't tie, check query filters and account mappings

## Dependencies

- `connectors/netsuite_connect.py` — for data pulls
- `metrics-definitions.md` — canonical metric formulas
- `opiniion-chief-of-staff` — formatting standards, output path

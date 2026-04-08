# SaaS Metrics Definitions — Opiniion

Canonical definitions for all SaaS metrics used at Opiniion. This document is the "single source of truth" — Finance, Sales, and Customer Success should all use these definitions.

## Revenue Metrics

### Ending ARR (Annual Recurring Revenue)
**Formula:** Sum of all active subscription revenue, annualized, as of the last day of the period.

**Calculation:**
```
Ending ARR = SUM(monthly_recurring_revenue * 12) for all active customers at period end
```

**Includes:** Recurring subscription fees only.
**Excludes:** One-time fees, implementation fees, professional services, overages.

### Beginning ARR
**Formula:** Ending ARR of the prior period.
```
Beginning ARR(t) = Ending ARR(t-1)
```

### New ARR
**Formula:** ARR from customers who were not active in the prior period.
```
New ARR = SUM(ARR) for customers where first_invoice_date is within the current period
```

### Expansion ARR
**Formula:** Incremental ARR from existing customers who increased their spend.
```
Expansion ARR = SUM(ARR_current - ARR_prior) for customers where ARR_current > ARR_prior AND ARR_prior > 0
```

### Contraction ARR (Downsell)
**Formula:** Decrease in ARR from existing customers who reduced their spend but did not fully churn.
```
Contraction ARR = SUM(ARR_prior - ARR_current) for customers where ARR_current < ARR_prior AND ARR_current > 0
```
Reported as a positive number in the waterfall (subtracted from Beginning ARR).

### Churned ARR
**Formula:** ARR lost from customers who fully canceled or did not renew.
```
Churned ARR = SUM(ARR_prior) for customers where ARR_current = 0 AND ARR_prior > 0
```
Reported as a positive number in the waterfall (subtracted from Beginning ARR).

### ARR Waterfall Identity
```
Ending ARR = Beginning ARR + New ARR + Expansion ARR - Contraction ARR - Churned ARR
```
This must always balance. If it doesn't, there's a classification error.

### MRR (Monthly Recurring Revenue)
```
MRR = Ending ARR / 12
```

---

## Retention Metrics

### Gross Retention Rate (GRR)
**Formula:** Measures revenue retained from existing customers, excluding any expansion.
```
GRR = (Beginning ARR - Contraction ARR - Churned ARR) / Beginning ARR
```
GRR is always <= 100%. A GRR above 100% indicates a calculation error.

**Opiniion 2025 benchmark:** 74%

### Net Retention Rate (NRR)
**Formula:** Measures revenue retained from existing customers, including expansion.
```
NRR = (Beginning ARR + Expansion ARR - Contraction ARR - Churned ARR) / Beginning ARR
```
NRR can exceed 100% when expansion outpaces churn + contraction.

**Opiniion 2025 benchmark:** 207%

---

## Efficiency Metrics

### Magic Number
**Formula:** Measures sales efficiency — how much net new ARR is generated per dollar of S&M spend.
```
Magic Number = (Ending ARR - Beginning ARR) / S&M Spend for the period
```
**Interpretation:**
- < 0.5x = Inefficient, review GTM strategy
- 0.5x - 0.75x = Acceptable
- 0.75x - 1.0x = Efficient
- > 1.0x = Highly efficient, consider increasing investment

**Opiniion 2025 benchmark:** 4.4x

### LTV (Customer Lifetime Value)
**Formula:**
```
LTV = ((New ARR + Expansion ARR) * Gross Margin %) / Gross Churn Rate
```
Where Gross Churn Rate = (Contraction ARR + Churned ARR) / Beginning ARR.

### CAC (Customer Acquisition Cost)
**Formula:**
```
CAC = (S&M Spend + Implementation Spend) for the period / New Customers Acquired
```

### LTV / CAC Ratio
```
LTV / CAC = LTV / CAC
```
**Interpretation:**
- < 1x = Losing money on customer acquisition
- 1x - 3x = Needs improvement
- 3x - 5x = Healthy
- > 5x = Very healthy, may be under-investing in growth

**Opiniion 2025 benchmark:** 10.2x

### CAC Payback Period
**Formula:**
```
CAC Payback (months) = CAC / (ARPU_monthly * Gross Margin %)
```
Where ARPU_monthly = ARPU / 12.

---

## Sales Velocity Metrics

### Win Rate
**Formula:**
```
Win Rate = Closed Won Opportunities / (Closed Won + Closed Lost Opportunities)
```
Excludes open/active opportunities. Only counts opportunities that reached a terminal state.

**Opiniion 2025 benchmark:** 71%

### Average Days to Close
**Formula:**
```
Avg Days to Close = SUM(closed_date - created_date) / COUNT(Closed Won Opportunities)
```
Only counts Closed Won opportunities. Excludes Closed Lost.

**Opiniion 2025 benchmark:** 50 days

### Average Deal Size
**Formula:**
```
Avg Deal Size = Total New ARR from Closed Won / COUNT(Closed Won Opportunities)
```

**Opiniion 2025 benchmark:** $2.3K

---

## Unit Economics

### ARPU (Average Revenue Per Unit/Customer)
**Formula:**
```
ARPU = Ending ARR / Count of Active Customers
```
Where active customers = customers with ARR > 0 at period end.

Can be segmented by:
- **Industry** (if tagged in CRM)
- **Customer size tier** (by ARR band)
- **Cohort** (by sign-up year/quarter)

---

## Data Sources

| Metric Component | Primary Source | Backup Source |
|---|---|---|
| Revenue / ARR | NetSuite (invoices, transactions) | Databricks (if available) |
| Customer list | NetSuite (customer records) | HubSpot (companies) |
| S&M Spend | NetSuite (GL: S&M department expenses) | Manual input |
| Implementation Spend | NetSuite (GL: implementation accounts) | Manual input |
| Win/Loss data | HubSpot (deal stage = Closed Won / Closed Lost) | — |
| Days to Close | HubSpot (deal createdate vs. closedate) | — |
| Gross Margin % | Financial statements (Revenue - COGS) / Revenue | Manual input |

---

## Notes

- All dollar metrics are in USD unless otherwise stated.
- TTM = Trailing Twelve Months. Default period for retention and efficiency metrics.
- When comparing periods, use the same length (e.g., TTM vs. prior TTM, not TTM vs. quarterly).
- Round units/customer counts to whole numbers. Never round revenue, rates, or percentages.
- Compound monthly growth: `(1 + annual_rate)^(1/12)`, not `annual_rate / 12`.

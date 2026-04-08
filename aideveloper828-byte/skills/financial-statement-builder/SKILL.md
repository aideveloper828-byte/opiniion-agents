---
name: financial-statement-builder
description: >-
  Build P&L, Balance Sheet, and Cash Flow Statement workbooks from NetSuite GL
  data. Use when the user asks to build, rebuild, regenerate, or update the
  financial statements, P&L, profit and loss, balance sheet, cash flow, or says
  "build the statements." Covers Income Statement, Balance Sheet, and Cash Flow
  Statement with actuals, forecast overlay, and full formatting.
---

# Financial Statement Builder — Opiniion

Generates formatted Excel workbooks with P&L (Income Statement), Balance Sheet, and Cash Flow Statement from NetSuite GL actuals. Adapted from Entrata's build-income-statement skill, redesigned for Opiniion's NetSuite-first architecture.

## When to Use

- "Build the financial statements" / "Build the P&L"
- "Rebuild the IS" / "Update the statements"
- "Pull actuals for [month]"
- "Generate the board financial package"
- Any request for income statement, balance sheet, or cash flow statement

## Architecture

```
NetSuite (SuiteQL: GL actuals by account/period)
    ↓
connectors/netsuite_connect.py (auth + query)
    ↓
build_statements.py
    ├── Account mapping config (account-mapping.md)
    ├── P&L tab (Revenue → COGS → Gross Margin → OpEx → EBITDA → Net Income)
    ├── Balance Sheet tab (Assets → Liabilities → Equity)
    └── Cash Flow tab (Operating → Investing → Financing)
    ↓
openpyxl (formatted Excel with Opiniion branding)
    ↓
~/Desktop/ or configured output path
```

## Key Design: Parameterized Account Mapping

Unlike the Entrata version (which hardcoded Adaptive account prefixes), Opiniion's builder uses a **configurable account mapping** defined in [account-mapping.md](account-mapping.md). This mapping file translates NetSuite GL accounts to financial statement line items.

The account mapping is populated using System Discovery output — run `discover_netsuite.py` first to get the chart of accounts, then configure the mapping.

## Before Running: Confirm Configuration

1. **Account mapping populated?** Check `account-mapping.md` has been filled in with Opiniion's actual account codes (from System Discovery).
2. **Period**: Which months? Default = YTD through latest closed month.
3. **Forecast**: Include forecast columns? (manual input until Pigment/Rillet decision)
4. **Comparison**: Year-over-year? Budget vs. Actuals?

## Output Workbook

`Opiniion_Financial_Statements_[YYYY-MM].xlsx` with these tabs:

### Tab 1: Income Statement (P&L)
- Revenue (by product/category if available)
- Cost of Revenue
- Gross Margin ($ and %)
- Operating Expenses by department (S&M, R&D, G&A)
- Total OpEx
- EBIT
- Other Income/Expense
- EBT (Earnings Before Tax)
- Taxes
- Net Income
- EBITDA Reconciliation (Net Income + D&A + SBC + Interest + Taxes)

Monthly columns + YTD Total. Actuals vs. Forecast visually distinguished.

### Tab 2: Balance Sheet
- Assets: Current → Fixed → Long-Term
- Liabilities: Current → Long-Term
- Equity
- Balance Check (Assets - L&E = 0)

### Tab 3: Cash Flow Statement
- Operating: Net Income + adjustments + working capital changes
- Investing: CapEx, acquisitions
- Financing: Debt, equity
- Net change in cash

### Tab 4: Assumptions
- Forecast assumptions (growth rates, expense ratios)
- Editable inputs with green fill, blue font

## Formatting

Follows Opiniion standards from chief-of-staff:
- `A1`: "opiniion" in teal, bold 22pt
- Actuals headers: white on dark gray
- Forecast headers: white on purple with "(F)" suffix
- Section headers: gray fill
- Subtotals: light teal fill
- Net Income / EBITDA: double bottom border
- YTD column: `=SUM()` formula across all months
- Currency: `"$"#,##0`; Percentages: `0.0%`

## SuiteQL Queries

### GL Actuals by Account and Period
```sql
SELECT
    a.acctnumber AS account_number,
    a.acctname AS account_name,
    a.accttype AS account_type,
    tal.postingperiod AS period_id,
    ap.periodname AS period_name,
    ap.startdate AS period_start,
    SUM(tal.amount) AS amount
FROM transactionaccountingline tal
JOIN transaction t ON tal.transaction = t.id
JOIN account a ON tal.account = a.id
JOIN accountingperiod ap ON tal.postingperiod = ap.id
WHERE ap.startdate >= '2025-01-01'
  AND ap.startdate < '2027-01-01'
  AND ap.isadjust = 'F'
  AND ap.isquarter = 'F'
  AND ap.isyear = 'F'
GROUP BY a.acctnumber, a.acctname, a.accttype, tal.postingperiod, ap.periodname, ap.startdate
ORDER BY ap.startdate, a.acctnumber
```

These queries use standard NetSuite record types. Column names may need adjustment based on Opiniion's configuration — verify with System Discovery output.

## Running

```bash
cd skills/financial-statement-builder/scripts
python3 build_statements.py                                # YTD actuals
python3 build_statements.py --start 2025-01 --end 2026-12 # Custom range
python3 build_statements.py --include-forecast             # With forecast overlay
python3 build_statements.py --output ~/Desktop/Opiniion_FS.xlsx
```

## Iteration Pattern

1. Run System Discovery to get chart of accounts
2. Populate account-mapping.md with Opiniion's GL structure
3. Run build_statements.py — verify totals against NetSuite reports
4. Iterate on mapping: adjust account classifications
5. Add forecast columns once budgets are established

## Dependencies

- `connectors/netsuite_connect.py` — GL data pulls
- `account-mapping.md` — account-to-line-item configuration
- `system-discovery` — provides chart of accounts for mapping
- `opiniion-chief-of-staff` — formatting standards

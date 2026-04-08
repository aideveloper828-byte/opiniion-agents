# Account Mapping — Opiniion

Maps NetSuite GL accounts to financial statement line items. This file is the configuration layer between the raw chart of accounts and the formatted financial statements.

**To populate:** Run `discover_netsuite.py` first, then fill in the account ranges below using Opiniion's actual chart of accounts.

## Income Statement Mapping

### Revenue
| Line Item | Account Range / Pattern | Notes |
|---|---|---|
| Subscription Revenue | TBD (e.g., 4000-4099) | Recurring SaaS revenue |
| Professional Services | TBD (e.g., 4100-4199) | Implementation, consulting |
| Other Revenue | TBD (e.g., 4200-4299) | Any non-subscription revenue |

### Cost of Revenue
| Line Item | Account Range / Pattern | Notes |
|---|---|---|
| Hosting & Infrastructure | TBD (e.g., 5000-5049) | AWS/cloud costs |
| Support Personnel | TBD (e.g., 5050-5099) | CS/support team salaries |
| Other COGS | TBD (e.g., 5100-5199) | |

### Operating Expenses
| Department | Account Range / Pattern | Notes |
|---|---|---|
| Sales & Marketing | TBD (e.g., 6000-6299) | All S&M accounts |
| Research & Development | TBD (e.g., 6300-6599) | All R&D accounts |
| General & Administrative | TBD (e.g., 6600-6999) | All G&A accounts |

### Below the Line
| Line Item | Account Range / Pattern | Notes |
|---|---|---|
| Interest Income | TBD (e.g., 7000-7049) | |
| Interest Expense | TBD (e.g., 7050-7099) | |
| Other Income/Expense | TBD (e.g., 7100-7199) | |
| Income Tax Expense | TBD (e.g., 8000-8099) | |

### EBITDA Adjustments
| Line Item | Account Pattern | Notes |
|---|---|---|
| Depreciation | TBD | Look for "depreciation" in account name |
| Amortization | TBD | Look for "amortization" in account name |
| Stock-Based Compensation | TBD | Look for "SBC" or "stock comp" |

## Balance Sheet Mapping

### Assets
| Line Item | Account Range / Pattern | Notes |
|---|---|---|
| Cash & Equivalents | TBD (e.g., 1000-1099) | |
| Accounts Receivable | TBD (e.g., 1100-1199) | |
| Prepaid Expenses | TBD (e.g., 1200-1299) | |
| Property & Equipment | TBD (e.g., 1500-1599) | |
| Accumulated Depreciation | TBD (e.g., 1600-1699) | Contra-asset |
| Intangible Assets | TBD (e.g., 1700-1799) | |
| Other Long-Term Assets | TBD (e.g., 1800-1899) | |

### Liabilities
| Line Item | Account Range / Pattern | Notes |
|---|---|---|
| Accounts Payable | TBD (e.g., 2000-2099) | |
| Accrued Liabilities | TBD (e.g., 2100-2199) | |
| Deferred Revenue | TBD (e.g., 2200-2299) | Critical for SaaS |
| Current Debt | TBD (e.g., 2300-2399) | |
| Long-Term Debt | TBD (e.g., 2500-2599) | |
| Other Liabilities | TBD (e.g., 2600-2699) | |

### Equity
| Line Item | Account Range / Pattern | Notes |
|---|---|---|
| Common Stock | TBD (e.g., 3000-3049) | |
| APIC | TBD (e.g., 3050-3099) | |
| Retained Earnings | TBD (e.g., 3100-3149) | |
| Treasury Stock | TBD (e.g., 3200-3249) | |

## Mapping Rules

1. **Exact match first, then pattern.** If an account has a specific line item assignment, use it. Otherwise, fall back to the account range.
2. **Revenue sign convention.** Revenue accounts typically have credit (negative) balances in NetSuite. The script flips the sign for display.
3. **Expense sign convention.** Expense accounts have debit (positive) balances. Displayed as positive in OpEx, negative impact on income.
4. **Unmapped accounts.** Any GL account not in this mapping is flagged in a separate "Unmapped" tab for review.
5. **Update this file** whenever Opiniion adds new GL accounts or restructures the chart of accounts.

## How to Populate

1. Run: `python3 discover_netsuite.py`
2. Open the resulting `Opiniion_NetSuite_Discovery_[date].xlsx`
3. Go to the "Chart of Accounts" tab
4. For each account, determine which financial statement line item it maps to
5. Fill in the "Account Range / Pattern" column in the tables above
6. Re-run `build_statements.py` to verify the mapping produces correct totals

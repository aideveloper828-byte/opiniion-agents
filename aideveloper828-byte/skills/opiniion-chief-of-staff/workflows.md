# Common Workflows

Patterns Jessica uses repeatedly at Opiniion. Reference these to maintain consistency across sessions.

## 1. Data Pull → Excel Pipeline

**Trigger:** "Pull [metric] from NetSuite" or any data request.

```
Clarify scope (date range, segment, metric definition)
    ↓
Run query via netsuite_connect.py or hubspot_connect.py
    ↓
Post-process in pandas (dedup, aggregate, validate)
    ↓
Output to Excel (openpyxl) with Opiniion formatting
    ↓
Offer: "Want this as a formatted workbook or just the numbers?"
```

**Key rules:**
- `pd.to_numeric(errors='coerce').fillna(0)` before any summing
- Date format: always `YYYY-MM-01` for monthly data
- Validate row counts and totals against source before outputting

## 2. Model Build → Audit → Iterate

**Trigger:** "Build a model for [initiative/scenario]"

```
Intake conversation (collect assumptions)
    ↓
Confirm assumptions in table format
    ↓
Generate build script → /tmp/build_[slug].py
    ↓
Run script → output to ~/Desktop/
    ↓
Audit pass (formula check, formatting, scenario consistency)
    ↓
Present results + offer iteration options
```

**Audit checklist:**
- [ ] All calculated cells are formulas (not hardcoded)
- [ ] Formulas reference Assumptions/Key Inputs tab
- [ ] Cross-sheet references use correct tab names
- [ ] Units are rounded to whole numbers
- [ ] Growth uses compound formula
- [ ] Scenarios are consistent (same structure, different parameters)
- [ ] Gridlines hidden, panes frozen
- [ ] Opiniion branding in A1 of every tab

## 3. Cross-System Reconciliation

**Trigger:** Comparing data across NetSuite and HubSpot.

```
Pull from each source for same period
    ↓
Normalize field names and date formats
    ↓
Join on stable keys (customer_id, account codes)
    ↓
Flag discrepancies > materiality threshold
    ↓
Document: which source is authoritative for which metric
```

**Source hierarchy (general):**
- GL actuals → NetSuite (primary)
- Pipeline / CRM data → HubSpot (primary)
- Warehouse / analytics → Databricks (primary)
- Forecasts / budget → Pigment or manual (TBD based on tool selection)

## 4. Git Workflow

**Trigger:** Saving skills, plans, or project artifacts to the repo.

```
Stage changes: git add [specific files]
    ↓
Review what's staged (never auto-commit everything)
    ↓
Commit with descriptive message
    ↓
Push to aideveloper828-byte
```

**Never push:** `.env`, credentials, raw financial data, `.xlsx` output files.

**Safe to push:** Skills (`skills/`), connectors (`connectors/`), markdown, non-sensitive scripts.

## 5. Executive Deliverable

**Trigger:** Board prep, Finance Flash, CEO/COO presentation material.

```
Build the underlying analysis (metrics, variance, pipeline)
    ↓
Format into 1-page Finance Flash or formatted Excel
    ↓
Key metrics with period-over-period comparison
    ↓
Narrative bullets: what changed, why it matters, what to do
    ↓
Offer: "Want me to add a sensitivity table or scenario comparison?"
```

## 6. Monthly Operating Cycle

**Trigger:** Month-end close, BvA, re-forecast.

```
Close window (day 1-5): Run close checklist, pull trial balance
    ↓
Post-close (day 5-10): BvA variance, SaaS metrics, Finance Flash
    ↓
Mid-month (day 15-20): Pipeline snapshot, re-forecast, board prep
    ↓
Document: close status, variance commentary, forecast changes
```

See `operating-rhythm` skill for detailed automation.

## 7. Blocked → Pivot Pattern

When a data source or permission is unavailable:

```
Document what's blocked and why
    ↓
Identify next-best source or workaround
    ↓
Proceed with available data
    ↓
Flag assumptions/gaps in output
    ↓
Circle back when access is restored
```

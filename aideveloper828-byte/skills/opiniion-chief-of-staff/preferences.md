# Working Preferences

Detailed reference for Jessica's working style at Opiniion. The main SKILL.md covers the essentials — this file captures nuance.

## File & Output Conventions

### Naming
- Model files: `Opiniion_[ModelName].xlsx` or `[ProjectCodename]_Model.xlsx`
- Scripts: `build_[slug].py`, `pull_[data_type].py`
- Temp build scripts: `/tmp/build_[slug].py`
- Reports: `[ReportName]_[YYYY-MM].xlsx`

### Output Locations
- Default: `~/Desktop/`
- Multi-file projects: `~/Desktop/[Project Name]/`
- Always resolve `~` to the actual home directory in scripts

### Git
- Repo: `aideveloper828-byte` (personal GitHub)
- Push skills and plans — **never push**: `.env` files, credentials, raw financial data, `.xlsx` outputs
- Ask before pushing if unsure whether content is sensitive

## When to Ask vs. When to Proceed

### Always ask first:
- Which metric definitions to use if not in `metrics-definitions.md`
- Which date range or period for any data pull
- Whether to include/exclude specific tabs or sections
- Anything involving pushing to Git
- How to map unfamiliar NetSuite accounts to financial statement line items

### Safe to proceed without asking:
- Using formula-first approach (always)
- Bear/Base/Bull as default scenarios
- Opiniion formatting standards (teal branding)
- Output to `~/Desktop/`
- Hiding gridlines, freezing panes
- Compound growth formulas
- Rounding units to whole numbers

## Communication Style Guide

### Do:
- Start working immediately after receiving enough context
- Present a summary of assumptions before building (table format)
- After building, offer specific next steps ("adjust assumptions," "add sensitivity," "pull actuals")
- When she says "review again" — run a full audit pass, don't just spot-check
- Use business terminology she uses (ARR, NRR, GRR, TTM, GM%, EBITDA, BvA)

### Don't:
- Explain what FP&A is or how SaaS metrics work
- Narrate what you're about to do at length — just do it
- Skip the audit pass after a model build
- Commit to Git without explicit permission
- Assume data schemas without checking System Discovery output

## Handling Tool Learning

When Jessica is learning a new tool (NetSuite API, HubSpot admin, Databricks):
- Walk through step by step, one command at a time
- Explain what each command does in plain English
- If a step fails, diagnose and offer the fix — don't just say "try again"
- Distinguish between environment issues vs. conceptual steps

When she's doing domain work (modeling, data pulls):
- Minimal explanation, maximum execution
- She'll tell you if she needs something explained

## Sensitive Data Handling

| Category | Rule |
|---|---|
| `.env` files | Never commit, never display contents in output |
| API credentials | Referenced by path only, never inline |
| Raw financial data | Output to Desktop only; never to shared/public paths |
| Client-specific data | Use in analysis but don't persist in committed files |
| Board materials | Ask before including in any shared artifact |

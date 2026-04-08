---
name: system-discovery
description: >-
  Catalog NetSuite chart of accounts, GL structure, and HubSpot pipeline schemas
  programmatically. Use when Jessica asks to "map the tech stack," "discover the
  data," "what's in NetSuite/HubSpot," "build a data dictionary," or during
  onboarding to accelerate system learning. Outputs a Data Dictionary Excel workbook.
---

# System Discovery

Programmatically catalogs the data schemas in Opiniion's core systems (NetSuite and HubSpot) so every subsequent agent knows the correct account codes, pipeline stages, and field names.

## When to Use

- "Map the tech stack" / "What's in NetSuite?"
- "Build a data dictionary"
- "Discover the chart of accounts"
- "What pipeline stages does HubSpot have?"
- During onboarding (Phase 1) to accelerate system learning
- When any other agent hits unknown account codes or field names

## Architecture

```
NetSuite (SuiteQL metadata queries)     HubSpot (Properties API)
    ↓                                       ↓
discover_netsuite.py                    discover_hubspot.py
    ↓                                       ↓
    └──────────── pandas + openpyxl ────────┘
                        ↓
         Opiniion_Data_Dictionary.xlsx
```

## Output Workbook

`Opiniion_Data_Dictionary.xlsx` with these tabs:

### NetSuite Tabs
- **Chart of Accounts**: Account number, name, type (Asset/Liability/Revenue/Expense/etc.), subtype, is_inactive, parent account
- **Departments**: Department hierarchy, internal IDs
- **Classes**: Classification structure
- **Subsidiaries**: Entity structure
- **Custom Records**: Custom record types and their fields
- **Saved Searches**: List of existing saved searches with descriptions

### HubSpot Tabs
- **Deal Pipelines**: Pipeline names, stages, probabilities, display order
- **Deal Properties**: All deal properties with types, groups, options
- **Contact Properties**: All contact properties
- **Company Properties**: All company properties
- **Owners**: Sales reps with IDs and emails
- **Custom Objects**: Any custom object types

### Data Quality Tab
- Fields with >50% null values (potential data quality issues)
- Fields that are populated vs. empty
- Record counts by object type

## Running

```bash
cd skills/system-discovery/scripts

# Full discovery (both systems)
python3 discover_netsuite.py && python3 discover_hubspot.py

# Individual systems
python3 discover_netsuite.py --output ~/Desktop/NS_Discovery.xlsx
python3 discover_hubspot.py --output ~/Desktop/HS_Discovery.xlsx
```

## How Other Skills Use This

- **SaaS Metrics Engine**: Confirms which NetSuite transaction types and account codes map to recurring revenue
- **Financial Statement Builder**: Uses the chart of accounts to build account-to-line-item mapping
- **Pipeline Intelligence**: Uses pipeline stage names and probabilities for velocity calculations
- **Operating Rhythm**: Uses the department list for BvA variance reporting

## Dependencies

- `connectors/netsuite_connect.py`
- `connectors/hubspot_connect.py`

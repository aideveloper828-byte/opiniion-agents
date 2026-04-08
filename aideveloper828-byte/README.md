# Opiniion Agent Ecosystem

Cursor agent skills for the Director of Finance & RevOps at Opiniion. Built to accelerate ramp-up and automate recurring finance and RevOps workflows.

## Setup

1. Clone this repo on your Opiniion machine
2. Copy `.env.example` to `.env` and populate with Opiniion credentials
3. Register the `skills/` directory in Cursor (Settings > Skills > Add Skill Folder)
4. Install Python dependencies: `pip install -r requirements.txt`

## Skills

| Skill | Purpose | Phase |
|---|---|---|
| `opiniion-chief-of-staff` | Foundation layer — persona, preferences, routing | Day 1 |
| `saas-metrics-engine` | ARR/NRR/GRR/LTV-CAC computation from NetSuite | Day 1 |
| `system-discovery` | Catalogs NetSuite chart of accounts + HubSpot pipeline schemas | Week 1-2 |
| `pipeline-intelligence` | HubSpot pipeline velocity, conversion, deal aging | Week 1-2 |
| `financial-statement-builder` | P&L, BS, CF from NetSuite GL actuals | Weeks 3-6 |
| `operating-rhythm` | Monthly close, BvA variance, Finance Flash, exec briefing | Weeks 5-8 |

## Connectors

Shared API connectors used by all skills:

- `connectors/netsuite_connect.py` — NetSuite REST API + SuiteQL
- `connectors/hubspot_connect.py` — HubSpot CRM API

## Tech Stack

- **GL / Financials**: NetSuite (SuiteQL)
- **CRM / Pipeline**: HubSpot
- **Data Warehouse**: Databricks
- **BI**: Lookr
- **Evaluating**: Rillet (accounting automation), Pigment (FP&A planning)

## Credential Management

All credentials live in `.env` (never committed). See `.env.example` for required variables.

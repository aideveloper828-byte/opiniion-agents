"""
HubSpot CRM API connector for Opiniion agent ecosystem.

Uses a Private App access token for authentication.
All credentials loaded from .env at the repo root.

Usage:
    from connectors.hubspot_connect import HubSpotClient
    client = HubSpotClient()
    deals = client.get_all_deals(properties=["dealname", "amount", "dealstage", "closedate"])
"""

import os
import sys
import time
from typing import Optional

import pandas as pd
import requests
from dotenv import load_dotenv

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_ROOT, ".env"))

HUBSPOT_ACCESS_TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN", "")
BASE_URL = "https://api.hubapi.com"


class HubSpotClient:
    """HubSpot CRM API client with pagination and rate-limit handling."""

    def __init__(self, access_token: str = HUBSPOT_ACCESS_TOKEN):
        self.access_token = access_token
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        json_body: dict = None,
        params: dict = None,
        max_retries: int = 3,
    ) -> requests.Response:
        """Execute an authenticated request with retry and rate-limit handling."""
        url = f"{BASE_URL}{endpoint}"

        for attempt in range(max_retries):
            try:
                resp = self._session.request(
                    method, url, json=json_body, params=params, timeout=60
                )
                if resp.status_code == 429:
                    wait = int(resp.headers.get("Retry-After", 10))
                    print(f"[HubSpot] Rate limited, waiting {wait}s (attempt {attempt + 1})")
                    time.sleep(wait)
                    continue
                resp.raise_for_status()
                return resp
            except requests.exceptions.RequestException as exc:
                if attempt == max_retries - 1:
                    raise
                print(f"[HubSpot] Request failed ({exc}), retrying in 2s...")
                time.sleep(2)

    # ── CRM Object Reads ───────────────────────────────────────────

    def _get_all_objects(
        self,
        object_type: str,
        properties: list[str] = None,
        limit: int = 100,
        filter_groups: list = None,
    ) -> list[dict]:
        """Paginate through all records of a CRM object type."""
        all_results = []
        after = None
        endpoint = f"/crm/v3/objects/{object_type}/search" if filter_groups else f"/crm/v3/objects/{object_type}"

        while True:
            if filter_groups:
                body = {"filterGroups": filter_groups, "limit": limit, "properties": properties or []}
                if after:
                    body["after"] = after
                resp = self._request("POST", endpoint, json_body=body)
            else:
                params = {"limit": limit}
                if properties:
                    params["properties"] = ",".join(properties)
                if after:
                    params["after"] = after
                resp = self._request("GET", endpoint, params=params)

            data = resp.json()
            results = data.get("results", [])
            all_results.extend(results)

            paging = data.get("paging", {})
            next_page = paging.get("next", {})
            after = next_page.get("after")
            if not after:
                break

        return all_results

    def get_all_deals(
        self,
        properties: list[str] = None,
        filter_groups: list = None,
    ) -> pd.DataFrame:
        """Fetch all deals with specified properties. Returns a DataFrame."""
        default_props = [
            "dealname", "amount", "dealstage", "pipeline",
            "closedate", "createdate", "hs_lastmodifieddate",
            "hubspot_owner_id", "hs_deal_stage_probability",
        ]
        props = properties or default_props
        records = self._get_all_objects("deals", properties=props, filter_groups=filter_groups)
        return self._records_to_df(records)

    def get_all_contacts(self, properties: list[str] = None) -> pd.DataFrame:
        """Fetch all contacts with specified properties."""
        default_props = [
            "firstname", "lastname", "email", "company",
            "lifecyclestage", "createdate", "hs_lastmodifieddate",
        ]
        props = properties or default_props
        records = self._get_all_objects("contacts", properties=props)
        return self._records_to_df(records)

    def get_all_companies(self, properties: list[str] = None) -> pd.DataFrame:
        """Fetch all companies with specified properties."""
        default_props = [
            "name", "domain", "industry", "numberofemployees",
            "annualrevenue", "createdate", "hs_lastmodifieddate",
        ]
        props = properties or default_props
        records = self._get_all_objects("companies", properties=props)
        return self._records_to_df(records)

    # ── Pipelines ──────────────────────────────────────────────────

    def get_pipelines(self, object_type: str = "deals") -> list[dict]:
        """Fetch all pipelines and their stages for a given object type."""
        resp = self._request("GET", f"/crm/v3/pipelines/{object_type}")
        return resp.json().get("results", [])

    def get_pipeline_stages(self, pipeline_id: str, object_type: str = "deals") -> pd.DataFrame:
        """Fetch stages for a specific pipeline as a DataFrame."""
        pipelines = self.get_pipelines(object_type)
        for p in pipelines:
            if p["id"] == pipeline_id:
                stages = p.get("stages", [])
                return pd.DataFrame([
                    {
                        "stage_id": s["id"],
                        "label": s["label"],
                        "display_order": s.get("displayOrder", 0),
                        "probability": s.get("metadata", {}).get("probability", ""),
                    }
                    for s in stages
                ])
        return pd.DataFrame()

    # ── Properties (Schema Discovery) ──────────────────────────────

    def get_properties(self, object_type: str) -> pd.DataFrame:
        """Fetch all properties for a CRM object type (schema discovery)."""
        resp = self._request("GET", f"/crm/v3/properties/{object_type}")
        props = resp.json().get("results", [])
        return pd.DataFrame([
            {
                "name": p["name"],
                "label": p["label"],
                "type": p["type"],
                "field_type": p.get("fieldType", ""),
                "group_name": p.get("groupName", ""),
                "description": p.get("description", ""),
                "has_unique_value": p.get("hasUniqueValue", False),
                "hidden": p.get("hidden", False),
                "options": [o["label"] for o in p.get("options", [])],
            }
            for p in props
        ])

    # ── Deal Stage History ─────────────────────────────────────────

    def get_deal_stage_history(self, deal_id: str) -> list[dict]:
        """Fetch the stage change history for a specific deal."""
        resp = self._request(
            "GET",
            f"/crm/v3/objects/deals/{deal_id}",
            params={"propertiesWithHistory": "dealstage"},
        )
        data = resp.json()
        history = data.get("propertiesWithHistory", {}).get("dealstage", [])
        return history

    # ── Owners ─────────────────────────────────────────────────────

    def get_owners(self) -> pd.DataFrame:
        """Fetch all HubSpot owners (sales reps)."""
        resp = self._request("GET", "/crm/v3/owners")
        owners = resp.json().get("results", [])
        return pd.DataFrame([
            {
                "owner_id": o["id"],
                "email": o.get("email", ""),
                "first_name": o.get("firstName", ""),
                "last_name": o.get("lastName", ""),
            }
            for o in owners
        ])

    # ── Helpers ────────────────────────────────────────────────────

    @staticmethod
    def _records_to_df(records: list[dict]) -> pd.DataFrame:
        """Flatten HubSpot CRM records into a DataFrame."""
        rows = []
        for r in records:
            row = {"id": r["id"]}
            row.update(r.get("properties", {}))
            rows.append(row)
        return pd.DataFrame(rows) if rows else pd.DataFrame()

    def test_connection(self) -> bool:
        """Verify credentials by fetching account info."""
        try:
            resp = self._request("GET", "/crm/v3/objects/deals", params={"limit": 1})
            count = resp.json().get("total", 0)
            print(f"[HubSpot] Connection OK — {count} total deals in CRM")
            return True
        except Exception as exc:
            print(f"[HubSpot] Connection FAILED: {exc}")
            return False


if __name__ == "__main__":
    client = HubSpotClient()
    if client.test_connection():
        print("Ready to use.")
    else:
        print("Check your .env HUBSPOT_ACCESS_TOKEN.", file=sys.stderr)
        sys.exit(1)

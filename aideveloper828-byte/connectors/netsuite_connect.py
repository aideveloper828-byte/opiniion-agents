"""
NetSuite REST API + SuiteQL connector for Opiniion agent ecosystem.

Supports Token-Based Authentication (TBA) and SuiteQL query execution.
All credentials loaded from .env at the repo root.

Usage:
    from connectors.netsuite_connect import NetSuiteClient
    client = NetSuiteClient()
    df = client.query("SELECT id, companyname FROM customer WHERE isinactive = 'F'")
"""

import os
import sys
import time
import hashlib
import hmac
import base64
import uuid
from urllib.parse import quote

import pandas as pd
import requests
from dotenv import load_dotenv

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_ROOT, ".env"))

NETSUITE_ACCOUNT_ID = os.getenv("NETSUITE_ACCOUNT_ID", "")
NETSUITE_CONSUMER_KEY = os.getenv("NETSUITE_CONSUMER_KEY", "")
NETSUITE_CONSUMER_SECRET = os.getenv("NETSUITE_CONSUMER_SECRET", "")
NETSUITE_TOKEN_ID = os.getenv("NETSUITE_TOKEN_ID", "")
NETSUITE_TOKEN_SECRET = os.getenv("NETSUITE_TOKEN_SECRET", "")

BASE_URL_TEMPLATE = "https://{account_id}.suitetalk.api.netsuite.com/services/rest"


class NetSuiteClient:
    """NetSuite REST API client with TBA authentication and SuiteQL support."""

    def __init__(
        self,
        account_id: str = NETSUITE_ACCOUNT_ID,
        consumer_key: str = NETSUITE_CONSUMER_KEY,
        consumer_secret: str = NETSUITE_CONSUMER_SECRET,
        token_id: str = NETSUITE_TOKEN_ID,
        token_secret: str = NETSUITE_TOKEN_SECRET,
    ):
        self.account_id = account_id.replace("_", "-").lower()
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.token_id = token_id
        self.token_secret = token_secret
        self.base_url = BASE_URL_TEMPLATE.format(account_id=self.account_id)
        self._session = requests.Session()

    def _build_oauth_header(self, method: str, url: str) -> str:
        """Build OAuth 1.0 Authorization header for TBA."""
        nonce = uuid.uuid4().hex
        timestamp = str(int(time.time()))

        params = {
            "oauth_consumer_key": self.consumer_key,
            "oauth_nonce": nonce,
            "oauth_signature_method": "HMAC-SHA256",
            "oauth_timestamp": timestamp,
            "oauth_token": self.token_id,
            "oauth_version": "1.0",
        }

        param_string = "&".join(
            f"{quote(k, safe='')}={quote(v, safe='')}"
            for k, v in sorted(params.items())
        )

        base_string = f"{method.upper()}&{quote(url, safe='')}&{quote(param_string, safe='')}"
        signing_key = f"{quote(self.consumer_secret, safe='')}&{quote(self.token_secret, safe='')}"

        signature = base64.b64encode(
            hmac.new(
                signing_key.encode("utf-8"),
                base_string.encode("utf-8"),
                hashlib.sha256,
            ).digest()
        ).decode("utf-8")

        params["oauth_signature"] = signature
        header_parts = ", ".join(f'{k}="{quote(v, safe="")}"' for k, v in params.items())
        return f"OAuth realm=\"{self.account_id}\", {header_parts}"

    def _request(
        self,
        method: str,
        endpoint: str,
        json_body: dict = None,
        params: dict = None,
        max_retries: int = 3,
    ) -> requests.Response:
        """Execute an authenticated request with retry logic."""
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": self._build_oauth_header(method, url),
            "Content-Type": "application/json",
            "Prefer": "transient",
        }

        for attempt in range(max_retries):
            try:
                resp = self._session.request(
                    method, url, headers=headers, json=json_body, params=params, timeout=120
                )
                if resp.status_code == 429:
                    wait = int(resp.headers.get("Retry-After", 5))
                    print(f"[NetSuite] Rate limited, waiting {wait}s (attempt {attempt + 1})")
                    time.sleep(wait)
                    headers["Authorization"] = self._build_oauth_header(method, url)
                    continue
                resp.raise_for_status()
                return resp
            except requests.exceptions.RequestException as exc:
                if attempt == max_retries - 1:
                    raise
                print(f"[NetSuite] Request failed ({exc}), retrying in 2s...")
                time.sleep(2)
                headers["Authorization"] = self._build_oauth_header(method, url)

    def query(self, sql: str, limit: int = 1000) -> pd.DataFrame:
        """Execute a SuiteQL query and return results as a DataFrame.

        Handles pagination automatically — fetches all pages if results exceed `limit`.
        """
        all_items = []
        offset = 0

        while True:
            body = {"q": sql}
            resp = self._request(
                "POST",
                "/query/v1/suiteql",
                json_body=body,
                params={"limit": limit, "offset": offset},
            )
            data = resp.json()
            items = data.get("items", [])
            all_items.extend(items)

            if not data.get("hasMore", False):
                break
            offset += limit

        if not all_items:
            return pd.DataFrame()

        return pd.DataFrame(all_items)

    def get_record(self, record_type: str, record_id: str) -> dict:
        """Fetch a single NetSuite record by type and internal ID."""
        resp = self._request("GET", f"/record/v1/{record_type}/{record_id}")
        return resp.json()

    def get_record_list(self, record_type: str, limit: int = 1000, offset: int = 0) -> list:
        """Fetch a list of records of a given type."""
        resp = self._request(
            "GET",
            f"/record/v1/{record_type}",
            params={"limit": limit, "offset": offset},
        )
        return resp.json().get("items", [])

    def test_connection(self) -> bool:
        """Verify credentials by running a trivial SuiteQL query."""
        try:
            df = self.query("SELECT id FROM currency WHERE id = '1'", limit=1)
            print(f"[NetSuite] Connection OK — returned {len(df)} row(s)")
            return True
        except Exception as exc:
            print(f"[NetSuite] Connection FAILED: {exc}")
            return False


if __name__ == "__main__":
    client = NetSuiteClient()
    if client.test_connection():
        print("Ready to use.")
    else:
        print("Check your .env credentials.", file=sys.stderr)
        sys.exit(1)

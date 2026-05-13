"""
Raw-HTTP Macrobond adapter for a client-side agent runtime.

Public API ΓÇö `MacrobondAdapter` exposes six methods:

    suggest_search_phrase(query)
    search_entities(text=, must_have_values=, must_not_have_values=,
                    entity_types=, include_discontinued=, metadata_mode=,
                    allow_long_result=)
    get_attribute_information(attributes=)
    list_attribute_values(attribute=)
    fetch_entities(names=, if_modified_since=)
    fetch_series(names=, date_end_of_period=, if_modified_since=)

All methods return plain dicts matching the shapes asserted by
tests/test_14_adapter_return_shapes.py. See .claude/commands/macrobond.md
for the canonical agent contract (tool invocation, search patterns, ranking
rules, response format) and metadata_guide.md for canonical attribute values.

Search results are candidate entities, not proof of uniqueness ΓÇö downstream
selection logic may still be needed when multiple plausible series exist.

Dependencies: requests.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests


class MacrobondAdapterError(Exception):
    pass


class MacrobondAuthError(MacrobondAdapterError):
    pass


class MacrobondRequestError(MacrobondAdapterError):
    pass


@dataclass
class MacrobondConfig:
    api_base_url: str = "https://api.macrobondfinancial.com"
    token_url: str = "https://apiauth.macrobondfinancial.com/mbauth/connect/token"
    scopes: List[str] = field(default_factory=lambda: [
        "macrobond_web_api.search_mb",
        "macrobond_web_api.read_mb",
    ])
    timeout_seconds: int = 30
    token_retry_once_on_401: bool = True
    fetch_names_per_request: int = 200


class MacrobondAdapter:
    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        env_path: str = ".env",
    ) -> None:
        self.config = MacrobondConfig()
        if client_id and client_secret:
            self.client_id = client_id
            self.client_secret = client_secret
        else:
            self._load_env_file(self._resolve_module_relative(env_path))
            self.client_id = client_id or os.environ.get("MACROBOND_CLIENT_ID")
            self.client_secret = client_secret or os.environ.get("MACROBOND_CLIENT_SECRET")
        if not self.client_id or not self.client_secret:
            raise MacrobondAuthError("MACROBOND_CLIENT_ID and MACROBOND_CLIENT_SECRET must be set.")

        self._token: Optional[str] = None
        self._token_expiry_epoch: float = 0.0

    @staticmethod
    def _resolve_module_relative(path: str) -> str:
        """Resolve a bare filename against the module's directory if not found in cwd.

        Lets `import macrobond_adapter_http` work from any working directory.
        Paths with a directory component (absolute or relative) are respected
        as-is.
        """
        if os.path.dirname(path):
            return path
        if os.path.isfile(path):
            return path
        module_relative = Path(__file__).resolve().parent / path
        if module_relative.is_file():
            return str(module_relative)
        return path

    @staticmethod
    def _load_env_file(env_path: str) -> None:
        if not os.path.isfile(env_path):
            return
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                os.environ.setdefault(key, value)

    def _token_is_valid(self) -> bool:
        return bool(self._token) and time.time() < self._token_expiry_epoch - 60

    def _fetch_token(self) -> str:
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": " ".join(self.config.scopes),
        }
        try:
            response = requests.post(self.config.token_url, data=payload, timeout=self.config.timeout_seconds)
        except requests.exceptions.Timeout:
            raise MacrobondAuthError(f"Token request timed out after {self.config.timeout_seconds}s")
        except requests.exceptions.ConnectionError as e:
            raise MacrobondAuthError(f"Token endpoint connection failed: {e}")
        if response.status_code != 200:
            raise MacrobondAuthError(f"Failed to fetch token: HTTP {response.status_code} - {response.text}")
        data = response.json()
        access_token = data.get("access_token")
        expires_in = int(data.get("expires_in", 1800))
        if not access_token:
            raise MacrobondAuthError("Token response did not include access_token.")
        self._token = access_token
        self._token_expiry_epoch = time.time() + expires_in
        return access_token

    def _get_token(self) -> str:
        if self._token_is_valid():
            return self._token  # type: ignore[return-value]
        return self._fetch_token()

    def _request(self, method: str, path: str, *, params: Optional[List[tuple]] = None, json_body: Optional[Any] = None, retry_on_401: bool = True) -> Any:
        url = f"{self.config.api_base_url}{path}"
        headers = {
            "Authorization": f"Bearer {self._get_token()}",
            "Accept": "application/json",
        }
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json_body,
                timeout=self.config.timeout_seconds,
            )
        except requests.exceptions.Timeout:
            raise MacrobondRequestError(f"Request timed out after {self.config.timeout_seconds}s for {method} {path}")
        except requests.exceptions.ConnectionError as e:
            raise MacrobondRequestError(f"Connection failed for {method} {path}: {e}")
        if response.status_code == 401 and retry_on_401 and self.config.token_retry_once_on_401:
            self._fetch_token()
            return self._request(method, path, params=params, json_body=json_body, retry_on_401=False)
        if response.status_code >= 400:
            raise MacrobondRequestError(f"HTTP {response.status_code} for {method} {path}: {response.text}")
        if not response.text:
            return None
        return response.json()

    @staticmethod
    def _as_list(value: Any) -> List[Any]:
        if value is None:
            return []
        if isinstance(value, list):
            return value
        return [value]

    def suggest_search_phrase(self, query: str) -> Dict[str, Any]:
        data = self._request("GET", "/v1/search/searchsuggestions", params=[("searchPhrase", query)])
        return {"query": query, "suggestions": data or []}

    def search_entities(
        self,
        *,
        text: Optional[str] = None,
        entity_types: Optional[List[str]] = None,
        must_have_values: Optional[Dict[str, Any]] = None,
        must_not_have_values: Optional[Dict[str, Any]] = None,
        include_discontinued: bool = False,
        metadata_mode: str = "full",
        allow_long_result: bool = False,
    ) -> Dict[str, Any]:
        params: List[tuple] = []
        if text:
            params.append(("text", text))
        for et in (entity_types or ["TimeSeries"]):
            params.append(("entityType", et))
        params.append(("noMetaData", "true" if metadata_mode == "names_only" else "false"))
        if include_discontinued:
            params.append(("includeDiscontinued", "true"))
        if allow_long_result:
            params.append(("allowLongResult", "true"))

        for attr, raw_value in (must_have_values or {}).items():
            for value in self._as_list(raw_value):
                params.append((attr, str(value)))

        for attr, raw_value in (must_not_have_values or {}).items():
            for value in self._as_list(raw_value):
                params.append((f"!{attr}", str(value)))

        data = self._request("GET", "/v1/search/entities", params=params)

        entities = []
        for item in data.get("results", []):
            entities.append(
                {
                    "name": item.get("Name") or item.get("PrimName"),
                    "entity_type": item.get("EntityType"),
                    "metadata": item,
                }
            )
        return {
            "entities": entities,
            "is_truncated": data.get("IsTruncated", data.get("isTruncated", False)),
            "filter_suggestions": data.get("FilterSuggestions", data.get("filterSuggestions", [])),
        }

    def get_attribute_information(self, attributes: List[str]) -> Dict[str, Any]:
        params = [("n", a) for a in attributes]
        data = self._request("GET", "/v1/metadata/getattributeinformation", params=params)
        return {"attributes": data}

    def list_attribute_values(self, attribute: str) -> Dict[str, Any]:
        data = self._request("GET", "/v1/metadata/listattributevalues", params=[("n", attribute)])
        values = []
        for item in data:
            values.append(
                {
                    "value": item.get("value") or item.get("name") or "",
                    "description": item.get("description") or item.get("fullDescription") or "",
                    "comment": item.get("comment"),
                }
            )
        return {"attribute": attribute, "values": values}

    def _batch_names(self, names: List[str]) -> List[List[str]]:
        batch_size = self.config.fetch_names_per_request
        return [names[i:i + batch_size] for i in range(0, len(names), batch_size)]

    @staticmethod
    def _classify_error(error_code: Any) -> str:
        if error_code is None:
            return "ok"
        if error_code in (304, 206) or error_code == "notModified":
            return "not_modified"
        return "missing"

    def fetch_entities(self, *, names: List[str], if_modified_since: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        if_modified_since = if_modified_since or {}
        entities, missing, not_modified = [], [], []

        for batch in self._batch_names(names):
            body = []
            for name in batch:
                entry: Dict[str, Any] = {"name": name}
                if name in if_modified_since:
                    entry["ifModifiedSince"] = if_modified_since[name]
                body.append(entry)

            data = self._request("POST", "/v1/series/fetchentities", json_body=body)
            for requested_name, item in zip(batch, data):
                status = self._classify_error(item.get("errorCode"))
                if status == "ok":
                    metadata = item.get("metadata", {})
                    entities.append({
                        "name": metadata.get("PrimName", requested_name),
                        "entity_type": metadata.get("EntityType"),
                        "metadata": metadata,
                    })
                elif status == "not_modified":
                    not_modified.append(requested_name)
                else:
                    missing.append(requested_name)

        return {"entities": entities, "missing": missing, "not_modified": not_modified}

    def fetch_series(self, *, names: List[str], date_end_of_period: bool = False, if_modified_since: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        if_modified_since = if_modified_since or {}
        series, missing, not_modified = [], [], []

        for batch in self._batch_names(names):
            body = []
            for name in batch:
                entry: Dict[str, Any] = {"name": name}
                if name in if_modified_since:
                    entry["ifModifiedSince"] = if_modified_since[name]
                body.append(entry)

            data = self._request(
                "POST",
                "/v1/series/fetchseries",
                params=[("dateEndOfPeriod", "true" if date_end_of_period else "false")],
                json_body=body,
            )

            for requested_name, item in zip(batch, data):
                status = self._classify_error(item.get("errorCode"))
                if status == "ok":
                    metadata = item.get("metadata", {})
                    series.append({
                        "name": metadata.get("PrimName", requested_name),
                        "metadata": metadata,
                        "dates": list(item.get("dates", [])),
                        "values": list(item.get("values", [])),
                    })
                elif status == "not_modified":
                    not_modified.append(requested_name)
                else:
                    missing.append(requested_name)

        return {"series": series, "missing": missing, "not_modified": not_modified}

    # -------------------------------------------------------------------------
    # Revision history methods
    # -------------------------------------------------------------------------

    def get_revision_info(self, names: List[str]) -> Dict[str, Any]:
        """Check if series store revision history and get available vintage timestamps.

        Returns:
            {
                "series": [
                    {
                        "name": str,
                        "stores_revisions": bool,
                        "has_revisions": bool,
                        "time_stamp_of_first_revision": str | None,
                        "time_stamp_of_last_revision": str | None,
                        "vintage_timestamps": [str, ...]
                    },
                    ...
                ],
                "errors": [{"name": str, "error": str}, ...]
            }
        """
        params = [("n", name) for name in names]
        data = self._request("GET", "/v1/series/getrevisioninfo", params=params)

        series_info, errors = [], []
        for name, item in zip(names, data):
            error_text = item.get("errorText")
            if error_text:
                errors.append({"name": name, "error": error_text})
            else:
                series_info.append({
                    "name": name,
                    "stores_revisions": item.get("storesRevisions", False),
                    "has_revisions": item.get("hasRevisions", False),
                    "time_stamp_of_first_revision": item.get("timeStampOfFirstRevision"),
                    "time_stamp_of_last_revision": item.get("timeStampOfLastRevision"),
                    "vintage_timestamps": item.get("vintageTimeStamps", []),
                })
        return {"series": series_info, "errors": errors}

    def fetch_vintage_series(
        self,
        *,
        vintage_time: str,
        names: List[str],
        get_times_of_change: bool = False,
        date_end_of_period: bool = False,
    ) -> Dict[str, Any]:
        """Fetch series as they were at a specific point in time.

        Args:
            vintage_time: ISO 8601 timestamp (e.g. "2020-01-01T00:00:00Z")
            names: List of series names to fetch
            get_times_of_change: If True, include when each value was last changed
            date_end_of_period: Return dates at end of period instead of start

        Returns:
            {
                "series": [...],
                "missing": [str, ...],
                "errors": [{"name": str, "error": str}, ...]
            }
        """
        params: List[tuple] = [
            ("t", vintage_time),
            ("getTimesOfChange", "true" if get_times_of_change else "false"),
            ("dateEndOfPeriod", "true" if date_end_of_period else "false"),
        ]
        for name in names:
            params.append(("n", name))

        data = self._request("GET", "/v1/series/fetchvintageseries", params=params)

        series, missing, errors = [], [], []
        for name, item in zip(names, data):
            error_text = item.get("errorText")
            error_code = item.get("errorCode")
            if error_text:
                if error_code == 404:
                    missing.append(name)
                else:
                    errors.append({"name": name, "error": error_text})
            else:
                entry = {
                    "name": item.get("metadata", {}).get("PrimName", name),
                    "metadata": item.get("metadata", {}),
                    "dates": list(item.get("dates", [])),
                    "values": list(item.get("values", [])),
                    "vintage_time_stamp": item.get("vintageTimeStamp"),
                }
                if get_times_of_change:
                    entry["times_of_change"] = item.get("timesOfChange")
                series.append(entry)
        return {"series": series, "missing": missing, "errors": errors}

    def fetch_all_vintages(
        self,
        *,
        name: str,
        if_modified_since: Optional[str] = None,
        last_revision: Optional[str] = None,
        last_revision_adjustment: Optional[str] = None,
        date_end_of_period: bool = False,
    ) -> Dict[str, Any]:
        """Fetch complete revision history for a single series.

        Args:
            name: Series name
            if_modified_since: Only return if modified since this timestamp
            last_revision: For incremental updates, pass LastRevisionTimeStamp from prior response
            last_revision_adjustment: For incremental updates, pass LastRevisionAdjustmentTimeStamp
            date_end_of_period: Return dates at end of period instead of start

        Returns:
            {
                "name": str,
                "vintages": [{"vintage_time_stamp": str, "dates": [...], "values": [...]}, ...],
                "is_incremental": bool,
                "not_modified": bool
            }
        """
        params: List[tuple] = [
            ("n", name),
            ("dateEndOfPeriod", "true" if date_end_of_period else "false"),
        ]
        if if_modified_since:
            params.append(("ifModifiedSince", if_modified_since))
        if last_revision:
            params.append(("lastRevision", last_revision))
        if last_revision_adjustment:
            params.append(("lastRevisionAdjustment", last_revision_adjustment))

        data = self._request("GET", "/v1/series/fetchallvintageseries", params=params)

        if data is None:
            return {"name": name, "vintages": [], "is_incremental": False, "not_modified": True}

        vintages = []
        for item in data:
            vintages.append({
                "vintage_time_stamp": item.get("vintageTimeStamp"),
                "dates": list(item.get("dates", [])),
                "values": list(item.get("values", [])),
            })
        return {"name": name, "vintages": vintages, "is_incremental": bool(last_revision), "not_modified": False}

    def fetch_nth_release(
        self,
        *,
        nth: int,
        names: List[str],
        get_times_of_change: bool = False,
        date_end_of_period: bool = False,
    ) -> Dict[str, Any]:
        """Fetch the nth release of series (0=first release, 1=first revision, etc.).

        Args:
            nth: Release number (0=first/initial, 1=first revision, etc.)
            names: List of series names
            get_times_of_change: If True, include when each value was released
            date_end_of_period: Return dates at end of period instead of start

        Returns:
            {
                "series": [...],
                "missing": [str, ...],
                "errors": [{"name": str, "error": str}, ...]
            }
        """
        params: List[tuple] = [
            ("nth", str(nth)),
            ("getTimesOfChange", "true" if get_times_of_change else "false"),
            ("dateEndOfPeriod", "true" if date_end_of_period else "false"),
        ]
        for name in names:
            params.append(("n", name))

        data = self._request("GET", "/v1/series/fetchnthreleaseseries", params=params)

        series, missing, errors = [], [], []
        for name, item in zip(names, data):
            error_text = item.get("errorText")
            error_code = item.get("errorCode")
            if error_text:
                if error_code == 404:
                    missing.append(name)
                else:
                    errors.append({"name": name, "error": error_text})
            else:
                entry = {
                    "name": item.get("metadata", {}).get("PrimName", name),
                    "metadata": item.get("metadata", {}),
                    "dates": list(item.get("dates", [])),
                    "values": list(item.get("values", [])),
                }
                if get_times_of_change:
                    entry["times_of_change"] = item.get("timesOfChange")
                series.append(entry)
        return {"series": series, "missing": missing, "errors": errors}

    def fetch_observation_history(
        self,
        *,
        name: str,
        observation_dates: List[str],
    ) -> Dict[str, Any]:
        """Get revision history for specific observation dates within a series.

        Args:
            name: Series name
            observation_dates: List of ISO observation dates (e.g. ["2023-10-01T00:00:00Z"])

        Returns:
            {
                "name": str,
                "observations": [
                    {"observation_date": str, "values": [...], "timestamps": [...]}
                ]
            }
        """
        params: List[tuple] = [("n", name)]
        for date in observation_dates:
            params.append(("t", date))

        data = self._request("GET", "/v1/series/fetchobservationhistory", params=params)

        observations = []
        for item in data:
            observations.append({
                "observation_date": item.get("observationDate"),
                "values": list(item.get("values", [])),
                "timestamps": list(item.get("timeStamps", [])),
            })
        return {"name": name, "observations": observations}

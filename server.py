"""
Macrobond MCP Server

Exposes the MacrobondAdapter methods as MCP tools for AI agents.

Credential handling
-------------------
Set ``MACROBOND_CLIENT_ID`` and ``MACROBOND_CLIENT_SECRET`` environment
variables.  The server is started automatically by the AI agent via stdio
transport — no manual server management needed.

Each unique client-id gets its own ``MacrobondAdapter`` instance whose OAuth
token is cached and refreshed automatically.  All state is held in the server
process; no credentials are persisted to disk.
"""

import os
import threading
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers

from macrobond_adapter_http import MacrobondAdapter, MacrobondAuthError


mcp = FastMCP("macrobond")

_adapters: dict[str, MacrobondAdapter] = {}
_adapters_lock = threading.Lock()


def _get_credentials() -> tuple[str, str]:
    """Return (client_id, client_secret) from request headers or env vars.

    HTTP mode  : reads ``X-Macrobond-Client-ID`` / ``X-Macrobond-Client-Secret`` headers.
    stdio mode : falls back to ``MACROBOND_CLIENT_ID`` / ``MACROBOND_CLIENT_SECRET`` env vars.
    """
    client_id = ""
    client_secret = ""
    try:
        headers = get_http_headers(
            include={"x-macrobond-client-id", "x-macrobond-client-secret"}
        )
        client_id = headers.get("x-macrobond-client-id", "")
        client_secret = headers.get("x-macrobond-client-secret", "")
    except Exception:
        pass

    client_id = client_id or os.environ.get("MACROBOND_CLIENT_ID", "")
    client_secret = client_secret or os.environ.get("MACROBOND_CLIENT_SECRET", "")

    if not client_id or not client_secret:
        raise MacrobondAuthError(
            "Credentials required. Set MACROBOND_CLIENT_ID and "
            "MACROBOND_CLIENT_SECRET environment variables."
        )
    return client_id, client_secret


def _get_adapter() -> MacrobondAdapter:
    """Return the cached adapter for the current caller, creating one if needed."""
    client_id, client_secret = _get_credentials()
    with _adapters_lock:
        if client_id not in _adapters:
            _adapters[client_id] = MacrobondAdapter(
                client_id=client_id,
                client_secret=client_secret,
            )
    return _adapters[client_id]


@mcp.tool()
def search_entities(
    text: Optional[str] = None,
    must_have_values: Optional[Dict[str, Any]] = None,
    must_not_have_values: Optional[Dict[str, Any]] = None,
    entity_types: Optional[List[str]] = None,
    include_discontinued: bool = False,
) -> Dict[str, Any]:
    """Search for Macrobond time series by text and metadata filters. Returns entity names and metadata."""
    adapter = _get_adapter()
    return adapter.search_entities(
        text=text,
        must_have_values=must_have_values,
        must_not_have_values=must_not_have_values,
        entity_types=entity_types,
        include_discontinued=include_discontinued,
    )


@mcp.tool()
def fetch_series(
    names: List[str],
    date_end_of_period: bool = False,
) -> Dict[str, Any]:
    """Fetch time series data (dates and values) for one or more series by name."""
    adapter = _get_adapter()
    return adapter.fetch_series(names=names, date_end_of_period=date_end_of_period)


@mcp.tool()
def fetch_entities(names: List[str]) -> Dict[str, Any]:
    """Fetch entity metadata (without observation values). Use for Release entities or metadata-only queries."""
    adapter = _get_adapter()
    return adapter.fetch_entities(names=names)


@mcp.tool()
def suggest_search_phrase(query: str) -> Dict[str, Any]:
    """Get search phrase suggestions for a natural language query."""
    adapter = _get_adapter()
    return adapter.suggest_search_phrase(query=query)


@mcp.tool()
def list_attribute_values(attribute: str) -> Dict[str, Any]:
    """List all valid values for a metadata attribute (e.g., Region, Frequency, Source)."""
    adapter = _get_adapter()
    return adapter.list_attribute_values(attribute=attribute)


@mcp.tool()
def get_attribute_information(attributes: List[str]) -> Dict[str, Any]:
    """Get information about metadata attributes (verify they exist)."""
    adapter = _get_adapter()
    return adapter.get_attribute_information(attributes=attributes)


@mcp.tool()
def get_revision_info(names: List[str]) -> Dict[str, Any]:
    """Check if series store revision history and get available vintage timestamps."""
    return _get_adapter().get_revision_info(names=names)


@mcp.tool()
def fetch_vintage_series(
    names: List[str],
    vintage_time: str,
    get_times_of_change: bool = False,
    date_end_of_period: bool = False,
) -> Dict[str, Any]:
    """Fetch series as they were at a specific point in time (vintage snapshot).

    Args:
        names: Series names to fetch.
        vintage_time: ISO 8601 timestamp, e.g. "2020-01-01T00:00:00Z".
        get_times_of_change: Include when each value was last changed.
        date_end_of_period: Return dates at end of period instead of start.
    """
    return _get_adapter().fetch_vintage_series(
        vintage_time=vintage_time,
        names=names,
        get_times_of_change=get_times_of_change,
        date_end_of_period=date_end_of_period,
    )


@mcp.tool()
def fetch_all_vintages(
    name: str,
    if_modified_since: Optional[str] = None,
    last_revision: Optional[str] = None,
    last_revision_adjustment: Optional[str] = None,
    date_end_of_period: bool = False,
) -> Dict[str, Any]:
    """Fetch the complete revision history for a single series.

    Args:
        name: Series name.
        if_modified_since: Only return data if modified since this ISO timestamp.
        last_revision: For incremental updates — LastRevisionTimeStamp from prior response.
        last_revision_adjustment: For incremental updates — LastRevisionAdjustmentTimeStamp from prior response.
        date_end_of_period: Return dates at end of period instead of start.
    """
    return _get_adapter().fetch_all_vintages(
        name=name,
        if_modified_since=if_modified_since,
        last_revision=last_revision,
        last_revision_adjustment=last_revision_adjustment,
        date_end_of_period=date_end_of_period,
    )


@mcp.tool()
def fetch_nth_release(
    names: List[str],
    nth: int,
    get_times_of_change: bool = False,
    date_end_of_period: bool = False,
) -> Dict[str, Any]:
    """Fetch the nth release of series (0=first/initial release, 1=first revision, etc.).

    Useful for constructing real-time datasets using only initially-released values.

    Args:
        names: Series names to fetch.
        nth: Release number (0=first release, 1=first revision, 2=second revision, ...).
        get_times_of_change: Include when each value was released.
        date_end_of_period: Return dates at end of period instead of start.
    """
    return _get_adapter().fetch_nth_release(
        nth=nth,
        names=names,
        get_times_of_change=get_times_of_change,
        date_end_of_period=date_end_of_period,
    )


@mcp.tool()
def fetch_observation_history(
    name: str,
    observation_dates: List[str],
) -> Dict[str, Any]:
    """Get the revision history for specific observation dates within a series.

    Shows how the value for each date changed across successive data releases.

    Args:
        name: Series name.
        observation_dates: ISO observation dates, e.g. ["2023-10-01T00:00:00Z"].
    """
    return _get_adapter().fetch_observation_history(
        name=name,
        observation_dates=observation_dates,
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")

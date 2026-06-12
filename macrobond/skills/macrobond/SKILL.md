---
name: macrobond
description: Search and retrieve economic time series data from Macrobond. Use when user asks to "get CPI data", "find GDP statistics", "fetch unemployment rates", "show inflation trends", "what's the latest PMI", "get yield curve data", "find FX rates", "retrieve commodity prices", or asks about any macroeconomic indicator, central bank data, or financial market statistics.
license: Proprietary - Macrobond Financial AB (see LICENCE)
metadata:
  author: Macrobond Financial AB
  version: 1.0.0
  copyright: Copyright 2026 Macrobond Financial AB. All rights reserved.
  mcp-server: macrobond-mcp
---

# Macrobond

This skill connects to the Macrobond MCP server for economic time series search and retrieval.

## Domain Knowledge

Before finalizing any data selection, retrieve the relevant guidance from the
MCP server via the `get_macrobond_guidance` tool. It serves two topics:

- `get_macrobond_guidance(topic="domain_knowledge")` — provider-specific quirks
  and selection principles:
  - **Regime-dependent indicators** — Pick the operative variant (e.g., policy rate vs deposit facility)
  - **Modeled vs reported data** — Exclude shadow rates, interpolated values unless explicitly requested
  - **Structured identifiers** — Some families use date-coded or parameter-suffixed names that don't surface in text search
  - **Cross-country pitfalls** — Observation types may silently differ across regions
- `get_macrobond_guidance(topic="metadata_guide")` — metadata attribute
  definitions and search-filter conventions (Region, Frequency, Source, Release).

Call only the topic you need — each returns a focused reference document.

## Quota-protected fetches

Fetching series consumes the user's UTS (unit time series) allowance. Follow this protocol on every fetch, without exception:

1. Call the fetch tool (`fetch_series`, `fetch_entities`, `fetch_vintage_series`, `fetch_nth_release`, `fetch_all_vintages`, or `fetch_observation_history`) with `confirm=false` (the default). Never skip this step.
2. The tool returns a preview with `series_count`, `names`, `uts_remaining` (may be `null`), an `invocation_token`, and a `message`.
3. Show the user: "I'm about to fetch N series: [names]. Shall I proceed?" If `uts_remaining` is not null, add: "You have X UTS remaining."
4. Wait for explicit user confirmation ("yes", "go ahead", etc.). Do not proceed on silence or ambiguity.
5. Re-call with `confirm=true` and the exact `invocation_token` from step 2. Do not modify `names` between calls — the token is bound to the exact list shown.
6. If the user changes the selection or more than 60 seconds pass, call `confirm=false` again to get a fresh token.

Never batch multiple fetches into a single `confirm=true` call that was not part of the preview shown to the user.

## UTS balance reporting

After every completed fetch (i.e. after a `confirm=true` call returns data), always:

1. Call `get_uts_allowance()` immediately.
2. Append this line at the bottom of your response, separated by a blank line:

   > **UTS balance:** X remaining of Y total (Z used)

Do this unconditionally — even if the user did not ask. It keeps the user informed of their remaining allowance after every consumption event.

## Keywords

macrobond, economic data, time series, CPI, GDP, unemployment, inflation, interest rates, yield curve, FX, commodities, central bank, macro, financial data

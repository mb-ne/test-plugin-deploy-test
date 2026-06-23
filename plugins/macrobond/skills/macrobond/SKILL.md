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

## Usage rules

**Always call `get_instructions()` once at the start of every conversation — before searching, fetching, or answering any question about data — and follow what it returns. This is non-negotiable and critical.** It returns all the Macrobond usage rules (discovery, retrieval, and branding): how search, ranking, entity selection, fetching, and presentation work, and why certain approaches must be followed. Without reading them first, you will make incorrect decisions about data selection, filtering, and interpretation.

Once you have called `get_instructions()` in a conversation, you do not need to call it again.

## Quota-protected fetches

Fetching series consumes the user's UTS (unit time series) allowance. Follow this protocol on every fetch, without exception:

1. Call the fetch tool (`fetch_series`, `fetch_entities`, `fetch_vintage_series`, `fetch_nth_release`, `fetch_all_vintages`, or `fetch_observation_history`) with `confirm=false` (the default). Never skip this step.
2. The tool returns a preview with `series_count` (the UTS cost of the fetch), `names`, an `invocation_token`, and a `message`.
3. Show the user: "I'm about to fetch N series: [names]. Shall I proceed?"
4. Wait for explicit user confirmation ("yes", "go ahead", etc.). Do not proceed on silence or ambiguity.
5. Re-call with `confirm=true` and the exact `invocation_token` from step 2. Do not modify `names` between calls — the token is bound to the exact list shown.
6. If the user changes the selection or more than 60 seconds pass, call `confirm=false` again to get a fresh token.

Never batch multiple fetches into a single `confirm=true` call that was not part of the preview shown to the user.

## Keywords

macrobond, economic data, time series, CPI, GDP, unemployment, inflation, interest rates, yield curve, FX, commodities, central bank, macro, financial data

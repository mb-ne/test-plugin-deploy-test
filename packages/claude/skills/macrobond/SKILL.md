---
name: macrobond
description: Search and retrieve economic time series data from Macrobond. Use when user asks to "get CPI data", "find GDP statistics", "fetch unemployment rates", "show inflation trends", "what's the latest PMI", "get yield curve data", "find FX rates", "retrieve commodity prices", or asks about any macroeconomic indicator, central bank data, or financial market statistics.
license: Proprietary - Macrobond Financial AB (see LICENCE)
metadata:
  author: Macrobond Financial AB
  version: 1.1.0
  copyright: Copyright 2026 Macrobond Financial AB. All rights reserved.
  mcp-server: macrobond-mcp
---

# Macrobond

The Macrobond MCP server searches and retrieves economic and financial time series.
Follow these steps in order for every data request.

## Steps

1. **Ask only when the request is too generic to search.** "give me GDP" is: ask what is
   missing, the region, the measure, the frequency or the period. Skip this when the
   request already says what to look for.
2. **Read the instructions.** Call `get_instructions` with no topic, then
   `get_instructions` with topic `search`, and follow what they return. Load topic
   `selection` when several candidates look alike, `retrieval` for vintages or
   revisions, and `presentation` before answering with data.
3. **Search.** Call `search_entities`, one call per concept and region.
4. **Open the picker.** Always open `render_series_picker` with the `search_id` and the
   best results as the recommended names. The user picks in the picker; do not ask for
   confirmation in text.

## Hosts without the app tools

When `render_series_picker`, `render_chart` and `render_table` are not in your tool
list, the host draws no widgets. For step 4: show the candidates as a markdown table and
ask. Then call the fetch tool with `confirm=false`, show the preview, wait for a yes, and
call again with `confirm=true` and the `invocation_token` it returned. Show the values as
a markdown table. Then call `create_series_preview_url` with the codes from the search
result and show the returned link, so the user can open the series in Macrobond Analysis.

## Keywords

macrobond, economic data, time series, CPI, GDP, unemployment, inflation, interest
rates, yield curve, FX, commodities, central bank, macro, financial data

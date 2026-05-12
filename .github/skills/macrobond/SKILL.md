---
name: macrobond
description: Search and retrieve economic time series data from Macrobond. Use when user asks to "get CPI data", "find GDP statistics", "fetch unemployment rates", "show inflation trends", "what's the latest PMI", "get yield curve data", "find FX rates", "retrieve commodity prices", or asks about any macroeconomic indicator, central bank data, or financial market statistics.
license: Proprietary - Macrobond Financial AB (see LICENCE)
metadata:
  author: Macrobond Financial AB
  version: 1.0.0
  copyright: Copyright 2026 Macrobond Financial AB. All rights reserved.
  mcp-server: macrobond
---

# Macrobond Economic Data Skill

This skill connects to the Macrobond MCP server for economic time series search and retrieval.

## Domain Knowledge

Before finalizing any data selection, consult `references/domain_knowledge.md` for:
- **Regime-dependent indicators** — Pick the operative variant (e.g., policy rate vs deposit facility)
- **Modeled vs reported data** — Exclude shadow rates, interpolated values unless explicitly requested
- **Structured identifiers** — Some families use date-coded or parameter-suffixed names that don't surface in text search
- **Cross-country pitfalls** — Observation types may silently differ across regions

## References

- `references/domain_knowledge.md` — Provider-specific quirks and selection principles
- `references/metadata_guide.md` — Attribute definitions and filter usage

## Keywords

macrobond, economic data, time series, CPI, GDP, unemployment, inflation, interest rates, yield curve, FX, commodities, central bank, macro, financial data

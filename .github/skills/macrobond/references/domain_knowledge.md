# Macrobond Domain Knowledge

Macrobond-specific selection principles and data quirks that cannot be discovered through a single text search or metadata inspection. Read this file before finalising a candidate set ΓÇö these patterns are the recurring source of silently-wrong results across use cases.

This file complements `.claude/commands/macrobond.md` (the agent contract, including search patterns) and `metadata_guide.md` (filter conventions). It holds **principles**, not a lookup table of specific series. Do not treat its guidance as an authoritative code list ΓÇö always verify the current best series for the concept via search and metadata inspection.

---

## Regime-dependent indicators: pick the operative variant

Some institutions publish several variants of the same concept simultaneously ΓÇö different rates, different definitions, different consolidation treatments ΓÇö where only one is **operative** under the currently-prevailing framework. The most-cited historical variant is not always the binding one. Examples span central-bank rate corridors (target rate vs deposit facility vs main refinancing rate), fiscal consolidation treatments, and multiple "headline" measures of the same concept.

**Rule:** when asked for "the" indicator from a provider that publishes variants:

1. Identify which variant is currently operative or canonical under the prevailing framework.
2. Select that variant as the primary answer.
3. Offer alternatives with historical context only if the user has a cross-period or retrospective use case.

---

## Exclude modeled, derived, and academic-research series

Text search for a live indicator can surface academic-research outputs ΓÇö shadow rates, modeled effective rates, derivation-style estimates ΓÇö alongside the reported values. These outputs may be categorised under the same concept heading as the reported series in source catalogs, but they are **model outputs**, not reported data, and can differ from the reported value by substantial margins.

Similarly, parameter-indexed families (yield-curve tenors, term structures, scenario panels) often include implied or interpolated members for parameter values that are not actually observed ΓÇö tenors governments do not auction, horizons not directly surveyed, etc. These are modeled, not measured.

**Rule:** filter out candidates whose `FullDescription` contains "Shadow Rate", "Wu-Xia", "Implied", "Interpolated", "Modelled", "Estimated", or equivalent language indicating a derivation rather than a reported value, unless the user explicitly asked for modeled data. Prefer reported series for live-tracking and policy-reference use cases.

---

## Identifier conventions are not uniform within a family

Naming conventions do not always stay consistent within what looks like a single family ΓÇö a country's yield curve, a provider's survey panel, a commodity's futures chain. Within one family:

- Zero-padding may be used for some members and not others.
- Month-based and year-based suffixes may coexist for the same notional parameter.
- Daily-frequency variants may use different stems than monthly-frequency variants.
- Auctioned / surveyed members and interpolated members may use different conventions.

**Rule:** when a family member is missing and a neighbour is present, try pattern variants (zero-padded vs not, month vs year suffix, daily-stem vs monthly-stem) before reporting a gap. Fetch one or two peer members with `fetch_entities` and inspect their identifiers to learn the local convention.

---

## Structured identifiers that don't surface in text search

Some data families use **structured naming conventions** ΓÇö date-coded, parameter-suffixed, or template-shaped ΓÇö whose identifiers do not match how users phrase queries. Text search returns zero even when the data is indexed.

**Rule:** when you suspect a structured family exists but text search is empty:

1. Find one peer series from the same source or source category via a different path (search by concept, inspect the provider's broader catalog, probe a known-neighbouring series).
2. Use `fetch_entities` on the peer to learn the identifier convention.
3. Construct candidate names directly from the pattern.
4. Use `fetch_series`'s `missing` partition as cheap feedback on whether a constructed name exists.

Absence from text search is a weak signal for structured families ΓÇö do not conclude the data is absent without probing by identifier pattern.

---

## Name-vs-description mismatches

A series whose identifier implies one parameter value (a tenor, a horizon, a quarter) but whose `FullDescription` states another is ambiguous. Before including it in a set, verify that the name and the description agree on the underlying parameter. Flag the mismatch and ask the user to confirm rather than picking silently.

---

## Time-base mixing in rate and flow series

Flow and rate series can be published on different time bases: annualized rates (AR), quarterly flows, monthly flows, period-over-period changes, year-over-year changes. Mixing different time bases in the same comparison produces invisible scale errors ΓÇö a factor of 4 (quarterly vs annualized), a factor of 12 (monthly vs annualized), or a sign error (level vs change).

**Rule:** inspect `FullDescription` on every series in a flow/rate set for qualifiers like "AR", "Annualized", "Annual Rate", "Change P/P", "Change Y/Y". If any series uses a different time base from the others, convert, substitute, or exclude before presenting. For cross-country comparisons, prefer a single harmonised dataset with one time base over stitching together national-source series with different conventions.

---

## Cross-country set construction traps

### Prefer a single harmonised provider for cross-country comparability

For any cross-country set where methodology matters (fiscal aggregates, debt, price indices, labour-market definitions), prefer a single harmonised cross-country provider over stitching together national-source series. Harmonised providers apply consistent definitions, consolidation, and seasonal adjustment; mixing national sources introduces methodological differences that silently invalidate comparability.

### Coverage gaps in harmonised datasets

Harmonised datasets may have coverage gaps for specific countries or regions. Verify coverage before publishing a labeled "G7", "G10", or "EU" set. If a country is missing from expected coverage:

1. Supplement with the closest national-source or annual equivalent.
2. Flag the frequency and lag mismatch explicitly in the response.

Never silently omit a country from a labeled cross-country set.

### "SA" is not always a level index

A series tagged or described as "SA" for one country may be a level index, while another country's "SA" variant of the same concept is a period-over-period change or a moving-average-of-change. Side-by-side comparison silently mixes concepts and produces invisibly-wrong tables.

**Rule:** before presenting a cross-country set, inspect `FullDescription` of each series for phrases like "Change P/P", "Change Y/Y", "Moving Average", "Growth Rate". If any series differs from the others on observation type, flag explicitly or fall back to the NSA level with a note.

---

## Discontinued or stale benchmark series

Some benchmark series remain indexed and return normally from `search_entities`, but their observations have not updated in months or years ΓÇö they are effectively discontinued. Confirm `LastValueDate` / `EndDate` on every series used in a live or tracking context; substitute a timely alternative when a benchmark has gone stale.

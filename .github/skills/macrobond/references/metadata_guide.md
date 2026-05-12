# Metadata Quick Reference

Macrobond search is metadata-driven. Never rely on identifier strings for meaning ΓÇö always use metadata attributes.

## Key attributes for search filters

### `Region`
Geography or economic area. Use as a filter in `search_entities` and to verify results. Codes are lowercase ISO alpha-2 (e.g. `us`, `gb`, `de`). Use `list_attribute_values("Region")` to verify a code before filtering.

**Common trap:** Euro Area is `eu`, not `ea`. The code `ea` maps to Eurasia. Similarly, United Kingdom is `gb`, not `uk`.

### `RegionKey`
Cross-country concept identifier. The strongest filter for comparing the same indicator across countries.

**Workflow:** find a reference series ΓåÆ read its `RegionKey` from metadata ΓåÆ use that RegionKey with multiple Region values.

RegionKey values are not enumerated in this guide ΓÇö always discover the right value by reading the `RegionKey` metadata on a representative search result. Values are short lowercase tokens with underscore separators, commonly shaped as a concept stem plus a scope or seasonal-adjustment qualifier. Well-established statistical concepts tend to have stable RegionKey conventions across countries; niche or provider-specific concepts may not be RegionKey-tagged at all and require text + `Region` filter combinations instead.

### `RegionVariable`

A weaker concept-alignment tag than `RegionKey`. Some series carry `RegionVariable` (a country-specific concept descriptor) without a `RegionKey`. When choosing between otherwise-equivalent candidates for the same concept, prefer the RegionKey-tagged series ΓÇö it is the cross-country concept anchor used for fan-out. Use `RegionVariable`-only series as fallback; use untagged series only when neither tag is present.

### `Frequency`
Observation frequency. Canonical values (verified against `list_attribute_values("Frequency")`):

| Value | Description |
|-------|-------------|
| `daily` | Daily observations |
| `weekly` | Weekly observations |
| `bimonthly` | Bi-monthly observations (every two months) |
| `monthly` | Monthly observations |
| `quadmonthly` | Quad-monthly observations (every four months) |
| `quarterly` | Quarterly observations |
| `semiannual` | Semi-annual observations |
| `annual` | Annual observations |

Most macro data is `monthly`, `quarterly`, or `annual`; sub-monthly frequencies (`daily`, `weekly`) apply mainly to market-price, flow, and flash-indicator data. `bimonthly`, `quadmonthly`, and `semiannual` are uncommon. Verify the frequency of a concept by inspecting a representative series before filtering rather than assuming.

### `Source`
The data provider. Use to constrain search to a specific statistical agency or organisation.

### `Release`
The release entity associated with a series. Useful for finding publication schedules via `fetch_entities`.

## Key attributes for interpreting results

| Attribute | Use |
|-----------|-----|
| `FullDescription` | Human-readable series description ΓÇö primary tool for understanding what a series measures |
| `DisplayUnit` | Unit of measurement (e.g. "Index", "Percent", "Millions USD") |
| `Currency` | Currency denomination where applicable |
| `StartDate` | First available observation |
| `EndDate` | Most recent available observation |
| `LastModifiedTimeStamp` | When the series was last updated ΓÇö use for conditional fetch |
| `PrimName` | Canonical series name |

## Metadata discovery workflow

When you don't know the correct filter value:

1. `get_attribute_information(attributes=["AttributeName"])` ΓÇö verify the attribute exists and supports listing.
2. `list_attribute_values(attribute="AttributeName")` ΓÇö get all valid values.
3. Use the canonical values in your search filters.

## Using `filter_suggestions`

`search_entities` responses include `filter_suggestions` ΓÇö these are the API's recommendations for narrowing a broad result set. Use them to:
- Add filters to a follow-up search when results are too broad
- Discover which metadata dimensions are most discriminating for your query
- Identify available Region, Frequency, or Source values within your current result set

## Common mistakes

- **Guessing Region codes:** "uk" is not a valid code ΓÇö use "gb". Always verify with `list_attribute_values`.
- **Guessing RegionKey values:** Discover them by inspecting `RegionKey` metadata on a representative search result rather than constructing a name by analogy.
- **Inventing attribute values:** If unsure, use `list_attribute_values` to check.
- **Treating identifiers as semantics:** an identifier string is not a reliable description of what a series measures. Read the metadata, not the name.

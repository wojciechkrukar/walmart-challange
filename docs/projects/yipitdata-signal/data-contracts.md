# Data Contracts — YipitData Signal Validation

> Source of truth for the two CSVs the Lead Quant is allowed to read. Any deviation from the
> hashes / schema below is a STOP-WORK condition (escalate to HITL).

## Provenance

Both CSVs were handed to the team in `challange_docs/`. They were copied verbatim into `data/`
at mission kickoff. The originals in `challange_docs/` remain immutable evidence of the source
state.

## Files

### `data/retail_sales_fred.csv`

| Property | Value |
|---|---|
| Source description | Monthly U.S. retail-sales index from FRED, series `RSXFS` |
| Schema | `date` (ISO YYYY-MM-DD, month-start), `value` (float) |
| Rows | 195 observations + header |
| Date range | `2010-01-01` → `2026-03-01` |
| SHA-256 | `332d0d032b5eb1580d0e24fe3b9213749d2cdbc8f5d1b3b3c126d518a38c5aa1` |
| Sampling | Monthly. The FRED `value` for month *m* is conventionally observed at the start of *m* in this file but is **released by FRED ~6 weeks after month-end**. Lag alignment must respect the release calendar — see `methodology.md` § "Publication-lag rule". |

### `data/walmart_revenue.csv`

| Property | Value |
|---|---|
| Source description | Walmart quarterly revenue (WMT, CIK `0000104169`), pulled from SEC EDGAR XBRL |
| Schema | `date` (ISO YYYY-MM-DD, fiscal-quarter-end), `value` (float, USD) |
| Rows | 65 observations + header |
| Date range | `2010-01-31` → `2026-01-31` |
| SHA-256 | `c116c39388b35c482512649bb0a25bd451989d34343432219fb5c83e67979502` |
| Notes | Walmart's fiscal year ends late January. The `date` field is the fiscal-quarter-end, **not** the SEC filing date. Walmart 10-Q for fiscal-Q3 is typically filed **~6 weeks after** quarter-end (mid-Q4). The notebook MUST treat each revenue row as available no earlier than `date + ~45 days` for any prediction logic. |

## Hard rules

1. The Lead Quant MUST verify the SHA-256 hashes at the top of `analysis.ipynb` (assert, don't print).
   If a hash mismatches, halt and escalate.
2. The Lead Quant MUST NOT mutate either CSV in place. All cleaning, resampling, and merging
   happens in-memory inside the notebook.
3. The Lead Quant MUST NOT call any external API. Hashes confirm the local files are the canonical inputs.
4. Any derived intermediate the team needs across runs goes in `runtime/benchmarks/` or
   `runtime/validation/`, never back into `data/`.

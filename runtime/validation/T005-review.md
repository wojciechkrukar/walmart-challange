# Review Report — T005

**Reviewer role:** Critical Reviewer  
**Artifact:** analysis.ipynb § 5 (cells 33–37, notebook code cells 33–36 + markdown cells)  
**Date:** 2026-05-13  
**Verdict:** REQUEST_CHANGES

---

## Anti-pattern audit

### 1. Look-ahead bias / data leakage — PASS

Cell 34 (execution count 36) fits OLS on sub-samples of `analysis_df`. No new features are
constructed in § 5; the section reuses `analysis_df` as built and validated in T003. The
sub-sample fits are pure retrospective fits on training data — no prediction is generated for a
future quarter, no release-date rule is invoked here. The `analysis_df` rows that enter Cell 34
were individually validated in T003 for publication-lag compliance. **No new leakage vectors
are introduced in § 5.**

Three spot-checks on `analysis_df` rows used in `X_pand` (the pandemic-only sub-sample, 5
quarters 2020-01-31 → 2021-01-31): each row's `rsxfs_yoy` value is the lag-aligned FRED
regressor produced by T003's `merge_asof` join with a `+45 day` tolerance. T003 was approved
in T003-review.md. ✓

### 2. Train/test contamination — PASS

§ 5 introduces no new OOS split. All OOS evaluation results are locked in
`runtime/benchmarks/oos_errors.json` (task T004, reviewed and approved 2026-05-13). Cells
33–36 read `oos_errors.json` and `baseline.json` as immutable artefacts. No observation
from the held-out OOS window is used to fit any model in this section. ✓

### 3. Improper time-series cross-validation — PASS

No `KFold`, `ShuffleSplit`, `StratifiedKFold`, `train_test_split(…, shuffle=True)`, or any
randomised splitter appears in § 5. No cross-validation is performed at all — the section
characterises the regime and reports locked OOS figures. ✓

### 4. In-sample metric reporting — PASS

Cell 34 (execution count 36) labels every metric with the explicit disavowal:

- Cell-level comment: `# This is an IN-SAMPLE sub-sample check, labelled clearly.`  
- Print header: `=== In-sample M1 fits by regime (IN-SAMPLE ONLY — NOT OOS RESULTS) ===`  
- Per-row suffix inside `fit_ols_report`: `in-sample R²={r2:.3f} [IN-SAMPLE ONLY — not a result]`

No in-sample R² is presented as a headline or used in a comparative claim. The `=== FINAL
METRICS SUMMARY ===` block in Cell 36 uses exclusively OOS quantities from `oos_errors.json`. ✓

### 5. Baseline omission — PASS (N/A for § 5)

§ 5 is a regime-characterisation and T004 MINOR correction exercise, not a new model
evaluation. No new "X beats Y" claim is introduced beyond the locked T004 results. Baseline
comparisons in Cell 36 load SNA APE values from `baseline.json` via inner join (not hardcoded),
consistent with T004's methodology. ✓

### 6. Structural-break blindness — PASS

This section IS the structural-break treatment. Cell 33 produces an annotated YoY plot with
the pandemic window shaded red (see `runtime/validation/fig_yoy_regime.png`). Cell 34
explicitly quantifies the OLS beta change across regimes. Cell 35 provides a 4-part prose
block explaining the mechanism. The full-sample vs excl-pandemic dual reporting (Cell 36)
enforces the methodology § 8 requirement. ✓

---

## T005-specific checks

### 1. Pandemic window consistency — PASS

Cell 33 (execution count 35) declares:
```python
PANDEMIC_START = pd.Timestamp("2020-01-31")
PANDEMIC_END   = pd.Timestamp("2021-01-31")
```
The plot shading uses `ax.axvspan(PANDEMIC_START, PANDEMIC_END, ...)` — no hardcoded alternative
dates. Cross-checked against stored artefacts:

| Artefact | `pandemic_window.start` | `pandemic_window.end` |
|---|---|---|
| `oos_errors.json` | 2020-01-31 | 2021-01-31 |
| `baseline.json` | 2020-01-31 | 2021-01-31 |
| Cell 33 code | 2020-01-31 | 2021-01-31 |
| Cell 34 `excl` mask | 2020-01-31 | 2021-01-31 |

All four sources agree exactly. The 5-quarter pandemic set (2020-01-31, 2020-04-30,
2020-07-31, 2020-10-31, 2021-01-31) is confirmed by inspecting both `oos_errors.json` and
`baseline.json` per_quarter tables. ✓

### 2. In-sample labelling — PASS

Confirmed above (Anti-pattern audit § 4). No Cell 34 metric is presented as an OOS result
anywhere in § 5. ✓

### 3. Falsifiable claim — FAIL → **MAJOR** (see Findings)

Cell 35 (execution count 37) prints a falsifiable claim that satisfies the structural
requirements (specific number, specific window, specific threshold):

> "beats the same-quarter-last-year seasonal-naive baseline by **0.74 pp** on out-of-sample
> MAPE (2.57% vs 3.31%) across 2015–2026"

> "The improvement widens slightly to **0.84 pp** (CI [+0.52 pp, +1.74 pp]) once the 5-quarter
> COVID disruption window (2020Q1–2021Q1) is excluded."

> Threshold: "If, on a fresh 8-quarter held-out window (2022–2023), the delta MAPE falls below
> 0 pp, we would downgrade the signal to 'inconclusive'."

However, the 0.74pp and 0.84pp figures are the **unmatched** deltas from T004
(`SNA_MAPE_n49 − M1_MAPE_n42` and `SNA_MAPE_n44 − M1_MAPE_n37`). Cell 36 — the very next
cell, introduced to resolve T004 MINOR-1 — demonstrates via inner join that the **aligned**
deltas are materially different:

| Cut | Claim (Cell 35) | Aligned (Cell 36) | Difference |
|---|---|---|---|
| Full-sample | 0.74 pp | **+1.07 pp** | +0.33 pp (+44%) |
| Excl-pandemic | 0.84 pp | **+1.17 pp** | +0.33 pp (+39%) |

Independently verified by `runtime/validation/_check_t005.py`:
```
Aligned delta (full-sample):    +1.0682 pp
Aligned delta (excl-pandemic):  +1.1711 pp
SNA MAPE (matched, full):       3.6413%  [vs claim's 3.31% — different window]
```

Cell 35's falsifiable claim is the output that flows into the memo (T006). If the memo is
drafted from Cell 35's output, it will carry the stale, mismatched figure (0.74pp). This is
an intra-§5 self-contradiction: the section's own Cell 36 proves 0.74pp is the wrong number,
yet Cell 35 — which comes first — encodes it as the headline. **This is a MAJOR.**

The CIs cited in Cell 35 ([+0.41pp, +1.65pp] and [+0.52pp, +1.74pp]) are correct — they are
loaded from `oos_errors.json` and match exactly.

### 4. No cherry-picking — PASS

Both full-sample and excl-pandemic cuts are reported in Cell 36 with n counts:

```
Matched OOS quarters: 42 (full) / 37 (excl pandemic)
```

The pandemic window is defined from pre-specified constants `PANDEMIC_START` / `PANDEMIC_END`,
not a dynamically chosen interval. The 2020Q1–2021Q1 definition matches the pre-specified
window in `oos_errors.json` from T004 (not chosen post-hoc to improve results in T005). ✓

### 5. Causal language — PASS (with NIT noted)

Cell 35 does not use "causes" anywhere. Acceptable hedged language confirmed:

- "plausible mechanism" ✓  
- "RSXFS co-moves with Walmart" ✓  
- "the lag structure makes it 'leading' in a useful sense" (scare-quoted, hedged) ✓  
- "this co-movement may be a common-factor artifact, not a true causal lead" ✓  
- "not a true causal lead" ✓

The opening phrase "RSXFS leads Walmart revenue in two interrelated ways" is immediately
disambiguated as a publication-timing observation (item (a) = RSXFS released before Walmart
10-Q), not a Granger-causal claim. Acceptable. ✓

NIT: Task Brief specifies a "short prose block (3–6 sentences)." Cell 35's block contains
four numbered sections totalling ~25–30 sentences. While the content quality is high, it
exceeds the spec. Left as a NIT; memo condensation is T006 scope.

### 6. Aligned delta consistency — PASS

Independently recomputed from raw JSON files (`_check_t005.py`):

| Check | Expected | Actual | Match |
|---|---|---|---|
| Matched quarters (full) | 42 | 42 | ✓ |
| Matched quarters (excl pandemic) | 37 | 37 | ✓ |
| SNA MAPE (42 matched, full) | ~3.64% | 3.6413% | ✓ |
| Aligned delta (full) | ~+1.07pp | +1.0682pp | ✓ |
| Aligned delta (excl pandemic) | ~+1.17pp | +1.1711pp | ✓ |
| Bootstrap CI full | [+0.41pp, +1.65pp] | [+0.41pp, +1.65pp] | ✓ |
| Bootstrap CI excl | [+0.52pp, +1.74pp] | [+0.52pp, +1.74pp] | ✓ |

The inner join correctly matches all 42 OOS quarters (2015-10-31 → 2026-01-31) to their
corresponding SNA APE in `baseline.json`. Bootstrap CIs are loaded from `oos_errors.json`,
not recomputed — correct. The SNA MAPE over 42 matched quarters (3.64%) is higher than the
unmatched 3.31% (over 49 quarters) because the 7 pre-OOS baseline quarters
(2014-Q1 → 2015-Q3) had below-average SNA errors (confirmed: T004 MINOR-1 analysis). ✓

---

## Findings

### BLOCKERs
None.

### MAJORs

**MAJOR-1 — Falsifiable headline claim cites stale unmatched delta (Cell 35 vs Cell 36 self-contradiction)**

Cell 35's printed falsifiable claim states 0.74pp (full) and 0.84pp (excl-pandemic) as the
FRED–SNA MAPE deltas. Cell 36, introduced specifically to resolve T004 MINOR-1 (mismatched
evaluation windows), computes the aligned deltas as +1.07pp and +1.17pp respectively — values
that are 39–44% larger than the Cell 35 claim.

Since Cell 35 precedes Cell 36 in the notebook, its output is what the memo author (T006) will
read first. The memo will therefore be drafted from the wrong, mismatched figure unless the
Lead Quant explicitly overrides Cell 35.

**Smallest fix (deterministic next step):**  
In Cell 35's `causal_text` string, update the two delta figures and the SNA MAPE reference
to use the aligned values:

```python
# Change this in causal_text:
# "beats the same-quarter-last-year seasonal-naive baseline by 0.74 pp on out-of-sample
#  MAPE (2.57% vs 3.31%)"
# "The improvement widens slightly to 0.84 pp"

# To:
# "beats the same-quarter-last-year seasonal-naive baseline by 1.07 pp on out-of-sample
#  MAPE (2.57% vs 3.64%, evaluated on the 42 matched OOS quarters)"
# "The improvement widens slightly to 1.17 pp"
```

The CIs ([+0.41pp, +1.65pp] and [+0.52pp, +1.74pp]) are correct and need no change.

Alternatively, restructure Cell 35 to execute *after* Cell 36 and reference `aligned_full_delta`
and `aligned_excl_delta` programmatically rather than via hardcoded strings — eliminating the
possibility of future drift.

### MINORs

None (the causal block length excess is a NIT, not a MINOR; it does not affect correctness or
the memo headline).

### NITs

**NIT-1 — Causal "why" block exceeds spec length**  
Task Brief: "A short prose block (3–6 sentences)." Cell 35's block has ~25–30 sentences across
four numbered sections. Condensation is appropriate for T006 memo drafting, not a fix required
here.

---

## Acceptance-criteria checklist (from T005 Task Brief)

- [x] One annotated YoY plot with 2020Q1–2021Q1 shaded — **PASS**  
  (`fig_yoy_regime.png` saved; `ax.axvspan(PANDEMIC_START, PANDEMIC_END)` confirmed.)

- [x] Sub-sample fit excluding the regime, reported alongside full-sample — **PASS**  
  (Cell 34 fits M1 on full, non-pandemic, and pandemic-only sub-samples with clear in-sample
  labelling.)

- [ ] Short prose block (3–6 sentences) on causal "why" — **PARTIAL (NIT)**  
  (Content satisfies the three required elements — mechanism, common-factor risk, 2020
  breakdown explanation — but is ~5× the specified length.)

- [ ] Falsifiable headline claim with specific number, window, and threshold — **FAIL (MAJOR-1)**  
  (Present, but the specific number (0.74pp) contradicts the aligned computation in Cell 36.)

- [x] Reviewer's anti-pattern audit filed in `runtime/validation/T005-review.md` — **PASS**  
  (This document.)

---

## Summary

§ 5 is structurally sound. The regime treatment is thorough: pandemic shading matches the
pre-specified T004 window exactly; all in-sample fits are explicitly labelled; causal language
is properly hedged; the aligned delta computation in Cell 36 is arithmetically correct.

One MAJOR blocks approval: the falsifiable headline claim in Cell 35 carries the pre-fix,
mismatched delta (0.74pp / 0.84pp) that Cell 36 corrects to +1.07pp / +1.17pp. The claim
is self-consistent within § 5 only if a reader infers that Cell 36 supersedes Cell 35 —
which is not stated. The memo (T006) will be drafted from Cell 35's output. This
self-contradiction must be resolved before T006 begins.

**Verdict: REQUEST_CHANGES**  
One deterministic fix required: update the delta figures in Cell 35's `causal_text` string
to use the aligned values (+1.07pp full, +1.17pp excl-pandemic, SNA MAPE 3.64% on 42 matched
quarters). CIs and threshold remain correct. After this single edit, § 5 may be re-submitted
for a rapid re-review.

---

## Re-Review (MAJOR-1 Fix)

**Date:** 2026-05-13  
**Verdict change:** REQUEST_CHANGES → APPROVE

### MAJOR-1 resolution

Cell 35's `causal_text` item 4 ("Falsifiable headline claim") has been updated. The new text
reads verbatim:

> FRED RSXFS YoY growth, lagged one publication cycle and aligned to Walmart fiscal quarters,
> beats the same-quarter-last-year seasonal-naive baseline by 1.07 pp on out-of-sample MAPE
> (2.57% vs 3.64%, SN-A over matched 42-quarter OOS window) across 2015–2026, with a 95%
> bootstrap CI of [+0.41 pp, +1.65 pp].
> The improvement widens slightly to 1.17 pp (CI [+0.52 pp, +1.74 pp]) once the 5-quarter
> COVID disruption window (2020Q1–2021Q1) is excluded.
> (The 1.07 pp figure uses SN-A MAPE over the same 42 matched OOS quarters as M1;
> the raw T004 delta of 0.74 pp compared unmatched windows and understates the improvement.)

All four required elements are now present and correct:

| Required | Present | Value |
|---|---|---|
| Full-sample delta | ✓ | **1.07 pp** (was 0.74 pp) |
| Baseline MAPE (matched window) | ✓ | **3.64%** (was 3.31%) |
| Excl-pandemic delta | ✓ | **1.17 pp** (was 0.84 pp) |
| Clarifying note on 42 matched quarters | ✓ | Parenthetical in item 4 |

Cross-check against `_check_t005.py` output (unchanged from initial review):
- Aligned delta (full-sample): +1.0682 pp → rounds to **1.07 pp** ✓
- Aligned delta (excl-pandemic): +1.1711 pp → rounds to **1.17 pp** ✓
- SNA MAPE (42 matched quarters): 3.6413% → rounds to **3.64%** ✓

Bootstrap CIs ([+0.41 pp, +1.65 pp] and [+0.52 pp, +1.74 pp]) are unchanged — they were
correct in the prior version and remain correct. The falsification threshold
("If, on a fresh 8-quarter held-out window (2022–2023), the delta MAPE falls below 0 pp,
we would downgrade the signal to 'inconclusive'") is unchanged and remains correct.

The intra-§5 self-contradiction is resolved: Cell 35's printed claim now matches the aligned
computation in Cell 36 exactly.

### Side-effect scan

`git diff --name-only` confirms **only `analysis.ipynb` was modified** — no runtime artefacts
(`oos_errors.json`, `baseline.json`), no benchmark files, no other notebooks or scripts.

Cell-by-cell spot-check for accidental collateral edits:

| Cells | Verification method | Result |
|---|---|---|
| Cells 1–34 (notebook items 1–34) | Execution counts and line ranges unchanged per notebook summary | ✓ Untouched |
| Cell 35 (lines 1140–1199) | Read in full — only `causal_text` string updated; `print(causal_text)` call unchanged | ✓ Fix only |
| Cell 36 (lines 1202–1247) | Read in full — computation code (`aligned_full_delta`, `aligned_excl_delta`, inner join, all print statements) unchanged | ✓ Untouched |
| Cell 37 / markdown (lines 1250–1257) | Read in full — `§ 5 Complete` summary block unchanged | ✓ Untouched |

No new logic, imports, variable assignments, or structural changes were introduced. The edit
is a pure string-literal correction confined to `causal_text` in Cell 35.

NIT-1 (causal block length ~25–30 sentences vs spec 3–6) is still present and still NIT-grade;
it was not introduced by this edit and does not affect correctness.

**Verdict: APPROVE**  
T005 § 5 is approved. T006 (memo and prompts log) may proceed. The memo headline figure must
use **1.07 pp** (full-sample, 42 matched OOS quarters, 2015–2026).

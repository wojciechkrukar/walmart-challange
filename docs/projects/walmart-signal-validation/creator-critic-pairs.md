# Creator–Critic Pairs — walmart-signal-validation

The kernel mandates that every Worker output is reviewed by a designated Critic before reaching a Phase exit gate. For this Mission the pairing is fixed: **Lead Quant** is the Creator and **Critical Reviewer** is the Critic.

## Phase-by-Phase pairing

| Phase | Creator artifact | Critic adversarial probe |
|-------|------------------|--------------------------|
| P1 — Ingest | Loaded DataFrames + dtype + date-range summary | Verify both CSVs are read with correct date parsing; assert no NaN in revenue series; verify FRED is monthly + Walmart is quarterly |
| P2 — Baseline | `baseline_predictions`, `baseline_mape`, `baseline_rmse` | Verify mean YoY is computed on the *training window only* in the rolling-CV harness; verify `Q(t-4)` lookup uses the index, not a positional shift that could wrap |
| P3 — Signal | OLS `summary()` + feature list | Verify all features are constructed from data ≤ Q(t-1); verify `add_constant` is applied; verify in-sample R² is *not* used as the verdict metric |
| P4 — Rolling CV | `cv_predictions` + sub-period MAPEs | Verify training window grows monotonically; verify no test row leaks into the fit; verify MAPE is computed on actuals, not log-actuals; verify the verdict cell quotes OOS metrics, not in-sample |
| P5 — COVID audit | Structural-break section in notebook | Verify the COVID window is named explicitly (2020-Q1 → 2021-Q1); verify sub-period metrics are reported separately; verify no smoothing across the break |
| P6 — Memo | `memo.md` draft | Verify zero causal claims; verify the headline matches the OOS verdict; verify the memo discloses the COVID caveat |

## Critic veto power

The Critical Reviewer can veto any Phase exit by writing one entry into `guardrail_violations` in the shared state. The Director MUST NOT advance to the next Phase while `guardrail_violations` is non-empty.

## Scoring rubric

After each review the Critical Reviewer emits `critic_score ∈ [0, 1]`:

| Score range | Meaning | Director action |
|-------------|---------|-----------------|
| 0.85 – 1.00 | Clean — no defects | Advance to next Phase |
| 0.65 – 0.85 | Minor issues, fixable | Send back to Lead Quant with critique; do not advance |
| 0.40 – 0.65 | Serious defect — guardrail at risk | Send back; if same defect persists for 2 cycles, escalate |
| < 0.40 | Mission-critical violation | Halt Mission; HITL review required |

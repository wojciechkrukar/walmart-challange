# Challenge Brief — YipitData AI Engineer Take-Home

> Restated from `challange_docs/take_home_exam_candidate.{md,docx,pdf}`.
> The three formats are **content-identical** (verified by line-by-line diff and PDF
> text-extraction); only formatting differs. See [`caveats-and-discrepancies.md`](caveats-and-discrepancies.md).

## The customer's question (verbatim)

> "We track the monthly retail-sales series from FRED for our subsector. We are thinking about
> using it as a leading indicator of quarterly revenue for Walmart. Does it predict Walmart's
> revenue better than a naive baseline? If yes, by how much, and what should we worry about?
> If no, what evidence would change our minds?"

## What we send back (deliverables)

| Artifact | Owner (per `docs/team/roles.md`) | Audience | Constraints |
|---|---|---|---|
| `analysis.ipynb` | Lead Quant | Reviewer + HITL | Runs end-to-end without errors from a fresh kernel |
| `memo.md`        | Lead Quant (drafts) → Director (polishes) | Portfolio manager who took stats in college | One printed page; frame the question, give the answer, list worries |
| `prompts.md`     | Director | YipitData reviewer | Chronological prompt log + < 200-word reflection on what the assistant got right, where it was pushed back on, and how its output was checked |

## Time budget

The challenge sets a soft cap of 4 hours and a hard cap of 6 hours of human time.
For the agentic team, this translates to: **be ruthless about scope; one or two well-executed
models, not ten messy ones.**

## Mission-directive guardrails (binding for every Task)

These come from the orchestration mission directive and override anything in the original brief
that conflicts:

1. **No APIs.** The Lead Quant uses ONLY local files in `data/`:
   - `data/retail_sales_fred.csv`
   - `data/walmart_revenue.csv`
2. **Baseline imperative.** The Seasonal Naive Baseline (e.g., `Q(t) = Q(t-4) + average growth`)
   is built **before** any alternative model. The headline answer is whether the FRED signal
   beats this baseline OOS.
3. **Zero look-ahead.** Walmart Q3 revenue is reported in mid-Q4; FRED RSXFS for month *m* is
   typically released ~1.5 months after *m* ends. Predictions for quarter Q may use only data
   that was physically published before quarter Q starts.
4. **Out-of-sample only.** Strict forward-rolling time-series cross-validation. No randomised
   K-fold. No in-sample R² as the success metric. OOS MAPE and/or RMSE are the headline metrics.
5. **Causal reasoning + structural breaks.** The 2020 COVID period is treated as a structural
   break — not averaged over silently. The memo and notebook explicitly address regimes where
   the relationship strengthens / breaks down.

## What "good" looks like (from the brief)

A solid submission:
- picks a real baseline and beats it, or honestly says it didn't;
- runs the test out of sample with a proper time-series split;
- states caveats out loud, not in footnotes;
- uses one or two clean figures, not ten messy ones;
- runs end-to-end without errors.

A great submission also:
- says something non-obvious about *when* the signal works and when it doesn't;
- shows one or two places where the LLM got something subtly wrong and the human caught it;
- lands on a clear, falsifiable claim (e.g., "the signal beats the seasonal-naive baseline by
  X% on out-of-sample MAPE, but only outside recession periods").

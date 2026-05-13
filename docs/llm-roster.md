# LLM Roster — YipitData Signal Validation

> Authoritative tier matrix for the three personas. The mission directive specifies the Tier-1
> profile for each role; Tier-2 and Tier-3 are project defaults chosen for cost / offline
> reproducibility.

## Tier semantics

| Tier  | Env value         | Use case                                                    |
|-------|-------------------|-------------------------------------------------------------|
| tier1 | `LLM_TIER=tier1`  | Production-grade run; full capability per the directive     |
| tier2 | `LLM_TIER=tier2`  | Cost-optimised dev iteration                                |
| tier3 | `LLM_TIER=tier3`  | CI / offline — deterministic stubs, no network calls (default in CI) |

Default in CI: `LLM_TIER=tier3`.

## Role matrix

| Role                      | Tier 1 (per directive)            | Tier 2                | Tier 3 (deterministic)        |
|---------------------------|------------------------------------|-----------------------|-------------------------------|
| Director (Orchestrator)  | **GPT-4o**                         | GPT-5.4               | DeterministicDirectorStub     |
| Lead Quant (Generator)   | **Claude 3.5 Sonnet**              | Claude Haiku 3.5      | DeterministicQuantStub        |
| Critical Reviewer (Adversary) | **OpenAI o1** (deep reasoning) | GPT-4o                | DeterministicReviewerStub     |

## Rationale (from the mission directive, restated)

- **GPT-4o for Director.** Strong instruction-following, structured-output reliability, and the
  best price/latency profile for an orchestrator that mostly routes work and writes short
  status updates rather than producing long-form analysis itself.
- **Claude 3.5 Sonnet for Lead Quant.** Mission directive explicitly cites its "superior
  coding and data-science capabilities." The Lead Quant must produce clean, modular Pandas code
  with in-line statistical reasoning — Sonnet's verbosity-with-substance is a fit.
- **OpenAI o1 for Critical Reviewer.** Mission directive explicitly cites deep chain-of-thought
  reasoning. The Reviewer's job — hunting look-ahead bias, leakage, and improper CV — is a
  reasoning task more than a writing task.

## Fallback semantics

1. If the Tier-1 provider key is missing or returns 4xx, the resolver falls back to Tier-2 and
   logs a structured warning to `runtime/logs/`.
2. If Tier-2 also fails, the resolver falls back to Tier-3 (deterministic stub) and appends to
   `MissionState.errors`.
3. No silent degradation — every fallback is logged.

## Override knobs

- Global: `LLM_TIER=tier1|tier2|tier3` in `.env` (gitignored).
- Per-role: `get_llm(role="lead_quant", tier_override="tier2")`.
- Test: `LLM_TIER=tier3` is always used in CI; stubs return deterministic fixtures.

## Forbidden providers (security / cost-control)

- Any LLM provider not listed in this roster requires a PR that updates this file AND human
  approval before being added to `llm_factory`.
- API keys are never committed. `.env` is gitignored. Only `.env.example` is allowed in version
  control (when introduced).

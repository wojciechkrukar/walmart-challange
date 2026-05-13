# LLM Roster

> Authoritative per-role model assignment for the walmart-signal-validation Mission. Modelled after the kernel's `llm-roster.md` pattern. Modifying this file is a Class E PR (HITL approval required).

## Tier semantics

| Tier | Env value | Use case |
|------|-----------|----------|
| tier1 | `LLM_TIER=tier1` | Production / human-supervised — full capability |
| tier2 | `LLM_TIER=tier2` | Cost-optimised iteration |
| tier3 | `LLM_TIER=tier3` | Offline / CI — deterministic stubs, no network |

Default for any CI run: `LLM_TIER=tier3`.

## Role matrix (active roles for this Mission)

| Role | Tier 1 | Tier 2 | Tier 3 | Active in Phases |
|------|--------|--------|--------|------------------|
| Director (Orchestrator) | Claude Opus 4.7 | GPT-5.5 | Gemini 3 Pro | All |
| Lead Quant (Generator) | Claude Opus 4.7 | GPT-5.5 | DeepSeek V3.2 | P1, P2, P3, P4, P6 |
| Critical Reviewer (Critic) | Claude Opus 4.6 | GPT-5.5 | DeepSeek R1 | All |

## Inactive roles (documented for kernel completeness)

The full kernel matrix in `wojciechkrukar/agentic-workforce-kernel` defines additional roles (Implementer, Reviewer, Triage, Delivery, Vision Specialist, Dataset Curator, Eval Engineer, QA Tester) that are NOT activated for this single-notebook Mission. Their tier assignments would be inherited from the kernel default if a future Mission needs them.

## Fallback semantics

1. If the Tier-1 provider is unavailable, the Director drops the affected agent to Tier 2 and logs a warning to `runtime/logs/`.
2. If Tier 2 also fails, Tier 3 is used and `errors` is appended in the shared state.
3. **Critical Reviewer never falls back to a stub for adversarial probes.** If Tier 2 is unavailable, the Mission halts and the Director escalates to HITL.

## Override knobs

- Global: `LLM_TIER=tier1|tier2|tier3` in `.env`.
- Per-role: not supported in this Mission — the matrix is fixed because the same models drove the prototype validation.

## Rationale

### Director — Claude Opus 4.7

- Strongest published agentic-orchestration capability (SWE-bench Verified, Tau-bench, Aider Polyglot, 2025–2026).
- Reliably follows long, dense rule sets without drift — critical because this Mission has eight hard guardrails.
- Best-in-class at decomposing ambiguous human briefs into bounded Task contracts.

### Lead Quant — Claude Opus 4.7

- Top model on data-science authoring with embedded statistical justification (Aider Polyglot, MMLU-Pro Quantitative).
- Strongest at producing *clean, modular* pandas / statsmodels / matplotlib code — the Lead Quant deliverable is judged as much on code quality as on numerical results.
- GPT-5.5 (Tier 2) is a near-equivalent fallback; DeepSeek V3.2 (Tier 3) preserves quality on the OSS / offline path.

### Critical Reviewer — Claude Opus 4.6

- Deliberately a *different* model from the Lead Quant (4.6 vs. 4.7) so that systematic blind-spots in the Generator are not echoed by the Critic. This is a kernel-recommended pattern (see lex-triage-agent's Reviewer / Critic distinction: Opus 4.6 vs. Opus 4.7).
- Top model on adversarial code review, counterfactual reasoning, and formal-statistics scrutiny (GPQA Diamond, ARC-AGI-2 reasoning, Aider Refactor benchmark).
- DeepSeek R1's chain-of-thought reasoning makes it the best published OSS critic for offline runs.

### Why not GPT-5.5 for the Lead Quant?

GPT-5.5 is comparable on raw coding metrics, but Anthropic's models lead on *long-instruction adherence* — and this Mission's instruction set is dense (eight guardrails, six Phase contracts, no-API constraint, COVID protocol). The marginal capability gain is judged worth the risk of single-vendor dependence; Tier 2 explicitly mitigates by switching to GPT-5.5 if Anthropic is unavailable.

### Why a different LLM for the Critic vs. the Generator?

A Critic that shares the Generator's blind spots is functionally a yes-bot. The kernel's review policy treats this as a hard requirement: the model used by a Critic MUST differ from the model used by the Generator it reviews. We satisfy this with Opus 4.6 / 4.7. (A future iteration could go further and pair Opus-Generator with GPT-5.5-Critic for stronger cross-vendor diversity.)

## Parity contract

If a future iteration introduces an `llm_factory` module, a parity test MUST verify that this file and the module's `ROLE_TIER_MATRIX` constant are byte-identical. This mirrors the kernel pattern in `wojciechkrukar/lex-triage-agent`.

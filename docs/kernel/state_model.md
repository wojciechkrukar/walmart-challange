<!--
Vendored from agentic-workforce-kernel @ main.
Do not edit — update by re-vendoring from the source repo.
-->

# State Model

Each project defines a concrete `MissionState` schema in `docs/projects/<project>/architecture.md`.
The kernel mandates the following minimum keys:

```python
class MissionState(TypedDict):
    # Identity
    mission_id: str
    task_id: str | None

    # Inputs
    inputs: dict                       # paths or values supplied by HITL

    # Worker outputs (Generator)
    artifacts: dict                    # primary results — file paths, dataframes, metrics

    # Critic outputs
    critique: str | None
    critic_score: float | None         # 0–1 confidence in Worker output
    guardrail_violations: list[str]    # populated by Critic; non-empty → immediate halt

    # HITL
    hitl_required: bool
    human_decision: str | None         # approve | reject | reclassify | abort
    human_notes: str | None

    # Telemetry
    total_cost_usd: float
    total_latency_ms: int
    model_calls: list[dict]            # [{role, model, cost_usd, latency_ms}]

    # Errors
    errors: list[str]
```

## LLM tier contract

| Tier | Env value | Resolver behaviour |
|------|-----------|-------------------|
| tier1 | `LLM_TIER=tier1` | Full-capability models — production / human-supervised dev |
| tier2 | `LLM_TIER=tier2` | Cost-optimised models — internal iteration |
| tier3 | `LLM_TIER=tier3` | Deterministic stubs — no network calls (CI default) |

All tier resolution happens in a single `llm_factory` module (one per project).
Worker / Critic code MUST NOT import provider SDKs directly.

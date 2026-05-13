<!--
Vendored from agentic-workforce-kernel @ main.
Do not edit — update by re-vendoring from the source repo.
-->

# State Model

## MissionState

The shared state object every agent reads from and writes to.

```python
class MissionState(TypedDict):
    # Identity
    mission_id: str
    title: str
    objective: str

    # Lifecycle
    status: str             # PENDING | PENDING_HITL_CLEARANCE | IN_PROGRESS | REVIEW | DONE | ESCALATED | ABORTED
    owner: str              # current responsible agent role
    blockers: list[str]

    # Work breakdown
    tasks: list[dict]       # see task_contracts.md schema
    open_task_ids: list[str]
    done_task_ids: list[str]

    # HITL
    hitl_required: bool
    hitl_decision: str | None       # "approve" | "reject" | "modify"
    hitl_notes: str | None
    hitl_decision_at: str | None    # ISO-8601

    # Telemetry
    total_cost_usd: float
    total_latency_ms: int
    model_calls: list[dict]         # [{role, task_id, model, cost_usd, latency_ms}]

    # Errors
    errors: list[str]
```

## LLM tier contract

| Tier  | Env value         | Resolver behaviour                                          |
|-------|-------------------|-------------------------------------------------------------|
| tier1 | `LLM_TIER=tier1`  | Full-capability models per `docs/llm-roster.md`             |
| tier2 | `LLM_TIER=tier2`  | Cost-optimised models                                       |
| tier3 | `LLM_TIER=tier3`  | Deterministic stubs — no network calls (default in CI)      |

Tier resolution happens in a single `llm_factory` module per project. Worker agent code MUST
NOT import provider SDKs directly.

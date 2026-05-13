# GitHub Flow — YipitData Signal Validation

## Core rules

1. **Never push to `main` directly.** All changes go through a PR.
2. **One Task Brief per PR.** A PR must reference exactly one Task ID from `todos/`.
3. **CI must be green before merge.** When a notebook smoke-test workflow is added, no exceptions.
4. **Squash merge** feature branches to keep `main` history clean.
5. **The Director is the only role that opens PRs.** Workers commit to feature branches; Director rolls them up.

## Branch lifecycle

```
main
 └─ copilot/<orchestration-slug>      ← initial scaffolding (this PR)
 └─ task/T<NNN>-<slug>                 ← created per Task Brief
     └─ commits authored by the assigned Worker
     └─ PR opened → Reviewer audit → Director sign-off → HITL clearance → merged → branch deleted
```

## PR checklist

- [ ] PR class declared (A–E per `docs/team/review_policy.md`)
- [ ] Linked Task Brief (`todos/T<NNN>-*.md`)
- [ ] Task Completion Report attached as a PR comment
- [ ] Review Report attached as a PR comment (verdict + anti-pattern audit)
- [ ] Notebook Restart-and-Run-All passes (for Class B–E)
- [ ] No new files outside the paths in `docs/team/collaboration.md` § "Who touches what"
- [ ] No API keys or secrets committed (`.env` files are gitignored)

## Submission flow

1. Director confirms all milestone exit criteria are met (`docs/delivery_kpis.md`).
2. Critical Reviewer issues APPROVE on the final submission bundle (Class E).
3. Director updates `runtime/agent_handoffs/current_mission.md` to `STATUS: REVIEW`.
4. Director requests HITL clearance.
5. HITL appends `HITL_DECISION: approve` and the Director marks the mission `DONE`.
6. Director writes `runtime/run_reports/<date>-yipitdata-signal.md`.

## Commit message convention

Conventional Commits:
- `feat:` — new analytical capability
- `fix:` — bug fix in modelling code
- `docs:` — documentation change
- `chore:` — build, CI, scaffolding, or maintenance change
- `refactor:` — code restructuring without behaviour change

Recommended scope: agent role or Task ID — `feat(T002): seasonal naive baseline`.

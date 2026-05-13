# Kernel Governance Docs

> Vendored from `wojciechkrukar/agentic-workforce-kernel`.
> These docs define the universal operating contract for every agentic system built on the kernel.
> Treat this directory as **READ-ONLY**. Project-specific extensions live in `docs/team/`.

| Doc | Purpose |
|-----|---------|
| [director_protocol.md](director_protocol.md) | How the Director agent orchestrates Tasks |
| [task_contracts.md](task_contracts.md)       | Schema and lifecycle of a Task object |
| [escalation_matrix.md](escalation_matrix.md) | When and how agents escalate to humans |
| [review_policy.md](review_policy.md)         | Code and output review requirements |
| [state_model.md](state_model.md)             | Shared state schema across agents |
| [command_grammar.md](command_grammar.md)     | DSL for inter-agent commands |

To update any file in this directory, vendor a new version from the kernel repo at a pinned
SHA, prefix the commit message `chore: vendor kernel @ <sha>`, and require a human approver.

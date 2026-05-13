# `.agent/` — System Prompts & Role Cards

> Short-form system prompts for the three personas. The authoritative long-form role definitions
> live in [`../docs/team/roles.md`](../docs/team/roles.md). When the two disagree, the long-form
> doc wins and this directory must be updated to match.

| File | Persona | Tier-1 LLM (per `docs/llm-roster.md`) |
|---|---|---|
| [`director.md`](director.md)                       | The Director (Orchestrator) | GPT-4o |
| [`lead_quant.md`](lead_quant.md)                   | The Lead Quant (Generator)  | Claude 3.5 Sonnet |
| [`critical_reviewer.md`](critical_reviewer.md)     | The Critical Reviewer (Adversary) | OpenAI o1 |

## Loading conventions

Each role card is structured as:

```
## Identity
## Mission
## Scope and forbidden actions
## Operating contract
## Output format
```

Agent runtimes (LangGraph, CrewAI, OpenAI Assistants, etc.) load these as the system message
for the corresponding persona. The role cards intentionally cite the project docs rather than
repeating them, so the source of truth stays in `docs/`.

---
name: agent-architecture-audit
description: Audit the architecture and health of any AI agent system or LLM-integrated project. Uses the agchk Python library (agchk.report.v1) for structured reports with severity-ranked findings and code-first fix plans.
origin: https://github.com/huangrichao2020/agchk
---

# Agent Architecture Audit

Audit the architecture and health of any AI agent system or LLM-integrated project.

**The base model rarely fails. The wrapper architecture corrupts good answers into bad behavior.**

## When to Use

- An AI agent behaves worse than the base model via direct API
- The agent hallucinates, skips required tools, or reuses stale context
- "Must use tool X" is in the prompt but the model answers without calling it
- Old topics leak into new conversations
- Internal logs show correct answers but users see broken output
- Cost spikes with no visible output (runaway loops)

## Quick Start

```bash
pip install agchk
agchk /path/to/your/agent/project
```

Produces `audit_results.json` and `audit_report.md`.

## The 12-Layer Stack

| # | Layer | What Goes Wrong |
|---|-------|----------------|
| 1 | System prompt | Conflicting instructions, instruction bloat |
| 2 | Session history | Stale context from previous turns |
| 3 | Long-term memory | Pollution across sessions |
| 4 | Distillation | Compressed artifacts re-entering as pseudo-facts |
| 5 | Active recall | Redundant re-summary layers wasting context |
| 6 | Tool selection | Wrong tool routing, model skips required tools |
| 7 | Tool execution | Hallucinated execution — claims to call but doesn't |
| 8 | Tool interpretation | Misread or ignored tool output |
| 9 | Answer shaping | Format corruption in final response |
| 10 | Platform rendering | UI/API/CLI mutates valid answers |
| 11 | Hidden repair loops | Silent fallback/retry agents running second LLM pass |
| 12 | Persistence | Expired state or cached artifacts reused as live evidence |

## Audit Scanners

| # | Scanner | Severity | What It Catches |
|---|---------|----------|-----------------|
| 1 | Hardcoded Secrets | critical | API keys, tokens, credentials in source code |
| 2 | Tool Enforcement Gap | high | "Must use tool X" in prompt but no code validation |
| 3 | Hidden LLM Calls | high | Secret second-pass LLM calls in fallback/repair loops |
| 4 | Unrestricted Code Execution | critical | exec(), eval(), subprocess(shell=True) without sandbox |
| 5 | Memory Pattern Issues | medium | Unbounded context growth, missing TTL |
| 6 | Output Pipeline Mutation | medium | Response transformation corrupting correct answers |
| 7 | Missing Observability | medium | No tracing, logging, or cost tracking |

## Severity Model

| Level | Meaning |
|-------|---------|
| `critical` | Agent can confidently produce wrong operational behavior |
| `high` | Agent frequently degrades correctness or stability |
| `medium` | Correctness usually survives but output is fragile or wasteful |
| `low` | Mostly cosmetic or maintainability issues |

## Fix Strategy

Default fix order (code-first, not prompt-first):

1. **Code-gate tool requirements** — enforce in code, not just prompt text
2. **Remove or narrow hidden repair agents** — make fallback explicit with contracts
3. **Reduce context duplication** — same info through prompt + history + memory + distillation
4. **Tighten memory admission** — user corrections > agent assertions
5. **Tighten distillation triggers** — don't compress what shouldn't be compressed
6. **Reduce rendering mutation** — pass-through, don't transform
7. **Convert to typed JSON envelopes** — structured internal flow, not freeform prose

## Report Schema

Reports follow a formal JSON Schema (see `references/report-schema.json`) with:
- `overall_health`: critical_risk | high_risk | medium_risk | low_risk
- `findings`: array of severity-ranked issues with evidence refs
- `ordered_fix_plan`: prioritized fix steps with rationale

## Anti-Patterns to Avoid

- ❌ Saying "the model is weak" without falsifying the wrapper first
- ❌ Saying "memory is bad" without showing the contamination path
- ❌ Letting a clean current state erase a dirty historical incident
- ❌ Treating markdown prose as a trustworthy internal protocol
- ❌ Accepting "must use tool" in prompt text when code never enforces it

## Related

- GitHub: https://github.com/huangrichao2020/agchk
- PyPI: https://pypi.org/project/agchk/

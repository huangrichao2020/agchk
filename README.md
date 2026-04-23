# agchk

Audit the architecture and health of any AI agent system or LLM-integrated project.

**The base model rarely fails. The wrapper architecture corrupts good answers into bad behavior.**

```bash
pip install agchk
agchk /path/to/your/agent/project
```

## What It Does

`agchk` scans any Python/TypeScript/JavaScript codebase for 7 categories of agent architecture failures:

| # | Scanner | Severity | What It Catches |
|---|---------|----------|-----------------|
| 1 | Hardcoded Secrets | critical | API keys, tokens, credentials in source code |
| 2 | Tool Enforcement Gap | high | "Must use tool X" in prompt but no code validation |
| 3 | Hidden LLM Calls | high | Secret second-pass LLM calls in fallback/repair loops |
| 4 | Unrestricted Code Execution | critical | exec(), eval(), subprocess(shell=True) without sandbox |
| 5 | Memory Pattern Issues | medium | Unbounded context growth, missing TTL, no retention policy |
| 6 | Output Pipeline Mutation | medium | Response transformation corrupting correct answers |
| 7 | Missing Observability | medium | No tracing, logging, or cost tracking |

## Quick Start

```bash
# Install
pip install agchk

# Audit any agent project
agchk /path/to/your/langchain/project

# Generate human-readable report
agchk --report audit_results.json
```

## Python API

```python
from agchk import run_audit, generate_report

# Run full audit
results = run_audit("/path/to/your/agent/project")

# Generate markdown report
markdown = generate_report(results)

# Save to file
generate_report(results, output_file="audit_report.md")

# Validate results against JSON schema
from agchk.schema import validate_report
errors = validate_report(results)
```

## Programmatic Scanner Access

```python
from agchk.scanners import scan_secrets, scan_code_execution
from pathlib import Path

findings = scan_secrets(Path("/path/to/project"))
for f in findings:
    print(f"[{f['severity'].upper()}] {f['title']} at {f['evidence_refs']}")
```

## Example Output

```
🔍 Agent Architecture Audit
   Target: /Users/me/projects/my-agent
   Started: 2026-04-24 14:32:01

  Scanning: Hardcoded Secrets...
  Scanning: Tool Enforcement Gap...
  Scanning: Hidden LLM Calls...
  Scanning: Unrestricted Code Execution...
  Scanning: Memory Pattern Issues...
  Scanning: Output Pipeline Mutation...
  Scanning: Missing Observability...

──────────────────────────────────────────
✅ Audit complete. Found 5 issues in 0.3s:
   CRITICAL: 1
   HIGH:     2
   MEDIUM:   2
   LOW:      0
   Overall:  critical_risk

📋 Results: audit_results.json
📄 Report: audit_report.md
```

## The 12-Layer Stack

Every agent system has these layers. `agchk` audits all of them:

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

## Fix Strategy

Default fix order (code-first, not prompt-first):

1. **Code-gate tool requirements** — enforce in code, not just prompt text
2. **Remove or narrow hidden repair agents** — make fallback explicit with contracts
3. **Reduce context duplication** — same info through prompt + history + memory + distillation
4. **Tighten memory admission** — user corrections > agent assertions
5. **Tighten distillation triggers** — don't compress what shouldn't be compressed
6. **Reduce rendering mutation** — pass-through, don't transform
7. **Convert to typed JSON envelopes** — structured internal flow, not freeform prose

## Anti-Patterns to Avoid

- ❌ Saying "the model is weak" without falsifying the wrapper first
- ❌ Saying "memory is bad" without showing the contamination path
- ❌ Letting a clean current state erase a dirty historical incident
- ❌ Treating markdown prose as a trustworthy internal protocol
- ❌ Accepting "must use tool" in prompt text when code never enforces it

## License

Apache-2.0

## Related

- Full production skill: [oh-my-agent-check](https://github.com/huangrichao2020/oh-my-agent-check)
- Integrated into: Langflow, GenericAgent, superpowers, Everything Claude Code, OpenCode, Anthropic Skills

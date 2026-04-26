#!/usr/bin/env python3
"""Generate the oh-my-agent-check Skill package from agchk scanners and schema.

Usage:
    python scripts/gen-skill.py

Reads scanner patterns, audit logic, and JSON schema from the agchk package,
then writes a complete oh-my-agent-check Skill package to output/oh-my-agent-check/.
"""

import json
import re
from pathlib import Path

AGCHK_ROOT = Path(__file__).parent.parent


def read_scanner_patterns():
    """Extract anti-pattern descriptions from scanner source files."""
    scanners = AGCHK_ROOT / "agchk" / "scanners"
    patterns = []

    for fp in sorted(scanners.glob("*.py")):
        if fp.name.startswith("_"):
            continue
        content = fp.read_text()
        # Extract docstring as description
        m = re.search(r'^"""(.+?)"""', content, re.DOTALL)
        desc = m.group(1).strip() if m else ""
        # Extract patterns
        pat_lines = re.findall(r're\.compile\((r?["\'](.+?)["\'])', content)
        patterns.append(
            {
                "module": fp.stem.replace("_", " ").title(),
                "file": fp.name,
                "description": desc.split("\n")[0],
                "regex_count": len(pat_lines),
            }
        )
    return patterns


def generate_code_patterns_md():
    """Generate references/code-patterns.md from scanner regexes."""
    scanners_dir = AGCHK_ROOT / "agchk" / "scanners"

    sections = []
    for fp in sorted(scanners_dir.glob("*.py")):
        if fp.name.startswith("_"):
            continue
        content = fp.read_text()
        module_name = fp.stem.replace("_", " ").title()

        # Extract patterns with names
        # Pattern: re.compile(r"...", ...) or (name, re.compile(...))
        name_pat = re.findall(r'(?:re\.compile|r)"([^"]+)"', content)

        section = f"## {module_name}\n\n"
        section += f"**Scanner file**: `agchk/scanners/{fp.name}`\n\n"

        # Get severity from the file
        sev_match = re.search(r'"severity":\s*"(critical|high|medium|low)"', content)
        severity = sev_match.group(1) if sev_match else "medium"

        section += f"**Default severity**: `{severity}`\n\n"
        section += "**Regex patterns**:\n\n"

        for pat in name_pat:
            section += f"- `{pat}`\n"

        sections.append(section)

    header = """# Code-Level Anti-Patterns

Concrete grep-searchable patterns to find agent wrapper failures in source code.

These patterns are auto-generated from the [agchk](https://github.com/huangrichao2020/agchk) Python scanners.
Each section lists the regex patterns used by that scanner.

## Usage

```bash
pip install agchk
agchk /path/to/your/agent/project
```

Or run individual grep scans manually:

"""

    return header + "\n".join(sections)


def generate_skill_md():
    """Generate SKILL.md from agchk's README + schema + scanners."""
    schema = json.loads((AGCHK_ROOT / "agchk" / "schema.json").read_text())

    skill = f"""---
name: agent-architecture-audit
description: Audit the architecture and health of any AI agent system or LLM-integrated project. Uses the agchk Python library ({schema.get("properties", {}).get("schema_version", {}).get("const", "unknown")}) for structured reports with severity-ranked findings and code-first fix plans.
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
"""
    return skill


def generate_playbooks_md():
    """Generate references/playbooks.md from README content."""
    return """# Playbooks

Use one of these as the primary audit mode. Each playbook maps to one or more agchk scanners.

## wrapper-regression

Use when: the base model works fine but the wrapped agent is worse.
Scanner: `scan_hidden_llm_calls`, `scan_output_pipeline`
Focus: system prompt conflicts, duplicated context, hidden formatting layers.

## memory-contamination

Use when: old topics bleed into new conversations.
Scanner: `scan_memory_patterns`
Focus: same-session artifact reentry, stale session reuse, weak memory admission.

## tool-discipline

Use when: the agent skips required tools or hallucinates execution.
Scanner: `scan_tool_enforcement`
Focus: code-enforced vs prompt-enforced tool requirements, skip paths.

## rendering-transport

Use when: internal answer is correct but delivery is broken.
Scanner: `scan_output_pipeline`
Focus: transport payload assumptions, platform-layer mutations.

## hidden-agent-layers

Use when: silent repair/retry/summarize loops run without contracts.
Scanner: `scan_hidden_llm_calls`
Focus: hidden repair agents, second-pass LLM calls, maintenance-worker synthesis.

## code-execution-safety

Use when: the agent uses exec/eval/shell without sandboxing.
Scanner: `scan_code_execution`
Focus: resource limits, input validation, isolation.

## memory-growth-hazard

Use when: memory/context grows without limits.
Scanner: `scan_memory_patterns`
Focus: size limits, TTL, retention policies.

## observability-gap

Use when: there is no tracing or debugging capability.
Scanner: `scan_observability`
Focus: add logging, cost metrics, session replay.
"""


def main():
    output_dir = AGCHK_ROOT / "output" / "oh-my-agent-check"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate files
    files = {
        "SKILL.md": generate_skill_md(),
        "references/code-patterns.md": generate_code_patterns_md(),
        "references/playbooks.md": generate_playbooks_md(),
    }

    # Copy schema.json as report-schema.json
    schema_content = (AGCHK_ROOT / "agchk" / "schema.json").read_text()
    files["references/report-schema.json"] = schema_content

    # Copy README from root
    readme = (AGCHK_ROOT / "README.md").read_text()
    files["README.md"] = readme

    for name, content in files.items():
        fp = output_dir / name
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(content)
        print(f"  ✓ {fp.relative_to(AGCHK_ROOT)}")

    print(f"\nGenerated {len(files)} files to {output_dir.relative_to(AGCHK_ROOT)}/")
    print("To sync to oh-my-agent-check repo:")
    print(f"  rsync -av {output_dir}/ /path/to/oh-my-agent-check/")


if __name__ == "__main__":
    main()

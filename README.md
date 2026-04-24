# agchk

Audit the architecture and health of any AI agent system or LLM-integrated project.

**The base model rarely fails. The wrapper architecture corrupts good answers into bad behavior.**

`agchk` is also being built as a sustainable 100-year open source project for agent architecture doctrine, self-audit methods, and reusable review workflows.

```bash
pip install agchk
agchk /path/to/your/agent/project
```

Now with profile-aware scanning for:
- `personal` development
- `enterprise` production

By default, `agchk` now behaves like a **personal developer architecture review**:

- first look for internal drag and architecture mess
- then look at safety issues that can actually leak secrets or expose the project to outside intrusion
- do not treat normal prototype shortcuts as if they were enterprise incidents

## What It Does

`agchk` scans Python/TypeScript/JavaScript agent projects in two layers.

### Default personal-development focus

These checks are the default emphasis for solo builders and local prototypes:

| # | Scanner | Severity | What It Catches |
|---|---------|----------|-----------------|
| 1 | Internal Orchestration Sprawl | high | Planner/router/subagent/scheduler/retry layers that create internal drag |
| 2 | Memory Freshness Confusion | high | Too many checkpoints, summaries, archives, and memory generations |
| 3 | Skill Duplication | medium | Repeated SOPs, skills, and runbooks with unclear canonical versions |
| 4 | Startup Surface Sprawl | high | Too many launchers, wrappers, and boot paths |
| 5 | Runtime Surface Sprawl | high | One repo mixing too many runtime surfaces and deployment concerns |
| 6 | Memory Pattern Issues | low/medium | Unbounded context growth and retention drift |
| 7 | Hidden LLM Calls | medium/high | Secondary model paths that bypass the main loop |
| 8 | Tool Enforcement Gap | medium/high | Prompt-only tool requirements without code-level validation |

### Additional safety and production checks

These remain available, but are softer in `personal` and stricter in `enterprise`:

| # | Scanner | Severity | What It Catches |
|---|---------|----------|-----------------|
| 9 | Hardcoded Secrets | critical | API keys, tokens, credentials in source code |
| 10 | Unrestricted Code Execution | medium/critical | `exec()`, `eval()`, `subprocess(..., shell=True)` and similar execution paths |
| 11 | Output Pipeline Mutation | low/medium | Response transformation that can change what the user sees |
| 12 | Missing Observability | low/medium | No tracing, logging, or cost tracking |
| 13 | Excessive Agency | high/critical | Powerful agent capabilities without enough enterprise controls |

## Quick Start

```bash
# Install
pip install agchk

# Audit any agent project
agchk /path/to/your/langchain/project

# Default personal-developer mode: check internal architecture drag first
agchk /path/to/your/agent

# Enterprise-production audit with machine-readable outputs
agchk /path/to/your/agent \
  --profile enterprise \
  --sarif audit.sarif.json \
  --fail-on high

# Generate human-readable report
agchk report audit_results.json
```

## Profiles

`agchk` now ships with two human-friendly strictness modes:

| Profile | Intended Use | Agency Rule |
|---------|--------------|-------------|
| `personal` | Solo dev, local prototyping, early experiments | Approval/sandbox/allowlist controls are optional |
| `enterprise` | Production agents, team-owned internal tools, customer-facing systems | Approval, sandbox, allowlist must cover at least **2 of 3** control categories |

Profile differences are not just about safety gates. They also change what `agchk` cares about first:

- `personal` defaults to internal architecture review:
  - orchestration sprawl
  - memory freshness confusion
  - duplicated skills/SOPs
  - startup and runtime complexity
- `personal` also softens common prototype findings:
  - `exec` / `eval` / `shell=True` findings are downgraded and the fix guidance focuses on untrusted input rather than blanket removal
  - missing observability, loose tool enforcement, hidden secondary LLM paths, and unbounded memory growth are treated as softer concerns
  - internal safety gate issues are not the main focus
- `enterprise` keeps stricter severities and more conservative remediation guidance, especially for code execution, observability, and high-agency runtimes

In short:

- `personal` asks: "Where is this project wasting attention, introducing internal drag, or becoming hard to reason about?"
- `enterprise` asks: "What could leak, break, loop forever, or become dangerous in production?"

## Python API

```python
from agchk import run_audit, generate_report, generate_sarif
from agchk.config import AuditConfig

# Run full audit
results = run_audit(
    "/path/to/your/agent/project",
    config=AuditConfig.from_profile("enterprise"),
)

# Generate markdown report
markdown = generate_report(results)

# Generate SARIF for GitHub code scanning
sarif = generate_sarif(results)

# Save to file
generate_report(results, output_file="audit_report.md")

# Validate results against JSON schema
from agchk.schema import validate_report
errors = validate_report(results)
```

## Programmatic Scanner Access

```python
from agchk.scanners import scan_secrets, scan_code_execution, scan_excessive_agency
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
🛡️  SARIF: audit.sarif.json
```

## GitHub Code Scanning

`agchk` can now emit SARIF 2.1.0 so findings can flow into GitHub code scanning alerts.

```bash
agchk /path/to/your/repo --profile enterprise --sarif audit.sarif.json
```

Then upload `audit.sarif.json` in GitHub Actions with `github/codeql-action/upload-sarif`.

This makes `agchk` usable as:

- a local architecture audit
- a CI gate via `--fail-on`
- a GitHub code scanning signal for AI-specific risks

## Mission

`agchk` is not only a scanner package. It is intended to become long-lived public infrastructure for:

- naming agent design problems precisely
- turning self-scan results into reusable open source method
- keeping doctrine, contracts, scanners, and governance evolving together

The guiding idea is simple:

- doctrine is the primary asset
- code is a lubricant that makes doctrine runnable
- real-world agent failures should flow back into the project as generalized open source improvements

## Contribution Backflow

The preferred upstream path is fork-based:

`self-scan -> local review -> owner consent -> public-safe bundle -> fork PR -> upstream generalization`

This keeps contributions open, reviewable, and safer for projects whose own agents scan themselves.

Start here:

- [CONTRIBUTING.md](./CONTRIBUTING.md)
- [Doctrine Index](./docs/doctrine/README.md)
- [GitHub Repo Setup](./docs/governance/github-repo-setup.md)
- [Contribution Bundles](./contributions/README.md)

## Contribution CLI

`agchk` now includes a contribution flow that converts a self-scan into a fork-based upstream PR.

### 1. Prepare a contribution bundle

Use an existing audit JSON:

```bash
agchk contribute prepare audit_results.json
```

Or scan a target directory directly:

```bash
agchk contribute prepare /path/to/agent --profile enterprise
```

This creates a local bundle under `.agchk/contributions/...` containing:

- `bundle.json`
- `SUMMARY.md`
- `PULL_REQUEST_BODY.md`

### 2. Open a fork-based upstream PR

After the agent owner agrees and the content is confirmed public-safe:

```bash
agchk contribute pr .agchk/contributions/<bundle-slug> \
  --owner-consent \
  --public-safe
```

By default this opens a **draft** PR against `huangrichao2020/agchk`.

You can override selected fields:

```bash
agchk contribute pr .agchk/contributions/<bundle-slug> \
  --owner-consent \
  --public-safe \
  --title "[self-scan] tighten provider-aware hidden_llm routing" \
  --layer scanner \
  --why-generalizes "Provider modules are common across agent runtimes."
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
8. **Match controls to deployment reality** — prototype fast, but require stronger controls in enterprise production

## Anti-Patterns to Avoid

- ❌ Saying "the model is weak" without falsifying the wrapper first
- ❌ Saying "memory is bad" without showing the contamination path
- ❌ Letting a clean current state erase a dirty historical incident
- ❌ Treating markdown prose as a trustworthy internal protocol
- ❌ Accepting "must use tool" in prompt text when code never enforces it

## Project Structure

```
agchk/                          ← 唯一源码库 (single source of truth)
├── .github/                    ← PR templates, governance workflow, code owners
├── agchk/
│   ├── scanners/               ← 8 个反模式扫描器
│   ├── audit.py                ← 主编排器
│   ├── contribute.py           ← 自扫描贡献包与 fork PR 流程
│   ├── report.py               ← 报告生成
│   ├── schema.py               ← JSON Schema 验证
│   ├── cli.py                  ← 命令行入口
│   └── schema.json             ← 正式报告 Schema
├── contributions/              ← 上游 self-scan 贡献包落点
├── docs/
│   ├── doctrine/               ← 方法论、分层架构、贡献回流设计
│   └── governance/             ← GitHub 项目治理与 PR 流程
├── scripts/
│   └── gen-skill.py            ← 一键生成 oh-my-agent-check
└── output/
    └── oh-my-agent-check/      ← 自动生成的 Skill 包
         ├── SKILL.md
         ├── references/
         └── README.md
```

## Related

- **oh-my-agent-check**: https://github.com/huangrichao2020/oh-my-agent-check — AI agent Skill 包格式（由 agchk 自动生成）
- **PyPI**: https://pypi.org/project/agchk/

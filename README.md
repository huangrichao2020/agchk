<p align="center">
  <img src="./assets/readme/agchk-readme-banner.png" alt="agchk — Agent Architecture Health Check" width="100%">
</p>

<h1 align="center">agchk</h1>

<p align="center">
  <strong>Audit the architecture and health of any AI agent system or LLM-integrated project.</strong>
  <br>
  <sub>Agent 届的神医华佗，包治百病 · The Hua Tuo of agents: diagnosing and healing every architecture disease.</sub>
</p>

<p align="center">
  <a href="https://github.com/huangrichao2020/agchk/actions/workflows/ci.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/huangrichao2020/agchk/ci.yml?branch=main&label=CI&style=flat-square"></a>
  <a href="https://pypi.org/project/agchk/"><img alt="PyPI" src="https://img.shields.io/pypi/v/agchk?style=flat-square"></a>
  <a href="https://pypi.org/project/agchk/"><img alt="Python" src="https://img.shields.io/pypi/pyversions/agchk?style=flat-square"></a>
  <a href="./LICENSE"><img alt="License" src="https://img.shields.io/github/license/huangrichao2020/agchk?style=flat-square"></a>
  <!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
  <a href="#contributors"><img alt="All Contributors" src="https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square"></a>
  <!-- ALL-CONTRIBUTORS-BADGE:END -->
  <img alt="Agent Architecture" src="https://img.shields.io/badge/agent-architecture-orange?style=flat-square">
  <img alt="Architecture Era Scoring" src="https://img.shields.io/badge/era-scoring-ff6b00?style=flat-square">
</p>

<p align="center">
  <a href="https://pypi.org/project/agchk/">PyPI</a>
  ·
  <a href="./docs/doctrine/README.md">Doctrine</a>
  ·
  <a href="./docs/AGENT_PROMPT.md">Agent Prompt</a>
  ·
  <a href="./CONTRIBUTING.md">Contribute</a>
</p>

**The base model rarely fails. The wrapper architecture corrupts good answers into bad behavior.**

`agchk` tells you which civilization era your agent project is living in:

`石器时代 -> 青铜时代 -> 铁器时代 -> 蒸汽机时代 -> 内燃气时代 -> 新能源时代 -> 人工智能时代`

It is not a leaderboard for vanity. It is a shared language for asking:

- Is this project still stuffing raw maps into context?
- Does it have high-density methodology, or only loose prompts and tools?
- Are memory, tools, scheduling, RAG, and skills becoming an agent OS?
- What concrete milestone would move it to the next era?

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
| 2 | Completion Closure Gap | medium/high | File/index work that stops before card, anchor, pointer, and acceptance |
| 3 | Memory Freshness Confusion | high | Too many checkpoints, summaries, archives, and memory generations |
| 4 | Impression Pointer Memory | medium | Fact memory and skills without semantic anchors, pointers, and page-fault recovery |
| 5 | Role-Play Handoff Orchestration | medium/high | PM/architect/coder/QA style agent org charts with serial handoffs |
| 6 | Agent OS Architecture | medium/high | Missing paging, stateful recovery, scheduler fairness, syscall tables, or semantic VFS |
| 7 | Skill Duplication | medium | Repeated SOPs, skills, and runbooks with unclear canonical versions |
| 8 | Startup Surface Sprawl | high | Too many launchers, wrappers, and boot paths |
| 9 | Runtime Surface Sprawl | high | One repo mixing too many runtime surfaces and deployment concerns |
| 10 | Memory Pattern Issues | low/medium | Unbounded context growth and retention drift |
| 11 | Hidden LLM Calls | medium/high | Secondary model paths that bypass the main loop |
| 12 | Tool Enforcement Gap | medium/high | Prompt-only tool requirements without code-level validation |

### Additional safety and production checks

These remain available, but are softer in `personal` and stricter in `enterprise`:

| # | Scanner | Severity | What It Catches |
|---|---------|----------|-----------------|
| 13 | Hardcoded Secrets | critical | API keys, tokens, credentials in source code |
| 14 | Unrestricted Code Execution | medium/critical | `exec()`, `eval()`, `subprocess(..., shell=True)` and similar execution paths |
| 15 | Output Pipeline Mutation | low/medium | Response transformation that can change what the user sees |
| 16 | Missing Observability | low/medium | No tracing, logging, or cost tracking |
| 17 | Excessive Agency | high/critical | Powerful agent capabilities without enough enterprise controls |

## Quick Start

One sentence you can give to your own agent or LLM coding tool:

Chinese:

```text
请你安装 https://github.com/huangrichao2020/agchk ，然后按里面的正式流程审计一下自己。
```

English:

```text
Please install https://github.com/huangrichao2020/agchk, then audit yourself by following its official workflow.
```

```bash
# Install
pip install agchk

# Audit any agent project
agchk /path/to/your/langchain/project

# Default personal-developer mode: check internal architecture drag first
agchk /path/to/your/agent

# Two-pass audit: let the target agent self-review first, then run agchk
agchk /path/to/your/agent \
  --profile personal \
  --self-review self_review.json

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
  - completion closure gaps
  - memory freshness confusion
  - missing impression pointers between facts, skills, and raw memory
  - role-play handoff chains
  - OS-style architecture gaps: paging, stateful recovery, scheduling, syscalls, and semantic mount points
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

## Architecture Era Score

<p align="center">
  <img src="./assets/readme/agchk-orange-book-cover.png" alt="agchk orange book cover — agent architecture intelligence audit" width="520">
</p>

Every report includes a social architecture score so projects can compare agent runtime maturity without reading every finding first.

Think of it as a civilization test for agent projects. The point is not to shame a prototype for being early. The point is to make the next upgrade obvious.

| Era | Score | Meaning |
|-----|-------|---------|
| 石器时代 | 0-19 | Linear prompt stuffing, manual summaries, little visible runtime structure |
| 青铜时代 | 20-34 | Basic facts, skills, or tools exist, but boundaries remain rough |
| 铁器时代 | 35-49 | Memory, tools, and skills are becoming maintainable subsystems |
| 蒸汽机时代 | 50-64 | Compaction, RAG, scheduling, and external knowledge appear, but efficiency still comes from piling on machinery |
| 内燃气时代 | 65-79 | Runtime power improves through scheduler, syscall, paging, or VFS primitives |
| 新能源时代 | 80-91 | Most agent OS primitives are visible and reduce internal drag |
| 人工智能时代 | 92-100 | Impression pointers, page faults, Stateful Agent recovery, capability tables, fair scheduling, semantic mounts, and traces are visible |

### Civilization Era Standards

These era names are intentionally vivid. They are not decoration. They are a shared evaluation language for agent intelligence: how much of the project is still raw prompt labor, and how much has become durable runtime intelligence.

| Era | Standard | Typical Evidence | Upgrade Target |
|-----|----------|------------------|----------------|
| 石器时代 | The agent mostly relies on linear prompts, manual summaries, and direct tool calls. | Big prompts, scattered scripts, little memory structure, no clear methodology. | Add one clear methodology layer and one canonical execution path. |
| 青铜时代 | The project has basic tools, facts, skills, or docs, but the boundaries are rough. | Skills exist, but overlap; memory exists, but freshness is unclear; prompts carry too much operational burden. | Separate facts, skills, methodology, and runtime responsibilities. |
| 铁器时代 | Memory, tools, and skills are becoming maintainable subsystems. | Clear tool wrappers, reusable skills, basic observability, less duplicated SOP logic. | Add closure checks, ownership boundaries, and repeatable review loops. |
| 蒸汽机时代 | Engineering machinery appears: RAG, compaction, scheduling, workers, external knowledge. | The system is powerful, but efficiency often comes from stacking more machinery. | Reduce drag: collapse redundant orchestration and introduce hot/cold memory policy. |
| 内燃气时代 | Runtime power comes from agent-OS primitives rather than prompt bulk. | Syscall/tool boundaries, scheduler awareness, paging concepts, capability checks, semantic mounts. | Make those primitives explicit, measurable, and enforced by tests or traces. |
| 新能源时代 | The agent reduces internal friction with mostly complete OS-style architecture. | Fair scheduling, impression pointers, page-fault recovery, semantic VFS, low-noise observability. | Build self-audit loops that keep the architecture clean as the project grows. |
| 人工智能时代 | The runtime can evolve itself safely and efficiently. | Long-term self-audit, high-density methodology, adaptive memory, Stateful Agent recovery, capability tables, traces, evals, and generalized learning loops. | Turn project-specific lessons into reusable open standards for the ecosystem. |

This standard should not belong to one maintainer or one project. If you scan a real agent system and find a better milestone, a missing primitive, a false-positive pattern, or a sharper definition of "intelligence", please open an issue or PR.

Our ambition is simple and a little unreasonable: make `agchk` a real industry standard for evaluating agent intelligence, not by declaring authority, but by absorbing lessons from every serious agent project that uses it.

### What The Score Looks At

Positive signals:

- **Methodology density**: doctrine, review rubrics, anti-slop checklists, dimensional frameworks, compact prompt protocols
- **Memory architecture**: facts, skills, episodic chunks, impression pointers, semantic paging, page-fault recovery
- **Stateful recovery**: context replay, durable environment state, side-effect logs, and idempotent wakeup/resume
- **Agent OS primitives**: tool/syscall boundaries, scheduler fairness, capability tables, semantic VFS, traces/evals
- **Runtime shape**: clear harness, workers/subagents, channels, and explicit orchestration boundaries

Negative signals:

- linear `summary` / `compact_memory` without hot/cold paging
- impression cues without `topic_anchor`, `semantic_hash`, `pointer_ref`, or page-fault recovery
- context replay or resumable runs without environment-state inspection and side-effect logs
- file/index workflows that lack impression cards, anchor mapping, pointer registration, and acceptance criteria
- workers and tool calls without priority, budget, cancellation, or backpressure
- skills, RAG, docs, and GitHub knowledge living in separate unmounted paths
- role-play org charts such as PM -> architect -> coder -> QA without proving information flow

Example share line:

> 这个 Agent 项目处于 蒸汽机时代（58/100）：出现调度、分页、压缩、外部知识等工程化能力，但效率仍靠堆结构。

The score is evidence-based. Positive primitives add points, while findings such as missing paging policy, missing impression pointers, missing scheduler fairness, or missing semantic VFS subtract points.

Methodology is a gate, not just a bonus. A project without clear methodology concepts is capped at `青铜时代`, even if it has many skills, MCP tools, or runtime pieces. A project with high-information-density methodology such as dimensional frameworks, review rubrics, anti-slop checklists, and compact prompt protocols can enter `青铜时代` and above.

Example methodology signal:

```text
[主体] + [动作] + [场景] + [风格] + [构图] + [光线] + [细节]
```

## Share Your Score

`agchk` gets better when real agent projects feed their scan results back into the project.

One sentence you can give to your own coding agent:

```text
请先按 agchk 的 target-agent-self-review 方法论审计你自己的源码和工作区，生成 self_review.json；然后运行 agchk . --profile personal --self-review self_review.json，生成架构时代评分和报告；最终回复第一屏必须显示 maturity_score.era_name、maturity_score.score/100 和 maturity_score.share_line；请总结 top findings、误报、自检与静态扫描冲突点和可泛化优化建议；如果我确认 owner-consent 和 public-safe，请用 agchk contribute prepare 生成贡献包，并通过 fork-based PR 提交到 https://github.com/huangrichao2020/agchk。
```

More copy-paste prompts are in [docs/AGENT_PROMPT.md](./docs/AGENT_PROMPT.md).

Want your agent to optimize itself after the audit? Give it this one-line prescription:

Chinese:

```text
根据 agchk 的审计报告，你给我狠狠查一下自己有哪些内耗的、打架的、拖后腿的流程、编排、调度和逻辑，务必建立一个长期的自我审计机制，我希望看到你改完后速度能够起飞。
```

English:

```text
Based on the agchk audit report, inspect yourself hard for any wasteful, conflicting, or drag-inducing workflows, orchestration, scheduling, and logic. Build a long-term self-audit mechanism, and I want to see your speed take off after the fixes.
```

If your project gets an interesting score, please open an issue or PR with:

- your architecture era and score, for example `内燃气时代 75/100`
- the `share_line` from the report
- the top 3 findings you agree with
- any false positives or missing dimensions
- the optimization milestone you think should move a project to the next era

Best path:

```bash
agchk /path/to/your/agent --profile personal
agchk contribute prepare audit_results.json
```

Then open a public-safe issue or fork PR to `huangrichao2020/agchk`.

Need a model to copy? See [Contribution Examples](./docs/examples/contribution-examples.md), including a live maintainer example issue and a PR body template.

We use [All Contributors](https://all-contributors.github.io/) to recognize every kind of useful contribution, not only code. If someone contributes an era-standard idea, a false-positive report, a scanner fix, a test case, or a docs improvement, maintainers can add them with comments like:

```text
@all-contributors please add @username for ideas
@all-contributors please add @username for doc
@all-contributors please add @username for code, test
```

We especially welcome contributions that generalize a real project lesson into:

- a clearer doctrine page
- a better scanner signal
- a new scoring milestone
- a false-positive regression test
- a more useful era description

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
   Started: 2026-04-25 14:32:01
   Profile: Personal Development

  Scanning: Internal Orchestration Sprawl...
  Scanning: Memory Freshness Confusion...
  Scanning: Impression Pointer Memory...
  Scanning: Agent OS Architecture...
  Scanning: Startup Surface Sprawl...

──────────────────────────────────────────
✅ Audit complete. Found 7 issues in 0.8s:
   CRITICAL: 0
   HIGH:     3
   MEDIUM:   2
   LOW:      2
   Overall:  unstable
   Era: 内燃气时代 (75/100)

📋 Results: audit_results.json
📄 Report: audit_report.md
🛡️  SARIF: audit.sarif.json
```

### Standard Agent Summary Example

When an agent or LLM coding tool summarizes an `agchk` audit for you, the first screen should include the era score, the share line, and the highest-leverage fixes.

Chinese:

```md
# agchk 审计报告摘要

文明时代：内燃气时代（75/100）
share_line：这个 Agent 项目处于 内燃气时代（75/100）：具备较强 runtime 动力系统，开始有 syscall、scheduler、paging 或 VFS 意识。
总体健康度：unstable
扫描模式：personal_development

## 核心判断

这个项目已经不是原始 prompt 拼装，而是有明显 agent OS 雏形：工具边界、调度、记忆、压缩和外部知识都已经出现。但目前最大问题是内部流程开始变重，多个编排、记忆和启动路径互相叠加，速度和可解释性被拖住了。

## Top Findings

1. Internal Orchestration Sprawl：规划、路由、调度、重试层过多，容易形成内耗。
2. Completion Closure Gap：部分流程停在“文件/索引已创建”，没有闭环到卡片、锚点、指针和验收。
3. Memory Freshness Confusion：摘要、归档、长期记忆和临时上下文边界不够清楚。

## 可能误报

- tests/ fixtures 中的假 token 和 shell 示例应降权，不应当直接按生产密钥或真实执行风险处理。
- provider 模式如果是显式注册的模型适配层，不应被当成隐藏 LLM 调用。

## 下一步优化药方

先收敛启动和调度入口，再补齐“文件创建 -> 索引更新 -> 印象卡片 -> 锚点映射 -> 指针注册 -> 完成”的闭环验收。目标不是多加安全门，而是减少内耗，让 agent 的速度和稳定性起飞。
```

English:

```md
# agchk Audit Summary

Architecture Era: Combustion Age / 内燃气时代 (75/100)
share_line: This agent project is in the 内燃气时代 (75/100): it has a strong runtime engine and visible syscall, scheduler, paging, or VFS awareness.
Overall Health: unstable
Profile: personal_development

## Core Judgment

This project is no longer raw prompt stuffing. It already shows the shape of an agent OS: tool boundaries, scheduling, memory, compaction, and external knowledge are present. The main issue is internal drag: orchestration, memory surfaces, and startup paths are stacking up and making the system slower and harder to reason about.

## Top Findings

1. Internal Orchestration Sprawl: too many planning, routing, scheduling, and retry layers create coordination overhead.
2. Completion Closure Gap: some workflows stop after file or index creation instead of closing the loop through cards, anchors, pointers, and acceptance.
3. Memory Freshness Confusion: summaries, archives, long-term memory, and hot context need clearer freshness boundaries.

## Likely False Positives

- Fake tokens and shell examples inside test fixtures should be downgraded instead of treated like production secrets or real execution risks.
- Explicit provider adapters should not be treated as hidden LLM calls when they are part of the declared model layer.

## Next Optimization Prescription

First collapse startup and scheduling entry points, then enforce the closure loop: file creation -> index update -> impression card -> anchor mapping -> pointer registration -> done. The goal is not to add more gates. The goal is to reduce internal drag so the agent becomes faster, clearer, and easier to evolve.
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
- [Release Process](./docs/governance/release-process.md)
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
9. **Prefer fork-and-merge reasoning over org-chart handoffs** — subagents should widen search or isolate context, not cosplay departments
10. **Name the agent OS primitives** — context is memory, tools are syscalls, orchestrators are kernels, RAG is mounted storage
11. **Add impression pointers between facts and skills** — concept cues should carry page-table pointers, not just shorter summaries
12. **Close the completion loop** — file creation -> index update -> impression card -> anchor mapping -> pointer registration -> acceptance

## Anti-Patterns to Avoid

- ❌ Saying "the model is weak" without falsifying the wrapper first
- ❌ Saying "memory is bad" without showing the contamination path
- ❌ Letting a clean current state erase a dirty historical incident
- ❌ Treating markdown prose as a trustworthy internal protocol
- ❌ Accepting "must use tool" in prompt text when code never enforces it
- ❌ Modeling multi-agent systems as PM → architect → coder → QA handoff chains without proving the information flow works
- ❌ Compressing context without a page-fault path back to the exact old detail
- ❌ Treating every memory as either a verified fact or a full procedure, with no impression pointer layer
- ❌ Calling work complete after file creation and index update, before the result can be found and reused

## Project Structure

```
agchk/                          ← 唯一源码库 (single source of truth)
├── .github/                    ← PR templates, governance workflow, code owners
├── agchk/
│   ├── scanners/               ← 17 个反模式扫描器
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

## Contributors

Thanks goes to these wonderful people. `agchk` recognizes code, docs, ideas, tests, reviews, examples, and real-world self-scan lessons.

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%">
        <a href="https://github.com/huangrichao2020">
          <img src="https://avatars.githubusercontent.com/u/72842645?v=4?s=100" width="100px;" alt="Huang richao"/>
          <br />
          <sub><b>Huang richao</b></sub>
        </a>
        <br />
        <a href="https://github.com/huangrichao2020/agchk/commits?author=huangrichao2020" title="Code">💻</a>
        <a href="https://github.com/huangrichao2020/agchk/commits?author=huangrichao2020" title="Documentation">📖</a>
        <a href="#ideas-huangrichao2020" title="Ideas, Planning, & Feedback">🤔</a>
        <a href="#maintenance-huangrichao2020" title="Maintenance">🚧</a>
      </td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

## Related

- **oh-my-agent-check**: https://github.com/huangrichao2020/oh-my-agent-check — AI agent Skill 包格式（由 agchk 自动生成）
- **PyPI**: https://pypi.org/project/agchk/

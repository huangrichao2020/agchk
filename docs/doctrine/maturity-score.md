# Architecture Era Score

`agchk` gives each scanned project a social, comparable architecture-era score.

The score is not a security grade. It is a runtime maturity signal: how far the project has evolved from raw prompt stuffing toward an agent operating system.

## Era Ladder

| Era | Score Range | Meaning |
|-----|-------------|---------|
| 石器时代 | 0-19 | Linear prompt stuffing, manual summaries, and little visible runtime structure |
| 青铜时代 | 20-34 | Basic facts, skills, or tools exist, but boundaries remain rough |
| 铁器时代 | 35-49 | Memory, tools, and skills are becoming maintainable subsystems |
| 蒸汽机时代 | 50-64 | Scheduling, compaction, RAG, and external knowledge appear, but efficiency still comes from piling on machinery |
| 内燃气时代 | 65-79 | Runtime power improves through scheduler, syscall, paging, or VFS primitives |
| 新能源时代 | 80-91 | Most agent OS primitives are present and reduce internal drag |
| 人工智能时代 | 92-100 | The runtime can evolve: impression pointers, page faults, capability tables, fair scheduling, semantic mounts, and traces are visible |

## What Raises The Score

The score rewards concrete runtime primitives:

- agent runtime or harness
- tool/syscall boundary
- fact memory
- skill memory
- context compaction
- semantic paging
- page-fault recovery
- impression cues
- impression pointers
- scheduler/workers
- fair scheduling controls
- capability table
- semantic VFS
- traces/evals

## What Lowers The Score

Findings subtract points. The largest deductions come from architecture gaps that create internal drag:

- context memory lacks paging policy
- impression memory or impression pointers are missing
- scheduler lacks fairness controls
- tool syscalls lack an explicit capability table
- knowledge surfaces lack semantic VFS
- orchestration sprawl or role-play handoffs dominate the runtime

## Why This Is Social

The score produces a shareable line such as:

> This agent project is in the 蒸汽机时代 (58/100).

That line is intentionally simple. It lets maintainers compare projects, celebrate upgrades, and talk about architecture without drowning in scanner details.

The serious part is the evidence underneath: `strengths`, `next_milestones`, and `evidence_refs` explain why the project got that era and what would move it forward.

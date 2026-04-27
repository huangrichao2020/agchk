# agchk Twitter/X Launch Kit

This document is the working playbook for promoting `agchk` on Twitter/X without turning the account into noisy automation.

## Positioning

`agchk` is an agent architecture health check for AI-agent projects.

Core message:

> The base model rarely fails. The wrapper architecture corrupts good answers into bad behavior.

Short positioning:

> agchk audits AI-agent architecture: memory, tools, loops, RAG, skills, runtime boundaries, observability, token usage, and completion closure.

Chinese positioning:

> agchk 是 agent 架构体检工具：专门审计记忆、工具、循环、RAG、技能、运行时边界、可观测性、token 消耗和任务闭环。

What to avoid:

- Do not frame ordinary architecture findings as security disclosures.
- Do not imply a project is broken without evidence.
- Do not publish secrets, private audit details, or maintainer-facing criticism without a constructive fix path.
- Do not spam maintainers. One useful audit report beats ten generic replies.

## Account Setup

Bio option:

```text
Agent architecture health check. Audits memory, tools, loops, RAG, skills, observability, token usage, and runtime boundaries.
```

Short bio option:

```text
Architecture health checks for AI agents.
```

Pinned post:

```text
Most agent failures are not model failures.

They come from wrapper architecture:
- messy memory
- runaway loops
- hidden LLM calls
- tool boundaries that drift
- missing completion closure
- huge token waste

I built agchk to audit these patterns.

pip install agchk
agchk /path/to/agent

https://github.com/huangrichao2020/agchk
```

Profile link:

```text
https://github.com/huangrichao2020/agchk
```

Visual assets:

- README banner: `assets/readme/agchk-readme-banner.png`
- Orange book cover: `assets/readme/agchk-orange-book-cover.png`

Use the banner for launch posts and the orange book cover for doctrine / scoring posts.

## 7-Day Content Plan

Day 1: Launch and positioning

- Publish pinned post.
- Publish one short Chinese post for the existing Chinese builder circle.
- Reply to 3-5 relevant agent-builder discussions with one useful architecture observation, not a link dump.

Day 2: Era scoring

- Explain the civilization ladder: 石器时代 -> 青铜时代 -> 铁器时代 -> 蒸汽机时代 -> 内燃气时代 -> 新能源时代 -> 人工智能时代.
- Use the orange book cover.
- Ask builders which era their agent is probably in.

Day 3: Token usage

- Explain why large token spend is an architecture smell.
- Tie it to memory retrieval, context compaction, semantic paging, and CLI worker patterns.

Day 4: Completion closure

- Explain why "created the file" is not done unless there is index/card/pointer/verification/handoff closure.
- Show a mini checklist.

Day 5: Self-evolution loop

- Explain the standard: external signal -> source dissection -> pattern extraction -> constraint adaptation -> safe landing -> verification closure -> hands-on validation -> methodology/skill/impression assetization.

Day 6: Audit report example

- Publish a sanitized sample: score, era, top 3 findings, top 3 strengths, next upgrade target.
- Do not name a target project unless the audit is already public and constructive.

Day 7: Contributor call

- Ask for real agent repos to audit.
- Invite scanners for LangGraph, CrewAI, browser agents, MCP-heavy agents, local personal assistants, and enterprise agent runtimes.

## First 10 Posts

### 1. Launch

```text
Most agent failures are not model failures.

They come from wrapper architecture:
- memory gets stale
- tools bypass policy
- loops run forever
- hidden LLM calls appear
- tasks stop before closure
- token usage explodes

I built agchk to audit that.

pip install agchk
agchk /path/to/agent

https://github.com/huangrichao2020/agchk
```

### 2. Chinese launch

```text
做 agent 越久越觉得：

很多问题不是模型不行，而是外面那层 wrapper 架构把好答案搞坏了。

agchk 专门审计这些问题：
- 记忆混乱
- 工具边界漂移
- 循环失控
- token 浪费
- RAG 没治理
- 做完事没有闭环

pip install agchk
agchk /path/to/agent

https://github.com/huangrichao2020/agchk
```

### 3. Civilization score

```text
agchk gives agent projects an architecture era score:

石器时代 -> 青铜时代 -> 铁器时代 -> 蒸汽机时代 -> 内燃气时代 -> 新能源时代 -> 人工智能时代

It is not a vanity leaderboard.

It is a way to ask:
"What runtime primitive would make this agent less fragile?"
```

### 4. Token usage

```text
Token usage is not just a cost issue.

In agent systems, huge token spend often means:
- memory retrieval is weak
- summaries are unmanaged
- the agent lacks semantic paging
- CLI workers dump too much context
- old facts never decay

agchk now treats token waste as architecture debt.
```

### 5. Completion closure

```text
"The file was created" is not completion.

For an agent, completion usually needs:
- artifact created
- index updated
- memory/card/pointer registered
- before/after evidence captured
- verification run
- handoff note written when needed

agchk checks for completion closure gaps.
```

### 6. Observability

```text
Good agents leave evidence.

Not just logs.

Useful evidence:
- what changed
- why it changed
- before/after state
- tool calls and outcomes
- verification result
- handoff/workbook notes for the next agent

No evidence, no trust.
```

### 7. Personal vs enterprise

```text
agchk has personal and enterprise profiles.

Personal mode asks:
"Where is this project wasting attention or becoming hard to reason about?"

Enterprise mode asks:
"What could leak, break, loop forever, or become dangerous in production?"

Different stage, different audit pressure.
```

### 8. Self-evolution

```text
A serious agent should not just "learn" a new skill.

It should:
1. study the source
2. run a real task
3. verify the outcome
4. extract the method
5. create a reusable skill/manual
6. leave an impression pointer for future retrieval

agchk audits this self-evolution loop.
```

### 9. Project reply template

```text
This is a useful agent project. One architecture question I would check:

Does the runtime have a clear completion-closure path after tool/file work?

In long-running agents, "task done" usually needs artifact + index + memory pointer + verification evidence.

I am building agchk to audit patterns like this.
```

Use this as a reply only when the project actually has agent/tool/file workflows.

### 10. Contributor call

```text
Looking for agent projects to test agchk against:

- LangGraph / CrewAI apps
- browser agents
- MCP-heavy agents
- local personal assistants
- multi-agent runtimes
- enterprise agent platforms

Goal: find architecture debt and turn it into useful scanner rules.

Repo: https://github.com/huangrichao2020/agchk
```

## Reply Style

Good replies:

```text
This looks like the exact kind of runtime where completion closure matters:
tool result -> artifact -> index -> memory pointer -> verification.

Without that chain, agents often appear successful but lose state later.
```

```text
One thing worth checking: does the agent distinguish active rules from historical memory?

If all old summaries are equally retrievable, memory becomes noise instead of context.
```

```text
Interesting project. The risk I would audit first is not model quality, but whether hidden secondary LLM calls bypass the main policy/runtime path.
```

Bad replies:

```text
Your project is broken. Run agchk.
```

```text
This is insecure.
```

```text
My tool can fix this.
```

## Operating Rules

- Public posts can be drafted freely.
- Before publishing direct criticism of a named project, prepare evidence and a constructive fix.
- For maintainer-facing replies, lead with the project-specific observation, not the agchk link.
- Use screenshots sparingly. Prefer one strong report excerpt over many UI images.
- If a finding is speculative, label it as an architecture question, not a confirmed bug.
- When a project maintainer engages, offer to run a fresh audit and post the exact report.

## Metrics

Track weekly:

- GitHub stars
- PyPI downloads
- profile visits
- post impressions
- replies from agent builders
- audit requests
- upstream issue / PR opportunities
- scanner ideas discovered from real projects

Quality metric:

> Did this week produce at least one better scanner, report example, doctrine page, or contribution opportunity?

## Suggested First Session

1. Update profile bio.
2. Set GitHub repo as profile link.
3. Post the launch thread with README banner.
4. Pin the launch post.
5. Post the Chinese launch post.
6. Search for recent posts about "agent framework", "AI agent memory", "MCP agent", "LangGraph agent", and "browser agent".
7. Leave 3 useful architecture replies without hard-selling.

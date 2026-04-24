# One-Sentence Agent Prompt

Use this when you want your coding agent or LLM code tool to run `agchk` and contribute the result upstream.

## Short Version

```text
请在当前项目安装并运行 agchk，用 personal profile 生成架构时代评分和报告；请总结 share_line、top findings、误报和可泛化优化建议；如果我确认 owner-consent 和 public-safe，请用 agchk contribute prepare 生成贡献包，并通过 fork-based PR 提交到 https://github.com/huangrichao2020/agchk。
```

## English Version

```text
Install and run agchk on this project with the personal profile, generate the architecture era score and report, summarize the share_line, top findings, false positives, and generalizable improvement ideas; if I confirm owner-consent and public-safe, run agchk contribute prepare and open a fork-based PR to https://github.com/huangrichao2020/agchk.
```

## Safer Long Version

```text
You are helping me self-scan this agent or LLM-integrated project with agchk.

1. Install agchk if needed.
2. First produce a target-agent self-review JSON using the method in `docs/doctrine/target-agent-self-review.md`.
3. Run: agchk . --profile personal --self-review self_review.json
4. Read audit_results.json and audit_report.md.
5. Tell me the architecture era score, share_line, top 3 findings, likely false positives, target self-review disagreements, and the most useful upstream improvement idea.
6. Do not publish anything yet.
7. If I explicitly confirm both owner-consent and public-safe, run:
   agchk contribute prepare audit_results.json
8. Review the generated bundle for private data.
9. If still public-safe, open a fork-based draft PR to:
   https://github.com/huangrichao2020/agchk
10. The PR should explain why the lesson generalizes beyond my project.
```

## Required Consent

Agents should not open the upstream PR until the project owner explicitly confirms both:

- `owner-consent`: the owner agrees to publish the contribution
- `public-safe`: the bundle does not contain private code, secrets, customer data, or sensitive internal context

Without both confirmations, the agent should stop at a local report or local contribution bundle.

## What Makes A Good Upstream Contribution

Good contributions usually include one of:

- a new false-positive regression case
- a new scanner signal
- a better era scoring milestone
- a clearer doctrine page
- a real project lesson that can be generalized

The goal is not to upload private project details. The goal is to make `agchk` better for the next agent project.

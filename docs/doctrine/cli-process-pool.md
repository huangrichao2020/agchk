# CLI Process Pool

A CLI process pool lets a master agent delegate work to external LLM code tools without building a socket protocol or permanent daemon.

The pattern is intentionally Unix-shaped:

```text
Master agent -> Task JSON/task file -> natural-language worker prompt -> qwen/codex/claude CLI worker -> stdout/stderr/exit code -> master agent
```

## Roles

- Master agent: decomposes the task, chooses the worker, writes the task envelope, starts the process, captures results, and merges the outcome.
- CLI worker: a short-lived Qwen, Codex, Claude, Gemini, or OpenCode process that reads a natural-language prompt or a referenced task file, does the work, and exits.
- Task envelope: a structured JSON file containing goal, context, file paths, constraints, acceptance criteria, and output contract.

## Why This Is An Architecture Primitive

This is not role-play orchestration. The master agent is not pretending to have departments. It is using the operating system process model as a worker substrate.

The design has useful properties:

- zero extra infrastructure: shell, files, stdout, stderr, and exit codes are enough
- natural lifecycle: worker CLIs start, work, report, and exit
- fast delegation: no folder polling loop is required
- inspectable recovery: task files and process outputs can be logged

## Contract

A mature CLI process pool should define:

- which external LLM CLIs are allowed
- how the master writes Task JSON
- how the master converts Task JSON into a natural-language stdin prompt or task-file reference for CLI tools that do not accept raw JSON
- where stdout, stderr, exit code, and result artifacts are captured
- timeout, cancellation, concurrency, and retry policy
- how worker output is merged into the master context
- which filesystem or network capabilities each worker can use

## Scanner Implication

`agchk` rewards projects that describe LLM CLI workers and task envelopes.

It flags projects that mention Qwen, Codex, Claude, or other external LLM CLI workers but do not describe Task JSON, prompt handoff, output capture, and process controls. Without that contract, CLI delegation becomes shell-shaped hidden orchestration instead of an auditable agent OS primitive.

One sharp rule: do not blindly pipe raw Task JSON into a human-oriented LLM CLI. Keep JSON as the durable task envelope and audit artifact, then pass a natural-language prompt or a task-file reference to stdin.

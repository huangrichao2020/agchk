# Contributing to agchk

`agchk` is not just a scanner collection. We are building it as a sustainable 100-year open source project for agent architecture doctrine, self-audit methods, and reusable engineering patterns.

We welcome contributions from anywhere in the world, especially from real agent systems that scan themselves and surface:

- new design failure modes
- scanner false positives
- generalized fixes
- framework-specific patterns
- better doctrine and vocabulary

## Contribution Principles

1. Doctrine before cleverness.
2. Generalize before upstreaming.
3. Public-safe evidence only.
4. Tests and docs should move with scanner logic.
5. `agchk` should remain layered, explainable, and extensible.

## The Five Layers

Every contribution should say which layer it improves:

- `Doctrine`: principles, vocabulary, failure modes, prioritization
- `Contract`: `agchk.yaml` or future architecture declarations
- `Scanner`: concrete detection logic
- `Contribution Flow`: self-scan bundles and upstream contribution mechanics
- `Governance`: PR policy, code ownership, review workflow, repo rules

## Preferred Contribution Flow

For external agent projects, the preferred path is fork-based upstreaming:

1. Run `agchk` against the local project.
2. Review the report with the agent owner.
3. Run `agchk contribute prepare` to build a local contribution bundle.
4. Decide what can be generalized into a public contribution.
5. Remove or rewrite any private code, customer details, secrets, prompts, or internal paths.
6. Use `agchk contribute pr --owner-consent --public-safe` to open a fork-based upstream PR.
7. Use the repository PR template and complete all required sections.

## Self-Scan Contributions

Self-scan contributions are especially valuable, but they must meet a higher bar.

They must include:

- explicit owner consent to publish the contribution upstream
- public-safe evidence only
- a clear explanation of why the pattern generalizes beyond one project
- tests or fixtures that protect the new behavior
- doctrine or README updates if the change affects method or vocabulary

They must not include:

- raw private repositories or large proprietary code dumps
- secrets, credentials, internal URLs, customer data, or sensitive logs
- scanner changes without a claim about what got less noisy or more accurate

## Pull Request Expectations

All pull requests should explain:

- why this change matters to the long-term mission
- which layer(s) it changes
- whether it is a self-scan contribution or a maintainer-originated change
- what evidence supports the change
- what validation was run

For self-scan contributions, the PR title should start with `[self-scan]`.

## Review Standard

Upstream maintainers will review for:

- public safety
- generalizability
- layering and extensibility
- signal-to-noise improvement
- tests and docs quality

The best contributions do not merely fix one project. They improve `agchk` as shared method infrastructure for future agent systems.

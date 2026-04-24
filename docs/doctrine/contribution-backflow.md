# Contribution Backflow

The preferred upstreaming model for `agchk` is:

`self-scan -> local review -> owner consent -> public-safe bundle -> fork PR -> upstream generalization`

This is the recommended `B` path for long-term governance.

## Why Fork-Based PRs

Fork-based contributions are the right default because they:

- preserve contributor control
- keep upstream review explicit
- avoid forcing write access or direct-PR automation
- reduce the risk of accidental private-data publication
- fit public open source governance better than direct repository writes

## Self-Scan Backflow Flow

1. An external agent project loads `agchk` and scans itself.
2. The agent or maintainer reviews the report locally.
3. They decide what is worth generalizing into `agchk`.
4. The agent owner explicitly consents before anything public is prepared.
5. A contribution bundle is created with only public-safe, minimal evidence.
6. The contributor opens a fork-based PR to `huangrichao2020/agchk`.
7. The upstream PR explains:
   - the pattern
   - why it generalizes
   - which layer it improves
   - what tests/docs were added

## What Should Flow Back

Good upstream candidates include:

- a false positive that can be generalized away
- a true positive pattern seen repeatedly across projects
- a framework-specific interpretation rule
- doctrine improvements that sharpen vocabulary or review judgment
- governance improvements that improve contribution quality

## What Should Not Flow Back

Do not upstream:

- raw customer code
- proprietary prompts or datasets
- credentials or tokens
- internal URLs or environment topology
- project-specific churn that does not generalize

## CLI Surface

The current CLI surface is:

- `agchk contribute prepare`
- `agchk contribute pr --owner-consent`

`prepare` should build a local contribution bundle.

`pr` is opt-in and defaults to a fork-based upstream flow. It should never become a blind direct push to the canonical repository.

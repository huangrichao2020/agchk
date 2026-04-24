# Release Process

`agchk` releases should publish three things together:

- a PyPI package
- a GitHub Release with generated notes
- public contributor credit for the people who moved the standard forward

GitHub's generated release notes include merged pull requests, contributors, and a full changelog link. `agchk` customizes those notes with `.github/release.yml` so changes are grouped around the project mission: agent intelligence standards, scanner signals, contribution flow, docs, and release infrastructure.

## Release Checklist

1. Make sure `main` is green.
2. Make sure the version in `pyproject.toml` is the version you want to publish.
3. Confirm merged PRs have useful labels, especially:
   - `era-scoring`
   - `methodology`
   - `doctrine`
   - `scanner`
   - `false-positive`
   - `governance`
   - `contribution-flow`
   - `contributors`
   - `docs`
   - `ci`
   - `release`
   - `packaging`
4. Add All Contributors credit for non-code contributions before tagging when possible.
5. Create and push a version tag:

```bash
git switch main
git pull --ff-only
git tag v0.2.0
git push origin v0.2.0
```

## What Automation Does

Pushing a `v*` tag runs the normal CI pipeline:

- lint
- repository hygiene checks
- tests on Python 3.10, 3.11, 3.12, and 3.13
- package build
- GitHub Release creation with generated release notes and contributors
- PyPI publish through trusted publishing

## What The Release Should Show

A good release should make contributors visible, not buried:

```md
## What's Changed

- docs: define civilization era standards by @contributor in #12
- fix(scanner): reduce provider false positives by @contributor in #13

### Contributors

@contributor and @another-contributor

Full Changelog: v0.2.0...v0.2.1
```

The goal is not just to ship packages. The goal is to make every useful improvement to the agent-intelligence standard visible and creditable.

# agchk Hardening And Profiles Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `agchk` reliable enough for real CI usage by fixing the CLI/report contract, adding machine-readable SARIF output, and introducing personal vs enterprise-production agency checks.

**Architecture:** Keep the package lightweight, but introduce one shared audit config layer and one scanner registry so the CLI, orchestrator, schema validation, report generation, and new scanner all consume the same contract. Use profile-driven policy for excessive agency checks: personal development skips approval/sandbox/allowlist requirements, while enterprise production requires at least two of the three controls.

**Tech Stack:** Python 3.8+, pytest, jsonschema, argparse, standard-library JSON serialization.

---

### Task 1: Lock the contract with tests

**Files:**
- Create: `tests/test_cli.py`
- Create: `tests/test_report_schema.py`
- Create: `tests/test_excessive_agency.py`
- Create: `tests/test_sarif.py`

- [ ] Write failing tests for direct-path CLI invocation, schema-valid audit output, profile-driven agency checks, and SARIF export.
- [ ] Run targeted pytest commands and confirm they fail for the current implementation.

### Task 2: Introduce shared config and scanner registry

**Files:**
- Create: `agchk/config.py`
- Modify: `agchk/scanners/__init__.py`
- Modify: `agchk/audit.py`

- [ ] Add an audit config dataclass with `profile`, `enabled_scanners`, and agency control policy.
- [ ] Convert the scanner list into a small registry so orchestrator and docs can derive scanner metadata from one place.
- [ ] Thread config into `run_audit`.

### Task 3: Repair the output model

**Files:**
- Modify: `agchk/schema.json`
- Modify: `agchk/schema.py`
- Modify: `agchk/report.py`
- Modify: `agchk/__init__.py`

- [ ] Make runtime output actually match the published schema.
- [ ] Replace the hand-written validator with real JSON Schema validation.
- [ ] Update the markdown report generator to read the new result shape.

### Task 4: Add enterprise-production agency scanning

**Files:**
- Create: `agchk/scanners/excessive_agency.py`
- Modify: `agchk/audit.py`
- Modify: `agchk/report.py`

- [ ] Add a scanner that detects privileged agent capabilities.
- [ ] Treat `approval`, `sandbox`, and `allowlist` as the three control categories.
- [ ] In `personal` profile, skip this control requirement.
- [ ] In `enterprise_production` profile, require at least two of the three control categories.

### Task 5: Improve CLI and CI integration

**Files:**
- Create: `agchk/sarif.py`
- Modify: `agchk/cli.py`
- Modify: `pyproject.toml`
- Modify: `.github/workflows/ci.yml`
- Modify: `README.md`

- [ ] Restore `agchk /path/to/project` backward compatibility.
- [ ] Add SARIF output support for GitHub code scanning ingestion.
- [ ] Add a severity threshold option for CI failure.
- [ ] Make CI install test/lint dependencies and run the new test suite.
- [ ] Document profiles, SARIF output, and enterprise usage in the README.

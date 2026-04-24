"""Shared audit configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Optional


@dataclass(frozen=True)
class AuditProfile:
    """Profile-specific policy knobs for audits."""

    key: str
    display_name: str
    min_agency_controls: int
    enforce_agency_controls: bool


PROFILE_PRESETS = {
    "personal_development": AuditProfile(
        key="personal_development",
        display_name="Personal Development",
        min_agency_controls=0,
        enforce_agency_controls=False,
    ),
    "enterprise_production": AuditProfile(
        key="enterprise_production",
        display_name="Enterprise Production",
        min_agency_controls=2,
        enforce_agency_controls=True,
    ),
}

PROFILE_ALIASES = {
    "personal": "personal_development",
    "personal_development": "personal_development",
    "enterprise": "enterprise_production",
    "enterprise_production": "enterprise_production",
}

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
FAIL_THRESHOLD_ORDER = {"none": 4, **SEVERITY_ORDER}


@dataclass(frozen=True)
class AuditConfig:
    """Runtime config shared across the CLI, orchestrator, and scanners."""

    profile: AuditProfile
    enabled_scanners: Optional[FrozenSet[str]] = None
    fail_on: str = "none"
    extra: dict = field(default_factory=dict)

    @classmethod
    def from_profile(
        cls,
        profile_name: str,
        *,
        enabled_scanners: Optional[list[str]] = None,
        fail_on: str = "none",
    ) -> "AuditConfig":
        profile = resolve_profile(profile_name)
        return cls(
            profile=profile,
            enabled_scanners=frozenset(enabled_scanners) if enabled_scanners else None,
            fail_on=fail_on,
        )


def resolve_profile(profile_name: str | None) -> AuditProfile:
    normalized = PROFILE_ALIASES.get((profile_name or "personal").strip().lower())
    if not normalized:
        valid = ", ".join(sorted(PROFILE_ALIASES))
        raise ValueError(f"Unknown audit profile '{profile_name}'. Expected one of: {valid}")
    return PROFILE_PRESETS[normalized]


def should_fail_for_threshold(results: dict, threshold: str) -> bool:
    """Return True when results should trigger a CI failure."""

    threshold_value = FAIL_THRESHOLD_ORDER[threshold]
    if threshold == "none":
        return False

    for finding in results.get("findings", []):
        severity = finding.get("severity", "low")
        if SEVERITY_ORDER.get(severity, 99) <= threshold_value:
            return True
    return False

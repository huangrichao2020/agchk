"""Scanner registry and exports."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List

from agchk.config import AuditConfig
from agchk.scanners.code_execution import scan_code_execution
from agchk.scanners.excessive_agency import scan_excessive_agency
from agchk.scanners.hidden_llm import scan_hidden_llm_calls
from agchk.scanners.memory_patterns import scan_memory_patterns
from agchk.scanners.observability import scan_observability
from agchk.scanners.output_pipeline import scan_output_pipeline
from agchk.scanners.secrets import scan_secrets
from agchk.scanners.tool_enforcement import scan_tool_enforcement

ScannerFunc = Callable[[Path, AuditConfig], List[dict]]


@dataclass(frozen=True)
class ScannerSpec:
    slug: str
    name: str
    func: ScannerFunc
    audited_layers: tuple[str, ...]


def _adapt(scan_fn: Callable[[Path], List[dict]]) -> ScannerFunc:
    return lambda target, config: scan_fn(target)


SCANNER_REGISTRY = [
    ScannerSpec(
        slug="secrets",
        name="Hardcoded Secrets",
        func=_adapt(scan_secrets),
        audited_layers=("persistence",),
    ),
    ScannerSpec(
        slug="tool_enforcement",
        name="Tool Enforcement Gap",
        func=_adapt(scan_tool_enforcement),
        audited_layers=("tool_selection", "tool_execution"),
    ),
    ScannerSpec(
        slug="hidden_llm",
        name="Hidden LLM Calls",
        func=_adapt(scan_hidden_llm_calls),
        audited_layers=("fallback_loops", "tool_selection"),
    ),
    ScannerSpec(
        slug="code_execution",
        name="Unrestricted Code Execution",
        func=_adapt(scan_code_execution),
        audited_layers=("tool_execution",),
    ),
    ScannerSpec(
        slug="memory_patterns",
        name="Memory Pattern Issues",
        func=_adapt(scan_memory_patterns),
        audited_layers=("session_history", "long_term_memory"),
    ),
    ScannerSpec(
        slug="output_pipeline",
        name="Output Pipeline Mutation",
        func=_adapt(scan_output_pipeline),
        audited_layers=("answer_shaping", "platform_rendering"),
    ),
    ScannerSpec(
        slug="observability",
        name="Missing Observability",
        func=_adapt(scan_observability),
        audited_layers=("persistence",),
    ),
    ScannerSpec(
        slug="excessive_agency",
        name="Excessive Agency",
        func=scan_excessive_agency,
        audited_layers=("tool_selection", "tool_execution"),
    ),
]


def get_enabled_scanners(config: AuditConfig) -> list[ScannerSpec]:
    if not config.enabled_scanners:
        return SCANNER_REGISTRY
    return [spec for spec in SCANNER_REGISTRY if spec.slug in config.enabled_scanners]


__all__ = [
    "ScannerSpec",
    "SCANNER_REGISTRY",
    "get_enabled_scanners",
    "scan_code_execution",
    "scan_excessive_agency",
    "scan_hidden_llm_calls",
    "scan_memory_patterns",
    "scan_observability",
    "scan_output_pipeline",
    "scan_secrets",
    "scan_tool_enforcement",
]

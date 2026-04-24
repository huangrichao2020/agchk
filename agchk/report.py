"""Generate human-readable markdown reports."""

from __future__ import annotations

from typing import Any, Dict, Optional

SEVERITY_EMOJI = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}


def generate_report(results: Dict[str, Any], output_file: Optional[str] = None) -> str:
    """Generate a markdown report from audit results."""

    verdict = results.get("executive_verdict", {})
    scope = results.get("scope", {})
    metadata = results.get("scan_metadata", {})
    summary = results.get("severity_summary", {})

    lines = [
        "# Agent Architecture Audit Report",
        "",
        f"**Target**: `{scope.get('target_name', 'Unknown')}`",
        f"**Profile**: `{metadata.get('profile', 'unknown')}`",
        f"**Date**: {metadata.get('scan_timestamp', 'Unknown')}",
        f"**Duration**: {metadata.get('scan_duration_seconds', 'N/A')}s",
        f"**Overall Health**: **{verdict.get('overall_health', 'Unknown')}**",
        f"**Primary Failure Mode**: {verdict.get('primary_failure_mode', 'Unknown')}",
        f"**Most Urgent Fix**: {verdict.get('most_urgent_fix', 'Unknown')}",
        "",
        "## Scope",
        "",
        f"- Entry points: {', '.join(scope.get('entrypoints', [])) or 'Unknown'}",
        f"- Channels: {', '.join(scope.get('channels', [])) or 'Unknown'}",
        f"- Model stack: {', '.join(scope.get('model_stack', [])) or 'Unknown'}",
        f"- Audited layers: {', '.join(scope.get('layers_to_audit', [])) or 'Unknown'}",
        "",
        "## Summary",
        "",
        "| Severity | Count |",
        "|----------|-------|",
    ]

    for severity in ("critical", "high", "medium", "low"):
        lines.append(f"| {SEVERITY_EMOJI.get(severity, '')} {severity.upper()} | {summary.get(severity, 0)} |")
    lines.extend(["", f"**Total findings**: {sum(summary.values())}", ""])

    if results.get("evidence_pack"):
        lines.extend(["## Evidence Pack", ""])
        for evidence in results["evidence_pack"]:
            lines.append(
                f"- `{evidence['kind']}` {evidence['location']} — {evidence['summary']}"
            )
        lines.append("")

    for index, finding in enumerate(results.get("findings", []), start=1):
        severity = finding.get("severity", "low")
        lines.extend(
            [
                f"### {index}. {SEVERITY_EMOJI.get(severity, '')} [{severity.upper()}] {finding.get('title', '')}",
                "",
            ]
        )
        for key in ("symptom", "user_impact", "source_layer", "mechanism", "root_cause", "recommended_fix"):
            if finding.get(key):
                lines.append(f"**{key.replace('_', ' ').title()}**: {finding[key]}")
        if finding.get("evidence_refs"):
            lines.append("**Evidence**:")
            for ref in finding["evidence_refs"]:
                lines.append(f"- `{ref}`")
        if finding.get("confidence") is not None:
            lines.append(f"**Confidence**: {finding['confidence']:.0%}")
        lines.append("")

    if results.get("ordered_fix_plan"):
        lines.extend(["## Ordered Fix Plan", ""])
        for step in results["ordered_fix_plan"]:
            lines.append(f"{step['order']}. **{step['goal']}** — {step['why_now']}")
        lines.append("")

    markdown = "\n".join(lines)
    if output_file:
        with open(output_file, "w", encoding="utf-8") as handle:
            handle.write(markdown)
    return markdown

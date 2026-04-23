"""Generate human-readable markdown reports."""
from typing import Dict, Any, Optional

SEVERITY_EMOJI = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}

def generate_report(results: Dict[str, Any], output_file: Optional[str] = None) -> str:
    """Generate a markdown report from audit results."""
    r = results
    lines = [f"# Agent Architecture Audit Report", "",
        f"**Target**: `{r.get('target_name', 'Unknown')}`",
        f"**Date**: {r.get('scan_timestamp', 'Unknown')}",
        f"**Duration**: {r.get('scan_duration_seconds', 'N/A')}s",
        f"**Overall Health**: **{r.get('overall_health', 'Unknown')}**", ""]
    
    s = r.get("severity_summary", {})
    lines += ["## Summary", "", "| Severity | Count |", "|----------|-------|"]
    for sev in ["critical","high","medium","low"]:
        lines.append(f"| {SEVERITY_EMOJI.get(sev,'')} {sev.upper()} | {s.get(sev,0)} |")
    lines += ["", f"**Total findings**: {sum(s.values())}", ""]
    
    for i, f in enumerate(r.get("findings", []), 1):
        sev = f.get("severity","low")
        lines += [f"### {i}. {SEVERITY_EMOJI.get(sev,'')} [{sev.upper()}] {f.get('title','')}", ""]
        for key in ["symptom","user_impact","source_layer","mechanism","root_cause","recommended_fix"]:
            if f.get(key): lines.append(f"**{key.replace('_',' ').title()}**: {f[key]}")
        if f.get("evidence_refs"):
            lines.append("**Evidence**:")
            for ref in f["evidence_refs"]: lines.append(f"- `{ref}`")
        if f.get("confidence"): lines.append(f"**Confidence**: {f['confidence']:.0%}")
        lines.append("")
    
    if r.get("ordered_fix_plan"):
        lines += ["## Ordered Fix Plan", ""]
        for step in r["ordered_fix_plan"]:
            lines.append(f"{step['order']}. **{step['goal']}** — {step.get('why_now','')}")
        lines.append("")
    
    md = "\n".join(lines)
    if output_file:
        with open(output_file, "w") as f: f.write(md)
    return md

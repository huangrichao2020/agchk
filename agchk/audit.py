"""Main audit orchestrator."""
import json, sys, time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Callable, Optional

from agchk.scanners import (
    scan_secrets, scan_tool_enforcement, scan_hidden_llm_calls,
    scan_code_execution, scan_memory_patterns, scan_output_pipeline,
    scan_observability,
)

SCANNERS = [
    ("Hardcoded Secrets", scan_secrets),
    ("Tool Enforcement Gap", scan_tool_enforcement),
    ("Hidden LLM Calls", scan_hidden_llm_calls),
    ("Unrestricted Code Execution", scan_code_execution),
    ("Memory Pattern Issues", scan_memory_patterns),
    ("Output Pipeline Mutation", scan_output_pipeline),
    ("Missing Observability", scan_observability),
]
SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}

def run_audit(target_path: str, scanners: Optional[list] = None, verbose: bool = True) -> dict:
    """Run all anti-pattern scans against the target directory."""
    target = Path(target_path)
    if not target.exists():
        raise FileNotFoundError(f"Target path does not exist: {target_path}")
    if not target.is_dir():
        raise NotADirectoryError(f"Target path is not a directory: {target_path}")
    
    if verbose:
        print(f"\n🔍 Agent Architecture Audit")
        print(f"   Target: {target_path}")
        print(f"   Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    findings = []
    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    start = time.time()
    
    for name, scanner in scanners or SCANNERS:
        if verbose: print(f"  Scanning: {name}...")
        try:
            for f in scanner(target):
                findings.append(f)
                severity_counts[f.get("severity", "low")] += 1
        except Exception as e:
            if verbose: print(f"    ⚠️  Error in {name}: {e}")
    
    findings.sort(key=lambda x: SEVERITY_ORDER.get(x.get("severity", "low"), 4))
    health = "critical_risk" if severity_counts["critical"] else "high_risk" if severity_counts["high"] else "medium_risk" if severity_counts["medium"] else "low_risk"
    
    results = {
        "schema_version": "agchk.report.v1",
        "target_name": str(target_path),
        "scan_timestamp": datetime.now().isoformat(),
        "scan_duration_seconds": round(time.time() - start, 2),
        "overall_health": health,
        "severity_summary": severity_counts,
        "findings": findings,
        "ordered_fix_plan": [{"order": i+1, "goal": f["title"], "severity": f["severity"], "why_now": f"Fix before lower-priority issues", "expected_effect": f.get("recommended_fix", "")} for i, f in enumerate(findings)],
    }
    
    if verbose:
        total = sum(severity_counts.values())
        print(f"\n{'─'*50}\n✅ Audit complete. Found {total} issues in {time.time()-start:.1f}s:")
        for s in ["critical","high","medium","low"]: print(f"   {s.upper()}: {severity_counts[s]}")
        print(f"   Overall: {health}")
    
    return results

def save_results(results: dict, path: str = "audit_results.json") -> str:
    with open(path, "w") as f: json.dump(results, f, indent=2)
    return path

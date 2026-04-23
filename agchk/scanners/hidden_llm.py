"""Scan for hidden or secondary LLM calls that may bypass the main agent loop."""

import re
from pathlib import Path
from typing import Any, Dict, List

# Precompiled patterns
LLM_CALL_RE = re.compile(
    r"(?:chat\.create|messages\.create|completions\.create|llm\.invoke|"
    r"fallback.*llm|repair.*prompt|second.*pass|re-prompt|"
    r"openai\.chat|anthropic\.messages|vertexai\.predict|"
    r"bedrock.*invoke|model\.generate|completion\.create)",
    re.IGNORECASE,
)

MAIN_LOOP_RE = re.compile(
    r"(?:agent.*loop|main.*loop|orchestrat|chain.*run|agent.*run|"
    r"agent_executor|react.*loop|tool.*loop|cycle.*run)",
    re.IGNORECASE,
)

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", "test", "tests"}
SKIP_FILE_NAMES = {"main", "agent", "orchestrat", "chain"}
# Provider/adapter files that legitimately contain LLM calls — exclude from
# hidden-LLM detection. These are the infrastructure layer, not hidden loops.
SKIP_PROVIDER_RE = re.compile(
    r"(?:provider|adapter|client_factory|model_backend|llm_gateway)",
    re.IGNORECASE,
)
SCAN_EXTENSIONS = {".py", ".ts", ".js"}


def _should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def _is_skip_filename(name: str) -> bool:
    stem = name.lower().split(".")[0]
    return any(skip in stem for skip in SKIP_FILE_NAMES)


def scan_hidden_llm_calls(target: Path) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    has_main_loop = False
    llm_call_sites: List[tuple[Path, int, str]] = []

    files = [target] if target.is_file() else sorted(target.rglob("*"))

    for fp in files:
        if not fp.is_file() or _should_skip(fp) or fp.suffix not in SCAN_EXTENSIONS:
            continue
        if _is_skip_filename(fp.name):
            continue
        # Skip provider/adapter/adapter-like files — they legitimately contain
        # LLM calls as their purpose. Flagging them dilutes signal.
        if SKIP_PROVIDER_RE.search(fp.stem):
            continue

        try:
            lines = fp.read_text(encoding="utf-8", errors="ignore").splitlines()
        except (OSError, PermissionError):
            continue

        for lineno, line in enumerate(lines, start=1):
            if MAIN_LOOP_RE.search(line):
                has_main_loop = True
            if LLM_CALL_RE.search(line):
                llm_call_sites.append((fp, lineno, line.strip()[:120]))

    # Report hidden LLM calls found outside main loop files
    for fp, lineno, snippet in llm_call_sites:
        findings.append({
            "severity": "high",
            "title": "Hidden or secondary LLM call detected",
            "symptom": f"LLM API call found at {fp.name}:{lineno}: {snippet}",
            "user_impact": "Secondary LLM calls may bypass tool restrictions, safety checks, or cost controls defined in the main agent loop.",
            "source_layer": "llm_routing",
            "mechanism": f"Regex match for LLM call pattern outside main agent loop file.",
            "root_cause": "Additional LLM invocations exist outside the primary orchestration path, potentially unguarded.",
            "evidence_refs": [f"{fp}:{lineno}"],
            "confidence": 0.8,
            "fix_type": "code_change",
            "recommended_fix": "Consolidate all LLM calls through the main agent loop. If a secondary call is intentional, add explicit documentation, guardrails, and cost tracking.",
        })

    if not has_main_loop and llm_call_sites:
        findings.append({
            "severity": "high",
            "title": "No main agent loop pattern found",
            "symptom": "LLM calls detected but no recognized main loop (agent_loop, main_loop, orchestrator, chain_run) pattern.",
            "user_impact": "Without a clear orchestration loop, LLM calls may be scattered and uncoordinated, making it hard to enforce tool policies or cost limits.",
            "source_layer": "llm_routing",
            "mechanism": "No match for main loop patterns (agent.*loop, main.*loop, orchestrat, chain.*run).",
            "root_cause": "Missing or non-standard agent orchestration structure.",
            "evidence_refs": [f"{fp}:{lineno}" for fp, lineno, _ in llm_call_sites],
            "confidence": 0.7,
            "fix_type": "code_change",
            "recommended_fix": "Implement a clear main agent loop that centralizes all LLM invocations, tool routing, and policy enforcement.",
        })

    return findings

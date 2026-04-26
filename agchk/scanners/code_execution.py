"""Scan for unsafe code execution patterns (exec, eval, shell=True, etc.)."""

import ast
import re
from pathlib import Path
from typing import Any, Dict, List

from agchk.scanners.path_filters import iter_source_files, should_skip_path

# Precompiled patterns
# NOTE: Built-in `compile(...)` can still be risky, but `re.compile(...)`
# and other dotted variants are routine safe usage. Keep the pattern narrow
# so we only match direct builtin-style calls.
DANGEROUS_CALLS = {
    "exec(": re.compile(r"(?<!\.)\bexec\s*\("),
    "eval(": re.compile(r"(?<!\.)\beval\s*\("),
    "compile(": re.compile(r"(?<!\.)\bcompile\s*\("),
    "os.system(": re.compile(r"\bos\.system\s*\("),
    "new Function(": re.compile(r"\bnew\s+Function\s*\("),
}

SHELL_TRUE_RE = re.compile(r"subprocess\..*shell\s*=\s*True", re.IGNORECASE)

SANDBOX_RE = re.compile(
    r"(?:sandbox|docker|container|seccomp|chroot|\bvm\b|"
    r"subprocess.*timeout|resource\.setrlimit|jail|"
    r"nsjail|firejail|gvisor|kata)",
    re.IGNORECASE,
)

SCAN_EXTENSIONS = {".py", ".ts", ".js"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}


def _should_skip(path: Path) -> bool:
    return should_skip_path(path, SKIP_DIRS)


def _line_at(lines: list[str], lineno: int) -> str:
    if 1 <= lineno <= len(lines):
        return lines[lineno - 1].strip()[:100]
    return ""


def _imported_subprocess_calls(tree: ast.AST) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "subprocess":
            for alias in node.names:
                if alias.name in {"run", "call", "check_call", "check_output", "Popen"}:
                    names.add(alias.asname or alias.name)
    return names


def _is_subprocess_call(func: ast.AST, imported_subprocess_calls: set[str]) -> bool:
    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
        return func.value.id == "subprocess"
    if isinstance(func, ast.Name):
        return func.id in imported_subprocess_calls
    return False


def _has_shell_true(node: ast.Call) -> bool:
    for keyword in node.keywords:
        if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant):
            return keyword.value.value is True
    return False


def _finding(
    fp: Path, lines: list[str], lineno: int, pattern_name: str, has_sandbox: bool, mechanism: str
) -> Dict[str, Any]:
    severity = "critical" if pattern_name in ("exec(", "eval(", "subprocess(shell=True)", "os.system(") else "high"

    return {
        "severity": severity,
        "title": f"Unsafe code execution: {pattern_name}",
        "symptom": f"Found {pattern_name} at {fp.name}:{lineno}: {_line_at(lines, lineno)}",
        "user_impact": "Arbitrary code execution from untrusted input can lead to full system compromise, data exfiltration, or remote code execution.",
        "source_layer": "code_execution",
        "mechanism": mechanism,
        "root_cause": f"Use of {pattern_name} without proper input sanitization or sandboxing.",
        "evidence_refs": [f"{fp}:{lineno}"],
        "confidence": 0.65 if has_sandbox else 0.9,
        "fix_type": "code_change",
        "recommended_fix": (
            "Replace with safe alternatives: use ast.literal_eval instead of eval(), "
            "subprocess.run with list args instead of shell=True, or execute in an isolated sandbox "
            "(Docker, gVisor, nsjail) with resource limits and network disabled."
        ),
    }


def _scan_python_ast(fp: Path, content: str, lines: list[str], has_sandbox: bool) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []

    tree = ast.parse(content, filename=str(fp))
    imported_subprocess_calls = _imported_subprocess_calls(tree)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        pattern_name = None
        if isinstance(node.func, ast.Name) and node.func.id in {"exec", "eval", "compile"}:
            pattern_name = f"{node.func.id}("
        elif (
            isinstance(node.func, ast.Attribute)
            and node.func.attr == "system"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "os"
        ):
            pattern_name = "os.system("
        elif _is_subprocess_call(node.func, imported_subprocess_calls) and _has_shell_true(node):
            pattern_name = "subprocess(shell=True)"

        if pattern_name:
            findings.append(
                _finding(
                    fp,
                    lines,
                    getattr(node, "lineno", 1),
                    pattern_name,
                    has_sandbox,
                    f"AST call match for dangerous function: {pattern_name}",
                )
            )

    return findings


def _mask_string_literals(line: str) -> str:
    return re.sub(r"(['\"])(?:\\.|(?!\1).)*\1", '""', line)


def _scan_file(fp: Path) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []

    try:
        full_content = fp.read_text(encoding="utf-8", errors="ignore")
    except (OSError, PermissionError):
        return findings

    lines = full_content.splitlines()

    # Check for sandbox/safety patterns across the whole file
    has_sandbox = bool(SANDBOX_RE.search(full_content))

    if fp.suffix == ".py":
        try:
            return _scan_python_ast(fp, full_content, lines, has_sandbox)
        except SyntaxError:
            pass

    for lineno, line in enumerate(lines, start=1):
        scan_line = _mask_string_literals(line.split("#", 1)[0] if fp.suffix == ".py" else line)
        matched_pattern = None
        pattern_name = None

        # Check dangerous function calls
        for name, pat in DANGEROUS_CALLS.items():
            if pat.search(scan_line):
                matched_pattern = pat
                pattern_name = name
                break

        # Check subprocess shell=True
        if not matched_pattern and SHELL_TRUE_RE.search(scan_line):
            pattern_name = "subprocess(shell=True)"

        if pattern_name:
            findings.append(
                _finding(
                    fp,
                    lines,
                    lineno,
                    pattern_name,
                    has_sandbox,
                    f"Text match outside Python comments/strings for dangerous function: {pattern_name}",
                )
            )

    return findings


def scan_code_execution(target: Path) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []

    files = list(iter_source_files(target))

    for fp in files:
        if not fp.is_file() or _should_skip(fp) or fp.suffix not in SCAN_EXTENSIONS:
            continue
        findings.extend(_scan_file(fp))

    return findings

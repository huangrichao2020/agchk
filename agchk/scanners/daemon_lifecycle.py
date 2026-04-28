"""Scan always-on agent daemons for restart, drain, and recovery safeguards."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List

from agchk.scanners.path_filters import iter_source_files, should_skip_path

SCAN_EXTENSIONS = {
    ".py",
    ".ts",
    ".js",
    ".tsx",
    ".jsx",
    ".md",
    ".sh",
    ".bash",
    ".zsh",
    ".yaml",
    ".yml",
    ".toml",
    ".json",
    ".service",
    ".plist",
}
SKIP_DIRS = {".git", ".github", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", "coverage"}
MAX_FILE_BYTES = 250_000

DAEMON_RE = re.compile(
    r"\b(?:daemon|gateway|watchdog|run_forever|always[-_ ]?on|service|systemd|launchagent|pm2|supervisor|"
    r"detached|pid[_ -]?file|background worker|heartbeat)\b",
    re.IGNORECASE,
)
RESTART_RE = re.compile(
    r"\b(?:restart|reload|replace|respawn|crash|backoff|SIGTERM|SIGKILL|kill\s+-|terminate)\b", re.IGNORECASE
)
ACTIVE_WORK_RE = re.compile(
    r"\b(?:active[_ -]?(?:agents|runs|jobs|tasks|sessions)|running[_ -]?(?:jobs|tasks|sessions)|"
    r"job[_ -]?queue|task[_ -]?queue|inflight|in[-_ ]?flight|pending[_ -]?jobs|session[_ -]?state)\b",
    re.IGNORECASE,
)
DRAIN_RE = re.compile(
    r"\b(?:drain|graceful[_ -]?(?:shutdown|restart|stop)|quiesce|wait[_ -]?for[_ -]?(?:idle|jobs)|"
    r"stop[_ -]?accepting|pre[_ -]?restart|restart[_ -]?barrier|safe[_ -]?restart)\b",
    re.IGNORECASE,
)
RECOVERY_RE = re.compile(
    r"\b(?:checkpoint|resume|recover|replay|journal|side[-_ ]?effect[_ -]?log|operation[_ -]?log|"
    r"idempotent|session[_ -]?replay|state[_ -]?restore|crash[_ -]?recovery)\b",
    re.IGNORECASE,
)
CHANNEL_VERIFY_RE = re.compile(
    r"\b(?:connected|health[_ -]?check|status|ready|readiness|websocket|gateway[_ -]?state|post[_ -]?restart)\b",
    re.IGNORECASE,
)
SELF_RESTART_TARGET_RE = re.compile(r"\b(?:agent|assistant|bot|gateway|daemon|service|worker)\b", re.IGNORECASE)
SELF_RESTART_COMMAND_RE = re.compile(
    r"\b(?:systemctl\s+(?:restart|try-restart|reload-or-restart|stop|kill)\b|"
    r"service\s+\S+\s+(?:restart|stop)\b|"
    r"pm2\s+restart\b|"
    r"launchctl\s+(?:kickstart|bootout)\b)",
    re.IGNORECASE,
)
SHELL_EXECUTION_CONTEXT_RE = re.compile(
    r"\b(?:subprocess\.(?:run|call|Popen)|os\.system|terminal\s*\(|execute_code|shell\s*=|"
    r"command\s*=|spawn\s*\(|exec\s*\(|run_command|execute_shell)\b",
    re.IGNORECASE,
)
SAFE_EXTERNAL_RESTART_RE = re.compile(
    r"\b(?:systemd-run|transient unit|--on-active|at\s+now|external supervisor|service manager|"
    r"supervisor handoff|restart_requested|request_restart|exit code\s+75|EX_TEMPFAIL)\b",
    re.IGNORECASE,
)
DIRECT_SHELL_EXTENSIONS = {".sh", ".bash", ".zsh", ".service"}


def _should_skip(path: Path) -> bool:
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return True
    except OSError:
        return True
    return should_skip_path(path, SKIP_DIRS)


def _looks_like_self_restart_line(fp: Path, line: str, context: str = "") -> bool:
    if SAFE_EXTERNAL_RESTART_RE.search(line):
        return False
    if not SELF_RESTART_COMMAND_RE.search(line):
        return False
    if not SELF_RESTART_TARGET_RE.search(line):
        return False
    return fp.suffix in DIRECT_SHELL_EXTENSIONS or bool(SHELL_EXECUTION_CONTEXT_RE.search(line + "\n" + context))


def _collect_refs(target: Path) -> dict[str, list[str]]:
    refs = {key: [] for key in ("daemon", "restart", "active", "drain", "recovery", "verify", "self_restart")}
    files = list(iter_source_files(target))
    for fp in files:
        if not fp.is_file() or _should_skip(fp) or fp.suffix not in SCAN_EXTENSIONS:
            continue
        try:
            lines = fp.read_text(encoding="utf-8", errors="ignore").splitlines()
        except (OSError, PermissionError):
            continue
        for lineno, line in enumerate(lines, start=1):
            ref = f"{fp}:{lineno}"
            if DAEMON_RE.search(line):
                refs["daemon"].append(ref)
            if RESTART_RE.search(line):
                refs["restart"].append(ref)
            if ACTIVE_WORK_RE.search(line):
                refs["active"].append(ref)
            if DRAIN_RE.search(line):
                refs["drain"].append(ref)
            if RECOVERY_RE.search(line):
                refs["recovery"].append(ref)
            if CHANNEL_VERIFY_RE.search(line):
                refs["verify"].append(ref)
            context_window = "\n".join(lines[max(0, lineno - 4) : min(len(lines), lineno + 3)])
            if _looks_like_self_restart_line(fp, line, context_window):
                refs["self_restart"].append(ref)
    return refs


def _evidence(refs: dict[str, list[str]], *keys: str, limit: int = 9) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for key in keys:
        for ref in refs.get(key, []):
            if ref not in seen:
                out.append(ref)
                seen.add(ref)
            if len(out) >= limit:
                return out
    return out


def scan_daemon_lifecycle(target: Path) -> List[Dict[str, Any]]:
    refs = _collect_refs(target)
    if not refs["self_restart"] and (len(refs["daemon"]) < 2 or not refs["restart"]):
        return []

    findings: list[dict[str, Any]] = []
    if refs["self_restart"]:
        findings.append(
            {
                "severity": "critical",
                "title": "Self-restart can kill its own control plane",
                "symptom": (
                    "Detected an agent/gateway restart path that may run service stop/restart commands from inside "
                    "the same long-lived agent process."
                ),
                "user_impact": (
                    "A self-stop or in-cgroup service restart can kill the active turn before the matching start "
                    "or recovery step runs, leaving the user with a silent stopped agent."
                ),
                "source_layer": "daemon_lifecycle",
                "mechanism": (
                    "Repository scan for in-process systemctl/service/pm2/launchctl restart commands targeting "
                    "agent, gateway, daemon, service, bot, or worker runtimes without an external restart handoff."
                ),
                "root_cause": (
                    "The restart executor appears coupled to the control plane it is trying to replace, instead of "
                    "delegating restart work to an external supervisor or detached service-manager job."
                ),
                "evidence_refs": _evidence(refs, "self_restart", "daemon", "restart"),
                "confidence": 0.82,
                "fix_type": "architecture_change",
                "recommended_fix": (
                    "Route self-restart requests through an external supervisor or service-manager job such as a "
                    "transient systemd unit, exit-code handoff, or durable restart request. The agent turn should "
                    "return before the old process is stopped, and startup must verify the new PID and channels."
                ),
            }
        )

    if len(refs["daemon"]) < 2 or not refs["restart"]:
        return findings

    guard_categories = {
        "active_work_check": refs["active"],
        "drain_protocol": refs["drain"],
        "recovery_checkpoint": refs["recovery"],
        "post_restart_verification": refs["verify"],
    }
    present = {name: values for name, values in guard_categories.items() if values}
    if len(present) >= 3:
        return findings

    present_summary = ", ".join(sorted(present)) if present else "none"
    severity = "high" if refs["active"] or len(refs["daemon"]) >= 4 else "medium"
    findings.append(
        {
            "severity": severity,
            "title": "Daemon restart lacks active-work drain protocol",
            "symptom": (
                f"Detected daemon/gateway restart behavior, but only {len(present)} restart-safety categories were "
                f"visible ({present_summary})."
            ),
            "user_impact": (
                "Restarting an always-on agent without checking active runs can interrupt in-flight work, lose partial "
                "optimization or tool state, and leave the user unsure whether channels reconnected correctly."
            ),
            "source_layer": "daemon_lifecycle",
            "mechanism": (
                "Repository scan for daemon/restart behavior versus active-work checks, graceful drain, recovery "
                "checkpoints, and post-restart health verification."
            ),
            "root_cause": "The runtime appears to support long-lived execution before defining a safe restart lifecycle.",
            "evidence_refs": _evidence(refs, "daemon", "restart", "active", "drain", "recovery", "verify"),
            "confidence": 0.7,
            "fix_type": "architecture_change",
            "recommended_fix": (
                "Add a restart contract: inspect active agents/jobs first, stop accepting new work, drain or checkpoint "
                "in-flight runs, restart with old/new PID and log evidence, then verify messaging channels and gateway "
                "health before declaring success."
            ),
        }
    )
    return findings

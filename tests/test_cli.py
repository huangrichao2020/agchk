from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def _write_project(root: Path, code: str) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / "agent.py").write_text(code, encoding="utf-8")
    return root


def _cli_env() -> dict[str, str]:
    env = os.environ.copy()
    repo_root = str(Path(__file__).resolve().parents[1])
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = repo_root if not existing else f"{repo_root}{os.pathsep}{existing}"
    return env


def test_cli_accepts_direct_target_path_and_writes_outputs(tmp_path: Path) -> None:
    project = _write_project(
        tmp_path / "project",
        "import subprocess\nsubprocess.run(command, shell=True)\n",
    )
    json_output = tmp_path / "audit.json"
    report_output = tmp_path / "audit.md"
    sarif_output = tmp_path / "audit.sarif.json"

    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "agchk.cli",
            str(project),
            "--profile",
            "enterprise",
            "-o",
            str(json_output),
            "-r",
            str(report_output),
            "--sarif",
            str(sarif_output),
        ],
        capture_output=True,
        text=True,
        cwd=tmp_path,
        env=_cli_env(),
    )

    assert proc.returncode == 0, proc.stderr
    assert json_output.exists()
    assert report_output.exists()
    assert sarif_output.exists()

    data = json.loads(json_output.read_text(encoding="utf-8"))
    assert data["scan_metadata"]["profile"] == "enterprise_production"


def test_cli_can_fail_ci_on_severity_threshold(tmp_path: Path) -> None:
    project = _write_project(
        tmp_path / "project",
        "import subprocess\nsubprocess.run(command, shell=True)\n",
    )

    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "agchk.cli",
            "audit",
            str(project),
            "--profile",
            "enterprise",
            "--fail-on",
            "high",
        ],
        capture_output=True,
        text=True,
        cwd=tmp_path,
        env=_cli_env(),
    )

    assert proc.returncode == 1

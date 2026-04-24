from __future__ import annotations

from pathlib import Path

from agchk.audit import run_audit
from agchk.config import AuditConfig
from agchk.schema import validate_report


def test_run_audit_produces_schema_valid_report(tmp_path: Path) -> None:
    (tmp_path / "agent.py").write_text(
        "import subprocess\nsubprocess.run(command, shell=True)\n",
        encoding="utf-8",
    )

    results = run_audit(
        str(tmp_path),
        config=AuditConfig.from_profile("enterprise"),
        verbose=False,
    )

    assert validate_report(results) == []
    assert results["schema_version"] == "agchk.report.v1"
    assert results["executive_verdict"]["overall_health"] in {
        "critical",
        "high_risk",
        "unstable",
        "acceptable",
        "strong",
    }
    assert results["scope"]["target_name"] == str(tmp_path)
    assert results["scope"]["layers_to_audit"]
    assert results["severity_summary"]["critical"] >= 1
    assert results["evidence_pack"]


def test_run_audit_scope_ignores_dependency_entrypoints(tmp_path: Path) -> None:
    site_package = tmp_path / ".venv" / "lib" / "python3.12" / "site-packages" / "dependency"
    site_package.mkdir(parents=True)
    (site_package / "main.py").write_text("print('dependency')\n", encoding="utf-8")
    (tmp_path / "app.py").write_text("print('project')\n", encoding="utf-8")

    results = run_audit(
        str(tmp_path),
        config=AuditConfig.from_profile("personal"),
        verbose=False,
    )

    assert results["scope"]["entrypoints"] == [str(tmp_path / "app.py")]

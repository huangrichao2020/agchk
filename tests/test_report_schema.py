from __future__ import annotations

from pathlib import Path

from agchk.audit import run_audit
from agchk.schema import validate_report


def test_run_audit_produces_schema_valid_report(tmp_path: Path) -> None:
    (tmp_path / "agent.py").write_text(
        "import subprocess\nsubprocess.run(command, shell=True)\n",
        encoding="utf-8",
    )

    results = run_audit(str(tmp_path), verbose=False)

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

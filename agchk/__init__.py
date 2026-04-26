"""agchk — Audit any AI agent system architecture.

The base model rarely fails. The wrapper architecture corrupts good answers into bad behavior.

Usage:
    from agchk import run_audit, generate_report

    results = run_audit("/path/to/your/agent/project")
    print(generate_report(results))
"""

__version__ = "1.0.1"

from agchk.audit import run_audit, save_results
from agchk.contribute import prepare_contribution_bundle, publish_bundle_to_upstream
from agchk.report import generate_report
from agchk.sarif import generate_sarif, save_sarif

__all__ = [
    "run_audit",
    "generate_report",
    "generate_sarif",
    "prepare_contribution_bundle",
    "publish_bundle_to_upstream",
    "save_results",
    "save_sarif",
]

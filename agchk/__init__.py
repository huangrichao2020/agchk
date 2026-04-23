"""agchk — Audit any AI agent system architecture.

The base model rarely fails. The wrapper architecture corrupts good answers into bad behavior.

Usage:
    from agchk import run_audit, generate_report

    results = run_audit("/path/to/your/agent/project")
    print(generate_report(results))
"""

__version__ = "0.1.0"

from agchk.audit import run_audit, save_results
from agchk.report import generate_report

__all__ = ["run_audit", "generate_report", "save_results"]

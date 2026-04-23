"""JSON Schema and validation for audit reports."""
import json
from importlib.resources import files
from typing import Dict, Any

REPORT_SCHEMA = json.loads(files("agchk").joinpath("schema.json").read_text())


def validate_report(report: Dict[str, Any]) -> list:
    errors = []
    for field in ["schema_version", "overall_health", "findings"]:
        if field not in report:
            errors.append(f"Missing required field: {field}")
    for i, finding in enumerate(report.get("findings", [])):
        for req in ["severity", "title", "source_layer", "mechanism", "recommended_fix"]:
            if req not in finding:
                errors.append(f"Finding {i}: missing '{req}'")
        if finding.get("severity") not in ("critical", "high", "medium", "low"):
            errors.append(f"Finding {i}: invalid severity")
    return errors

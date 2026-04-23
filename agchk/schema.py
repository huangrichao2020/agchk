"""JSON Schema and validation for audit reports."""
import json
from pathlib import Path
from typing import Dict, Any

SCHEMA_PATH = Path(__file__).parent / "schema.json"
with open(SCHEMA_PATH) as f:
    REPORT_SCHEMA = json.load(f)

def validate_report(report: Dict[str, Any]) -> list:
    errors = []
    for field in ["schema_version", "overall_health", "findings"]:
        if field not in report: errors.append(f"Missing required field: {field}")
    for i, finding in enumerate(report.get("findings", [])):
        for req in ["severity", "title", "source_layer", "mechanism", "recommended_fix"]:
            if req not in finding: errors.append(f"Finding {i}: missing '{req}'")
        if finding.get("severity") not in ("critical","high","medium","low"):
            errors.append(f"Finding {i}: invalid severity")
    return errors

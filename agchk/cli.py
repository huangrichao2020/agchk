"""CLI entry point for agchk."""
import sys, json
from agchk.audit import run_audit, save_results
from agchk.report import generate_report
from agchk.schema import validate_report

def main():
    if len(sys.argv) < 2:
        print("Usage: agchk /path/to/your/agent/project")
        print("       agchk --report audit_results.json")
        sys.exit(1)
    
    if sys.argv[1] == "--report":
        if len(sys.argv) < 3:
            print("Usage: agchk --report audit_results.json")
            sys.exit(1)
        with open(sys.argv[2]) as f: results = json.load(f)
        print(generate_report(results))
        return
    
    target = sys.argv[1]
    results = run_audit(target)
    save_results(results)
    md = generate_report(results, "audit_report.md")
    print(f"\n📋 Results: audit_results.json")
    print(f"📄 Report: audit_report.md")

if __name__ == "__main__":
    main()

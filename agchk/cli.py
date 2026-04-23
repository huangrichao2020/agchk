"""CLI entry point for agchk."""
import argparse
import json
import sys

from agchk import __version__
from agchk.audit import run_audit, save_results
from agchk.report import generate_report
from agchk.schema import validate_report


def cmd_audit(args):
    """Run audit against target directory."""
    results = run_audit(args.target, verbose=not args.quiet)
    save_results(results, args.output)
    md = generate_report(results, args.report)
    if not args.quiet:
        print(f"\n📋 Results: {args.output}")
        print(f"📄 Report: {args.report}")


def cmd_report(args):
    """Generate markdown report from JSON results."""
    with open(args.input) as f:
        results = json.load(f)

    errors = validate_report(results)
    if errors:
        print("⚠️  Schema validation errors:")
        for e in errors:
            print(f"  - {e}")
        print()

    md = generate_report(results)
    if args.output:
        with open(args.output, "w") as f:
            f.write(md)
        print(f"Report saved to: {args.output}")
    else:
        print(md)


def main():
    parser = argparse.ArgumentParser(
        prog="agchk",
        description="Audit the architecture and health of any AI agent system or LLM-integrated project.",
        epilog="Examples:\n"
               "  agchk /path/to/your/agent/project\n"
               "  agchk --report audit_results.json\n"
               "  agchk --validate audit_results.json\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=f"agchk {__version__}")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed output")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress progress output")
    parser.add_argument("--output", "-o", default="audit_results.json", help="Output JSON file (default: audit_results.json)")
    parser.add_argument("--report", "-r", default="audit_report.md", help="Report markdown file (default: audit_report.md)")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # audit subcommand
    audit_parser = subparsers.add_parser("audit", help="Run audit against target directory")
    audit_parser.add_argument("target", help="Path to agent project directory")
    audit_parser.add_argument("-o", "--output", default="audit_results.json", help="Output JSON file")
    audit_parser.add_argument("-r", "--report", default="audit_report.md", help="Report markdown file")
    audit_parser.add_argument("-q", "--quiet", action="store_true", help="Suppress progress output")
    audit_parser.set_defaults(func=cmd_audit)

    # report subcommand
    report_parser = subparsers.add_parser("report", help="Generate report from JSON results")
    report_parser.add_argument("input", help="Input JSON results file")
    report_parser.add_argument("-o", "--output", help="Output markdown file (prints to stdout if omitted)")
    report_parser.set_defaults(func=cmd_report)

    # validate subcommand
    validate_parser = subparsers.add_parser("validate", help="Validate audit results against schema")
    validate_parser.add_argument("input", help="JSON results file to validate")
    validate_parser.set_defaults(func=lambda args: cmd_validate(args))

    args = parser.parse_args()

    # Handle positional target argument (backward compatible with `agchk /path`)
    if not hasattr(args, "func"):
        # Check if first non-flag argument looks like a path
        if len(sys.argv) >= 2 and not sys.argv[1].startswith("-"):
            # Treat as audit command
            args.target = sys.argv[1]
            args.command = "audit"
            args.func = cmd_audit
            if not hasattr(args, "output"):
                args.output = "audit_results.json"
            if not hasattr(args, "report"):
                args.report = "audit_report.md"
        else:
            parser.print_help()
            sys.exit(0)

    args.func(args)


def cmd_validate(args):
    """Validate audit results against JSON schema."""
    with open(args.input) as f:
        results = json.load(f)

    errors = validate_report(results)
    if errors:
        print(f"❌ Schema validation failed ({len(errors)} errors):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("✅ Schema validation passed")


if __name__ == "__main__":
    main()

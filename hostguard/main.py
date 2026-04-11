import argparse
import sys

from hostguard.checks.firewall_checks import FirewallEnabledCheck
from hostguard.checks.password_policy_checks import PasswordPolicyCheck
from hostguard.checks.permissions_checks import WorldWritableEtcCheck
from hostguard.checks.service_checks import LegacyServicesCheck
from hostguard.checks.ssh_checks import SSHRootLoginCheck
from hostguard.models import CheckResult
from hostguard.reporting.html_report import write_html_report
from hostguard.reporting.json_report import write_json_report


def run_all_checks() -> list[CheckResult]:
    checks = [
        SSHRootLoginCheck(),
        FirewallEnabledCheck(),
        PasswordPolicyCheck(),
        LegacyServicesCheck(),
        WorldWritableEtcCheck(),
    ]

    results: list[CheckResult] = []
    for check in checks:
        results.extend(check.run())

    return results


def print_results(results: list[CheckResult]) -> None:
    print("\nHostGuard Security Audit Results")
    print("=" * 40)

    for result in results:
        print(f"[{result.status}] {result.check_id} - {result.check_name}")
        print(f"  {result.message}")
        if result.remediation:
            print(f"  Remediation: {result.remediation}")
        print()

    total = len(results)
    passed = sum(1 for r in results if r.status == "PASS")
    failed = sum(1 for r in results if r.status == "FAIL")
    warned = sum(1 for r in results if r.status == "WARN")
    errored = sum(1 for r in results if r.status == "ERROR")

    print("=" * 40)
    print(f"Total: {total} | PASS: {passed} | FAIL: {failed} | WARN: {warned} | ERROR: {errored}")


def main() -> int:
    parser = argparse.ArgumentParser(description="HostGuard Linux security baseline auditor")
    parser.add_argument(
        "--json-out",
        help="Path to save JSON report, for example reports/report.json",
    )
    parser.add_argument(
        "--html-out",
        help="Path to save HTML report, for example reports/report.html",
    )
    args = parser.parse_args()

    results = run_all_checks()
    print_results(results)

    if args.json_out:
        write_json_report(results, args.json_out)
        print(f"\nJSON report written to: {args.json_out}")

    if args.html_out:
        write_html_report(results, args.html_out)
        print(f"HTML report written to: {args.html_out}")

    has_failures_or_errors = any(result.status in {"FAIL", "ERROR"} for result in results)
    return 1 if has_failures_or_errors else 0


if __name__ == "__main__":
    sys.exit(main())
import sys

from pathlib import Path

from hostguard.checks.password_policy_checks import PasswordPolicyCheck
from hostguard.checks.ssh_checks import SSHRootLoginCheck
from hostguard.main import main
from hostguard.models import CheckResult


def test_ssh_root_login_uses_first_matching_directive(monkeypatch):
    monkeypatch.setattr(Path, "exists", lambda self: True)

    config = """
    PermitRootLogin yes
    PermitRootLogin no
    """
    monkeypatch.setattr(SSHRootLoginCheck, "read_text_file", lambda self, path: config)

    results = SSHRootLoginCheck().run()

    assert len(results) == 1
    assert results[0].status == "FAIL"
    assert "yes" in results[0].message


def test_main_returns_nonzero_for_error_results(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["hostguard"])
    monkeypatch.setattr(
        "hostguard.main.run_all_checks",
        lambda: [
            CheckResult(
                check_id="TEST-001",
                check_name="Example",
                status="ERROR",
                message="Unable to inspect system state.",
            )
        ],
    )
    monkeypatch.setattr("hostguard.main.print_results", lambda results: None)

    assert main() == 1


def test_password_policy_checks_min_days(monkeypatch):
    monkeypatch.setattr(Path, "exists", lambda self: True)

    config = """
    PASS_MAX_DAYS 90
    PASS_MIN_DAYS 0
    PASS_WARN_AGE 7
    """
    monkeypatch.setattr(PasswordPolicyCheck, "read_text_file", lambda self, path: config)

    results = PasswordPolicyCheck().run()

    min_days_result = next(result for result in results if "PASS_MIN_DAYS" in result.message)

    assert min_days_result.status == "FAIL"
    assert "0" in min_days_result.message

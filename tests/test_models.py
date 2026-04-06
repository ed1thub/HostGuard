from hostguard.models import CheckResult


def test_checkresult_to_dict():
    result = CheckResult(
        check_id="TEST-001",
        check_name="Example Check",
        status="PASS",
        message="Everything looks good.",
        remediation=None,
    )

    data = result.to_dict()

    assert data["check_id"] == "TEST-001"
    assert data["status"] == "PASS"
    assert data["message"] == "Everything looks good."
from pathlib import Path
from typing import List

from hostguard.checks.base import BaseCheck
from hostguard.models import CheckResult


class PasswordPolicyCheck(BaseCheck):
    check_id = "PWD-001"
    check_name = "Password Aging Policy"

    def run(self) -> List[CheckResult]:
        login_defs = Path("/etc/login.defs")

        if not login_defs.exists():
            return [
                self.result(
                    "WARN",
                    "/etc/login.defs not found.",
                    "Verify password policy files are present on this system.",
                )
            ]

        try:
            content = self.read_text_file(str(login_defs))
        except Exception as exc:
            return [
                self.result(
                    "ERROR",
                    f"Could not read /etc/login.defs: {exc}",
                    "Run the tool with sufficient permissions.",
                )
            ]

        values = {}
        keys_to_capture = {"PASS_MAX_DAYS", "PASS_MIN_DAYS", "PASS_WARN_AGE"}

        for raw_line in content.splitlines():
            line = raw_line.split("#", 1)[0].strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) >= 2 and parts[0] in keys_to_capture:
                values[parts[0]] = parts[1]

        results: List[CheckResult] = []

        max_days = values.get("PASS_MAX_DAYS")
        if max_days is None:
            results.append(
                self.result(
                    "WARN",
                    "PASS_MAX_DAYS is not set.",
                    "Set PASS_MAX_DAYS to 90 or less.",
                )
            )
        else:
            try:
                if int(max_days) <= 90:
                    results.append(self.result("PASS", f"PASS_MAX_DAYS is {max_days}."))
                else:
                    results.append(
                        self.result(
                            "FAIL",
                            f"PASS_MAX_DAYS is {max_days}.",
                            "Set PASS_MAX_DAYS to 90 or less.",
                        )
                    )
            except ValueError:
                results.append(
                    self.result(
                        "ERROR",
                        f"PASS_MAX_DAYS is not numeric: {max_days}",
                        "Correct the value in /etc/login.defs.",
                    )
                )

            min_days = values.get("PASS_MIN_DAYS")
            if min_days is None:
                results.append(
                    self.result(
                        "WARN",
                        "PASS_MIN_DAYS is not set.",
                        "Set PASS_MIN_DAYS to at least 1.",
                    )
                )
            else:
                try:
                    if int(min_days) >= 1:
                        results.append(self.result("PASS", f"PASS_MIN_DAYS is {min_days}."))
                    else:
                        results.append(
                            self.result(
                                "FAIL",
                                f"PASS_MIN_DAYS is {min_days}.",
                                "Set PASS_MIN_DAYS to at least 1.",
                            )
                        )
                except ValueError:
                    results.append(
                        self.result(
                            "ERROR",
                            f"PASS_MIN_DAYS is not numeric: {min_days}",
                            "Correct the value in /etc/login.defs.",
                        )
                    )

        warn_age = values.get("PASS_WARN_AGE")
        if warn_age is None:
            results.append(
                self.result(
                    "WARN",
                    "PASS_WARN_AGE is not set.",
                    "Set PASS_WARN_AGE to at least 7.",
                )
            )
        else:
            try:
                if int(warn_age) >= 7:
                    results.append(self.result("PASS", f"PASS_WARN_AGE is {warn_age}."))
                else:
                    results.append(
                        self.result(
                            "FAIL",
                            f"PASS_WARN_AGE is {warn_age}.",
                            "Set PASS_WARN_AGE to at least 7.",
                        )
                    )
            except ValueError:
                results.append(
                    self.result(
                        "ERROR",
                        f"PASS_WARN_AGE is not numeric: {warn_age}",
                        "Correct the value in /etc/login.defs.",
                    )
                )

        return results
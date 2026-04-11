from pathlib import Path
from typing import List

from hostguard.checks.base import BaseCheck
from hostguard.models import CheckResult


class SSHRootLoginCheck(BaseCheck):
    check_id = "SSH-001"
    check_name = "SSH Root Login Disabled"

    def run(self) -> List[CheckResult]:
        sshd_config = Path("/etc/ssh/sshd_config")

        if not sshd_config.exists():
            return [
                self.result(
                    "WARN",
                    "/etc/ssh/sshd_config not found.",
                    "Verify SSH server is installed and configuration file exists.",
                )
            ]

        try:
            content = self.read_text_file(str(sshd_config))
        except Exception as exc:
            return [
                self.result(
                    "ERROR",
                    f"Could not read sshd_config: {exc}",
                    "Run the tool with sufficient permissions.",
                )
            ]

        permit_root_login = None

        for raw_line in content.splitlines():
            line = raw_line.split("#", 1)[0].strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) >= 2 and parts[0].lower() == "permitrootlogin":
                permit_root_login = parts[1].lower()
                break

        if permit_root_login is None:
            return [
                self.result(
                    "WARN",
                    "PermitRootLogin is not explicitly set in sshd_config.",
                    "Set 'PermitRootLogin no' in /etc/ssh/sshd_config.",
                )
            ]

        if permit_root_login == "no":
            return [self.result("PASS", "SSH root login is disabled.")]

        return [
            self.result(
                "FAIL",
                f"SSH root login is set to '{permit_root_login}'.",
                "Set 'PermitRootLogin no' and restart the SSH service.",
            )
        ]
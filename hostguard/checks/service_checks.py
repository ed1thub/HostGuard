from typing import List

from hostguard.checks.base import BaseCheck
from hostguard.models import CheckResult


class LegacyServicesCheck(BaseCheck):
    check_id = "SVC-001"
    check_name = "Legacy Insecure Services Disabled"

    SERVICES = [
        "telnet",
        "telnet.socket",
        "vsftpd",
        "rsh.socket",
        "rexec.socket",
    ]

    def run(self) -> List[CheckResult]:
        active_services = []

        for service in self.SERVICES:
            try:
                result = self.run_command(["systemctl", "is-active", service])
                if result.stdout.strip() == "active":
                    active_services.append(service)
            except Exception:
                continue

        if active_services:
            return [
                self.result(
                    "FAIL",
                    f"Active insecure services detected: {', '.join(active_services)}",
                    "Disable and remove unnecessary legacy services.",
                )
            ]

        return [self.result("PASS", "No active insecure legacy services detected.")]
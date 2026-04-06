from typing import List

from hostguard.checks.base import BaseCheck
from hostguard.models import CheckResult


class FirewallEnabledCheck(BaseCheck):
    check_id = "FW-001"
    check_name = "Firewall Enabled"

    def run(self) -> List[CheckResult]:
        try:
            ufw_result = self.run_command(["ufw", "status"])
            ufw_output = (ufw_result.stdout + ufw_result.stderr).lower()
            if "status: active" in ufw_output:
                return [self.result("PASS", "UFW firewall is active.")]
        except Exception:
            pass

        try:
            firewalld_result = self.run_command(["systemctl", "is-active", "firewalld"])
            if firewalld_result.stdout.strip() == "active":
                return [self.result("PASS", "firewalld is active.")]
        except Exception:
            pass

        try:
            nft_result = self.run_command(["systemctl", "is-active", "nftables"])
            if nft_result.stdout.strip() == "active":
                return [self.result("PASS", "nftables service is active.")]
        except Exception:
            pass

        return [
            self.result(
                "FAIL",
                "No active host firewall was detected.",
                "Enable UFW, firewalld, or nftables.",
            )
        ]
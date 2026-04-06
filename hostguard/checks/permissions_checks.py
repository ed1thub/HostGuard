import os
import stat
from typing import List

from hostguard.checks.base import BaseCheck
from hostguard.models import CheckResult


class WorldWritableEtcCheck(BaseCheck):
    check_id = "PERM-001"
    check_name = "No World-Writable Files Under /etc"

    def run(self) -> List[CheckResult]:
        findings = []

        for root, _, files in os.walk("/etc"):
            for name in files:
                path = os.path.join(root, name)
                try:
                    file_stat = os.stat(path, follow_symlinks=False)
                    if stat.S_ISREG(file_stat.st_mode) and (file_stat.st_mode & stat.S_IWOTH):
                        findings.append(path)
                except (PermissionError, FileNotFoundError, OSError):
                    continue

        if findings:
            preview = ", ".join(findings[:5])
            extra = ""
            if len(findings) > 5:
                extra = f" ... and {len(findings) - 5} more"

            return [
                self.result(
                    "FAIL",
                    f"World-writable files found under /etc: {preview}{extra}",
                    "Remove world-write permissions from sensitive files.",
                )
            ]

        return [self.result("PASS", "No world-writable regular files found under /etc.")]
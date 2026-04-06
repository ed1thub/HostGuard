import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from hostguard.models import CheckResult


class BaseCheck(ABC):
    check_id = "BASE"
    check_name = "Base Check"

    @abstractmethod
    def run(self) -> List[CheckResult]:
        raise NotImplementedError

    def read_text_file(self, path: str) -> str:
        return Path(path).read_text(encoding="utf-8", errors="ignore")

    def run_command(self, command: list[str]) -> subprocess.CompletedProcess:
        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )

    def result(self, status: str, message: str, remediation: str | None = None) -> CheckResult:
        return CheckResult(
            check_id=self.check_id,
            check_name=self.check_name,
            status=status,
            message=message,
            remediation=remediation,
        )
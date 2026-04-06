from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class CheckResult:
    check_id: str
    check_name: str
    status: str
    message: str
    remediation: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)
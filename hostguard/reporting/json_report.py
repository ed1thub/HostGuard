import json
from datetime import datetime, UTC
from pathlib import Path

from hostguard.models import CheckResult


def write_json_report(results: list[CheckResult], output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "summary": {
            "total": len(results),
            "pass": sum(1 for r in results if r.status == "PASS"),
            "fail": sum(1 for r in results if r.status == "FAIL"),
            "warn": sum(1 for r in results if r.status == "WARN"),
            "error": sum(1 for r in results if r.status == "ERROR"),
        },
        "results": [result.to_dict() for result in results],
    }

    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
from datetime import UTC, datetime
from html import escape
from pathlib import Path

from hostguard.models import CheckResult


def status_class(status: str) -> str:
    mapping = {
        "PASS": "status-pass",
        "FAIL": "status-fail",
        "WARN": "status-warn",
        "ERROR": "status-error",
    }
    return mapping.get(status, "status-unknown")


def build_summary(results: list[CheckResult]) -> dict[str, int]:
    return {
        "total": len(results),
        "pass": sum(1 for r in results if r.status == "PASS"),
        "fail": sum(1 for r in results if r.status == "FAIL"),
        "warn": sum(1 for r in results if r.status == "WARN"),
        "error": sum(1 for r in results if r.status == "ERROR"),
    }


def render_result_card(result: CheckResult) -> str:
    remediation_html = ""
    if result.remediation:
        remediation_html = f"""
        <div class="remediation">
            <strong>Remediation:</strong> {escape(result.remediation)}
        </div>
        """

    return f"""
    <div class="result-card">
        <div class="result-header">
            <span class="check-id">{escape(result.check_id)}</span>
            <span class="status-badge {status_class(result.status)}">{escape(result.status)}</span>
        </div>
        <h3>{escape(result.check_name)}</h3>
        <p>{escape(result.message)}</p>
        {remediation_html}
    </div>
    """


def write_html_report(results: list[CheckResult], output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    summary = build_summary(results)
    generated_at = datetime.now(UTC).isoformat()
    cards_html = "\n".join(render_result_card(result) for result in results)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HostGuard Security Audit Report</title>
    <style>
        :root {{
            --bg: #0f172a;
            --panel: #111827;
            --panel-2: #1f2937;
            --text: #e5e7eb;
            --muted: #9ca3af;
            --border: #374151;
            --pass: #22c55e;
            --fail: #ef4444;
            --warn: #f59e0b;
            --error: #a855f7;
            --unknown: #6b7280;
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            padding: 0;
            font-family: Arial, Helvetica, sans-serif;
            background: var(--bg);
            color: var(--text);
        }}

        .container {{
            max-width: 1100px;
            margin: 0 auto;
            padding: 32px 20px 48px;
        }}

        .hero {{
            background: linear-gradient(135deg, #111827, #1e293b);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
        }}

        .hero h1 {{
            margin: 0 0 8px;
            font-size: 2rem;
        }}

        .hero p {{
            margin: 6px 0;
            color: var(--muted);
        }}

        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}

        .summary-card {{
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 18px;
        }}

        .summary-card h2 {{
            margin: 0;
            font-size: 1.8rem;
        }}

        .summary-card p {{
            margin: 8px 0 0;
            color: var(--muted);
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 0.04em;
        }}

        .results-section {{
            margin-top: 12px;
        }}

        .results-section h2 {{
            margin-bottom: 16px;
        }}

        .results-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 16px;
        }}

        .result-card {{
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 18px;
        }}

        .result-card h3 {{
            margin: 12px 0 10px;
            font-size: 1.05rem;
        }}

        .result-card p {{
            margin: 0 0 12px;
            color: var(--text);
            line-height: 1.5;
        }}

        .result-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
        }}

        .check-id {{
            font-size: 0.9rem;
            color: var(--muted);
            font-weight: bold;
        }}

        .status-badge {{
            display: inline-block;
            padding: 6px 10px;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: bold;
            color: white;
        }}

        .status-pass {{ background: var(--pass); }}
        .status-fail {{ background: var(--fail); }}
        .status-warn {{ background: var(--warn); color: #111827; }}
        .status-error {{ background: var(--error); }}
        .status-unknown {{ background: var(--unknown); }}

        .remediation {{
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid var(--border);
            color: var(--muted);
            line-height: 1.5;
        }}

        .footer {{
            margin-top: 28px;
            color: var(--muted);
            font-size: 0.9rem;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <section class="hero">
            <h1>HostGuard Security Audit Report</h1>
            <p>Generated at: {escape(generated_at)}</p>
            <p>Linux security baseline audit results for common hardening checks.</p>
        </section>

        <section class="summary-grid">
            <div class="summary-card">
                <h2>{summary["total"]}</h2>
                <p>Total Results</p>
            </div>
            <div class="summary-card">
                <h2>{summary["pass"]}</h2>
                <p>Pass</p>
            </div>
            <div class="summary-card">
                <h2>{summary["fail"]}</h2>
                <p>Fail</p>
            </div>
            <div class="summary-card">
                <h2>{summary["warn"]}</h2>
                <p>Warn</p>
            </div>
            <div class="summary-card">
                <h2>{summary["error"]}</h2>
                <p>Error</p>
            </div>
        </section>

        <section class="results-section">
            <h2>Detailed Results</h2>
            <div class="results-grid">
                {cards_html}
            </div>
        </section>

        <div class="footer">
            Built with HostGuard
        </div>
    </div>
</body>
</html>
"""
    path.write_text(html, encoding="utf-8")
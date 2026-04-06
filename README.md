# HostGuard

HostGuard is a Python-based Linux security baseline auditing tool that checks a host for common hardening issues and generates structured security audit results.

## Why I built this

I built HostGuard as a cybersecurity portfolio project to demonstrate practical Linux hardening, baseline auditing, secure configuration review, and Python automation skills.

The goal was to create a lightweight tool that can inspect a Linux system and clearly report whether key security settings pass or fail basic baseline checks.

## Features

- Checks whether SSH root login is disabled
- Detects whether a host firewall is active
- Reviews password aging policy
- Detects active legacy insecure services
- Flags world-writable files under `/etc`
- Exports audit results to JSON
- Uses a modular check-based architecture for easy extension

## Current Checks

| Check ID | Check Name | Description |
|---|---|---|
| SSH-001 | SSH Root Login Disabled | Verifies whether `PermitRootLogin` is disabled |
| FW-001 | Firewall Enabled | Detects whether UFW, firewalld, or nftables is active |
| PWD-001 | Password Aging Policy | Reviews `PASS_MAX_DAYS` and `PASS_WARN_AGE` |
| SVC-001 | Legacy Insecure Services Disabled | Detects insecure legacy services such as telnet |
| PERM-001 | No World-Writable Files Under `/etc` | Flags risky file permissions under `/etc` |

## Project Structure

```text
HostGuard/
├── hostguard/
│   ├── main.py
│   ├── models.py
│   ├── checks/
│   └── reporting/
├── reports/
├── sample_reports/
├── screenshots/
├── tests/
├── README.md
├── requirements.txt
└── pyproject.toml
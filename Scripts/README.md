# Scripts

Python and PowerShell tools for automating SOC analysis tasks.

---

## Contents

| Script | Language | Purpose |
|--------|----------|---------|
| `failed_login_parser.py` | Python 3 | Parses Splunk CSV exports to detect brute force and password spray patterns |

## Usage

```bash
# Export failed logins from Splunk as CSV, then analyze:
python3 failed_login_parser.py splunk_export.csv
```

### Sample Output

```
==============================================================
  FAILED LOGIN ANALYSIS REPORT
==============================================================

  Total Failed Login Events (4625): 14

  ⚠️  PASSWORD SPRAY DETECTED

  Source IP: 192.168.50.30
  Failures: 10 across 5 accounts
  Accounts: j.smith, j.doe, b.wilson, svc_sql, s.bostick
```

---

## Goal

Demonstrate practical scripting skills for SOC automation and log analysis.

# Scripts

Python tools for automating SOC analysis tasks (PowerShell examples appear in lab and attack write-ups, not as `.ps1` scripts in this folder).

---

## Contents

| Script | Language | Purpose |
|--------|----------|---------|
| `failed_login_parser.py` | Python 3 | Parses Splunk CSV exports to detect brute force and password spray patterns |
| `discord_bot.py` | Python 3 | SOC command bot; requires `DISCORD_BOT_TOKEN` (copy `discord-bot.env.example` → `discord-bot.env`, or export in your shell) |
| `ransomware_sim.py` | Python 3 | Controlled ransomware-style behavior simulation for lab detection (use only in isolated environments) |

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

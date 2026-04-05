# Incident Reports & SOC Playbooks

This folder contains SOC-style incident reports and response playbooks created from attack simulations in the home lab.

---

## Incident Reports

| Report | Attack Type | Severity |
|--------|-------------|----------|
| `001_brute_force_smb.md` | SMB brute force against Win11 | High |
| `002_ad_password_spray.md` | AD password spray against DC01 | High |
| `002_wazuh_fim_alert.md` | Wazuh File Integrity Monitoring alert | Medium |

## Related analyses (Wazuh SIEM)

These live under `Wazuh_SIEM/` but pair well with incident-response documentation.

| Report | Topic | Severity |
|--------|-------|----------|
| [`vulnerability_assessment.md`](../Wazuh_SIEM/vulnerability_assessment.md) | Wazuh Vulnerability Detector findings | High |
| [`rootkit_anomaly_detection.md`](../Wazuh_SIEM/rootkit_anomaly_detection.md) | Wazuh Rootcheck — anomaly investigation | Critical |

## Response Playbooks

| Playbook | ID | MITRE ATT&CK |
|----------|----|---------------|
| `playbook_brute_force.md` | PB-001 | T1110 — Brute Force |
| `playbook_suspicious_process.md` | PB-002 | T1059 — Command & Scripting |
| `playbook_kerberoasting.md` | PB-003 | T1558.003 — Kerberoasting |

## Templates

| File | Purpose |
|------|---------|
| `incident_report_template.md` | Reusable SOC incident report format |

---

## Goal

Document incident response workflows with detection queries, investigation steps, containment procedures, and remediation actions.

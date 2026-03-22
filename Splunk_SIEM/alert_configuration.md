# Splunk Alert Configuration — Detection Engineering
**Analyst:** Stacy  
**Environment:** Splunk Enterprise 10.2.0  
**Alert Type:** Real-time  
**Action:** Add to Triggered Alerts
---
## Overview
This document details the three real-time alerts configured in Splunk Enterprise for detecting malicious activity in the home lab environment. All alerts are configured to trigger immediately upon detection and are added to the Triggered Alerts queue for analyst review.
---
## Alert 1: Brute Force — Multiple Failed Logins
| Field              | Value                                          |
|--------------------|------------------------------------------------|
| **Name**           | Brute Force — Multiple Failed Logins           |
| **Type**           | Real-time                                      |
| **Severity**       | High                                           |
| **Expires**        | 24 hours                                       |
| **Trigger**        | Number of Results > 0                          |
### SPL Query
```spl
index=main EventCode=4625
| stats count by src_ip
| where count > 5
```
### What It Detects
This alert fires when a single source IP generates more than 5 failed login attempts. This pattern indicates:
- Automated password guessing tools (Hydra, CrackMapExec)
- Credential stuffing attacks
- Password spraying campaigns
### MITRE ATT&CK
- **Tactic:** Credential Access (TA0006)
- **Technique:** Brute Force: Password Guessing (T1110.001)
---
## Alert 2: Suspicious Process Execution Detected
| Field              | Value                                          |
|--------------------|------------------------------------------------|
| **Name**           | Suspicious Process Execution Detected          |
| **Type**           | Real-time                                      |
| **Severity**       | High                                           |
| **Expires**        | 24 hours                                       |
| **Trigger**        | Number of Results > 0                          |
### SPL Query
```spl
index=main source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1
  (Image="*powershell*" OR Image="*cmd.exe*" OR Image="*mshta*")
```
### What It Detects
This alert fires when Sysmon detects the execution of commonly abused Windows binaries:
- **PowerShell** — Frequently used for fileless malware, C2 frameworks, and lateral movement
- **cmd.exe** — Used for batch scripting, privilege escalation, and system reconnaissance
- **mshta.exe** — Used to execute malicious HTA (HTML Application) files, often as a living-off-the-land technique
### MITRE ATT&CK
- **Tactic:** Execution (TA0002)
- **Technique:** Command and Scripting Interpreter: PowerShell (T1059.001)
- **Technique:** System Binary Proxy Execution: Mshta (T1218.005)
---
## Alert 3: Port Scan Detected
| Field              | Value                                          |
|--------------------|------------------------------------------------|
| **Name**           | Port Scan Detected                             |
| **Type**           | Real-time                                      |
| **Severity**       | High                                           |
| **Expires**        | 24 hours                                       |
| **Trigger**        | Number of Results > 0                          |
### SPL Query
```spl
index=main source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=3
| stats dc(DestinationPort) as unique_ports by SourceIp
| where unique_ports > 20
```
### What It Detects
This alert fires when a single source IP connects to more than 20 unique destination ports. This pattern indicates:
- Nmap port scanning
- Network reconnaissance
- Automated vulnerability scanning
### MITRE ATT&CK
- **Tactic:** Reconnaissance (TA0043)
- **Technique:** Active Scanning: Port Scanning (T1595.001)
### Note
The default SwiftOnSecurity Sysmon configuration disables EventCode=3 (Network Connection) logging to reduce noise. To enable this alert in production, modify the Sysmon config to include network connection events for high-value assets.
---
## Alert Management
### Viewing Triggered Alerts
Navigate to **Activity → Triggered Alerts** in Splunk Web to view all alerts that have fired.
### Alert Tuning Recommendations
- Adjust the failed login threshold (currently 5) based on your environment's baseline
- Add exclusions for known service accounts that may generate legitimate failed logins
- Consider adding `src_ip` exclusions for trusted management subnets
- For the process alert, consider excluding known-good parent processes to reduce false positives
---
*This alert configuration document is maintained as part of a cybersecurity home lab portfolio for SOC analyst skill development.*

# Incident Report — SMB Brute Force Attack (Simulated)
**Date:** 2026-02-28  
**Analyst:** Stacy  
**Environment:** Home Lab (Ubuntu Server, Windows 11, Kali Linux, Splunk SIEM)  
**Severity:** High  
**Status:** Closed — Simulated Exercise
---
## 1. Executive Summary
A brute-force authentication attack was simulated from the Kali Linux attack machine (`192.168.50.30`) targeting the Windows 11 workstation (`192.168.50.20`) over SMB (port 445). The attack used the CrackMapExec tool with the `rockyou.txt` wordlist to attempt credential guessing against the local `administrator` account.
Splunk SIEM successfully ingested Windows Security Event Logs from the target machine and detected **10 failed login attempts** (EventCode 4625) within an 18-second window. The real-time **"Brute Force — Multiple Failed Logins"** alert was triggered, and the incident was investigated and documented.
---
## 2. Incident Details
- **Incident Type:** Brute Force Authentication Attack (SMB)
- **Target System:** Windows 11 Workstation (`192.168.50.20`)
- **Source System:** Kali Linux (`192.168.50.30`)
- **Protocol:** SMB (TCP/445)
- **Tool Used:** CrackMapExec v5.x
- **Wordlist:** `/usr/share/wordlists/rockyou.txt` (~14.3 million entries)
### MITRE ATT&CK Mapping
| Field     | Value                                                    |
|-----------|----------------------------------------------------------|
| Tactic    | Credential Access (TA0006)                               |
| Technique | Brute Force: Password Guessing (T1110.001)               |
| Tactic    | Initial Access (TA0001)                                  |
| Technique | Valid Accounts: Local Accounts (T1078.003)               |
---
## 3. Timeline of Events
| Time (EST)       | Event                                                        |
|------------------|--------------------------------------------------------------|
| 10:19 AM         | Nmap reconnaissance scan initiated from Kali                 |
| 10:20 AM         | TCP Connect scan (`-sT`) confirmed port 445 open            |
| 10:28 AM         | CrackMapExec brute force attack launched against SMB         |
| 10:28:13 AM      | First failed login attempt recorded (EventCode 4625)         |
| 10:28:30 AM      | 10th failed login attempt recorded                           |
| 10:28:31 AM      | Windows rate-limits NETBIOS connections                      |
| 10:28:35 AM      | CrackMapExec encounters connection timeouts, attack slows    |
| 10:37 AM         | Analyst queries Splunk — 10 EventCode 4625 events confirmed  |
| 10:38 AM         | Splunk "Brute Force" alert confirmed triggered               |
| 10:44 AM         | Correlated attack source IP across all log sources           |
---
## 4. Indicators of Compromise (IOCs)
| IOC Type           | Value                          |
|--------------------|--------------------------------|
| Source IP           | 192.168.50.30 (Kali Linux)     |
| Target IP           | 192.168.50.20 (Windows 11)     |
| Target Port         | 445/TCP (SMB)                  |
| Username Attempted  | administrator                  |
| Failure Reason      | Unknown user name or bad password |
| Tool Signature      | Rapid sequential login attempts (~2s interval) |
| Event Count         | 10 failed (4625), 2 auth events (4624) |
---
## 5. Log Analysis
### Failed Login Events (EventCode 4625)
**SPL Query:**
```spl
index=main EventCode=4625
| table _time, Account_Name, Source_Network_Address, Failure_Reason
| head 20
```
**Results:** 10 events returned, all targeting `administrator` with reason `Unknown user name or bad password`. All events occurred within an 18-second window — a clear indicator of automated credential stuffing.
### Correlation — All Events from Attacker IP
**SPL Query:**
```spl
index=main "192.168.50.30"
| stats count by source, EventCode
| sort -count
```
**Results:**
| Source                  | EventCode | Count |
|-------------------------|-----------|-------|
| WinEventLog:Security    | 4625      | 10    |
| WinEventLog:Security    | 4624      | 2     |
### Brute Force Timeline Visualization
**SPL Query:**
```spl
index=main EventCode=4625
| timechart span=1m count
```
This query displays a sharp spike at the exact minute the attack occurred, contrasting with zero baseline activity — a textbook brute force signature.
---
## 6. Detection & Alerting
| Alert Name                          | Type      | Trigger                          | Status    |
|-------------------------------------|-----------|----------------------------------|-----------|
| Brute Force — Multiple Failed Logins | Real-time | EventCode 4625 count > 5        | ✅ Fired   |
| Suspicious Process Execution         | Real-time | PowerShell/CMD/mshta execution   | Not triggered |
| Port Scan Detected                   | Real-time | 20+ unique destination ports     | Pending verification |
---
## 7. Response & Remediation
### Immediate Actions Taken
1. Verified the attack source was the lab's Kali Linux VM (confirmed via MAC address and IP)
2. Confirmed no successful credential compromise occurred
3. Re-enabled Windows Firewall on all profiles after the simulation
4. Documented all findings for portfolio evidence
### Recommended Mitigations (Production Environment)
- **Account lockout policy:** Lock accounts after 5 failed attempts within 5 minutes
- **Network segmentation:** Restrict SMB access to authorized subnets only
- **Multi-factor authentication (MFA):** Require MFA for all privileged accounts
- **Firewall rules:** Block inbound SMB (445) from untrusted networks
- **Monitoring:** Maintain real-time SIEM alerts for EventCode 4625 spikes
- **Credential hygiene:** Enforce strong password policies and regular rotation
---
## 8. Lessons Learned
1. **Splunk detection worked as designed** — The real-time alert successfully identified the brute force pattern within seconds of the attack
2. **Windows Security Logs are essential** — EventCode 4625 provided clear, actionable evidence including timestamps, target accounts, and failure reasons
3. **Rate limiting is a first line of defense** — Windows automatically throttled NETBIOS connections after detecting rapid login attempts, slowing the attack
4. **Tool selection matters** — Hydra failed to connect to modern Windows 11 SMBv3; CrackMapExec succeeded, demonstrating the importance of using appropriate tools for the target environment
5. **Firewall configuration is critical** — The attack only succeeded after temporarily disabling Windows Firewall; in production, proper firewall rules would block this entirely
---
## 9. Evidence
- Splunk search results showing 10 failed login events
- CrackMapExec terminal output showing `STATUS_LOGON_FAILURE`
- Nmap scan confirming port 445 open
- SOC Analyst Overview dashboard with populated panels
---
*This incident report was created as part of a cybersecurity home lab portfolio exercise. All attacks were performed in an isolated virtual environment for educational purposes only.*

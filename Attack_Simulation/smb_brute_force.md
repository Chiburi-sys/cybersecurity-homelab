# Attack Simulation — SMB Brute Force with CrackMapExec
**Date:** 2026-02-28  
**Attacker:** Kali Linux (`192.168.50.30`)  
**Target:** Windows 11 Workstation (`192.168.50.20`)  
**Tool:** CrackMapExec v5.x  
**Protocol:** SMB (TCP/445)
---
## Objective
Simulate a credential brute-force attack against the Windows 11 SMB service to test SIEM detection capabilities. This mirrors real-world attacks where adversaries attempt to guess local administrator passwords to gain unauthorized access to file shares and remote administration.
---
## MITRE ATT&CK Mapping
| Field     | Value                                              |
|-----------|----------------------------------------------------|
| Tactic    | Credential Access (TA0006)                         |
| Technique | Brute Force: Password Guessing (T1110.001)         |
| Tactic    | Initial Access (TA0001)                            |
| Technique | Valid Accounts: Local Accounts (T1078.003)         |
| Tactic    | Lateral Movement (TA0008)                          |
| Technique | Remote Services: SMB/Windows Admin Shares (T1021.002) |
---
## Prerequisites
1. Nmap scan confirmed port 445 (SMB) is open on the target
2. Windows Firewall temporarily disabled for attack simulation
3. Splunk SIEM actively receiving logs from the Windows 11 target
4. `rockyou.txt` wordlist extracted on Kali
---
## Commands Executed
### Step 1: Extract the Wordlist
```bash
sudo gunzip /usr/share/wordlists/rockyou.txt.gz
```
### Step 2: Initial Attempt with Hydra (Failed)
```bash
hydra -l administrator -P /usr/share/wordlists/rockyou.txt smb://192.168.50.20 -t 4
```
**Result:** `[ERROR] invalid reply from target smb://192.168.50.20:445/`
Hydra's SMB module is incompatible with Windows 11's modern SMBv3 + NTLMv2 implementation. The tool expects legacy SMB protocol responses that Windows 11 no longer provides.
### Step 3: Successful Attack with CrackMapExec
```bash
crackmapexec smb 192.168.50.20 -u "administrator" -p /usr/share/wordlists/rockyou.txt
```
**Result:**
```
SMB   192.168.50.20  445  WINDOWS  [*] Windows 11 / Server 2025 Build 26100 x64
                                       (name:WINDOWS) (domain:Windows)
                                       (signing:True) (SMBv1:False)
SMB   192.168.50.20  445  WINDOWS  [-] Windows\administrator:123456789 STATUS_LOGON_FAILURE
SMB   192.168.50.20  445  WINDOWS  [-] Connection Error: The NETBIOS connection
                                       with the remote host timed out.
[... repeated connection timeouts ...]
```
---
## Attack Results
| Metric                     | Value                                 |
|----------------------------|---------------------------------------|
| Total login attempts        | ~10 (before rate limiting)            |
| Successful logins           | 0                                     |
| Failed logins (4625)        | 10                                    |
| Auth events (4624)          | 2                                     |
| Attack duration             | ~18 seconds (active)                  |
| Windows response            | NETBIOS connection rate-limiting      |
| Attack outcome              | **Unsuccessful** — Credentials not found |
---
## Target Reconnaissance (Pre-Attack)
### Enum4linux Enumeration
```bash
enum4linux -a 192.168.50.20
```
**Findings:**
- **Computer Name:** WINDOWS
- **Workgroup:** WORKGROUP
- **Known Usernames:** administrator, guest, krbtgt, domain admins, root, bin, none
- **Null Session:** Denied — "Server doesn't allow session using username '', password ''"
---
## Detection Evidence in Splunk
### Query 1: Failed Login Attempts
```spl
index=main EventCode=4625
| table _time, Account_Name, Source_Network_Address, Failure_Reason
| head 20
```
**Result:** 10 events — all targeting `administrator` with reason `Unknown user name or bad password`. Timestamps show 2-second intervals, confirming automated tool usage.
### Query 2: All Events from Attacker IP
```spl
index=main "192.168.50.30"
| stats count by source, EventCode
| sort -count
```
**Result:**
| Source                 | EventCode | Count |
|------------------------|-----------|-------|
| WinEventLog:Security   | 4625      | 10    |
| WinEventLog:Security   | 4624      | 2     |
### Query 3: Brute Force Alert Trigger
```spl
index=main EventCode=4625
| stats count by src_ip
| where count > 5
```
This query powers the real-time **"Brute Force — Multiple Failed Logins"** alert that was triggered during the attack.
---
## Key Observations
1. **CrackMapExec > Hydra for modern Windows** — Hydra's SMB module failed against Windows 11's SMBv3. CrackMapExec handled the modern protocol stack correctly.
2. **Windows rate-limiting is effective** — After ~10 login attempts, Windows began throttling NETBIOS connections, significantly slowing the attack.
3. **SMB signing was enabled** — CrackMapExec reported `signing:True`, which prevents man-in-the-middle attacks on SMB traffic.
4. **SMBv1 was disabled** — The target correctly disabled the legacy SMBv1 protocol, eliminating EternalBlue-class vulnerabilities.
---
## Recommendations
- Implement account lockout policies (lock after 5 failed attempts)
- Enable SMB access logging and forward to SIEM
- Restrict SMB access to authorized subnets via firewall rules
- Consider disabling SMB entirely if file sharing is not required
- Deploy MFA for all administrative accounts
- Monitor for EventCode 4625 spikes as a primary brute force indicator
---
*This attack simulation was performed in an isolated virtual lab environment for educational purposes only.*

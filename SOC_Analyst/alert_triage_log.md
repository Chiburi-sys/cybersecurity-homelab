# Alert Triage Log — SOC Analyst Shift

**Analyst:** Stacy Bostick
**Date:** 2026-03-02
**Shift:** Day Shift (08:00 – 20:00 EST)
**SIEM:** Splunk Enterprise
**Environment:** cybersec.local (192.168.50.0/24)

---

## Triage Summary

| Verdict | Count |
|---------|-------|
| ✅ True Positive | 5 |
| ❌ False Positive | 3 |
| ⬜ Benign | 2 |
| **Total Alerts** | **10** |

---

## Alert #1 — Brute Force: Multiple Failed Logins

| Field | Value |
|-------|-------|
| **Time** | 2026-03-02 10:15 AM |
| **Alert** | Brute Force — Multiple Failed Logins |
| **Severity** | High |
| **Source IP** | 192.168.50.30 (Kali Linux) |
| **Target** | DC01 (192.168.50.5) |
| **Verdict** | ✅ **True Positive** |

**Investigation:**

```spl
index=main EventCode=4625 src_ip="192.168.50.30"
| stats count by Account_Name, Source_Network_Address
| sort -count
```

**Findings:**

- 10 failed login attempts across 5 domain accounts within 2 minutes
- CrackMapExec SMB password spray pattern
- `j.smith` login succeeded (EventCode 4624) after failures

**Action:** Opened ticket SOC-005. Recommended account lockout policy and password reset for j.smith.

---

## Alert #2 — Suspicious Process: PowerShell on Win11

| Field | Value |
|-------|-------|
| **Time** | 2026-03-02 10:32 AM |
| **Alert** | Suspicious Process Execution Detected |
| **Severity** | High |
| **Host** | WINDOWS (192.168.50.20) |
| **Process** | powershell.exe |
| **Verdict** | ❌ **False Positive** |

**Investigation:**

```spl
index=main source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1
  host="WINDOWS" Image="*powershell*"
| table _time, User, Image, CommandLine, ParentImage
| sort -_time
```

**Findings:**

- PowerShell launched by `SYSTEM` account
- Parent process: `services.exe` (standard Windows service manager)
- Command line: `powershell.exe -nop -exec bypass -file C:\Windows\Temp\sysmon_update.ps1`
- This is a scheduled Sysmon configuration update — benign activity

**Action:** Closed alert. Added tuning recommendation: whitelist `services.exe` → `powershell.exe` path for Sysmon updates.

---

## Alert #3 — Port Scan Detected

| Field | Value |
|-------|-------|
| **Time** | 2026-03-02 11:05 AM |
| **Alert** | Port Scan — High Volume Connection Attempts |
| **Severity** | Medium |
| **Source IP** | 192.168.50.30 |
| **Target** | 192.168.50.20 (Win11) |
| **Verdict** | ✅ **True Positive** |

**Investigation:**

```spl
index=main src_ip="192.168.50.30" dest_ip="192.168.50.20"
| stats dc(dest_port) as unique_ports, count by src_ip
```

**Findings:**

- 1000 unique destination ports scanned in under 60 seconds
- Nmap TCP connect scan (`-sT`) pattern
- 3 ports responded as open: 135, 139, 445

**Action:** Opened ticket SOC-003. Verified this was an authorized penetration test. Closed after confirmation.

---

## Alert #4 — Failed Login: Admin Account

| Field | Value |
|-------|-------|
| **Time** | 2026-03-02 11:45 AM |
| **Alert** | Brute Force — Multiple Failed Logins |
| **Severity** | Medium |
| **Source** | DC01 console |
| **Account** | s.admin |
| **Verdict** | ⬜ **Benign** |

**Investigation:**

```spl
index=main EventCode=4625 Account_Name="s.admin"
| table _time, Source_Network_Address, Logon_Type, Failure_Reason
```

**Findings:**

- Only 2 failed attempts, both from the DC01 console (Logon Type 2 — Interactive)
- Followed immediately by a successful login (EventCode 4624)
- Pattern consistent with a mistyped password

**Action:** Closed as benign. Below alert threshold (5 failures). Normal admin login behavior.

---

## Alert #5 — Kerberoasting: TGS Request with RC4

| Field | Value |
|-------|-------|
| **Time** | 2026-03-02 12:10 PM |
| **Alert** | Kerberoasting — Suspicious TGS Request |
| **Severity** | Critical |
| **Source IP** | 192.168.50.30 (Kali Linux) |
| **Service** | svc_sql (DC01/svc_sql.cybersec.local:60111) |
| **Verdict** | ✅ **True Positive** |

**Investigation:**

```spl
index=main EventCode=4769 Ticket_Encryption_Type=0x17
  Service_Name!="krbtgt" Service_Name!="*$"
| table _time, Account_Name, Service_Name, Client_Address, Ticket_Encryption_Type
```

**Findings:**

- TGS ticket requested for `svc_sql` with RC4 encryption (0x17)
- Request came from `j.smith` account on 192.168.50.30
- RC4 encryption = offline crackable hash — classic Kerberoasting
- `impacket-GetUserSPNs` tool signature

**Action:** Opened ticket SOC-002. **Escalated to Tier 2** — credential theft requires immediate service account password rotation and investigation of the j.smith account compromise.

---

## Alert #6 — New Service Installed on Win11

| Field | Value |
|-------|-------|
| **Time** | 2026-03-02 01:30 PM |
| **Alert** | Suspicious Process Execution Detected |
| **Severity** | Medium |
| **Host** | WINDOWS (192.168.50.20) |
| **Process** | msiexec.exe |
| **Verdict** | ❌ **False Positive** |

**Investigation:**

```spl
index=main source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1
  host="WINDOWS" Image="*msiexec*"
| table _time, User, CommandLine, ParentImage
```

**Findings:**

- `msiexec.exe` installing Splunk Universal Forwarder MSI package
- Launched by Administrator account via interactive session
- Installation matches scheduled maintenance window
- Service `SplunkForwarder` created as expected

**Action:** Closed as false positive. Known maintenance activity — Splunk Forwarder installation.

---

## Alert #7 — Excessive LDAP Queries

| Field | Value |
|-------|-------|
| **Time** | 2026-03-02 02:15 PM |
| **Alert** | Anomalous LDAP Query Volume |
| **Severity** | Medium |
| **Source IP** | 192.168.50.30 (Kali Linux) |
| **Target** | DC01 (192.168.50.5) |
| **Verdict** | ✅ **True Positive** |

**Investigation:**

```spl
index=main EventCode=4662 Access_Mask="0x100" src_ip="192.168.50.30"
| stats count by Account_Name, Object_Name
| sort -count
```

**Findings:**

- 40+ LDAP queries from a single source in under 5 minutes
- Querying user objects, group memberships, and computer objects
- Pattern consistent with `enum4linux` or `ldapsearch` enumeration
- Attacker building domain recon data

**Action:** Documented as part of ongoing attack chain from 192.168.50.30. Correlated with Alert #1 and #5.

---

## Alert #8 — Account Lockout: j.doe

| Field | Value |
|-------|-------|
| **Time** | 2026-03-02 03:00 PM |
| **Alert** | Account Lockout Detected |
| **Severity** | Low |
| **Account** | j.doe |
| **OU** | HR |
| **Verdict** | ⬜ **Benign** |

**Investigation:**

```spl
index=main EventCode=4740 Account_Name="j.doe"
| table _time, Account_Name, Caller_Computer_Name
```

**Findings:**

- Account locked out after 5 failed password attempts
- All attempts from the same workstation (console login)
- No external source IP involved
- User confirmed they forgot their password after vacation

**Action:** Closed as benign. Password reset via Service Desk. No security incident.

---

## Alert #9 — Successful Login After Brute Force

| Field | Value |
|-------|-------|
| **Time** | 2026-03-02 10:16 AM |
| **Alert** | Brute Force — Login Success After Failures |
| **Severity** | Critical |
| **Source IP** | 192.168.50.30 |
| **Account** | j.smith |
| **Verdict** | ✅ **True Positive** |

**Investigation:**

```spl
index=main (EventCode=4625 OR EventCode=4624) src_ip="192.168.50.30"
| table _time, EventCode, Account_Name, Source_Network_Address
| sort _time
```

**Findings:**

- 4 failed logins (4625) at 10:15 AM followed by 1 success (4624) at 10:16 AM
- Same source IP — attacker found valid credentials
- `j.smith` account compromised via password spray
- Account was then used for Kerberoasting (Alert #5)

**Action:** Opened ticket SOC-001. **Escalated** — successful compromise requires immediate password reset and full account audit.

---

## Alert #10 — DNS Query for Suspicious Domain

| Field | Value |
|-------|-------|
| **Time** | 2026-03-02 04:30 PM |
| **Alert** | Suspicious DNS Query Detected |
| **Severity** | Low |
| **Host** | WINDOWS (192.168.50.20) |
| **Domain** | settings-win.data.microsoft.com |
| **Verdict** | ❌ **False Positive** |

**Investigation:**

```spl
index=main sourcetype=DNS query="*microsoft.com"
| stats count by query, src_ip
| sort -count
```

**Findings:**

- Standard Windows telemetry/settings domain
- Resolves to known Microsoft infrastructure IPs
- Query pattern consistent with Windows Update checks
- No indicators of DGA or C2 communication

**Action:** Closed as false positive. Whitelisted `*.data.microsoft.com` from DNS alerts.

---

## Shift Metrics

| Metric | Value |
|--------|-------|
| Total Alerts Reviewed | 10 |
| True Positives | 5 (50%) |
| False Positives | 3 (30%) |
| Benign | 2 (20%) |
| Tickets Opened | 5 |
| Escalated to Tier 2 | 2 |
| Tuning Recommendations | 2 |
| Average Triage Time | ~8 minutes |

---

*This alert triage log is part of a cybersecurity home lab portfolio demonstrating Tier 1 SOC Analyst skills.*

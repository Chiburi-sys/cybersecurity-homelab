# Splunk Detection Rules — Active Directory Attacks

**Author:** Stacy Bostick  
**Last Updated:** 2026-03-01  
**Environment:** Splunk Enterprise → DC01 (cybersec.local)

---

## Overview

These detection rules supplement the existing Splunk alert configuration with Active Directory-specific detections. They are designed to identify common AD attack techniques observed during penetration testing engagements.

---

## Alert 4: Kerberoasting Detected

### Configuration

| Setting | Value |
|---|---|
| Alert Name | Kerberoasting — Suspicious TGS Requests |
| Search Type | Real-time |
| Severity | Critical |
| MITRE ATT&CK | T1558.003 |

### SPL Query

```spl
index=main EventCode=4769 Ticket_Encryption_Type=0x17
  Service_Name!="krbtgt" Service_Name!="*$"
| stats count dc(Service_Name) as unique_spns by Account_Name, Client_Address
| where count > 3 OR unique_spns > 2
```

### Trigger Condition

- Fires when a single user requests TGS tickets for more than 3 services or 2+ unique SPNs with RC4 encryption

### Why This Works

- Legitimate users rarely request multiple service tickets in rapid succession
- RC4 (0x17) encryption is outdated and preferred by attackers for offline cracking
- Machine accounts ($) are excluded to avoid false positives from normal domain operations

---

## Alert 5: Password Spray Detected

### Configuration

| Setting | Value |
|---|---|
| Alert Name | Password Spray — Multiple Users Same Source |
| Search Type | Real-time |
| Severity | High |
| MITRE ATT&CK | T1110.003 |

### SPL Query

```spl
index=main EventCode=4625
| bin _time span=10m
| stats dc(TargetUserName) as unique_users count by src_ip, _time
| where unique_users > 3
```

### Trigger Condition

- Fires when a single IP attempts to authenticate as more than 3 different users within 10 minutes

### Why This Works

- Normal users authenticate as themselves; testing multiple usernames from one IP is anomalous
- The 10-minute window catches automated tools while reducing false positives
- The `dc()` (distinct count) function specifically identifies the spray pattern

---

## Alert 6: Domain Admin Logon from Non-Standard Host

### Configuration

| Setting | Value |
|---|---|
| Alert Name | Domain Admin Logon — Anomalous Workstation |
| Search Type | Real-time |
| Severity | Critical |
| MITRE ATT&CK | T1078.002 |

### SPL Query

```spl
index=main EventCode=4624 Account_Name!="*$"
| lookup local=true domain_admins_lookup Account_Name OUTPUT is_admin
| where is_admin="true" AND Workstation_Name!="DC01"
  AND Workstation_Name!="ADMIN-WS"
| table _time, Account_Name, Workstation_Name, LogonType, Source_Network_Address
```

### Alternative (Without Lookup)

```spl
index=main EventCode=4624
  (Account_Name="s.bostick" OR Account_Name="Administrator")
  Workstation_Name!="DC01"
| table _time, Account_Name, Workstation_Name, LogonType, Source_Network_Address
```

### Why This Works

- Domain Admins should only log into authorized admin workstations
- Any DA logon from unexpected hosts could indicate credential theft
- Excludes computer accounts ($) and the DC itself

---

## Alert 7: LDAP Reconnaissance Detected

### Configuration

| Setting | Value |
|---|---|
| Alert Name | LDAP Enumeration — Excessive Queries |
| Search Type | Scheduled (every 15 min) |
| Severity | Medium |
| MITRE ATT&CK | T1087.002 |

### SPL Query

```spl
index=main EventCode=4662 Access_Mask="0x100"
| stats count by Account_Name, Object_Type
| where count > 50
| sort -count
```

---

## Alert Summary Table

| # | Alert Name | EventCode | MITRE | Severity | Type |
|---|---|---|---|---|---|
| 1 | Brute Force — Multiple Failed Logins | 4625 | T1110 | High | Real-time |
| 2 | Suspicious Process Execution | Sysmon 1 | T1059 | High | Real-time |
| 3 | Port Scan Detected | Sysmon 3 | T1046 | Medium | Real-time |
| 4 | Kerberoasting — Suspicious TGS | 4769 | T1558.003 | Critical | Real-time |
| 5 | Password Spray — Multiple Users | 4625 | T1110.003 | High | Real-time |
| 6 | Domain Admin — Anomalous Logon | 4624 | T1078.002 | Critical | Real-time |
| 7 | LDAP Enumeration — Excessive Queries | 4662 | T1087.002 | Medium | Scheduled |

---

## Dashboard Panel — AD Attack Overview

### Panel: AD Authentication Events (Timechart)

```spl
index=main (EventCode=4625 OR EventCode=4624 OR EventCode=4769 OR EventCode=4771)
| timechart span=5m count by EventCode
```

### Panel: Top Attacking IPs

```spl
index=main EventCode=4625
| stats count by src_ip
| sort -count
| head 10
```

### Panel: Kerberos Ticket Requests by User

```spl
index=main EventCode=4769
| stats count by Account_Name, Service_Name
| sort -count
```

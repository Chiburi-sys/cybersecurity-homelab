# Incident Report #002 — Active Directory Password Spray Attack

**Incident ID:** IR-002  
**Date Detected:** 2026-03-02  
**Analyst:** Stacy Bostick  
**Severity:** High  
**Status:** Closed — Simulated Attack  
**MITRE ATT&CK:** T1110.003 — Brute Force: Password Spraying

---

## Executive Summary

A password spray attack was detected targeting multiple domain accounts on the cybersec.local Active Directory domain. The attack originated from 192.168.50.30 (Kali Linux) and tested a single common password against 5 domain accounts via SMB (port 445). One account was successfully compromised.

---

## Detection Timeline

| Time | Event |
|------|-------|
| 18:05 PM | First SMB authentication attempt detected (j.smith) |
| 18:05 PM | Multiple failed logins (EventCode 4625) from same source IP |
| 18:05 PM | Successful login (EventCode 4624) for j.smith |
| 18:06 PM | Analyst alerted via Splunk "Brute Force — Multiple Failed Logins" alert |

---

## Attack Details

### Source

- **IP Address:** 192.168.50.30 (Kali Linux)
- **Tool Used:** CrackMapExec (SMB module)
- **Method:** Password spray — single password tested against multiple accounts

### Target

- **Domain:** cybersec.local
- **Domain Controller:** DC01 (192.168.50.5)
- **Protocol:** SMB (TCP/445)

### Accounts Targeted

| Account | OU | Result |
|---------|-----|--------|
| j.smith | IT | ✅ Compromised |
| j.doe | HR | ❌ Failed |
| b.wilson | Finance | ❌ Failed |
| svc_sql | IT | ❌ Failed |
| s.bostick | IT | ❌ Failed |

### Attack Command (Observed)

```bash
crackmapexec smb 192.168.50.5 -u '<username>' -p 'Password123!' -d cybersec.local
```

---

## Splunk Detection

### Query Used

```spl
index=main EventCode=4625
| table _time, Account_Name, Source_Network_address, Failure_Reason
| head 20
```

### Results

- **10 failed login events** (EventCode 4625) — 2 per account attempt
- **2 successful login events** (EventCode 4624) — j.smith authenticated
- **Failure Reason:** `Unknown user name or bad password`
- **Source IP:** All events from 192.168.50.30

### Supporting Queries

**Timechart of failures:**

```spl
index=main EventCode=4625 | timechart span=1m count
```

**Events by source IP and EventCode:**

```spl
index=main "192.168.50.30" | stats count by source, EventCode | sort -count
```

---

## Evidence

| Screenshot | Description |
|------------|-------------|
| `Kali_password_spray_crackmapexec.png` | CrackMapExec output showing success/failure |
| `Splunk_failed_logins_4625_table.png` | Splunk table of failed login events |
| `Splunk_failed_logins_timechart.png` | Timechart showing burst of failed logins |
| `Splunk_attack_events_by_source_ip.png` | Events correlated by attacker IP |
| `Splunk_SOC_dashboard_with_data.png` | SOC dashboard showing event patterns |

---

## Response Actions

1. ✅ **Identified the compromised account** — j.smith (weak password: Password123!)
2. ✅ **Correlated events in Splunk** — Confirmed 10 failed + 2 successful logins from attacker IP
3. ✅ **Documented the attack pattern** — Single password tested across 5 accounts
4. ⬜ **Recommended:** Reset j.smith password immediately
5. ⬜ **Recommended:** Implement account lockout policy (5 failures / 30 min lockout)
6. ⬜ **Recommended:** Block 192.168.50.30 at firewall (if non-lab environment)

---

## Root Cause

The j.smith account used a weak, commonly guessed password (`Password123!`). No account lockout policy was configured on the domain, allowing unlimited authentication attempts.

---

## Recommendations

1. **Enforce password complexity** — Minimum 12 characters, no common patterns
2. **Implement account lockout** — Lock after 5 failed attempts for 30 minutes
3. **Deploy MFA** — Multi-factor authentication for all domain accounts
4. **Monitor for spray patterns** — Alert on multiple 4625 events from a single source IP within 5 minutes
5. **Use Splunk alert** — "Brute Force — Multiple Failed Logins" is already configured

---

## Lessons Learned

- Password spraying is effective against domains with weak password policies
- A single compromised account gives attackers a foothold for lateral movement
- Splunk's real-time alerting on EventCode 4625 successfully detected this attack
- Time correlation between failed and successful logins reveals the spray pattern

---

*This incident report is part of a cybersecurity home lab portfolio for SOC analyst skill development.*
